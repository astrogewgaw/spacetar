from textwrap import dedent
from typing import Any, List
from rich.panel import Panel
from rich.table import Table
from rich.table import Column
from rich.console import Console
from rich.markdown import Markdown

from .core import __version__


screen = Console()


def ul(objarr: List[Any]) -> str:

    """"""

    return "\n".join([f"[yellow]*[/] {obj.name}" for obj in objarr])


def commas(objarr: List[Any]) -> str:

    """"""

    return ", ".join([f"{obj.name}" for obj in objarr])


def kindof(obj: Any) -> str:

    """"""

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

    """"""

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

    """"""

    return [
        "[b]{formula}[/]\n[b]{name}[/]\n[u]{kind}[/]".format(
            formula=formulate(mol.formula),
            name=mol.name,
            kind=kindof(mol),
        ),
        f"{mol.year}",
        ul(mol.sources),
        ul(mol.telescopes),
        ul(mol.wavelengths),
        f"{mol.mass}",
        f"A = {str(mol.A)}\nB = {str(mol.B)}\nC = {str(mol.C)}",
        f"\u03BA = {str(mol.kappa)}",
    ]


def mol_header():

    """"""

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

    """"""

    grid = Table.grid()
    grid.add_column(justify="left")
    grid.add_column(justify="right")

    grid.add_row("Formula:", f"{formulate(mol.formula)}")
    grid.add_row("Molecular mass (in a.m.u.):", f"{mol.mass}")
    grid.add_row("Type:", f"{kindof(mol)}")
    grid.add_row("Discovery year:", f"{mol.year}")
    grid.add_row("Detected in:", f"{commas(mol.sources)}")
    grid.add_row("         by:", f"{commas(mol.telescopes)}")
    grid.add_row("         in wavelength(s):", f"{commas(mol.wavelengths)}")
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


def src_row(src: Any):

    """"""

    return [
        f"{src.name}",
        f"{src.kind}",
        f"{src.ra}",
        f"{src.dec}",
        f"{src.detects}",
        f"{src.simbad_url}",
    ]


def src_header():

    """"""

    return [
        Column(header="Name", justify="center"),
        Column(header="Type", justify="center"),
        Column(header="RA", justify="center"),
        Column(header="DEC", justify="center"),
        Column(header="Number of Detections", justify="center"),
        Column(header="SIMBAD Database URL", justify="center"),
    ]


def src_summary(src: Any):

    """"""

    pass


def tel_row(tel: Any):

    """"""

    return [
        f"{tel.name}",
        f"{tel.nick}",
        f"{tel.kind}",
        commas(tel.wavelengths),
        f"{tel.latitude}",
        f"{tel.longitude}",
        f"{tel.diameter}",
        f"{tel.built}",
        f"{tel.decommissioned}",
        f"{tel.detects}",
    ]


def tel_header():

    """"""

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

    """"""

    pass


def rich_tabular_repr(rows: List, kind: str) -> Table:

    """"""

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

    """"""

    return {"mol": mol_summary, "src": src_summary, "tel": tel_summary}[kind](obj)


def print_usage():

    """"""

    return Panel(
        Markdown(
            dedent(
                """
                # Usage

                This is *spacetar*.
                """
            ).strip()
        ),
        title="Usage",
    )


def print_version():

    """"""

    return ""
