from spacetar import search_molecule


def test_name():

    """"""

    results = search_molecule(name="acetone")

    mol = results[0]

    assert mol.name == "acetone"
    assert mol.formula == "(CH3)2CO"


def test_formula():

    """"""

    results = search_molecule(formula="CH3COOH")

    mol = results[0]

    assert mol.name == "acetic acid"
    assert mol.formula == "CH3COOH"


def test_year():

    """"""

    results = search_molecule(year=[1990])

    assert results[0].name == "carbon monophosphide"
    assert results[0].formula == "CP"

    results = search_molecule(year=[1990, 2000])

    assert len(results) == 33
    assert results[-1].name == "glycolaldehyde"
    assert results[-1].formula == "CH2OHCHO"
    assert results[-1].year == 2000


def test_source():

    """"""

    results = search_molecule(source="TMC-1")

    assert len(results) == 41
    assert results[0].name == "cyanoethynyl radical"
    assert results[0].formula == "C3N"
    assert results[0].sources[0].name == "IRC+10216"
    assert results[0].sources[1].name == "TMC-1"


def test_telescope():

    """"""

    results = search_molecule(telescope="NRAO 36-ft")

    assert len(results) == 33
    assert results[0].name == "carbon monoxide"
    assert results[0].formula == "CO"
    assert results[0].telescopes[0].name == "NRAO 36-ft Telescope"


def test_wavelength():

    """"""

    results = search_molecule(wavelength="mm")

    assert len(results) == 132
    assert results[0].name == "carbon monoxide"
    assert results[0].formula == "CO"
    assert results[0].wavelengths[0].name == "mm"


def test_neutral():

    """"""

    results = search_molecule(neutral=True)

    assert len(results) == 186
    assert results[0].name == "methylidyne"
    assert results[0].formula == "CH"
    assert results[0].neutral


def test_cation():

    """"""

    results = search_molecule(cation=True)

    assert len(results) == 28
    assert results[0].name == "methylidyne cation"
    assert results[0].formula == "CH+"
    assert results[0].cation


def test_anion():

    """"""

    results = search_molecule(anion=True)

    assert len(results) == 6
    assert results[0].name == "hexatriynyl anion"
    assert results[0].formula == "C6H-"
    assert results[0].anion


def test_radical():

    """"""

    results = search_molecule(radical=True)

    assert len(results) == 48
    assert results[0].name == "cyano radical"
    assert results[0].formula == "CN"
    assert results[0].radical


def test_cyclic():

    """"""

    results = search_molecule(cyclic=True)

    assert len(results) == 15
    assert results[0].name == "silacyclopropynylidene"
    assert results[0].formula == "SiC2"
    assert results[0].cyclic


def test_fullerene():

    """"""

    results = search_molecule(fullerene=True)

    assert len(results) == 3
    assert results[0].name == "buckminsterfullerene"
    assert results[0].formula == "C60"
    assert results[0].fullerene


def test_polyaromatic():

    """"""

    results = search_molecule(polyaromatic=True)

    assert len(results) == 2
    assert results[0].name == "1-cyanonaphthalene"
    assert results[0].formula == "C10H7CN"
    assert results[0].polyaromatic


def test_ice():

    """"""

    results = search_molecule(ice=True)

    assert len(results) == 9
    assert results[0].name == "ammonia"
    assert results[0].formula == "NH3"
    assert results[0].ice


def test_ppd():

    """"""

    results = search_molecule(ppd=True)

    assert len(results) == 24
    assert results[0].name == "cyano radical"
    assert results[0].formula == "CN"
    assert results[0].ppd


def test_exgal():

    """"""

    results = search_molecule(exgal=True)

    assert len(results) == 66
    assert results[0].name == "methylidyne"
    assert results[0].formula == "CH"
    assert results[0].exgal


def test_exo():

    """"""

    results = search_molecule(exo=True)

    assert len(results) == 6
    assert results[0].name == "water"
    assert results[0].formula == "H2O"
    assert results[0].exo


def test_like():

    """"""

    results = search_molecule(like=True, name="acid")

    assert len(results) == 9
    assert results[0].name == "formic acid"
    assert results[0].formula == "HCOOH"
