from typing import Any, List
from rich.panel import Panel
from rich.table import Table
from rich.table import Column
from rich.console import Console
from rich.markdown import Markdown

from .core import __here__, __version__


screen = Console()


def unordered_list(objarr: List[Any]) -> str:

    """
    Takes an array of objects (one of `Molecule`, `Source`, or `Telescope`)
    and returns a unordered/bulleted list of the members as a string ready
    to be rendered onto the terminal.

    Args:
        objarr:     The array of objects.

    Returns:
        An unordered/bulleted list as a string.
    """

    return "\n".join([f"[yellow]*[/] {obj.name}" for obj in objarr])


def comma_join(objarr: List[Any]) -> str:

    """
    Takes an array of objects (one of `Molecule`, `Source`, or `Telescope`)
    and returns a comma-separated string made from the `name` attributes of
    all the members.

    Args:
        objarr:     The array of objects.

    Returns:
        A comma-separated string of member names.
    """

    return ", ".join([f"{obj.name}" for obj in objarr])


def render_mol_type(obj: Any) -> str:

    """
    Take a `Molecule` object and return the type of molecule as a
    string ready to be rendered onto the terminal. The type of each
    molecule is stored as a couple of boolean values. This function
    takes those values and renders a string according to which values
    evaluate to `True`.

    Args:
        obj:    A `Molecule` object.

    Returns:
        A string that encodes the molecule's type.
    """

    return ", ".join(
        [
            name
            for name, value in {
                "neutral": obj.neutral,
                "cation": obj.cation,
                "anion": obj.anion,
                "radical": obj.radical,
                "cyclic": obj.cyclic,
                "fullerene": obj.fullerene,
                "polyaromatic": obj.polyaromatic,
            }.items()
            if value
        ]
    )


def formulate(formula: str) -> str:

    """
    Takes a molecular formula and renders all numbers in it as
    subscripts, using Unicode characters (the \\u208x series).
    This is the best, and only, way to render subscripts onto
    the terminal. This will only work for terminals with Unicode
    support.

    Args:
        formula:    The molecular formula, represented as a string.

    Returns:
        The molecular formula back again, this time with subscripts.
    """

    for num, sub in {
        0: "\u2080",
        1: "\u2081",
        2: "\u2082",
        3: "\u2083",
        4: "\u2084",
        5: "\u2085",
        6: "\u2086",
        7: "\u2087",
        8: "\u2088",
        9: "\u2089",
    }.items():
        formula = formula.replace(str(num), str(sub))
    return formula


def mol_row(mol: Any) -> List[str]:

    """
    Render a row in a table of `Molecule`s.

    Args:
        mol:    A `Molecule`.

    Returns:
        A row in the table representing this `Molecule` instance
        as s list of strings. These strings contain console markup
        that works with the `rich` package. This function is used
        to render the table of molecules onto the terminal.
    """

    return [
        "[b]{formula}[/]\n[b]{name}[/]\n[u]{kind}[/]".format(
            formula=formulate(mol.formula),
            name=mol.name,
            kind=render_mol_type(mol),
        ),
        f"{mol.year}",
        unordered_list(mol.sources),
        unordered_list(mol.telescopes),
        unordered_list(mol.wavelengths),
        f"{mol.mass}",
        f"A = {str(mol.A)}\nB = {str(mol.B)}\nC = {str(mol.C)}",
        f"\u03BA = {str(mol.kappa)}",
    ]


def mol_header() -> List[Column]:

    """
    The header for a table of `Molecule`s.
    """

    return [
        Column(header="[u]Name[/] [b](Chemical Formula)[/]", justify="left"),
        Column(header="Discovery Year", justify="center"),
        Column(header="Source(s)", justify="left"),
        Column(header="Telescope(s)", justify="left"),
        Column(header="Wavelength(s)", justify="left"),
        Column(header="Molecular Mass\n(in a.m.u.)", justify="center"),
        Column(header="Rotational Constants\n(A, B, C)", justify="center"),
        Column(header="Ray's Asymmetry Parameter\n(\u03BA)", justify="center"),
    ]


def mol_summary(mol: Any) -> Panel:

    """
    Takes a `Molecule` and summarises the information about it into that
    can be rendered onto a terminal. We use `rich` again to pretty print
    the information as a `Panel`. This is inspired by a similar function
    in the `main_database.py` file in the original astrochemical census
    repository.

    Args:
        mol;    A `Molecule`.

    Returns:
        A `Panel` with summarised information about the molecule.
    """

    grid = Table.grid()
    grid.add_column(justify="left")
    grid.add_column(justify="right")

    grid.add_row("Formula:", f"{formulate(mol.formula)}")
    grid.add_row("Molecular mass (in a.m.u.):", f"{mol.mass}")
    grid.add_row("Type:", f"{render_mol_type(mol)}")
    grid.add_row("Discovery year:", f"{mol.year}")
    grid.add_row("Detected in:", f"{comma_join(mol.sources)}")
    grid.add_row("         by:", f"{comma_join(mol.telescopes)}")
    grid.add_row("         in wavelength(s):", f"{comma_join(mol.wavelengths)}")
    grid.add_row("Also detected in:", f"{mol.ice}")
    grid.add_row("Rotational Constants ([u]A, B, C[/])", f"{mol.A}, {mol.B}, {mol.C}")
    grid.add_row("Ray's Asymmetry Parameter (\u03BA)", f"{mol.kappa}")

    return Panel(
        grid,
        padding=2,
        expand=False,
        title=f"{mol.name}",
        title_align="left",
    )


def src_row(src: Any) -> List[str]:

    """
    Render a row in a table of `Source`s.

    Args:
        src:    A `Source`.

    Returns:
        A row in the table representing this `Source` instance
        as s list of strings. These strings contain console markup
        that works with the `rich` package. This function is used
        to render the table of sources onto the terminal.
    """

    return [
        f"{src.name}",
        f"{src.kind}",
        f"{src.ra}",
        f"{src.dec}",
        f"{src.detects}",
        f"{src.simbad_url}",
    ]


def src_header() -> List[Column]:

    """
    The header for a table of `Source`s.
    """

    return [
        Column(header="Name", justify="center"),
        Column(header="Type", justify="center"),
        Column(header="RA", justify="center"),
        Column(header="DEC", justify="center"),
        Column(header="Number of Detections", justify="center"),
        Column(header="SIMBAD Database URL", justify="center"),
    ]


def src_summary(src: Any):

    """
    Takes a `Source` and summarises the information about it into that
    can be rendered onto a terminal. We use `rich` again to pretty print
    the information as a `Panel`. This is inspired by a similar function
    in the `main_database.py` file in the original astrochemical census
    repository.

    Args:
        mol;    A `Source`.

    Returns:
        A `Panel` with summarised information about the source.
    """

    pass


def tel_row(tel: Any) -> List[str]:

    """
    Render a row in a table of `Telescope`s.

    Args:
        tel:    A `Telescope`.

    Returns:
        A row in the table representing this `Telescope` instance
        as s list of strings. These strings contain console markup
        that works with the `rich` package. This function is used
        to render the table of telescopes onto the terminal.
    """

    return [
        f"{tel.name}",
        f"{tel.nick}",
        f"{tel.kind}",
        comma_join(tel.wavelengths),
        f"{tel.latitude}",
        f"{tel.longitude}",
        f"{tel.diameter}",
        f"{tel.built}",
        f"{tel.decommissioned}",
        f"{tel.detects}",
    ]


def tel_header() -> List[Column]:

    """
    The header for a table of `Telescope`s.
    """

    return [
        Column(header="Name", justify="center"),
        Column(header="Nick", justify="center"),
        Column(header="Type", justify="center"),
        Column(header="Operational Wavelength(s)", justify="center"),
        Column(header="Latitude", justify="center"),
        Column(header="Longitude", justify="center"),
        Column(header="Diameter", justify="center"),
        Column(header="Built in", justify="center"),
        Column(header="Decommissioned in", justify="center"),
        Column(header="Number of Detections", justify="center"),
    ]


def tel_summary(tel: Any):

    """
    Takes a `Telescope` and summarises the information about it into that
    can be rendered onto a terminal. We use `rich` again to pretty print
    the information as a `Panel`. This is inspired by a similar function
    in the `main_database.py` file in the original astrochemical census
    repository.

    Args:
        mol;    A `Telescope`.

    Returns:
        A `Panel` with summarised information about the telescope.
    """

    pass


def rich_tabular_repr(rows: List, kind: str) -> Table:

    """
    Takes a list of search results and renders it into a table
    to be rendered onto the terminal.

    Args:
        rows:   The list of search results.
        kind:   The kind/type of object that is in the search
                results. This can be only one of `Molecule`,
                `Source` or `Telescope`.

    Returns:
        A `Table` to be rendered onto the terminal.
    """

    rich_row, rich_header = {
        "mol": (mol_row, mol_header),
        "src": (src_row, src_header),
        "tel": (tel_row, tel_header),
    }[kind]

    table = Table(
        *rich_header(),
        padding=0,
        expand=True,
        show_lines=True,
        title_style="bold",
        caption_style="bold",
        title=f"Number of results: {len(rows)}",
        caption="spacetar | Copyright (c) 2021 Ujjwal Panda",
    )

    for row in rows:
        table.add_row(*rich_row(row))
    return table


def summarize(obj: Any, kind: str) -> Panel:

    """
    Summarize the information about `obj` as a `Panel`, ready to be
    rendered onto the terminal.

    Args:
        obj:    The object to be summarized.
        kind:   The kind/type of object that is being summarized.
                This can be only one of `Molecule`, `Source` or
                `Telescope`.

    Returns:
        A `Panel` with the summarized information, ready to be
        rendered onto the terminal.
    """

    return {"mol": mol_summary, "src": src_summary, "tel": tel_summary}[kind](obj)


def print_usage():

    """
    Pretty print usage information about spacetar, using `rich`'s
    `Markdown` API. We use a pager to render the output to the
    terminal, because the usage examples are too long for a single
    window.
    """

    usage = __here__ / "data" / "usage.md"

    with screen.pager(styles=True):
        screen.print(Markdown(usage.read_text(encoding="utf-8")))


def print_version():

    """
    Pretty print the version of spacetar installed.
    """

    screen.print(f"Version: [u]{__version__}[/]")
