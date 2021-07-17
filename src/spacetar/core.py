import re
import json
import typing
import pathlib
import sqlalchemy as sql
import sqlalchemy.orm as orm
import importlib_metadata as imp

from .chimie import symbols, composition, molecular_mass


try:
    __version__ = imp.version("spacetar")
except imp.PackageNotFoundError:
    pass

_sep = re.compile(r"\s*[,]\s*")
_data = pathlib.Path(__file__).parent.resolve().joinpath("data")
_database = _data / "spacetar.db"
_nullnum = lambda _: (_ if _ is not None else 0.0)
_bands = ["sub-mm", "mm", "cm", "IR", "Vis", "UV"]
_raw = lambda name: json.loads((_data / f"{name}.json").read_text())
_logo = """
                               __            
   _________  ____ _________  / /_____ ______
  / ___/ __ \/ __ `/ ___/ _ \/ __/ __ `/ ___/
 (__  ) /_/ / /_/ / /__/  __/ /_/ /_/ / /    
/____/ .___/\__,_/\___/\___/\__/\__,_/_/     
    /_/                                      
"""

Base = orm.declarative_base()
Engine = sql.create_engine(f"sqlite:///{_database}", future=True)


class Molecule(Base):

    """"""

    __tablename__: str = "molecules"

    id = sql.Column(sql.Integer, primary_key=True)
    label = sql.Column(sql.String(50), unique=True, nullable=False)
    name = sql.Column(sql.String(50), nullable=False)
    formula = sql.Column(sql.String(50), nullable=False)
    year = sql.Column(sql.Integer)

    sources: typing.List["Source"] = orm.relationship(
        "Source",
        secondary=sql.Table(
            "assoc_mol_src",
            Base.metadata,
            sql.Column(
                "mol_id",
                sql.Integer,
                sql.ForeignKey("molecules.id"),
            ),
            sql.Column(
                "src_id",
                sql.Integer,
                sql.ForeignKey("sources.id"),
            ),
        ),
        backref=orm.backref("molecules", lazy="selectin"),
        lazy="selectin",
    )

    telescopes: typing.List["Telescope"] = orm.relationship(
        "Telescope",
        secondary=sql.Table(
            "assoc_mol_tel",
            Base.metadata,
            sql.Column(
                "mol_id",
                sql.Integer,
                sql.ForeignKey("molecules.id"),
            ),
            sql.Column(
                "tel_id",
                sql.Integer,
                sql.ForeignKey("telescopes.id"),
            ),
        ),
        backref=orm.backref("molecules", lazy="selectin"),
        lazy="selectin",
    )

    wavelengths: typing.List["Wavelength"] = orm.relationship(
        "Wavelength",
        sql.Table(
            "assoc_mol_wave",
            Base.metadata,
            sql.Column(
                "mol_id",
                sql.Integer,
                sql.ForeignKey("molecules.id"),
            ),
            sql.Column(
                "wave_id",
                sql.Integer,
                sql.ForeignKey("wavelengths.id"),
            ),
        ),
        backref=orm.backref("molecules", lazy="selectin"),
        lazy="selectin",
    )

    cyclic = sql.Column(sql.Boolean)
    fullerene = sql.Column(sql.Boolean)
    pah = sql.Column(sql.Boolean)

    A = sql.Column(sql.Float)
    B = sql.Column(sql.Float)
    C = sql.Column(sql.Float)

    mua = sql.Column(sql.Float)
    mub = sql.Column(sql.Float)
    muc = sql.Column(sql.Float)

    ice = sql.Column(sql.Boolean)
    ppd = sql.Column(sql.Boolean)
    exgal = sql.Column(sql.Boolean)
    exo = sql.Column(sql.Boolean)

    ism_refs = sql.Column(sql.String(500))
    lab_refs = sql.Column(sql.String(500))
    exo_refs = sql.Column(sql.String(500))
    exgal_refs = sql.Column(sql.String(500))

    isos = sql.Column(sql.String(50))
    isos_refs = sql.Column(sql.String(500))
    isos_lab_refs = sql.Column(sql.String(500))

    notes = sql.Column(sql.String(500))

    def __str__(self) -> str:
        return f"<Molecule: {self.formula} ({self.name})>"

    def __repr__(self) -> str:
        return str(self)

    @property
    def composition(self) -> typing.Dict:

        """"""

        if self.formula:
            return {
                symbols[Z - 1]: natoms
                for (
                    Z,
                    natoms,
                ) in composition(self.formula).items()
                if Z != 0
            }
        else:
            return {}

    @property
    def natoms(self):

        """"""

        return sum([natom for natom in self.composition.values()])

    @property
    def nelectrons(self):

        """"""

        return (
            sum(
                [
                    Z * natom
                    for (
                        Z,
                        natom,
                    ) in composition(self.formula).items()
                ]
            )
            - self.charge
        )

    @property
    def mass(self) -> float:

        """"""

        if self.formula:
            return molecular_mass(composition(self.formula))
        else:
            return 0.0

    @property
    def charge(self) -> int:

        """"""

        if self.formula:
            return composition(self.formula).get(0, 0)
        else:
            return 0

    @property
    def neutral(self) -> bool:

        """"""

        if self.charge == 0:
            return True
        else:
            return False

    @property
    def cation(self):

        """"""

        if not self.neutral and (self.charge > 0):
            return True
        else:
            return False

    @property
    def anion(self):

        """"""

        if not self.neutral and (self.charge < 0):
            return True
        else:
            return False

    @property
    def radical(self):

        """"""

        if (self.nelectrons % 2) == 0:
            return False
        else:
            return True

    @property
    def unsaturation(self):

        """"""

        for key in self.composition.keys():
            if key in (
                set(symbols)
                ^ {
                    "C",
                    "H",
                    "O",
                    "N",
                    "F",
                    "Cl",
                    "Br",
                    "I",
                    "At",
                    "Te",
                }
            ):
                return None
        else:
            return 1 + 0.5 * (
                self.composition.get("H", 0) * -1
                + self.composition.get("C", 0) * 2
                + self.composition.get("N", 0) * 1
                + self.composition.get("Cl", 0) * -1
                + self.composition.get("F", 0) * -1
            )

    @property
    def kappa(self) -> typing.Optional[float]:

        """"""

        if any(
            _ is not None
            for _ in [
                self.A,
                self.B,
                self.C,
            ]
        ):
            if self.A == None and self.C == None:
                return -1
            else:
                over = (2 * _nullnum(self.B)) - _nullnum(self.A) - _nullnum(self.C)
                under = _nullnum(self.A) - _nullnum(self.C)
                return over / under
        else:
            return None


class Source(Base):

    """"""

    __tablename__: str = "sources"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(50), unique=True)
    kind = sql.Column(sql.String(50))
    ra = sql.Column(sql.String(50))
    dec = sql.Column(sql.String(50))
    exgal = sql.Column(sql.Boolean)
    exo = sql.Column(sql.Boolean)
    simbad_url = sql.Column(sql.String(500))

    def __str__(self) -> str:
        return f"<Source: {self.name}>"

    def __repr__(self) -> str:
        return str(self)

    @property
    def detects(self):

        """"""

        return len(self.molecules)


class Telescope(Base):

    """"""

    __tablename__: str = "telescopes"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(50), unique=True)
    nick = sql.Column(sql.String(50), unique=True)
    kind = sql.Column(sql.String(50))
    wavelengths: typing.List["Wavelength"] = orm.relationship(
        "Wavelength",
        sql.Table(
            "assoc_tel_wave",
            Base.metadata,
            sql.Column(
                "tel_id",
                sql.Integer,
                sql.ForeignKey("telescopes.id"),
            ),
            sql.Column(
                "wave_id",
                sql.Integer,
                sql.ForeignKey("wavelengths.id"),
            ),
        ),
        backref="telescopes",
        lazy="selectin",
    )
    latitude = sql.Column(sql.Float)
    longitude = sql.Column(sql.Float)
    diameter = sql.Column(sql.Float)
    built = sql.Column(sql.Integer)
    decommissioned = sql.Column(sql.Integer)
    notes = sql.Column(sql.String(500))

    def __str__(self) -> str:
        return f"<Telescope: {self.name}>"

    def __repr__(self) -> str:
        return str(self)

    @property
    def detects(self):

        """"""

        return len(self.molecules)


class Wavelength(Base):

    """"""

    __tablename__: str = "wavelengths"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(50), unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return str(self)

    def __rich__(self) -> str:
        return f"{self.name}"


def _create_database():

    """"""

    from rich.progress import track

    _database.unlink(missing_ok=True)

    Base.metadata.create_all(Engine)

    with orm.Session(Engine) as session:

        for _ in track(
            _bands,
            description="[i][u]Storing wavelength bands: ",
        ):
            wavelength = Wavelength(name=_)
            session.add(wavelength)
            session.commit()

        for _ in track(
            _raw("galactic").values(),
            description="[i][u]Storing galactic sources: ",
        ):

            source = Source(
                name=_["name"],
                kind=_["kind"],
                ra=_["ra"],
                dec=_["dec"],
                exgal=False,
                exo=False,
                simbad_url=_["simbad_url"],
            )
            session.add(source)
            session.commit()

        for _ in track(
            _raw("extragalactic").values(),
            description="[i][u]Storing extragalactic sources: ",
        ):

            source = Source(
                name=_["name"],
                kind=_["kind"],
                ra=_["ra"],
                dec=_["dec"],
                exgal=True,
                exo=False,
                simbad_url=_["simbad_url"],
            )
            session.add(source)
            session.commit()

        for _ in track(
            _raw("exoplanets").values(),
            description="[i][u]Storing exoplanetary sources: ",
        ):

            source = Source(
                name=_["name"],
                kind=_["kind"],
                ra=_["ra"],
                dec=_["dec"],
                exgal=False,
                exo=True,
                simbad_url=_["simbad_url"],
            )
            session.add(source)
            session.commit()

        for _ in track(
            _raw("telescopes").values(),
            description="[i][u]Storing telescopes: ",
        ):
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

        for _ in track(
            _raw("molecules").values(),
            description="[i][u]Storing molecules: ",
        ):
            molecule = Molecule(
                name=_["name"],
                formula=_["formula"],
                label=_["label"],
                year=_["year"],
                cyclic=_["cyclic"],
                fullerene=_["fullerene"],
                pah=_["pah"],
                mua=_["mua"],
                mub=_["mub"],
                muc=_["muc"],
                isos=_["isos"],
                isos_refs=_["isos_refs"],
                isos_lab_refs=_["isos_lab_refs"],
                ice=_["ice"],
                ppd=_["ppd"],
                exgal=_["exgal"],
                exgal_refs=_["exgal_refs"],
                exo=_["exo"],
                exo_refs=_["exo_refs"],
                notes=_["notes"],
                A=_["A"],
                B=_["B"],
                C=_["C"],
                ism_refs=_["ism_refs"],
                lab_refs=_["lab_refs"],
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

            for name in re.split(
                _sep,
                str(_["exgal_sources"]),
            ):
                source = (
                    session.query(Source)
                    .filter_by(
                        name=name,
                    )
                    .first()
                )
                if source is not None:
                    molecule.sources.append(source)

            for name in re.split(
                _sep,
                str(_["exo_sources"]),
            ):
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
