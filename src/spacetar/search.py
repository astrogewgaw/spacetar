from math import inf
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from sqlalchemy import or_, and_, select
from sqlalchemy.sql.selectable import Select

from .core import (
    Engine,
    Source,
    Molecule,
    Telescope,
    Wavelength,
)


lk = lambda x, on: (x if not on else f"%{x}%") if x is not None else "%%"

rn = lambda x: (
    {
        0: [-inf, inf],
        1: x * 2,
        2: x,
    }[len(x)]
    if x is not None
    else [-inf, inf]
)


class Results(list):

    """"""

    def __str__(self) -> str:
        return f"<Results | Number of results: {self.count})>"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def from_query(cls, query: Select):
        with Session(Engine) as session:
            return cls([_[0] for _ in session.execute(query).all()])

    @property
    def count(self):
        return len(self)

    def search(
        self,
        column: str,
        term: Any,
    ):

        """"""

        return Results(filter(lambda _: getattr(_, column) == term, self))

    def most(self, column: str):

        """"""

        return Results(
            filter(
                lambda _: getattr(_, column)
                == getattr(
                    max(
                        self,
                        key=lambda _: getattr(_, column),
                    ),
                    column,
                ),
                self,
            )
        )

    def least(self, column: str):

        """"""

        return Results(
            filter(
                lambda _: getattr(_, column)
                == getattr(
                    min(
                        self,
                        key=lambda _: getattr(_, column),
                    ),
                    column,
                ),
                self,
            )
        )

    def between(
        self,
        column: str,
        between: List,
    ):

        """"""

        return Results(
            [
                result
                for result in self
                if (getattr(result, column) >= between[0])
                and (getattr(result, column) <= between[1])
            ]
        )

    def orderby(
        self,
        column: str,
        reverse: bool = False,
    ):

        """"""

        return Results(
            sorted(
                self,
                key=lambda _: getattr(_, column),
                reverse=reverse,
            )
        )


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
    pah: Optional[bool] = None,
    ice: Optional[bool] = None,
    ppd: Optional[bool] = None,
    exgal: Optional[bool] = None,
    exo: Optional[bool] = None,
) -> List:

    """"""

    results = Results.from_query(
        (
            (
                select(Molecule)
                .where(Molecule.name.like(lk(name, like)))
                .where(Molecule.formula.like(lk(formula, like)))
                .where(
                    and_(
                        Molecule.year >= rn(year)[0],
                        Molecule.year <= rn(year)[1],
                    )
                )
                .where(Molecule.sources.any(Source.name.like(lk(source, like))))
                .where(
                    Molecule.telescopes.any(
                        or_(
                            Telescope.name.like(lk(telescope, like)),
                            Telescope.nick.like(lk(telescope, like)),
                        )
                    )
                )
                .where(
                    Molecule.wavelengths.any(Wavelength.name.like(lk(wavelength, like)))
                )
                .where(
                    and_(
                        *[
                            getattr(Molecule, _) == __
                            for _, __ in [
                                ("cyclic", cyclic),
                                ("fullerene", fullerene),
                                ("pah", pah),
                                ("ice", ice),
                                ("ppd", ppd),
                                ("exgal", exgal),
                                ("exo", exo),
                            ]
                            if __ is not None
                        ]
                    )
                )
            )
        )
    )

    for _, __ in [
        ("neutral", neutral),
        ("cation", cation),
        ("anion", anion),
        ("radical", radical),
    ]:
        if __ is not None:
            results = results.search(column=_, term=__)

    return results.orderby("year")


def search_source(
    like: bool = False,
    name: Optional[str] = None,
    kind: Optional[str] = None,
    detects: Optional[List[int]] = None,
) -> List:

    """"""

    return (
        Results.from_query(
            select(Source)
            .where(Source.name.like(lk(name, like)))
            .where(Source.kind.like(lk(kind, like)))
        )
        .between("detects", between=rn(detects))
        .orderby("detects", reverse=True)
    )


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

    """"""

    query = (
        select(Telescope)
        .where(
            or_(
                Telescope.name.like(lk(name, like)),
                Telescope.nick.like(lk(name, like)),
            )
        )
        .where(Telescope.kind.like(lk(kind, like)))
        .where(Telescope.wavelengths.any(Wavelength.name.like(lk(wavelength, like))))
    )

    for name, term in [
        ("diameter", diameter),
        ("built", built),
        ("decommissioned", decommissioned),
    ]:
        if (term is not None) and (len(term) != 0):
            query = query.where(
                and_(
                    getattr(Telescope, name) >= rn(term)[0],
                    getattr(Telescope, name) <= rn(term)[1],
                    getattr(Telescope, name).is_not(None),
                )
            )

    return (
        Results.from_query(query)
        .between("detects", between=rn(detects))
        .orderby("detects", reverse=True)
    )
