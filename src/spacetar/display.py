from typing import List
from textwrap import dedent
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console, RenderGroup

from .core import _data, __version__
from .chimie import formula_to_unicode
from .core import Molecule, Source, Telescope


console = Console()


_kappa = "\u03BA"
_copyright = "[b]spacetar[/] | Copyright (c) 2021 [b]Ujjwal Panda[/]"
_commas = lambda _: ", ".join([f"{__.name}" for __ in _])
_bullets = lambda _: "\n".join([f"[yellow]*[/] {__.name}" for __ in _])
_kindof = lambda _: ", ".join(
    [
        name
        for name, value in {
            "Neutral": _.neutral,
            "Cation": _.cation,
            "Anion": _.anion,
            "Radical": _.radical,
            "Cyclic": _.cyclic,
            "Fullerene": _.fullerene,
            "Polyaromatic Hydrocarbon (PAH)": _.polyaromatic,
        }.items()
        if value
    ]
)
_detections = lambda _: Panel(
    "\n".join(
        [
            f"[yellow1]{str(i + 1)}[/]. {formula_to_unicode(str(__.formula))} ({__.name})"
            for (
                i,
                __,
            ) in enumerate(_.molecules)
        ]
    ),
    title=f"Number of molecules detected: {_.detects}",
)
_decommissioned = lambda _: (
    dedent(
        f"""
                {
                    (
                        _.decommissioned
                        if _.decommissioned is not None
                        else 'Still working...'
                    )
                }
                """
    )
    .replace("\n", "")
    .strip()
)


def render_usage(kind: str = "cli"):

    """"""

    if kind not in ["cli", "py"]:
        raise ValueError("There is no help for using spacetar this way. Exiting...")

    with console.pager(styles=True):
        console.print(
            Markdown(
                (_data / f"{kind}_usage.md").read_text(encoding="utf-8"),
                justify="full",
            )
        )


def render_version():

    """"""

    console.print(f"[b]Version[/]: [u]{__version__}[/]")


def summarize_molecule(molecule: Molecule):

    """"""

    grid = Table.grid()
    grid.add_column(justify="left")
    grid.add_column(justify="right")

    grid.add_row("Formula:", f"{formula_to_unicode(str(molecule.formula))}")
    grid.add_row("Molecular mass (in a.m.u.):", f"{molecule.mass}")
    grid.add_row("Type:", f"{_kindof(molecule)}")
    grid.add_row("Discovery year:", f"{molecule.year}")
    grid.add_row("Detected in:", f"{_commas(molecule.sources)}")
    grid.add_row("         by:", f"{_commas(molecule.telescopes)}")
    grid.add_row("         in wavelength(s):", f"{_commas(molecule.wavelengths)}")
    grid.add_row("[u]Rotational Constants[/]")
    grid.add_row("                   A:", f"{molecule.A}")
    grid.add_row("                   B:", f"{molecule.B}")
    grid.add_row("                   C:", f"{molecule.C}")
    grid.add_row("Ray's Asymmetry Parameter (\u03BA)", f"{molecule.kappa}")

    _alsos = "\n".join(
        [
            f"[yellow1]*[/] {__}"
            for _, __ in [
                (molecule.ice, "Interstellar Ices"),
                (molecule.ppd, "Protoplanetary Disks"),
                (molecule.exgal, "Extragalactic Sources"),
                (molecule.exo, "Exoplanets"),
            ]
            if _
        ]
    )

    if _alsos == "":
        _alsos = "Nothing else."

    return Panel(
        RenderGroup(
            grid,
            "\n",
            Panel(_alsos, title="Also detected in", padding=1),
            Panel(
                (f"\n{molecule.notes}" if molecule.notes is not None else "Nothing."),
                title="Notes",
                expand=True,
            ),
        ),
        padding=2,
        expand=False,
        title=f"{molecule.name} :test_tube:",
        title_align="left",
    )


def tabulate_molecules(molecules: List[Molecule]):

    """"""

    table = Table(
        expand=True,
        show_lines=True,
        title=dedent(
            f"""
            [u]Number of molecules[/]:
            [b]{len(molecules)}[/]
            out of a total of
            [b]220[/].
            """
        )
        .replace("\n", " ")
        .strip(),
        title_style="bold",
        caption=_copyright,
        caption_style="bold",
    )

    table.add_column("Space molecule", justify="left")
    table.add_column("Year discovered in", justify="center")
    table.add_column("Source(s) detected in", justify="left")
    table.add_column("Telescope(s) detected by", justify="left")
    table.add_column("Wavelength band(s) detected in", justify="left")
    table.add_column("Rotational constants", justify="center")
    table.add_column(f"Ray's asymmetry parameter\n({_kappa})", justify="center")

    for molecule in molecules:

        rot_consts = Table.grid(expand=True)
        rot_consts.add_column(justify="left")
        rot_consts.add_column(justify="right")

        rot_consts.add_row(
            "A:",
            f"""{
                molecule.A
                if molecule.A is not None
                else '[b u]None'
            }""",
        )

        rot_consts.add_row(
            "B:",
            f"""{
                molecule.B
                if molecule.B is not None
                else '[b u]None'
            }""",
        )

        rot_consts.add_row(
            "C:",
            f"""{
                molecule.C
                if molecule.C is not None
                else '[b u]None'
            }""",
        )

        table.add_row(
            dedent(
                f"""
                Formula: [b]{formula_to_unicode(str(molecule.formula))}[/]
                Name: [i]{molecule.name}[/]
                Type: {_kindof(molecule)}
                Molecular mass: {molecule.mass:.2f} a.m.u.
                """
            ).strip(),
            f"{molecule.year:d}",
            _bullets(molecule.sources),
            _bullets(molecule.telescopes),
            _bullets(molecule.wavelengths),
            rot_consts,
            (
                f"{_kappa} = {molecule.kappa:.6f}"
                if molecule.kappa is not None
                else f"{_kappa} = [b u]None"
            ),
        )

    return table


def summarize_source(source: Source):

    """"""

    grid = Table.grid()
    grid.add_column(justify="left")
    grid.add_column(justify="right")

    grid.add_row("Type:", f"{source.kind}")
    grid.add_row("Right Ascension:", f"{source.ra}")
    grid.add_row("Declination:", f"{source.dec}")
    grid.add_row("Number of molecules detected:", f"{source.detects}")
    grid.add_row("SIMBAD URL:", f"[link]{source.simbad_url}[/]")

    return Panel(
        RenderGroup(
            grid,
            "\n",
            _detections(source),
        ),
        padding=2,
        expand=False,
        title=f"{source.name} :milky_way:",
        title_align="left",
    )


def tabulate_sources(sources: List[Source]):

    """"""

    table = Table(
        padding=0,
        expand=True,
        show_lines=True,
        title=dedent(
            f"""
            [u]Number of sources[/]:
            [b]{len(sources)}[/]
            out of a total of
            [b]63[/].
            """
        )
        .replace("\n", " ")
        .strip(),
        title_style="bold",
        caption=_copyright,
        caption_style="bold",
    )

    for name in [
        "Name",
        "Type of source",
        "Right Ascension",
        "Declination",
        "Number of Detections",
        "URL in the SIMBAD Database",
    ]:
        table.add_column(name, justify="center")

    for source in sources:
        table.add_row(
            f"{source.name}",
            f"{source.kind}",
            f"{source.ra}",
            f"{source.dec}",
            f"{source.detects:d}",
            f"{source.simbad_url}",
        )
    return table


def summarize_telescope(telescope: Telescope):

    """"""

    grid = Table.grid()

    grid.add_column(justify="left")
    grid.add_column(justify="right")

    grid.add_row("Full name:", f"{telescope.name}")
    grid.add_row("Type:", f"{telescope.kind}")
    grid.add_row("Wavelength(s) it operates in:", f"{_commas(telescope.wavelengths)}")

    grid.add_row(
        "Where is it?",
        dedent(
            f"""
            [i]Lat.[/] {telescope.latitude},
            [i]Long.[/] {telescope.longitude}
            """
        )
        .replace("\n", " ")
        .strip(),
    )

    grid.add_row("Diameter:", f"{telescope.diameter}")
    grid.add_row("Built in:", f"{telescope.built}")
    grid.add_row("Decommissioned in:", _decommissioned(telescope))

    return Panel(
        RenderGroup(
            grid,
            "\n",
            _detections(telescope),
            Panel(
                (f"\n{telescope.notes}" if telescope.notes is not None else ""),
                title="Notes",
                expand=True,
            ),
        ),
        padding=2,
        expand=False,
        title=f"{telescope.nick} :telescope:",
        title_align="left",
    )


def tabulate_telescopes(telescopes: List[Telescope]):

    """"""

    table = Table(
        padding=0,
        expand=True,
        show_lines=True,
        title=dedent(
            f"""
            [u]Number of telescopes[/]:
            [b]{len(telescopes)}[/]
            out of a total of
            [b]47[/]
            """
        )
        .replace("\n", " ")
        .strip(),
        title_style="bold",
        caption=_copyright,
        caption_style="bold",
    )

    for name in [
        "Name",
        "Nick",
        "Type of telescope",
        "Operational Wavelength(s)",
        "Latitude",
        "Longitude",
        "Diameter",
        "Built in",
        "Decommissioned in",
        "Number of Detections",
    ]:
        table.add_column(name, justify="center")

    for telescope in telescopes:
        table.add_row(
            f"{telescope.name}",
            f"{telescope.nick}",
            f"{telescope.kind}",
            _commas(telescope.wavelengths),
            f"{telescope.latitude}",
            f"{telescope.longitude}",
            f"{telescope.diameter}",
            f"{telescope.built}",
            _decommissioned(telescope),
            f"{telescope.detects}",
        )
    return table
