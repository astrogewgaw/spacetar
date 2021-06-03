# Usage

To start exploring the database of *known* space molecules as is, just type:

```bash
spacetar
```

[**spacetar**][spacetar] has a lot of options to search the database of (*known*) space molecules. Here is a summary:

[spacetar]: https://github.com/astrogewgaw/spacetar

* `--formula`: Search by chemical formula. For example:

    ```bash
    spacetar --formula "CH+"
    ```

* `--year`: Search by year of discovery. This will search for molecules discovered in this *exact* year (for range based options, read on). For example:

    ```bash
    spacetar --year 2000
    ```

* `--before`: Search for all space molecules discovered **before** this year. This option (like all the other range based options) is *exclusive*; that is, it will **not** show you molecules discovered in the specified year itself. For example:

    ```bash
    spacetar --before 1990
    ```

* `--after`: Search for all space molecules discovered **after** this year. For example:

    ```bash
    spacetar --after 2019
    ```

* `--between`: Search for all space molecules discovered between two years. Note that the range is exclusive on *both* sides, and that you have to specify the past year first, and the future year after. That is:

    ```bash
    spacetar --between 1990 2000
    ```

    will work, but:

    ```bash
    spacetar --between 2000 1990
    ```

    won't.

* `--source`: Search for space molecules discovered in a particular source. This works, but sadly some of the sources in the database have names with Greek characters, so, unless you can type them out into your terminal, searching for them is not possible *yet*. I am working on cleaning up the database a bit so that this will no longer be a issue. Watch this [**repository**][spacetar]

    ```bash
    spacetar --source "TMC-1"
    ```

* `--emband`: Search for space molecules discovered in a particular EM band. There are three choices for this option: **Radio**, **IR**, and **UV/Vis**. This option is case-insensitive, so you can type *Radio* or *radio* and both will work. For example:

    ```bash
    spacetar --emband "UV/Vis"
    ```

* `--telescope`: Search for space molecules discovered by a particular telescope. You can search for a particular telescope both by its full name or its short name. For example:

    ```bash
    spacetar --telescope "NRAO 36-ft"
    ```

* `--author`: Search for space molecules by author. This will let you know how many discoveries is a particular scientist associated with. For example:

    ```bash
    spacetar --author "J. Cernicharo"
    ```

* `--extragalactic`: Search for space molecules discovered in a particular, *extragalactic* source. This database keeps a track of only the first extragalactic detection of each space molecule, so the actual number of space molecules associated with a source might be higher. I am trying to work out a solution for this as well, so watch this [**repository**][spacetar]!

* `--tentative`: Search for space molecules whose detection in space is still *tentative*; that is, it requires further confirmation from observations.

    ```bash
    spacetar --tentative
    ```

* `--like`: Instead of doing an exact match search, do a *like* search. This option allows you to enter just a part of a chemical formula, source name, telescope name, and so on. You should always try this option and when an exact match search fails. For example, say you wish to find out which molecules have been discovered thanks to a particular telescope, but you only remeber that it has "*NRAO*" in the name:

    ```bash
    spacetar --telescope NRAO --like
    ```

    or say you remember that a source name started with "*PKS*":

    ```bash
    spacetar --source PKS --like
    ```

Apart from all of these search options, there are a few more extra options, like:

* `--no-pager`: This specifies whether you want to see the output directly in the terminal, instead of using a pager, which is the default. Considering how many space molecules there are, viewing the database through a pager is more convenient. However, this flag is useful when the number of search results is not really great, and when you want to pipe the output into a text file.

* `--update`: This allows you to *update* the database. That means that the data will be scraped again, and then stored as an SQLite database. I would recommend not over-using this, because too many requests to a particular site *could* crash it. Let us be considerate of all the work David has put in for all of us and not do that :grin:!

* `--help`: Show the help message.

* `--version`: Show the version of [**spacetar**][spacetar] you are using.

[spacetar]: https://github.com/astrogewgaw/spacetar
