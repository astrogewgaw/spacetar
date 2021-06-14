import json
import pathlib
import sqlalchemy as sql  # type: ignore
import sqlalchemy.orm as orm  # type: ignore
import importlib_metadata as imp  # type: ignore

try:
    __version__ = imp.version("spacetar")
except imp.PackageNotFoundError:
    pass

_data = pathlib.Path(__file__).parent.resolve().joinpath("data")
_database = _data / "spacetar.db"
_bands = ["submm", "mm", "cm", "IR", "Vis", "UV"]
_raw = lambda name: json.loads((_data / f"{name}.json").read_text())

Base = orm.declarative_base()
Engine = sql.create_engine(f"sqlite:///{_database}", future=True)


class Molecule(Base):  # type: ignore

    """
    Represents a single space molecule in **spacetar**. This class is a *mapped
    class*; every row in the `molecules` table in the SQLite database directly
    maps to this class. It is used to search the `molecules` table and pretty
    print the results, thanks to `rich`'s Console Protocol. The methods in this
    class supply additional information on a single molecule, such as the number
    of atoms, its molecular mass, or its degree of unsaturation.

    Args:
        id:             The ID of the molecule in the `molecules` table.
        label:          The label used for the molecule in the table. This is used
                        because steroeisomers can have the same name and/or molecular
                        formula, so they cannot be used as unique labels. As of 2021,
                        this is only true for **1** molecule.
        name:           The name of the molecule.
        formula:        The molecular formula of the molecule.
        year:           The year the molecule was discovered.
        sources:        The source(s) it was discovered in.
        telescopes:     The telescope(s) it was discovered by.
        wavelengths:    The wavelength(s) in the electromagnetic spectrum it was
                        discovered in.
        neutral:        Flag indicating if the molecule is neutral.
        cation:         Flag indicating if the molecule is cation.
        anion:          Flag indicating if the molecule is anion.
        radical:        Flag indicating if the molecule is radical.
        cyclic:         Flag indicating if the molecule is cyclic.
        fullerene:      Flag indicating if the molecule is fullerene.
        polyaromatic:   Flag indicating if the molecule is polyaromatic.
        mass:           The molecular mass of the molecule, in a.m.u.
        A, B, C:        Rotational constants for the molecule.
        mua:            Dipole moment of the molecule along the axis of least moment of inertia.
        mub:            Dipole moment of the molecule along the axis of intermediate moment of inertia.
        muc:            Dipole moment of the molecule along the axis of greatest moment of inertia.
        kappa:          Ray's asymmetry parameter for the molecule. This can be calculated from
                        a molecule's rotational constants using: :math:`\\kappa = \\frac{2B - A - C}{A - C}`.
        ice:            Flag indicating if the molecule has been discovered in interstellar ices.
        ppd:            Flag indicating if the molecule has been discovered in protoplanetary disks.
        exgal:          Flag indicating if the molecule has been discovered in extragalactic sources.
        exo:            Flag indicating if the molecule has been discovered in exoplanets.
        isos:           Isomers that have been detected in the ISM for this molecule, if any.
        ppd_isos:       Isomers that have been detected in protoplanetary disks for this molecule, if any.
        ism_ref:        References for the molecule's detection in the ISM.
        lab_ref:        References for lab work that backs up this molecule's ISM detection.
        ice_ref:        References for the molecule's detection in interstellar ices.
        ice_lab_ref:    References for lab work that backs up this molecule's detection in interstellar ices.
        ppd_ref:        References for the molecule's detection in protoplanetary disks.
        ppd_lab_ref:    References for lab work that backs up this molecule's detection in protoplanetary disks.
        ppd_isos_ref:   References for the detection of the isomers of this molecule in protoplanetary disks.
        exgal_ref:      References for the molecule's detection in extragalactic sources.
        exgal_lab_ref:  References for lab work that backs up this molecule's detection in extragalactic sources.
        exgal_sources:  Extragalactic sources that this molecule has been detected in.
        exo_ref:        References for the molecule's detection in exoplanets.
        exo_lab_ref:    References for lab work that backs up this molecule's detection in exoplanets.
        isos_ref:       References for the detection of this molecule's isomers in space.
        isos_lab_ref:   References for lab work that backs up the detection of this molecule's isomers.
        notes:          Notes about this molecule, if any.
    """

    __tablename__: str = "molecules"

    id = sql.Column(sql.Integer, primary_key=True)
    label = sql.Column(sql.String(50), unique=True)
    name = sql.Column(sql.String(50))
    formula = sql.Column(sql.String(50))
    year = sql.Column(sql.Integer)

    sources = orm.relationship(
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

    telescopes = orm.relationship(
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

    wavelengths = orm.relationship(
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

    neutral = sql.Column(sql.Boolean)
    cation = sql.Column(sql.Boolean)
    anion = sql.Column(sql.Boolean)
    radical = sql.Column(sql.Boolean)
    cyclic = sql.Column(sql.Boolean)
    fullerene = sql.Column(sql.Boolean)
    polyaromatic = sql.Column(sql.Boolean)

    mass = sql.Column(sql.Float)

    A = sql.Column(sql.Float)
    B = sql.Column(sql.Float)
    C = sql.Column(sql.Float)

    mua = sql.Column(sql.Float)
    mub = sql.Column(sql.Float)
    muc = sql.Column(sql.Float)

    kappa = sql.Column(sql.Float)

    ice = sql.Column(sql.Boolean)
    ppd = sql.Column(sql.Boolean)
    exgal = sql.Column(sql.Boolean)
    exo = sql.Column(sql.Boolean)

    isos = sql.Column(sql.String(50))
    ppd_isos = sql.Column(sql.String(50))

    ism_ref = sql.Column(sql.String(500))
    lab_ref = sql.Column(sql.String(500))

    ice_ref = sql.Column(sql.String(500))
    ice_lab_ref = sql.Column(sql.String(500))

    ppd_ref = sql.Column(sql.String(500))
    ppd_lab_ref = sql.Column(sql.String(500))
    ppd_isos_ref = sql.Column(sql.String(500))

    exgal_ref = sql.Column(sql.String(500))
    exgal_lab_ref = sql.Column(sql.String(500))
    exgal_sources = sql.Column(sql.String(50))

    exo_ref = sql.Column(sql.String(500))
    exo_lab_ref = sql.Column(sql.String(500))

    isos_ref = sql.Column(sql.String(500))
    isos_lab_ref = sql.Column(sql.String(500))

    notes = sql.Column(sql.String(500))

    def __str__(self) -> str:
        return f"<Molecule: {self.formula} ({self.name})>"

    def __repr__(self) -> str:
        return str(self)


class Source(Base):  # type: ignore

    """
    Represents a astronomical source in **spacetar**. This class is a *mapped class*;
    every row in the `sources` table in the SQLite database directly maps to this
    class. It is used to search the `sources` table and pretty print the results, thanks
    to `rich`'s Console Protocol. The methods in this class supply useful information
    about the astronomical source in question, such as its coordinates or its URL in
    the SIMBAD database.

    Args:
        id:             The ID of the source in the table.
        name:           The name of the source.
        kind:           The kind/type of astronomical object the source is, such as a dark or
                        line-of-sight (LOS) cloud, a star forming region (SFR), or a HI/HII
                        region.
        ra:             The right ascension of the source.
        dec:            The declination of the source.
        detects:        The number of molecules detected in this source.
        molecules:      The molecules detected in this source.
        simbad_url:     The URL for this source in the SIMBAD database, if it exists.
    """

    __tablename__: str = "sources"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(50), unique=True)
    kind = sql.Column(sql.String(50))
    ra = sql.Column(sql.String(50))
    dec = sql.Column(sql.String(50))
    detects = sql.Column(sql.Integer)
    simbad_url = sql.Column(sql.String(500))

    def __str__(self) -> str:
        return f"<Source: {self.name}>"

    def __repr__(self) -> str:
        return str(self)


class Telescope(Base):  # type: ignore

    """
    Represents a telescope in **spacetar**. This class is a *mapped class*;
    each row in the `telescopes` table in the SQLite database maps to an
    instance of this class. It is used to search the `telescope` table and
    pretty print the results, thanks to `rich`'s Console Protocol.

    Args:
        id:                 The ID of the telescope in the table.
        name:               The full name of the telescope.
        nick:               The short name (a.k.a. nick) of the telescope.
        wavelengths:        The wavelength(s) in the electromagnetic spectrum
                            this telescope operates in.
        latitude:           The latitude of the telescope.
        longitude:          The longitude of the telescope.
        diameter:           The diameter of this telescope, if applicable.
        built:              The year this telescope was built.
        decommissioned:     The year this telescope was decommissioned, if applicable.
        notes:              Notes about this telescope, if any.
        detects:            The number of molecules detected by this telescope.
    """

    __tablename__: str = "telescopes"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(50), unique=True)
    nick = sql.Column(sql.String(50), unique=True)
    kind = sql.Column(sql.String(50))
    wavelengths = orm.relationship(
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
    detects = sql.Column(sql.Integer)

    def __str__(self) -> str:
        return f"<Telescope: {self.name}>"

    def __repr__(self) -> str:
        return str(self)


class Wavelength(Base):  # type: ignore

    """
    Represents a wavelength band in the electromagentic spectrum in **spacetar**.
    This class is a *mapped class*; every row in the `wavelengths` table in the
    SQLite database maps to an instance of this class. There are six wavelength
    _bands in **spacetar**: submm, mm, cm, IR, Vis, and UV. This table shares a
    many-to-many orm.relationship with two tables: `molecules` (as the wavelength(s)
    the molecule was discovered in) and `telescopes` (as the wavelength(s) the
    telescope operates in).

    Args:
        id:     The ID of the wavelength band in the table.
        name:   The name of the wavelength band.
    """

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

    """
    Create the SQLite database from the JSON data. This function is meant
    for internal usage only, and should be used only when the author of
    this library (that's me) or the user (that's you) modifies the JSON
    data and needs to update the SQLite database. If you end up updating
    the JSON data and/or the SQLite database, you can definitely make a
    pull request to this repository so that other users can also access
    your changes. All PRs that update the database in some constructive
    way are welcome.

    Note:
        The database is recreated every time this function is run. We don't
        insert rows into the SQLite database, because the modifications to
        the JSON data could be breaking changes (such as changing the name
        or type of an attribute).
    """

    from rich.progress import track

    _database.unlink(missing_ok=True)

    Base.metadata.create_all(Engine)

    with orm.Session(Engine) as session:

        for _ in track(
            _bands,
            description="Creating the `wavelengths` table...",
        ):
            wavelength = Wavelength(name=_)
            session.add(wavelength)
            session.commit()

        for _ in track(
            _raw("sources").values(),
            description="Creating the `sources` table...",
        ):

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

        for _ in track(
            _raw("telescopes").values(),
            description="Creating the `telescopes` table...",
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

        for _ in track(
            _raw("molecules").values(),
            description="Creating the `molecules` table...",
        ):
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
