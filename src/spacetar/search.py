import attr

from typing import Any, List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import or_, and_, select  # type: ignore

from .display import rich_tabular_repr
from .orm import Engine, Source, Molecule, Telescope, Wavelength


@attr.s(repr=False, auto_attribs=True)
class Results(object):

    """
    Represents the results of a query into the SQLite database.
    The primary purpose of this class is to enable us to work
    with search results using a common API, and to pretty print
    them, using `rich`'s Console Protocol.

    Args:
        rows:   A list of search results from the SQLite database.
                All items in the list should be of the same type,
                and this should be one of `Molecule`, `Source`, or
                `Telescope`.
    """

    rows: List[Any]

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return str(self)

    def __rich__(self) -> Any:
        return rich_tabular_repr(
            rows=self.rows,
            kind={
                Source: "src",
                Molecule: "mol",
                Telescope: "tel",
            }[type(self.rows[0])],
        )


def likable(term: str) -> str:

    """
    Ready a search term for a *like* search. This just meahs adding a
    *%* character onto either side of the string. These serve the same
    purpose as a *wildcard* character.

    Args:
        term:   The search term to make *likable*. Must be a string.

    Returns:
        A string that is ready to be given as input to a SQL query for
        a like search.
    """

    return f"%{term}%"


def results(query: Any) -> Results:

    """
    Query the SQLite database and return the results as a `Result` object.

    Args:
        query:  The SQL query to execute.

    Returns:
        A `Results` object encapsulating the search results.
    """

    with Session(Engine) as session:
        return Results(rows=[_[0] for _ in session.execute(query).all()])


def search_molecule(
    like: bool = False,
    name: Optional[str] = None,
    formula: Optional[str] = None,
    year: Optional[List[int]] = None,
    source: Optional[str] = None,
    telescope: Optional[str] = None,
    wavelength: Optional[str] = None,
    neutral: Optional[bool] = None,
    cation: Optional[bool] = None,
    anion: Optional[bool] = None,
    radical: Optional[bool] = None,
    cyclic: Optional[bool] = None,
    fullerene: Optional[bool] = None,
    polyaromatic: Optional[bool] = None,
    ice: Optional[bool] = None,
    ppd: Optional[bool] = None,
    exgal: Optional[bool] = None,
    exo: Optional[bool] = None,
) -> Results:

    """
    Search for space molecules from the `molecules` table in the SQLite database.

    Args:
        like:           Do a *like* search. This inserts wildcard characters into
                        both sides of a string parameter and searches the SQLite
                        database. This allows the user to use parts of a name or
                        formula in their search, for instance.
        name:           Search for molecules by name.
        formula:        Seach for molecules by its molecular formula.
        year:           Search for molecules by the year were discovered.
        source:         Search for molecules by the source(s) they were discovered in.
        telescope:      Search for molecules by the telescope(s) they were discovered by.
        wavelength:     Search for molecules by the wavelength(s) in the electromagnetic
                        spectrum they were discovered in.
        neutral:        Search for molecules if they is neutral.
        cation:         Search for molecules if they is cation.
        anion:          Search for molecules if they is anion.
        radical:        Search for molecules if they is radical.
        cyclic:         Search for molecules if they is cyclic.
        fullerene:      Search for molecules if they is fullerene.
        polyaromatic:   Search for molecules if they is polyaromatic.
        ice:            Search for molecules if they has been discovered in interstellar ices.
        ppd:            Search for molecules if they has been discovered in protoplanetary disks.
        exgal:          Search for molecules if they has been discovered in extragalactic sources.
        exo:            Search for molecules if they has been discovered in exoplanets.

    Returns:
        A `Results` object.
    """

    params = {
        0: name,
        1: formula,
        2: year,
        3: source,
        4: telescope,
        5: wavelength,
        6: neutral,
        7: cation,
        8: anion,
        9: radical,
        10: cyclic,
        11: fullerene,
        12: polyaromatic,
        13: ice,
        14: ppd,
        15: exgal,
        16: exo,
    }

    queries = {
        0: lambda _, __: _.where(Molecule.name.like(__)),
        1: lambda _, __: _.where(Molecule.formula.like(__)),
        2: lambda _, __: _.where(
            and_(
                (Molecule.year >= __[0]),
                (Molecule.year <= __[1]),
            )
        ),
        3: lambda _, __: _.where(Molecule.sources.any(Source.name.like(__))),
        4: lambda _, __: _.where(
            Molecule.telescopes.any(
                or_(
                    Telescope.name.like(__),
                    Telescope.nick.like(__),
                )
            )
        ),
        5: lambda _, __: _.where(
            Molecule.wavelengths.any(
                Wavelength.name.like(__),
            )
        ),
        6: lambda _, __: _.where(Molecule.neutral == __),
        7: lambda _, __: _.where(Molecule.cation == __),
        8: lambda _, __: _.where(Molecule.anion == __),
        9: lambda _, __: _.where(Molecule.radical == __),
        10: lambda _, __: _.where(Molecule.cyclic == __),
        11: lambda _, __: _.where(Molecule.fullerene == __),
        12: lambda _, __: _.where(Molecule.polyaromatic == __),
        13: lambda _, __: _.where(Molecule.ice == __),
        14: lambda _, __: _.where(Molecule.ppd == __),
        15: lambda _, __: _.where(Molecule.exgal == __),
        16: lambda _, __: _.where(Molecule.exo == __),
    }

    query = select(Molecule)
    terms = {_: __ for _, __ in params.items() if __ is not None}

    if len(terms) == 0:
        return results(query)

    for id, term in terms.items():
        if like:
            if isinstance(term, str):
                term = likable(term)
        query = queries[id](query, term)
    return results(query)


def search_source(
    like: bool = False,
    name: Optional[str] = None,
    kind: Optional[str] = None,
    detects: Optional[List[int]] = None,
) -> Any:

    """
    Search for an astronomical source from the `sources` table in the SQLite database.

    Args:
        like:           Do a *like* search. This inserts wildcard characters into
                        both sides of a string parameter and searches the SQLite
                        database. This allows the user to use parts of a name in
                        the search, for instance.
        name:           Search for sources by their name.
        kind:           Search for sources by their kind/type.
        detects:        Search for sources by the number of molecules detected in them.
    """

    params = {
        0: name,
        1: kind,
        2: detects,
    }

    queries = {
        0: lambda _, __: _.where(Source.name.like(__)),
        1: lambda _, __: _.where(Source.kind == __),
        2: lambda _, __: _.where(
            and_(
                (Source.detects >= __[0]),
                (Source.detects <= __[1]),
            )
        ),
    }

    query = select(Source)
    terms = {_: __ for _, __ in params.items() if __ is not None}

    if len(terms) == 0:
        return results(query)

    for id, term in terms.items():
        if like:
            if isinstance(term, str):
                term = likable(term)
        query = queries[id](query, term)
    return results(query)


def search_telescope(
    like: bool = False,
    name: Optional[str] = None,
    kind: Optional[str] = None,
    wavelength: Optional[str] = None,
    diameter: Optional[int] = None,
    built: Optional[List[int]] = None,
    decommissioned: Optional[List[int]] = None,
    detects: Optional[List[int]] = None,
):

    """
    Search for a telescope from the `telescopes` table in the SQLite database.

    Args:
        like:               Do a *like* search. This inserts wildcard characters into
                            both sides of a string parameter and searches the SQLite
                            database. This allows the user to use parts of a name in
                            the search, for instance.
        name:               Search for telescopes by their full name.
        nick:               Search for telescopes by their short name (a.k.a. nick).
        wavelengths:        Search for telescopes by the wavelength(s) in the electromagnetic spectrum
                            they operate in.
        diameter:           Search for telescopes by their diameter, if applicable.
        built:              Search for telescopes by the year they were built in.
        decommissioned:     Search for telescopes by the year they were decommissioned in, if applicable.
        detects:            Search for telescopes by the number of molecules they have discovered.
    """

    params = {
        0: name,
        1: kind,
        2: wavelength,
        3: diameter,
        4: built,
        5: decommissioned,
        6: detects,
    }

    queries = {
        0: lambda _, __: _.where(
            or_(
                Telescope.name.like(__),
                Telescope.nick.like(__),
            )
        ),
        1: lambda _, __: _.where(Telescope.kind == __),
        2: lambda _, __: _.where(Telescope.wavelengths.any(Wavelength.name.like(__))),
        3: lambda _, __: _.where(
            and_(
                (Telescope.diameter >= __[0]),
                (Telescope.diameter <= __[1]),
            )
        ),
        4: lambda _, __: _.where(
            and_(
                (Telescope.built >= __[0]),
                (Telescope.built <= __[1]),
            )
        ),
        5: lambda _, __: _.where(
            and_(
                (Telescope.decommissioned >= __[0]),
                (Telescope.decommissioned <= __[1]),
            )
        ),
        6: lambda _, __: _.where(
            and_(
                (Telescope.detects >= __[0]),
                (Telescope.detects <= __[1]),
            )
        ),
    }

    query = select(Telescope)
    terms = {_: __ for _, __ in params.items() if __ is not None}

    if len(terms) == 0:
        return results(query)

    for id, term in terms.items():
        if like:
            if isinstance(term, str):
                term = likable(term)
        query = queries[id](query, term)
    return results(query)
