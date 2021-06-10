import nox


@nox.session
def lint(session):

    """
    Lint the entire package using `black`. This installs black into
    a virtual environment and then uses it to lint all files in this
    directory and all sub-directories. This helps me add linting to
    my GitHub workflow. Locally, my files are linted on save, thanks
    to VSCode.
    """

    session.install("black")
    session.run("black", ".")


@nox.session(python=["3.6", "3.7", "3.8", "3.9"], reuse_venv=True)
def tests(session):

    """
    Run tests for spacetar, using `pytest`, and then generate a coverage
    report using the `pytest-cov` plugin. This coverage report will then
    be uploaded to Coveralls. Like all my packages, spacetar is also tested
    for all Python versions from 3.6 to 3.9. These are the Python versions
    currently supported by most big and small Python packages out there;
    support for most of the older versions (including 3.5) have been dropped
    by many.
    """

    session.install("pytest", "pytest-cov")
    session.run("pip", "install", "-e", ".")
    session.run("pytest", "-vv", "--cov", "--cov-report", "term-missing", "tests")
