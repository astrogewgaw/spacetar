from spacetar import search_telescope


def test_name():

    """"""

    results = search_telescope(name="NRAO/ARO 12-m")

    assert len(results) == 1

    tel = results[0]

    assert tel.name == "NRAO/ARO 12-m Telescope"
    assert tel.kind == "Single Dish"
    assert tel.wavelengths[0].name == "mm"
    assert tel.latitude == 31.9533
    assert tel.longitude == -111.615
    assert tel.diameter == 12.0
    assert tel.built == 1984
    assert tel.decommissioned is None
    assert tel.detects == 27


def test_kind():

    """"""

    results = search_telescope(kind="Single Dish")

    assert len(results) == 24

    tel = results[0]

    assert tel.name == "Maryland Point Observatory Naval Research Lab 85-foot Telescope"
    assert tel.nick == "NRL 85-ft"
    assert tel.kind == "Single Dish"
    assert tel.wavelengths[0].name == "cm"
    assert tel.latitude == 38.3741667
    assert tel.longitude == -77.230833
    assert tel.diameter == 26.0
    assert tel.built == 1965
    assert tel.decommissioned == 1994
    assert tel.detects == 1


def test_wavelength():

    """"""

    results = search_telescope(wavelength="UV")

    assert len(results) == 5

    tel = results[0]

    assert tel.name == "Hubble Space Telescope"
    assert tel.nick == "Hubble"
    assert tel.kind == "Space"
    assert [_.name for _ in tel.wavelengths] == ["IR", "Vis", "UV"]
    assert tel.latitude is None
    assert tel.longitude is None
    assert tel.diameter == 2.4
    assert tel.built == 1990
    assert tel.decommissioned is None
    assert tel.detects == 1


def test_diameter():

    """"""

    results = search_telescope(diameter=[100.0])

    assert len(results) == 2

    tel = results[0]

    assert tel.name == "Effelsberg 100-m Telescope"
    assert tel.nick == "Effelsberg"
    assert tel.kind == "Single Dish"
    assert tel.wavelengths[0].name == "cm"
    assert tel.latitude == 50.5247
    assert tel.longitude == -6.8828
    assert tel.diameter == 100.0
    assert tel.built == 1972
    assert tel.decommissioned is None
    assert tel.detects == 4


def test_built():

    """"""

    results = search_telescope(built=[1990])

    assert len(results) == 1

    tel = results[0]

    assert tel.name == "Hubble Space Telescope"
    assert tel.nick == "Hubble"
    assert tel.kind == "Space"
    assert [_.name for _ in tel.wavelengths] == ["IR", "Vis", "UV"]
    assert tel.latitude is None
    assert tel.longitude is None
    assert tel.diameter == 2.4
    assert tel.built == 1990
    assert tel.decommissioned is None
    assert tel.detects == 1

    results = search_telescope(built=[1990, 2014])

    assert len(results) == 13

    tel = results[4]

    assert tel.name == "Stratospheric Observatory for Infrared Astronomy"
    assert tel.nick == "SOFIA"
    assert tel.kind == "Airborne"
    assert [_.name for _ in tel.wavelengths] == ["submm", "IR"]
    assert tel.latitude is None
    assert tel.longitude is None
    assert tel.diameter == 2.5
    assert tel.built == 2010
    assert tel.decommissioned is None
    assert tel.detects == 2


def test_decommissioned():

    """"""

    results = search_telescope(decommissioned=[1970])

    assert len(results) == 1

    tel = results[0]

    assert tel.name == "Aerobee-150 Rocket"
    assert tel.nick == "Aerobee-150 Rocket"
    assert tel.kind == "Airborne"
    assert tel.wavelengths[0].name == "UV"
    assert tel.latitude is None
    assert tel.longitude is None
    assert tel.diameter is None
    assert tel.built == 1970
    assert tel.decommissioned == 1970
    assert tel.detects == 1

    results = search_telescope(decommissioned=[1970, 1990])

    assert len(results) == 8

    tel = results[-1]

    assert tel.name == "NRAO 36-ft Telescope"
    assert tel.nick == "NRAO 36-ft"
    assert tel.kind == "Single Dish"
    assert tel.wavelengths[0].name == "mm"
    assert tel.latitude == 31.9533
    assert tel.longitude == -111.615
    assert tel.diameter == 11.0
    assert tel.built == 1967
    assert tel.decommissioned == 1984
    assert tel.detects == 33


def test_detects():

    """"""

    results = search_telescope(detects=[6])

    assert len(results) == 1

    tel = results[-1]

    assert tel.name == "Atacama Large Millimeter/sub-millimeter Array"
    assert tel.nick == "ALMA"
    assert tel.kind == "Interferometer"
    assert [_.name for _ in tel.wavelengths] == ["mm", "submm"]
    assert tel.latitude == -23.0193
    assert tel.longitude == -67.7532
    assert tel.diameter is None
    assert tel.built == 2011
    assert tel.decommissioned is None
    assert tel.detects == 6
