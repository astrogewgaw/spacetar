# type: ignore

from pathlib import Path
from setuptools import setup, find_packages


here = Path(__file__).parent.resolve()
install_requires = ["attrs", "rich", "typer", "tabulate", "SQLAlchemy"]
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="spacetar",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Space molecules in your terminal!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astrogewgaw/spacetar",
    author="Ujjwal Panda",
    author_email="ujjwalpanda97@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    keywords=(
        "catalog",
        "terminal",
        "database",
        "astronomy",
        "catalogue",
        "astrochemistry",
        "space molecules",
        "command line tool",
    ),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_package_data=True,
    python_requires=">=3.5, <4",
    install_requires=install_requires,
    entry_points={"console_scripts": ["spacetar=spacetar.terminal:app"]},
    project_urls={
        "Documentation": "https://spacetar.readthedocs.io",
        "Source": "https://github.com/astrogewgaw/spacetar",
        "Bug Reports": "https://github.com/astrogewgaw/spacetar/issues",
        "Discussions": "https://github.com/astrogewgaw/spacetar/discussions",
    },
    cmd_class={},
    zip_safe=False,
)