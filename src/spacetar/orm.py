from sqlalchemy.orm import (  # type: ignore
    Session,
    relationship,
    declarative_base,
)

from sqlalchemy import (  # type: ignore
    Table,
    Float,
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    create_engine,
)

from rich.panel import Panel

from .display import summarize
from .core import data, waves, freezer


Base = declarative_base()
Engine = create_engine(f"sqlite:///{freezer}", future=True)


class Molecule(Base):  # type: ignore

    """"""

    __tablename__: str = "molecules"

    id = Column(Integer, primary_key=True)
    label = Column(String(50), unique=True)
    name = Column(String(50))
    formula = Column(String(50))
    year = Column(Integer)

    sources = relationship(
        "Source",
        secondary=Table(
            "assoc_mol_src",
            Base.metadata,
            Column(
                "mol_id",
                Integer,
                ForeignKey("molecules.id"),
            ),
            Column(
                "src_id",
                Integer,
                ForeignKey("sources.id"),
            ),
        ),
        backref="molecules",
        lazy="selectin",
    )

    telescopes = relationship(
        "Telescope",
        secondary=Table(
            "assoc_mol_tel",
            Base.metadata,
            Column(
                "mol_id",
                Integer,
                ForeignKey("molecules.id"),
            ),
            Column(
                "tel_id",
                Integer,
                ForeignKey("telescopes.id"),
            ),
        ),
        backref="molecules",
        lazy="selectin",
    )

    wavelengths = relationship(
        "Wavelength",
        Table(
            "assoc_mol_wave",
            Base.metadata,
            Column(
                "mol_id",
                Integer,
                ForeignKey("molecules.id"),
            ),
            Column(
                "wave_id",
                Integer,
                ForeignKey("wavelengths.id"),
            ),
        ),
        backref="molecules",
        lazy="selectin",
    )

    neutral = Column(Boolean)
    cation = Column(Boolean)
    anion = Column(Boolean)
    radical = Column(Boolean)
    cyclic = Column(Boolean)
    fullerene = Column(Boolean)
    polyaromatic = Column(Boolean)

    mass = Column(Float)

    A = Column(Float)
    B = Column(Float)
    C = Column(Float)

    mua = Column(Float)
    mub = Column(Float)
    muc = Column(Float)

    kappa = Column(Float)

    ice = Column(Boolean)
    ppd = Column(Boolean)
    exgal = Column(Boolean)
    exo = Column(Boolean)

    isos = Column(String(50))
    ppd_isos = Column(String(50))

    ism_ref = Column(String(500))
    lab_ref = Column(String(500))

    ice_ref = Column(String(500))
    ice_lab_ref = Column(String(500))

    ppd_ref = Column(String(500))
    ppd_lab_ref = Column(String(500))
    ppd_isos_ref = Column(String(500))

    exgal_ref = Column(String(500))
    exgal_lab_ref = Column(String(500))
    exgal_sources = Column(String(50))

    exo_ref = Column(String(500))
    exo_lab_ref = Column(String(500))

    isos_ref = Column(String(500))
    isos_lab_ref = Column(String(500))

    notes = Column(String(500))

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return str(self)

    def __rich__(self) -> Panel:
        return summarize(self, kind="mol")


class Source(Base):  # type: ignore

    """"""

    __tablename__: str = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    kind = Column(String(50))
    ra = Column(String(50))
    dec = Column(String(50))
    detects = Column(Integer)
    simbad_url = Column(String(500))

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return str(self)

    def __rich__(self) -> str:
        return ""


class Telescope(Base):  # type: ignore

    """"""

    __tablename__: str = "telescopes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    nick = Column(String(50), unique=True)
    kind = Column(String(50))
    wavelengths = relationship(
        "Wavelength",
        Table(
            "assoc_tel_wave",
            Base.metadata,
            Column(
                "tel_id",
                Integer,
                ForeignKey("telescopes.id"),
            ),
            Column(
                "wave_id",
                Integer,
                ForeignKey("wavelengths.id"),
            ),
        ),
        backref="telescopes",
        lazy="selectin",
    )
    latitude = Column(Float)
    longitude = Column(Float)
    diameter = Column(Float)
    built = Column(Integer)
    decommissioned = Column(Integer)
    notes = Column(String(500))
    detects = Column(Integer)

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return str(self)

    def __rich__(self) -> str:
        return ""


class Wavelength(Base):  # type: ignore

    """"""

    __tablename__: str = "wavelengths"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return str(self)

    def __rich__(self) -> str:
        return ""


def mrfreeze():

    """"""

    if freezer.exists():
        freezer.unlink()

    Base.metadata.create_all(Engine)

    with Session(Engine) as session:

        for wave in waves:
            wavelength = Wavelength(name=wave)
            session.add(wavelength)
            session.commit()

        for _ in data("sources").values():

            source = Source(
                name=_["name"],
                kind=_["kind"],
                ra=_["ra"],
                dec=_["dec"],
                detects=_["detects"],
                simbad_url=_["simbad_url"],
            )
            session.add(source)
            session.commit()

        for _ in data("telescopes").values():
            telescope = Telescope(
                name=_["name"],
                nick=_["nick"],
                kind=_["kind"],
                latitude=_["latitude"],
                longitude=_["longitude"],
                diameter=_["diameter"],
                built=_["built"],
                decommissioned=_["decommissioned"],
                notes=_["notes"],
                detects=_["detects"],
            )

            for name in _["wavelengths"]:
                wavelength = (
                    session.query(Wavelength)
                    .filter_by(
                        name=name,
                    )
                    .first()
                )
                if wavelength is not None:
                    telescope.wavelengths.append(wavelength)

            session.add(telescope)
            session.commit()

        for _ in data("molecules").values():
            molecule = Molecule(
                label=_["label"],
                name=_["name"],
                formula=_["formula"],
                year=_["year"],
                neutral=_["neutral"],
                cation=_["cation"],
                anion=_["anion"],
                radical=_["radical"],
                cyclic=_["cyclic"],
                fullerene=_["fullerene"],
                polyaromatic=_["polyaromatic"],
                mass=_["mass"],
                A=_["A"],
                B=_["B"],
                C=_["C"],
                mua=_["mua"],
                mub=_["mub"],
                muc=_["muc"],
                kappa=_["kappa"],
                ice=_["ice"],
                ppd=_["ppd"],
                exgal=_["exgal"],
                exo=_["exo"],
                isos=_["isos"],
                ppd_isos=_["ppd_isos"],
                ism_ref=_["ism_ref"],
                lab_ref=_["lab_ref"],
                ice_ref=_["ice_ref"],
                ice_lab_ref=_["ice_lab_ref"],
                ppd_ref=_["ppd_ref"],
                ppd_lab_ref=_["ppd_lab_ref"],
                ppd_isos_ref=_["ppd_isos_ref"],
                exgal_ref=_["exgal_ref"],
                exgal_lab_ref=_["exgal_lab_ref"],
                exgal_sources=_["exgal_sources"],
                exo_ref=_["exo_ref"],
                exo_lab_ref=_["exo_lab_ref"],
                isos_ref=_["isos_ref"],
                isos_lab_ref=_["isos_lab_ref"],
                notes=_["notes"],
            )

            for name in _["wavelengths"]:
                wavelength = (
                    session.query(Wavelength)
                    .filter_by(
                        name=name,
                    )
                    .first()
                )
                if wavelength is not None:
                    molecule.wavelengths.append(wavelength)

            for name in _["sources"]:
                source = (
                    session.query(Source)
                    .filter_by(
                        name=name,
                    )
                    .first()
                )
                if source is not None:
                    molecule.sources.append(source)

            for name in _["telescopes"]:
                telescope = (
                    session.query(Telescope)
                    .filter_by(
                        name=name,
                    )
                    .first()
                )
                if telescope is not None:
                    molecule.telescopes.append(telescope)

            session.add(molecule)
            session.commit()
