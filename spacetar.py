import re
import click

from pathlib import Path
from requests import get
from textwrap import dedent
from bs4 import Tag, BeautifulSoup  # type: ignore
from itertools import chain, zip_longest
from sqlalchemy.orm import Session, relationship, declarative_base  # type: ignore

from sqlalchemy import (  # type: ignore
    Table,
    select,
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    create_engine,
)

from typing import Any, List, Dict, Tuple, Optional, Callable


Base = declarative_base()


ShortStr = String(50)
LongStr = String(500)


# Association tables. These are used by SQLAlchemy to construct
# many-to-many relationships. Since the relationship between the
# space molecules and the sources/references are many-to-many
# relationships (as in, a molecules can be associated with multiple
# sources or references, and similarly a particular source or paper
# can be associated with the discovery of multiple space molecules),
# we use these tables to construct our ORM backend. There are three
# tables:
# 1. `mol2src`:     Association table between the `molecules` and `sources` table.
# 2. `mol2ref`:     Association table between the `molecules` and `references` table.
# 3. `mol2exgal`:   Association table between the `molecules` and `extragalactic` table.
# 4. `ref2auth`:    Association table between the `references` and `authors` table.

mol2src = Table(
    "mol2src",
    Base.metadata,
    Column("mol_id", Integer, ForeignKey("molecules.id")),
    Column("src_id", Integer, ForeignKey("sources.id")),
)

mol2ref = Table(
    "mol2ref",
    Base.metadata,
    Column("mol_id", Integer, ForeignKey("molecules.id")),
    Column("ref_id", Integer, ForeignKey("references.id")),
)

mol2exgal = Table(
    "mol2exgal",
    Base.metadata,
    Column("mol_id", Integer, ForeignKey("molecules.id")),
    Column("exgal_id", Integer, ForeignKey("extragalactic.id")),
)

ref2auth = Table(
    "ref2auth",
    Base.metadata,
    Column("ref_id", Integer, ForeignKey("references.id")),
    Column("auth_id", Integer, ForeignKey("authors.id")),
)


class Molecule(Base):  # type: ignore

    """
    This class represents a single space molecule in the **spacetar** database.

    Args:
        formula:        The chemical formula of the molecule.
        year:           The year the molecule was discovered in space.
        tentative:      A flag that indicates whether the detection is still tentative,
                        or whether it has been confirmed by other observations.
        sources:        The source(s) where the molecule was first observed.
        references:     Bibliographic references to the papers involved in the discovery.
        extragalactic:  The source where the first extragalactic detection of the molecule
                        was made.
    """

    __tablename__: str = "molecules"

    id = Column(Integer, primary_key=True)
    formula = Column(ShortStr)
    year = Column(Integer)
    tentative = Column(Boolean)
    sources = relationship(
        "Source",
        secondary=mol2src,
        backref="molecules",
        lazy="selectin",
    )
    references = relationship(
        "Reference",
        secondary=mol2ref,
        backref="molecules",
        lazy="selectin",
    )
    extragalactic = relationship(
        "Extragalactic",
        secondary=mol2exgal,
        backref="molecules",
        lazy="selectin",
    )

    def __str__(self) -> str:
        return dedent(
            f"""
            Molecule
            ========
            formula={self.formula!r},
            year={self.year!r},
            tentative={'Yes' if self.tentative else 'No'!r},
            sources={self.sources!r},
            references={self.references!r},
            extragalactic={self.extragalactic!r},
            """
        )

    def __repr__(self) -> str:
        return str(self)

    def __rich__(self) -> Any:
        pass


class Source(Base):  # type: ignore

    """
    This class represents a single astronomical source in the **spacetar** database.

    Args:
        name:       The name of the source.
        emband:     The band in the electromagnetic spectrum in which the discovery was
                    made for this particular source. This can be one of **Radio**, **IR**,
                    or **UV/Vis**.
        molecules:  The space molecules associated with this source.

    Todo:
        Add a `coords` argument that will give us the equatorial coordinates of
        the source as a `SkyCoord` object. To implement this, a name-to-coords
        map has to be built. This will probably have to be hardcoded.
    """

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(ShortStr)
    emband = Column(ShortStr)

    def __str__(self) -> str:
        return f"Source: name={self.name!r}, emband={self.emband!r}"

    def __repr__(self) -> str:
        return str(self)


class Extragalactic(Base):  # type: ignore

    """
    This class represents an extragalactic astronomical source in the **spacetar**
    database.

    Args:
        name: The name of the source.
        cdms: Link to the CDMS database entry for the extragalacitc detection.

    Todo:
        Add a `coords` argument that will give us the equatorial coordinates of
        the source as a `SkyCoord` object. To implement this, a name-to-coords
        map has to be built. This will probably have to be hardcoded.
    """

    __tablename__ = "extragalactic"

    id = Column(Integer, primary_key=True)
    name = Column(ShortStr)
    cdms = Column(LongStr)

    def __str__(self) -> str:
        return f"Extragalactic: name={self.name!r}, cdms={self.cdms!r}"

    def __repr__(self) -> str:
        return str(self)


class Reference(Base):  # type: ignore

    """
    This class represents a single bibliographic reference in the **spacetar** database.

    Args:
        name:       The name of the paper being referred to.
        link:       A link to the paper. This is usually an ADS or DOI link.
        authors:    A list of the authors.
        molecules:  The space molecules associated with this reference.
    """

    __tablename__ = "references"

    id = Column(Integer, primary_key=True)
    name = Column(LongStr)
    link = Column(LongStr)
    authors = relationship(
        "Author",
        secondary=ref2auth,
        backref="papers",
        lazy="selectin",
    )

    def __str__(self) -> str:
        return (
            f"Reference: name={self.name}, link={self.link}, authors={self.authors!r}"
        )

    def __repr__(self) -> str:
        return str(self)


class Author(Base):  # type: ignore

    """
    This class represents a single author in the **spacetar** database.

    Args:
        name:   The name of the author.
        papers: The papers they have authored.
    """

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(ShortStr)

    def __str__(self) -> str:
        return f"Author: name={self.name!r}"

    def __repr__(self) -> str:
        return str(self)


# Name of the package, stored as a global variable here for future use.
whoami = "spacetar"


def get_version() -> Optional[str]:

    """
    Get the version of the package, if installed.

    Returns:
        A version string, if the package is installed. Otherwise it returns nothing.
    """

    from importlib.metadata import version, PackageNotFoundError

    try:
        return version(whoami)
    except PackageNotFoundError:
        return None


# Important paths:
# 1. `here` is literally here; the parent directory of this file,
#    wherever it maybe on the user's file system. Using the `__file__`
#    parameter is an old and well-tested trick to navigate through
#    the file system in Python packages meant to be installed.
# 2. `data` is the data directory, where we will store our databases.
# 3. `jsonic` is the path to the JSON file which we will scrap.
# 4. `squealer` is the path to the SQLite database we will make from
#    the JSON database and store.
here = Path(__file__).parent.resolve()
data = here / "data"
jsonic = here / f"{whoami}.json"
squealer = here / f"{whoami}.db"

# The `Engine`, named after a particularly famous one *winks*.
thomas = create_engine(f"sqlite:///{squealer}", future=True)


class Nope(Exception):

    """
    Nope. Something is terribly wrong.
    """

    pass


def scrap() -> List[Dict]:

    """
    Scrap the space molecule database maintained at https://astrochymist.org/astrochymist_ism.html
    by David E. Woon. I am using this database because it is highly maintained, and easy
    to scrap. I have tried to scrap as much information as possible from the HTML source
    of this page, including whether the detection is still tentative or not. It is inspired
    from some of my own earlier attempts, and from a code by Kelvin Lee which you can find here:
    https://github.com/laserkelvin/Astrochymist.

    Returns:
        A list of dictionaries containing our scraped space molecule database.
    """

    url = "http://astrochymist.org/astrochymist_ism.html"

    space_rem = lambda x: "".join(x.split())

    formula = lambda x: space_rem(
        (
            lambda _: _("font")[0].text.replace(_("font")[1].text, "")
            if len(_("font")) > 1
            else _("font")[0].text
        )(x)
    )

    year = (
        lambda x: (x("font")[0].string or x("font")[0].b.string) if x("font") else None
    )

    tentative = lambda _: True if _("font")[0].i is not None else False

    sources = lambda x: [
        (name, emband)
        for name, emband in zip_longest(
            (
                lambda _: [
                    _[0].strip()
                    for _ in [
                        _
                        for _ in [
                            list(_.previous_siblings) for _ in _("hr", width="50%")
                        ]
                        if (_ != Tag(name="br")) and (_ != "\n")
                    ]
                ]
            )(x),
            (
                lambda _: {
                    {
                        "cyan": "Radio",
                        "pink": "IR",
                        "yellow": "UV/Vis",
                    }.get(_.get("color", None), None)
                    for _ in _("font")
                }
            )(x),
        )
    ]

    auth_regex = re.compile(
        r"""
        (
            ([A-Z][.]\s*)+  # Initials of the author.
            (\w{2,3})?\s*       # Surname prefix (optional).
            \w+             # Surname name of the author.
        )
        """,
        re.VERBOSE,
    )

    authors = lambda x: [
        re.findall(
            auth_regex,
            str(_.next_sibling),
        )
        for _ in x("br")
    ]

    references = lambda x: [
        (
            _.text.strip(),
            _.get("href", None),
            __,
        )
        for _, __ in zip(x("a"), authors(x))
    ]

    extragalactic = (
        lambda x: (x("font")[1].string, x.a.get("href", None))
        if (x.font is not None) and (x.a is not None)
        else (None, None)
    )

    response = get(url)
    if response.status_code != 200:
        raise Nope("Nope, this is not working at all.")

    molecules = [
        {
            "formula": formula(_[1]),
            "year": year(_[0]),
            "tentative": tentative(_[1]),
            "sources": sources(_[3]),
            "references": references(_[2]),
            "extragalactic": extragalactic(_[0]),
        }
        for _ in [
            _
            for _ in [
                _(["th", "td"], recursive=False)
                for _ in BeautifulSoup(response.content, "lxml",).body("table")[2](
                    "tr", recursive=False
                )[1:]
            ]
            if len(_) == 4
        ]
    ]

    return molecules


def deep_freeze(molecules: List[Dict]) -> None:

    """
    Put the data into deep freeze (so to say) by parsing it into a SQLite database.
    We are using an SQLite database for several reasons, such as:

    * The associated drivers are part of the standard library.
    * The database is read-only (that is, we don't mean to edit it), so there are
      no speed considerations involved.
    * As far as I know, we are not going to read the database from multiple threads
      or processes. Hopefully the need to do that never arises.

    This database can be updated by the user, using the `update` command in the cli.
    The database is made anew everytime the user decides to do that though. We do not
    add (or remove) additional rows using SQL.

    Args:
        molecules:  A dictionary containing all the molecules we just scraped,
                    ready to be thrown into the deep freeze.
    """

    if squealer.exists():
        squealer.unlink()

    Base.metadata.create_all(thomas)

    with Session(thomas) as session:
        for molecule in molecules:
            mole = Molecule(
                formula=molecule["formula"],
                year=molecule["year"],
                tentative=molecule["tentative"],
            )
            for name, emband in molecule["sources"]:
                if name is not None:
                    if name.find(",") != -1:
                        names = re.split(r"\s*[,]\s*", name)
                        embands = [emband] * len(names)
                        for name, emband in zip(names, embands):
                            if name == "etc.":
                                name = None
                                emband = None
                            source = Source(name=name, emband=emband)
                            mole.sources.append(source)
                    else:
                        source = Source(name=name, emband=emband)
                        mole.sources.append(source)
                else:
                    source = Source(name=name, emband=emband)
                    mole.sources.append(source)
            for name, link, authors in molecule["references"]:
                reference = Reference(name=name, link=link)
                for author in authors:
                    auth = Author(name=author[0].strip())
                    reference.authors.append(auth)
                mole.references.append(reference)
            extragalactic = Extragalactic(
                name=molecule["extragalactic"][0],
                cdms=molecule["extragalactic"][1],
            )
            mole.extragalactic.append(extragalactic)
            session.add(mole)
            session.commit()


def search(
    by_formula: Optional[str] = None,
    by_year_range: Optional[Tuple[int, int]] = None,
    by_tentative: Optional[bool] = None,
    by_source: Optional[str] = None,
    by_author: Optional[str] = None,
    by_extragalactic: Optional[str] = None,
):

    """
    Search the **spacetar** database. Here we basically construct SQL queries
    programatically using SQLAlchemy's excellent API for the same, and then
    return the results as a list.
    """

    the_zeroth = lambda x: [_[0] for _ in x]

    with Session(thomas) as session:

        parameters = [
            (0, by_formula),
            (1, by_year_range),
            (2, by_tentative),
            (3, by_source),
            (4, by_author),
            (5, by_extragalactic),
        ]

        query = select(Molecule)

        if all([_ is None for _ in parameters]):
            return the_zeroth(session.execute(query).all())

        riddler: Dict[int, Callable] = {
            0: lambda q, formula: q.where(Molecule.formula == formula),
            1: lambda q, year_range: q.where(Molecule.year == year_range[0])
            if year_range[0] == year_range[1]
            else (
                q.where(Molecule.year > year_range[0])
                if year_range[1] == -1
                else (
                    q.where(Molecule.year < year_range[1])
                    if year_range[0] == -1
                    else q.where(Molecule.year > year_range[0]).where(
                        Molecule.year < year_range[1]
                    )
                )
            ),
            2: lambda q, tentative: q.where(Molecule.tentative == tentative),
            3: lambda q, source: q.where(Molecule.sources.any(Source.name == source)),
            4: lambda q, author: q.where(
                Molecule.references.any(Reference.authors.any(Author.name == author))
            ),
            5: lambda q, extragalactic: q.where(
                Molecule.extragalactic.any(Extragalactic.name == extragalactic)
            ),
        }

        for id, parameter in [_ for _ in parameters if _[-1] is not None]:
            riddle = riddler.get(id, None)
            if riddle:
                query = riddle(query, parameter)

        return the_zeroth(session.execute(query).all())


def richie_rich(results: List, pager: bool = True) -> None:

    """
    Print the results using the excellent `rich` library (link to thw source
    at GitHub; https://github.com/willmcgugan/rich; the documentation is here:
    https://rich.readthedocs.io/). We use the `Table` class to print a nicely
    formatted table to the command line. By default, we display the output using
    a pager, because the reults will be long in the usual case. The user will be
    given the option to print the results out onto the command line as well, if
    they so choose.

    Args:
        results:    A list of search results.
        pager:      If True, use a pager for the output. (Default: True)
    """

    from rich.table import Table
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()

    rsize = len(results)

    header = [
        "Chemical Formula",
        "Discovery Year",
        "Tentative? (Yes/No)",
        "Astronomical Source",
        "Discovery References",
        "Extragalactic Detection",
    ]

    marked = lambda x: Markdown("\n".join([f"* {_}" for _ in x]))

    table = Table(
        *header,
        title=f"Query results | Number of results: {rsize}",
        title_justify="center",
    )

    for result in results:
        table.add_row(
            result.formula,
            str(result.year),
            f"{'Yes' if result.tentative else 'No'}",
            marked(
                [
                    f"Discovered in {_.name if _.name else 'N/A'} in the {_.emband} band."
                    for _ in result.sources
                ]
            ),
            marked([_.name for _ in result.references]),
            marked([_.name for _ in result.extragalactic]),
        )

    if pager:
        with console.pager():
            console.print(table)
    else:
        console.print(table)


@click.command()
@click.option("-f", "--formula", type=str)
@click.option("-iny", "--year", type=int)
@click.option("-bfy", "--before", type=int)
@click.option("-afy", "--after", type=int)
@click.option("-bwy", "--between", nargs=2, type=int)
@click.option("-s", "--source", type=str)
@click.option("-a", "--author", type=str)
@click.option("-e", "--extragalactic", type=str)
@click.option("-t", "--tentative", is_flag=True, default=None)
@click.option("-np", "--no-pager", is_flag=True, default=False)
@click.option("-h", "--help", is_flag=True, default=False)
@click.option("-u", "--update", is_flag=True, default=False)
@click.option("-v", "--version", is_flag=True, default=False)
def cli(
    formula: Optional[str],
    year: Optional[int],
    before: Optional[int],
    after: Optional[int],
    between: Optional[Tuple[int, int]],
    tentative: Optional[bool],
    source: Optional[str],
    author: Optional[str],
    extragalactic: Optional[str],
    no_pager: bool,
    help: bool,
    update: bool,
    version: bool,
):

    """
    The spacetar CLI tool.
    """

    from sys import exit
    from rich.panel import Panel
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()

    if help:
        console.print(
            Panel(
                Markdown(
                    (here / "USAGE.md")
                    .read_text(encoding="utf-8")
                    .replace("# Usage\n", "")
                ),
                padding=1,
                expand=True,
                title_align="left",
                title="[bold yellow]spacetar: Space molecules in your terminal![/]",
            )
        )
        exit(0)

    if update:
        with console.status("Updating database ...", spinner="material"):
            deep_freeze(scrap())
        console.print(":+1: Done")
        exit(0)

    if version:
        console.print(f"[italic]Version[/italic]: [green underline]{get_version()!r}")
        exit(0)

    def year_range():

        if (before is not None) and (after is None):
            return (-1, before)
        elif (after is not None) and (before is None):
            return (after, -1)
        elif (before is not None) and (after is not None):
            console.print(
                Markdown(
                    ":skull: Cannot specify both `-bwy/--before` and `-awy/--after` options at the same time! Exiting..."
                )
            )
            exit(2)

        if len(between) != 0:
            return between

        if year is not None:
            return (year, year)

        return None

    richie_rich(
        search(
            by_formula=formula,
            by_year_range=year_range(),
            by_tentative=tentative,
            by_source=source,
            by_author=author,
            by_extragalactic=extragalactic,
        ),
        pager=(not no_pager),
    )
