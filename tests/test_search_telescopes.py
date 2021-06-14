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

    assert tel.name == "IRAM 30-m"
    assert tel.nick == "IRAM"
    assert tel.kind == "Single Dish"
    assert [_.name for _ in tel.wavelengths] == ["mm", "submm"]
    assert tel.latitude == 37.066161
    assert tel.longitude == -3.392719
    assert tel.diameter == 30.0
    assert tel.built == 1984
    assert tel.decommissioned is None
    assert tel.detects == 60


def test_wavelength():

    """"""

    results = search_telescope(wavelength="UV")

    assert len(results) == 5

    tel = results[0]

    assert tel.name == "Mount Wilson 100-in"
    assert tel.nick == "Mt. Wilson"
    assert tel.kind == "Optical"
    assert [_.name for _ in tel.wavelengths] == ["UV", "Vis"]
    assert tel.latitude is None
    assert tel.longitude is None
    assert tel.diameter == 2.54
    assert tel.built == 1917
    assert tel.decommissioned == 1989
    assert tel.detects == 3


def test_diameter():

    """"""

    results = search_telescope(diameter=[100.0])

    assert len(results) == 2

    tel = results[0]

    assert tel.name == "Green Bank Telescope"
    assert tel.nick == "GBT"
    assert tel.kind == "Single Dish"
    assert [_.name for _ in tel.wavelengths] == ["cm", "mm"]
    assert tel.latitude == 38.433056
    assert tel.longitude == -79.839722
    assert tel.diameter == 100.0
    assert tel.built == 2004
    assert tel.decommissioned is None
    assert tel.detects == 24

    results = search_telescope(diameter=[10.0, 40.0])

    assert len(results) == 11

    tel = results[0]

    assert tel.name == "IRAM 30-m"
    assert tel.nick == "IRAM"
    assert tel.kind == "Single Dish"
    assert [_.name for _ in tel.wavelengths] == ["mm", "submm"]
    assert tel.latitude == 37.066161
    assert tel.longitude == -3.392719
    assert tel.diameter == 30.0
    assert tel.built == 1984
    assert tel.decommissioned is None
    assert tel.detects == 60


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

    tel = results[0]

    assert tel.name == "Green Bank Telescope"
    assert tel.nick == "GBT"
    assert tel.kind == "Single Dish"
    assert [_.name for _ in tel.wavelengths] == ["cm", "mm"]
    assert tel.latitude == 38.433056
    assert tel.longitude == -79.839722
    assert tel.diameter == 100.0
    assert tel.built == 2004
    assert tel.decommissioned is None
    assert tel.detects == 24


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

    tel = results[0]

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

    tel = results[0]

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

    results = search_telescope(detects=[6, 10])

    assert len(results) == 4

    tel = results[0]

    assert tel.name == "AT&T Bell Laboratories 7-m Telescope"
    assert tel.nick == "Bell 7-m"
    assert tel.kind == "Single Dish"
    assert tel.wavelengths[0].name == "cm"
    assert tel.latitude is None
    assert tel.longitude is None
    assert tel.diameter == 7.0
    assert tel.built == 1976
    assert tel.decommissioned == 1992
    assert tel.detects == 8
