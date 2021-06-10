import nox


@nox.session
def lint(session):

    """"""

    session.install("black")
    session.run("black", ".")


@nox.session(python=["3.6", "3.7", "3.8", "3.9"], reuse_venv=True)
def tests(session):

    """"""

    session.install("pytest", "pytest-cov")
    session.run("pip", "install", "-e", ".")
    session.run("pytest", "-vv", "--cov", "--cov-report", "term-missing", "tests")
