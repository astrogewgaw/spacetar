# spacetar

![License][license]
[![Gitmoji][gitmoji-badge]][gitmoji]
[![Code style: black][black-badge]][black]
[![Documentation Status][docs-badge]][docs]
[![Documentation Coverage Status][interrogate-badge]][interrogate]

## Space molecules in your terminal!

[**spacetar**][spacetar] is a command line interface that allows you to search the database of *known* space molecules across all sorts of parameters. The data is scraped from the well-maintained space molecule bibliography over at [**www.astrochymist.org**][astrochymist], created by David Woon. [**spacetar**][spacetar] scraps the HTML source code, gets all the data, and then stores it as an SQLite database. It then uses the brilliant ORM interface provided by [**SQLAlchemy**][SQLAlchemy] to search this database across all the parameters provided by you, the user. I also use the amazing [**rich**][rich] library to display the search results on the terminal. This project is still in its infancy, so I am sure it has its fair share of bugs :bug:. If you find one, open an [**issue**][issues]. If you have an idea, or a feature you would like to request, you can either open an [**issue**][issues], or start a [**discussion**][discussions]. Do let me know if you end up having some fun with this :grin: !

[gitmoji]: https://gitmoji.dev
[rich]: https://rich.readthedocs.io
[black]: https://github.com/psf/black
[docs]: https://spacetar.readthedocs.io
[SQLAlchemy]: https://www.sqlalchemy.org/
[interrogate-badge]: ./interrogate_badge.svg
[spacetar]: https://github.com/astrogewgaw/spacetar
[issues]: https://github.com/astrogewgaw/spacetar/issues
[interrogate]: https://interrogate.readthedocs.io/en/latest
[astrochymist]: http://astrochymist.org/astrochymist_ism.html
[license]: https://img.shields.io/badge/License-MIT-green.svg
[discussions]: https://github.com/astrogewgaw/spacetar/discussions
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[docs-badge]: https://readthedocs.org/projects/spacetar/badge/?version=latest
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square
