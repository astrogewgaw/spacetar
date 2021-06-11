# spacetar

![License][license]
[![Gitmoji][gitmoji-badge]][gitmoji]
[![Code style: black][black-badge]][black]
[![Documentation Status][docs-badge]][docs]
[![Documentation coverage][interrogate-badge]][interrogate]

## Space molecules 🧪 ⚗️ in your terminal 💻 !

To date, we have discovered *more than 200* molecules in the space. [**spacetar**][repo] brings them right into your terminal 💻. Do you want to know when the *first* space molecule was detected 🥇 ? Or which telescope 🔭 has detected the most molecules in space? Maybe you want to track down all the places in space where *ethanol* 🍻 has been detected, for when we all get ourselves a warp drive 👾. 

[**spacetar**][repo] can answer any and all questions about space molecules; all you have to do is start typing ⌨️ !

Want to know more? Check out the [**documentation**][docs] for help on how to use **spacetar**, both from within Python and from the command line.

**spacetar** works because it stands on the *shoulders of giants*: it uses data compiled for the [***2018 Census of Interstellar, Circumstellar, Extragalactic, Protoplanetary Disk, and Exoplanetary Molecules***][census-paper], which can be found [**here**][census]. Thanks to [**@bmcguir2**][brett] for the excellent work in compiling the database and making it available to all 😁. Many features in [**spacetar**][repo] are directly inspired from [**@bmcguir2**][brett]'s code. If you end up using spacetar for any serious work, particularly something that leads to a scientific publication, don't forget to cite his paper!

*Notes:*

* I have not attempted to make **spacetar** compatible for all kinds of systems. It is only compatible with Python versions greater than 3.6, for instance. While this is by design, **spacetar** hopes to atleast be compatible across Linux, Mac, and Windows. If you encounter any issues with installing or working with spacetar on your particular operating system, you are free to open an [**issue**][issues]. The same goes if you find a *bug* 🐛 !

* **spacetar** assumes some things about your terminal, such as Unicode compatibility. If you run into any trouble (for example, your terminal is full of ANSI escape sequences instead of nicely formatted tables), let me know by opening an [**issue**][issues].

[gitmoji]: https://gitmoji.dev
[rich]: https://rich.readthedocs.io
[brett]: https://github.com/bmcguir2
[black]: https://github.com/psf/black
[docs]: https://spacetar.readthedocs.io
[SQLAlchemy]: https://www.sqlalchemy.org/
[repo]: https://github.com/astrogewgaw/spacetar/
[issues]: https://github.com/astrogewgaw/spacetar/issues
[census-paper]: https://doi.org/10.3847/1538-4365/aae5d2
[census]: https://github.com/bmcguir2/astromolecule_census/
[interrogate]: https://interrogate.readthedocs.io/en/latest/
[discussions]: https://github.com/astrogewgaw/spacetar/discussions

[license]: https://img.shields.io/badge/License-MIT-green.svg
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[docs-badge]: https://readthedocs.org/projects/spacetar/badge/?version=latest
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square
[interrogate-badge]: https://raw.githubusercontent.com/astrogewgaw/spacetar/main/images/interrogate_badge.svg
