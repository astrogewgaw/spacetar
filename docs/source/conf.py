import os
import sys

sys.path.insert(0, os.path.abspath("../../src/spacetar"))

project = "spacetar"
copyright = "2021, Ujjwal Panda"
author = "Ujjwal Panda"

extensions = extensions = [
    "nbsphinx",
    "myst_parser",
    "sphinx_sitemap",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosectionlabel",
]

myst_enable_extensions = ["amsmath"]

html_theme = "sphinx_rtd_theme"
html_baseurl = "https://spacetar.readthedocs.io"
