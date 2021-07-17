# Installing *spacetar*

[**spacetar**][repo] is on PyPI, so installing it should be as simple as running:

```bash
pip install spacetar
```

on your command line 💻. If you have multiple versions of Python installed (which is true for many Linux-based operating systems), you should ideally prefix the above command to point to the correct version of Python. For instance, if you have both Python 3.7 and 3.8 installed, and you wish to install spacetar for the latter, you should type:

```bash
python3.8 -m pip install spacetar
```

instead.

You can also install spacetar manually, by running the following set of commands:

```bash
git clone https://github.com/astrogewgaw/spacetar.git
cd spacetar
make install
```

If you don't have [**make**][make] installed, just substitute the last command by:

```bash
pip install .
```

The same considerations for multiple Python versions apply.

Whether you installed [**spacetar**][repo] from PyPI or manually, you should now have access to all of its wonderful capabilities via your programs and the command line. To check, you can open up a terminal and run:

```bash
spacetar --version
```

This should print the version of [**spacetar**][repo], if it has been successfully installed on your system. You can also open your favourite Python REPL (such as IPython) and run:

```python
import spacetar
```

If either of these works without throwing an error, you are ready to explore the world of space molecules 🚀 !

[make]: https://www.gnu.org/software/make/
[repo]: https://github.com/astrogewgaw/spacetar
[contributing]: https://spacetar.readthedocs.io/en/latest/contributing.html
