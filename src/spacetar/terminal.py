import sys
import click

from .core import _bands

from .search import (
    search_source,
    search_molecule,
    search_telescope,
)

from .display import (
    console,
    render_usage,
    render_version,
    summarize_source,
    tabulate_sources,
    summarize_molecule,
    tabulate_molecules,
    summarize_telescope,
    tabulate_telescopes,
)


@click.group(invoke_without_command=True)
@click.option("--help", is_flag=True, is_eager=True, default=None)
@click.option("--usage", is_flag=True, is_eager=True, default=None)
@click.option("--version", is_flag=True, is_eager=True, default=None)
def main(**kwargs):

    """"""

    if kwargs["help"]:
        pass

    if kwargs["usage"]:
        render_usage()
        sys.exit(0)

    if kwargs["version"]:
        render_version()
        sys.exit(0)


@main.command()
@click.option("--like", is_flag=True, default=False)
@click.option("--no-pager", is_flag=True, default=False)
@click.option("--name", type=str, default=None)
@click.option("--formula", type=str, default=None)
@click.option("--year", multiple=True, type=int, default=None)
@click.option("--source", type=str, default=None)
@click.option("--telescope", type=str, default=None)
@click.option(
    "--wavelength",
    type=click.Choice(
        _bands,
        case_sensitive=False,
    ),
    default=None,
)
@click.option("--neutral", is_flag=True, default=None)
@click.option("--cation", is_flag=True, default=None)
@click.option("--anion", is_flag=True, default=None)
@click.option("--radical", is_flag=True, default=None)
@click.option("--cyclic", is_flag=True, default=None)
@click.option("--fullerene", is_flag=True, default=None)
@click.option("--polyaromatic", is_flag=True, default=None)
@click.option("--ice", is_flag=True, default=None)
@click.option("--ppd", is_flag=True, default=None)
@click.option("--exgal", is_flag=True, default=None)
@click.option("--exo", is_flag=True, default=None)
def molecules(**kwargs) -> None:

    """"""

    no_pager = kwargs.pop("no_pager")
    molecules = search_molecule(**kwargs)
    if len(molecules) == 0:
        console.print("Nothing to show. Maybe try again with `--like`")
        sys.exit(0)
    if len(molecules) == 1:
        to_display = summarize_molecule(molecules[0])
    if len(molecules) > 1:
        to_display = tabulate_molecules(molecules)

    if no_pager:
        console.print(to_display)
    else:
        with console.pager(styles=True):
            console.print(to_display)


@main.command()
@click.option("--like", is_flag=True, default=False)
@click.option("--no-pager", is_flag=True, default=False)
@click.option("--name", type=str, default=None)
@click.option("--kind", type=str, default=None)
@click.option("--detects", type=int, multiple=True, default=None)
def sources(**kwargs) -> None:

    """"""

    no_pager = kwargs.pop("no_pager")
    sources = search_source(**kwargs)
    if len(sources) == 0:
        console.print("Nothing to show. Maybe try again with `--like`")
        sys.exit(0)
    if len(sources) == 1:
        to_display = summarize_source(sources[0])
    if len(sources) > 1:
        to_display = tabulate_sources(sources)

    if no_pager:
        console.print(to_display)
    else:
        with console.pager(styles=True):
            console.print(to_display)


@main.command()
@click.option("--like", is_flag=True, default=False)
@click.option("--no-pager", is_flag=True, default=False)
@click.option("--name", type=str, default=None)
@click.option("--kind", type=str, default=None)
@click.option(
    "--wavelength",
    type=click.Choice(
        _bands,
        case_sensitive=False,
    ),
    default=None,
)
@click.option("--diameter", type=int, multiple=True, default=None)
@click.option("--built", type=int, multiple=True, default=None)
@click.option("--decommissioned", type=int, multiple=True, default=None)
@click.option("--detects", type=int, multiple=True, default=None)
def telescopes(**kwargs):

    """"""

    no_pager = kwargs.pop("no_pager")
    telescopes = search_telescope(**kwargs)
    if len(telescopes) == 0:
        console.print("Nothing to show. Maybe try again with `--like`")
        sys.exit(0)
    if len(telescopes) == 1:
        to_display = summarize_telescope(telescopes[0])
    if len(telescopes) > 1:
        to_display = tabulate_telescopes(telescopes)

    if no_pager:
        console.print(to_display)
    else:
        with console.pager(styles=True):
            console.print(to_display)
