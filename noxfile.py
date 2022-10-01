import nox


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def test(session: nox.Session) -> None:
    # session.install(".[dev]")
    session.run("pip", "install", "-qq", ".[dev]")
    session.run("pytest", "-vvv", "--durations=5")
