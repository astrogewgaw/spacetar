from spacetar import search_source


def test_name():

    """"""

    results = search_source(name="Sgr B2")

    assert len(results) == 1

    src = results[0]

    assert src.name == "Sgr B2"
    assert src.kind == "SFR"
    assert src.ra == "17:47:20.4"
    assert src.dec == "-28:23:07"
    assert src.detects == 68


def test_kind():

    """"""

    results = search_source(kind="Dark Cloud")

    assert len(results) == 8

    src = results[0]

    assert src.name == "TMC-1"
    assert src.kind == "Dark Cloud"
    assert src.ra == "04:41:45.9"
    assert src.dec == "+25:41:27"
    assert src.detects == 41


def test_detects():

    """"""

    results = search_source(detects=[1])

    assert len(results) == 32

    src = results[0]

    assert src.name == "AFGL 890 LOS"
    assert src.kind == "LOS Cloud"
    assert src.ra == "06:10:48.0"
    assert src.dec == "-06:12:00"
    assert src.detects == 1

    results = search_source(detects=[4, 6])

    assert len(results) == 6

    src = results[0]

    assert src.name == "rho Oph A"
    assert src.kind == "SFR"
    assert src.ra == "16:25:35.14"
    assert src.dec == "-23:26:49.9"
    assert src.detects == 6
