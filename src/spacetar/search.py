from sqlalchemy import or_, and_, select  # type: ignore
from sqlalchemy.orm import Query, Session  # type: ignore

from typing import Any, List, Optional

from .core import (
    Engine,
    Source,
    Molecule,
    Telescope,
    Wavelength,
)


_likable = lambda _: f"%{_}%"
_ranger = lambda _: (
    {
        0: None,
        1: _ * 2,
        2: _,
    }.get(len(_), None)
    if _ is not None
    else _
)


def _results(query: Query) -> List:
    with Session(Engine) as session:
        return [_[0] for _ in session.execute(query).all()]


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
) -> List:

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

    query = select(Molecule).order_by(Molecule.year)

    terms = [
        name,
        formula,
        _ranger(year),
        source,
        telescope,
        wavelength,
        neutral,
        cation,
        anion,
        radical,
        cyclic,
        fullerene,
        polyaromatic,
        ice,
        ppd,
        exgal,
        exo,
    ]

    extensions = [
        lambda _: query.where(Molecule.name.like(_)),
        lambda _: query.where(Molecule.formula.like(_)),
        lambda _: query.where(and_((Molecule.year >= _[0]), (Molecule.year <= _[1]))),
        lambda _: query.where(Molecule.sources.any(Source.name.like(_))),
        lambda _: query.where(
            Molecule.telescopes.any(
                or_(
                    Telescope.name.like(_),
                    Telescope.nick.like(_),
                )
            )
        ),
        lambda _: query.where(Molecule.wavelengths.any(Wavelength.name.like(_))),
        lambda _: query.where(Molecule.neutral == _),
        lambda _: query.where(Molecule.cation == _),
        lambda _: query.where(Molecule.anion == _),
        lambda _: query.where(Molecule.radical == _),
        lambda _: query.where(Molecule.cyclic == _),
        lambda _: query.where(Molecule.fullerene == _),
        lambda _: query.where(Molecule.polyaromatic == _),
        lambda _: query.where(Molecule.ice == _),
        lambda _: query.where(Molecule.ppd == _),
        lambda _: query.where(Molecule.exgal == _),
        lambda _: query.where(Molecule.exo == _),
    ]

    if not any(terms):
        return _results(query)

    for term, extension in zip(terms, extensions):
        if term is not None:
            if like:
                if isinstance(term, str):
                    term = _likable(term)
            query = extension(term)
    return _results(query)


def search_source(
    like: bool = False,
    name: Optional[str] = None,
    kind: Optional[str] = None,
    detects: Optional[List[int]] = None,
) -> List:

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

    query = select(Source).order_by(Source.detects)

    terms = [name, kind, _ranger(detects)]

    extensions = [
        lambda __: query.where(Source.name.like(__)),
        lambda __: query.where(Source.kind.like(__)),
        lambda __: query.where(
            and_(
                (Source.detects >= __[0]),
                (Source.detects <= __[1]),
            )
        ),
    ]

    if not any(terms):
        return _results(query)

    for term, extension in zip(terms, extensions):
        if term is not None:
            if like:
                if isinstance(term, str):
                    term = _likable(term)
            query = extension(term)
    return _results(query)


def search_telescope(
    like: bool = False,
    name: Optional[str] = None,
    kind: Optional[str] = None,
    wavelength: Optional[str] = None,
    diameter: Optional[List[int]] = None,
    built: Optional[List[int]] = None,
    decommissioned: Optional[List[int]] = None,
    detects: Optional[List[int]] = None,
) -> List:

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

    query = select(Telescope).order_by(Telescope.detects)

    terms = [
        name,
        kind,
        wavelength,
        _ranger(diameter),
        _ranger(built),
        _ranger(decommissioned),
        _ranger(detects),
    ]

    extensions = [
        lambda _: query.where(
            or_(
                Telescope.name.like(_),
                Telescope.nick.like(_),
            )
        ),
        lambda _: query.where(Telescope.kind == _),
        lambda _: query.where(Telescope.wavelengths.any(Wavelength.name.like(_))),
        lambda _: query.where(
            and_(
                (Telescope.diameter >= _[0]),
                (Telescope.diameter <= _[1]),
            )
        ),
        lambda _: query.where(
            and_(
                (Telescope.built >= _[0]),
                (Telescope.built <= _[1]),
            )
        ),
        lambda _: query.where(
            and_(
                (Telescope.decommissioned >= _[0]),
                (Telescope.decommissioned <= _[1]),
            )
        ),
        lambda _: query.where(
            and_(
                (Telescope.detects >= _[0]),
                (Telescope.detects <= _[1]),
            )
        ),
    ]

    if not any(terms):
        return _results(query)

    for term, extension in zip(terms, extensions):
        if term is not None:
            if like:
                if isinstance(term, str):
                    term = _likable(term)
            query = extension(term)
    return _results(query)
