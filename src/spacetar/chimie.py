import re
import typing as typ
import pyparsing as pyp  # type: ignore

from textwrap import dedent
from collections import defaultdict


SYMBOLS = (
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Uut",
    "Fl",
    "Uup",
    "Lv",
    "Uus",
    "Uuo",
)


MASSES = [
    (SYMBOL, MASS)
    for SYMBOL, MASS in zip(
        SYMBOLS,
        [
            1.008,
            4.002602,
            6.94,
            9.0121831,
            10.81,
            12.011,
            14.007,
            15.999,
            18.998403163,
            20.1797,
            22.98976928,
            24.305,
            26.9815385,
            28.085,
            30.973761998,
            32.06,
            35.45,
            39.948,
            39.0983,
            40.078,
            44.955908,
            47.867,
            50.9415,
            51.9961,
            54.938044,
            55.845,
            58.933194,
            58.6934,
            63.546,
            65.38,
            69.723,
            72.630,
            74.921595,
            78.971,
            79.904,
            83.798,
            85.4678,
            87.62,
            88.90584,
            91.224,
            92.90637,
            95.95,
            98,
            101.07,
            102.90550,
            106.42,
            107.8682,
            112.414,
            114.818,
            118.710,
            121.760,
            127.60,
            126.90447,
            131.293,
            132.90545196,
            137.327,
            138.90547,
            140.116,
            140.90766,
            144.242,
            145,
            150.36,
            151.964,
            157.25,
            158.92535,
            162.500,
            164.93033,
            167.259,
            168.93422,
            173.045,
            174.9668,
            178.49,
            180.94788,
            183.84,
            186.207,
            190.23,
            192.217,
            195.084,
            196.966569,
            200.592,
            204.38,
            207.2,
            208.98040,
            209,
            210,
            222,
            223,
            226,
            227,
            232.0377,
            231.03588,
            238.02891,
            237,
            244,
            243,
            247,
            247,
            251,
            252,
            257,
            258,
            259,
            266,
            267,
            268,
            269,
            270,
            269,
            278,
            281,
            282,
            285,
            286,
            289,
            289,
            293,
            294,
            294,
        ],
    )
]

SUBS = {
    "0": "₀",
    "1": "₁",
    "2": "₂",
    "3": "₃",
    "4": "₄",
    "5": "₅",
    "6": "₆",
    "7": "₇",
    "8": "₈",
    "9": "₉",
}

SUPS = {
    "+": "⁺",
    "-": "⁻",
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
}


class ParseError(Exception):

    """"""

    pass


def _formula_parser():

    """"""

    lpar = pyp.Suppress("(")
    rpar = pyp.Suppress(")")

    integer = pyp.Word(pyp.nums)
    integer.setParseAction(lambda token: int(token[0]))

    element = pyp.Regex(
        r"""
        A[cglmrstu]|
        B[aehikr]?|
        C[adeflmorsu]?|
        D[bsy]|
        E[rsu]|
        F[emr]?|
        G[ade]|
        H[efgos]?|
        I[nr]?|
        Kr?|
        L[airu]|
        M[dgnot]|
        N[abdeiop]?|
        Os?|
        P[abdmortu]?|
        R[abefghnu]|
        S[bcegimnr]?|
        T[abcehilm]|
        Uu[bhopqst]|U|V|W|Xe|Yb?|Z[nr]
        """,
        flags=re.VERBOSE,
    )

    formula = pyp.Forward()

    term = pyp.Group(
        (element | pyp.Group(lpar + formula + rpar)("sub"))
        + pyp.Optional(
            integer,
            default=1,
        )("mult")
    )

    formula << pyp.OneOrMore(term)

    def multiply(tokens: typ.List[pyp.Token]):

        """"""

        token = tokens[0]
        if token.sub:
            mult = token.mult
            for term in token.sub:
                term[1] *= mult
            return token.sub

    term.setParseAction(multiply)

    def summation(tokens: typ.List[pyp.Token]):

        """"""

        elements = [_[0] for _ in tokens]
        dupes = len(elements) > len(set(elements))

        if dupes:
            counter: typ.MutableMapping = defaultdict(int)
            for token in tokens:
                counter[token[0]] += token[1]
            return pyp.ParseResults(
                [
                    pyp.ParseResults(
                        [
                            key,
                            val,
                        ]
                    )
                    for key, val in counter.items()
                ]
            )

    formula.setParseAction(summation)

    return formula


def _partition_formula(formula: str) -> typ.List:

    """"""

    for prefix in ["c-", "l-", "i-", "n-"]:
        if formula.find(prefix) != -1:
            formula = formula.replace(prefix, "").strip()
            prefix_str = prefix
            break
        else:
            prefix_str = ""

    for token in "+-":
        if token in formula:
            if formula.count(token) > 1:
                raise ParseError(
                    dedent(
                        f"""
                        Cannot have two {token} in the same formula.
                        Exiting...
                        """
                    )
                    .replace("\n", " ")
                    .strip()
                )
            stoich_str, charge_str = formula.split(token)
            charge_str = token + charge_str
            return [prefix_str, stoich_str, charge_str]
    else:
        return [prefix_str, formula, ""]


def composition(formula: str) -> typ.Dict:

    """"""

    composed: typ.Dict = {}

    _, stoich_str, charge_str = _partition_formula(formula)

    stoich = {
        SYMBOLS.index(index) + 1: amount
        for (
            index,
            amount,
        ) in _formula_parser().parseString(stoich_str)
    }

    for element, amount in stoich.items():
        if element not in composed:
            composed[element] = amount
        else:
            composed[element] += amount

    if charge_str != "":
        matches = re.search(r"([+-])((?:\d+)?)", charge_str)
        if matches:
            sign, charge = matches.groups()
            composed[0] = int(
                "".join(
                    [
                        sign,
                        (charge if charge != "" else "1"),
                    ]
                )
            )
        else:
            composed[0] = 0
    return composed


def molecular_mass(composed: typ.Dict) -> float:

    """"""

    mass = 0.0
    for key, value in composed.items():
        if key == 0:
            mass -= value * 5.489e-4
        else:
            mass += value * MASSES[key - 1][-1]
    return mass


def formula_to_unicode(formula: str) -> str:

    """"""

    prefix_str, stoich_str, charge_str = _partition_formula(formula)
    for key, val in SUBS.items():
        stoich_str = stoich_str.replace(key, val)
    for key, val in SUPS.items():
        charge_str = charge_str.replace(key, val)
    return "".join([prefix_str, stoich_str, charge_str])
