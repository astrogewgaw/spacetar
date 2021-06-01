# Installation

Since [**spacetar**][spacetar] isn't on PyPI yet, the best way to install it right now is:

```bash
git clone https://github.com/astrogewgaw/spacetar.git
cd spacetar
make install
```

If you don't have [**make**][make] installed, you can just substitute `pip install -e .` for the last command. The `-e` flag is optional, and installs the package in *development mode*; that is, any change you make to the code will show up in the installed package. If you don't want to mess around with the code, you can just remove the flag. If you have multiple Python installations on your system, it would be wise to subsitute `python -m pip install .` for the last step, where `python` is whichever Python you prefer to install [**spacetar**][spacetar] in. Note that it supports only Python 3.6 and above. A PyPI release is coming *soon*.

[make]: https://www.gnu.org/software/make/
[spacetar]: https://github.com/astrogewgaw/spacetar
