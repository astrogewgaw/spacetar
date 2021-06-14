# spacetar

![Tests][tests]
[![Coverage Status][coveralls-badge]][coveralls]
[![Uses Gitmoji][gitmoji-badge]][gitmoji]
[![Uses Black][black-badge]][black]
![MIT License][license-badge]
[![Docs Status][docs-badge]][docs]
[![Docs Coverage][interrogate-badge]][interrogate]

## Space molecules :test_tube: :alembic: in your terminal :computer: !

Space is really cold :cold_face:. In fact, scientists thought it was too cold there for any molecules to form or react. So, when scientists actually detected the first molecules in space, they realised that they had to re-think everything they knew about the *interstellar medium* (the space between stars :star:). And so **astrochemistry**, the study of how space molecules form and react, was born. Since then, we have detected molecules like smelly **ammonia**, intoxicating **ethanol** :beers:, and even **ethylene glycol** (used in **anti-freeze** :snowflake:); the catalog of space molecules now has more than *200 unique species*.

[**spacetar**][repo] brings them right into your terminal :computer:.

Want to know when the *first molecule* was discovered in space :1st_place_medal: ? Or which telescope :telescope: has detected the *most number of molecules*? Or maybe you want to know where you can find the most ethanol :beers: :wine_glass: so that you know where to stock-up when we all get our warp drives :space_invader:? All you have to do is open your terminal and start typing in :keyboard: your questions :grin: :

* The *first molecule* ?

    ```bash
    spacetar molecules
    ```

    ![Molecules Table][molecules-table]

    (*This display the full table of molecules. The entries are arranged by year, so the first row is the first molecule discovered in space* :grin: *!*)

* Which telescope has discovered the *most molecules* ?

    ```bash
    spacetar telescopes
    ```

    ![Telescope Table][telescopes-table]

    (*This displays the full table of telescopes that have detected molecules in space. The entries are arranged by the number of molecules detected, so the first row is the telescope that has discovered the most number of molecules* :grin: *!*)

* Where is all the *ethanol* ?

    ```bash
    spacetar molecules --name ethanol
    ```

    ![Ethanol Summary][ethanol]

    (*This display a pretty summary for ethanol. You can read out all the destinations you are going to hit in the **Detected in** entry. As you can see, **Sgr B2** is the place to be. This cloud has so much ethanol in it that we could use it to supply us with beers for millions of years* :beers: *!*)

    You can also get to know more about **Sgr B2** by typing:

    ```bash
    spacetar sources --name "Sgr B2"
    ```

    ![Sgr B2 Summary][Sgr-B2]

Excited :grin:? Check out the [**docs**][docs] for more info on how to install and use spacetar, both from within Python and from the command line. If you find this project fun, star :star: the [**repo**][repo] on GitHub! You can also rave about spacetar, or bring up your ideas :bulb: / feature requests, in the [**discussions**][discuss] or via [**email**][me-email]. You can also make an [**issue**][issues] if you run into a bug :bug:.

[**spacetar**][repo], like everything else, stands on the *shoulders of giants*. It uses data compiled by [*Prof. Brett McGuire*][brett-github] for his paper, the [*2018 Census of Interstellar, Circumstellar, Extragalactic, Protoplanetary Disk, and Exoplanetary Molecules*][census-paper]. You can find the database, along with some of the code that inspired [**spacetar**][repo] in the first place, in the associated [*GitHub repository*][census-repo]. Thank you Brett for the wonderful work :smile: ! If you end up using the database in [**spacetar**][repo] for something that might lead to a scientific publication, don't forget to cite the associated paper above.

[gitmoji]: https://gitmoji.dev
[me-email]: ujjwalpanda97@gmail.com
[black]: https://github.com/psf/black
[docs]: https://spacetar.readthedocs.io
[me-github]: https://github.com/astrogewgaw
[brett-github]: https://github.com/bmcguir2
[me-twitter]: https://twitter.com/astrogewgaw
[repo]: https://github.com/astrogewgaw/spacetar
[census-paper]: https://doi.org/10.3847/1538-4365/aae5d2
[issues]: https://github.com/astrogewgaw/spacetar/issues
[interrogate]: https://interrogate.readthedocs.io/en/latest
[discuss]: https://github.com/astrogewgaw/spacetar/discussions
[census-repo]: https://github.com/bmcguir2/astromolecule_census
[license-badge]: https://img.shields.io/badge/License-MIT-green.svg
[coveralls]: https://coveralls.io/github/astrogewgaw/spacetar?branch=main
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[docs-badge]: https://readthedocs.org/projects/spacetar/badge/?version=latest
[tests]: https://github.com/astrogewgaw/spacetar/actions/workflows/tests.yaml/badge.svg
[Sgr-B2]: https://raw.githubusercontent.com/astrogewgaw/spacetar/main/images/Sgr_B2.png
[ethanol]: https://raw.githubusercontent.com/astrogewgaw/spacetar/main/images/ethanol.png
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square
[coveralls-badge]: https://coveralls.io/repos/github/astrogewgaw/spacetar/badge.svg?branch=main
[molecules-table]: https://raw.githubusercontent.com/astrogewgaw/spacetar/main/images/molecules_table.png
[telescopes-table]: https://raw.githubusercontent.com/astrogewgaw/spacetar/main/images/telescopes_table.png
[interrogate-badge]: https://raw.githubusercontent.com/astrogewgaw/spacetar/main/images/interrogate_badge.svg
