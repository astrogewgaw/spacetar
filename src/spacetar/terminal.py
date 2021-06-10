import sys
import typer

from textwrap import dedent
from typing import List, Optional
from rich.markdown import Markdown

from .display import screen, print_usage, print_version
from .search import search_source, search_molecule, search_telescope


app = typer.Typer()


@app.command()
def usage() -> None:

    """
    Show a bunch of usage examples for spacetar.
    This uses a pager to display the uotput onto
    the terminal.
    """

    print_usage()
    sys.exit(0)


@app.command()
def version() -> None:

    """
    Print the version of spacetar installed on the terminal.
    """

    print_version()
    sys.exit(0)


@app.command()
def mols(
    like: bool = False,
    no_pager: bool = False,
    name: Optional[str] = None,
    formula: Optional[str] = None,
    year: Optional[List[int]] = typer.Option(None),
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
) -> None:

    """
    Search the space molecules database in spacetar.
    """

    if year is not None:
        if len(year) > 2:
            screen.print("An year range cannot have more than two values. Exiting...")
            sys.exit(1)
        if len(year) == 1:
            year = year * 2
        if len(year) == 0:
            year = None

    molecules = search_molecule(
        like=like,
        name=name,
        formula=formula,
        year=year,
        source=source,
        telescope=telescope,
        wavelength=wavelength,
        neutral=neutral,
        cation=cation,
        anion=anion,
        radical=radical,
        cyclic=cyclic,
        fullerene=fullerene,
        polyaromatic=polyaromatic,
        ice=ice,
        ppd=ppd,
        exgal=exgal,
        exo=exo,
    )

    if len(molecules.rows) == 0:
        screen.print(
            Markdown(
                dedent(
                    """
                    No results to display.
                    Maybe add the  `--like` option and try again?
                    """
                )
                .strip()
                .replace("\n", " ")
            )
        )
        sys.exit(0)

    if len(molecules.rows) == 1:
        screen.print(molecules.rows[0])
        sys.exit(0)

    if no_pager:
        screen.print(molecules)
        sys.exit(0)
    else:
        with screen.pager(styles=True):
            screen.print(molecules)
        sys.exit(0)


@app.command()
def srcs(
    like: bool = False,
    no_pager: bool = False,
    name: Optional[str] = None,
    kind: Optional[str] = None,
    detects: Optional[List[int]] = typer.Option(None),
) -> None:

    """
    Search the astronomical sources in spacetar.
    """

    if detects is not None:
        if len(detects) > 2:
            screen.print("A range cannot have more than two values. Exiting...")
            sys.exit(1)
        if len(detects) == 1:
            detects = detects * 2
        if len(detects) == 0:
            detects = None

    sources = search_source(
        like=like,
        name=name,
        kind=kind,
        detects=detects,
    )

    if len(sources.rows) == 0:
        screen.print(
            Markdown(
                dedent(
                    """
                    No results to display.
                    Maybe add the  `--like` option and try again?
                    """
                )
                .strip()
                .replace("\n", " ")
            )
        )
        sys.exit(0)

    if len(sources.rows) == 1:
        screen.print(sources.rows[0])
        sys.exit(0)

    if no_pager:
        screen.print(sources)
        sys.exit(0)
    else:
        with screen.pager(styles=True):
            screen.print(sources)
        sys.exit(0)


@app.command()
def tels(
    like: bool = False,
    no_pager: bool = False,
    name: Optional[str] = None,
    kind: Optional[str] = None,
    wavelength: Optional[str] = None,
    diameter: Optional[int] = None,
    built: Optional[List[int]] = typer.Option(None),
    decommissioned: Optional[List[int]] = typer.Option(None),
    detects: Optional[List[int]] = typer.Option(None),
) -> None:

    """
    Search the telescopes database in spacetar.
    """

    if detects is not None:
        if len(detects) > 2:
            screen.print("A range cannot have more than two values. Exiting...")
            sys.exit(1)
        if len(detects) == 1:
            detects = detects * 2
        if len(detects) == 0:
            detects = None

    if built is not None:
        if len(built) > 2:
            screen.print("An year range cannot have more than two values. Exiting...")
            sys.exit(1)
        if len(built) == 1:
            built = built * 2
        if len(built) == 0:
            built = None

    if decommissioned is not None:
        if len(decommissioned) > 2:
            screen.print("An year range cannot have more than two values. Exiting...")
            sys.exit(1)
        if len(decommissioned) == 1:
            decommissioned = decommissioned * 2
        if len(decommissioned) == 0:
            decommissioned = None

    telescopes = search_telescope(
        like=like,
        name=name,
        kind=kind,
        wavelength=wavelength,
        diameter=diameter,
        built=built,
        decommissioned=decommissioned,
        detects=detects,
    )

    if len(telescopes.rows) == 0:
        screen.print(
            Markdown(
                dedent(
                    """
                    No results to display.
                    Maybe add the  `--like` option and try again?
                    """
                )
                .strip()
                .replace("\n", " ")
            )
        )
        sys.exit(0)

    if len(telescopes.rows) == 1:
        screen.print(telescopes.rows[0])
        sys.exit(0)

    if no_pager:
        screen.print(telescopes)
        sys.exit(0)
    else:
        with screen.pager(styles=True):
            screen.print(telescopes)
        sys.exit(0)
