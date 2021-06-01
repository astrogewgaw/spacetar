# spacetar

![License][license]
[![Gitmoji][gitmoji-badge]][gitmoji]
[![Code style: black][black-badge]][black]
[![Documentation Status][docs-badge]][docs]

## Space molecules in your terminal!

If you want to find out *anything* about space molecules, you just have to type:

```bash
spacetar
```

Running the cli without any arguments will show you the entire database of known space molecules, right there in your terminal! Since there are *a lot* of known space molecules (more than 200 of them!), [**spacetar**][spacetar] uses a *pager* to display the entire table. This is a program in your operating system that is used for displaying things that are too long for the screen, like the `man` pages in most Unix systems. Since most pagers are not capable of displaying colors or hyperlinks, [**spacetar**][spacetar] resorts to plain old black and white output, though there is some good old markdown-based formatting in there (thanks to [**rich**][rich]).

If you want to have more fun, you can ask [**spacetar**][spacetar] questions! For example, which space molecules were discovered before 1990? Just type:

```bash
spacetar --before 1990
```

What if you want to know which space molecules were discovered in the Taurus Molecular Cloud - 1 (a.k.a. TMC-1)? Just ask [**spacetar**][spacetar]:

```bash
spacetar --source "TMC-1"
```

For getting the most out of spacetar, check out the [**documentation**][docs].

[gitmoji]: https://gitmoji.dev
[rich]: https://rich.readthedocs.io
[black]: https://github.com/psf/black
[docs]: https://spacetar.readthedocs.io
[spacetar]: https://github.com/astrogewgaw/spacetar
[license]: https://img.shields.io/badge/License-MIT-green.svg
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[docs-badge]: https://readthedocs.org/projects/spacetar/badge/?version=latest
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square
