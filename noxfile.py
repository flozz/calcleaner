import nox


PYTHON_FILES = [
    "calcleaner",
    "setup.py",
    "noxfile.py",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("flake8", *PYTHON_FILES)
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)


# Requires inkscape
@nox.session(reuse_venv=True)
def gen_icons(session):
    session.install("yoga")
    icons = []
    for size in [32, 64, 128, 256]:
        output_icon = "./calcleaner/data/images/calcleaner_%i.png" % size
        session.run(
            "inkscape",
            "--export-area-page",
            "--export-filename=%s" % output_icon,
            "--export-width=%i" % size,
            "--export-height=%i" % size,
            "./calcleaner/data/images/calcleaner.svg",
            external=True,
        )
        session.run(
            "python",
            "-m",
            "yoga",
            "image",
            "--png-slow-optimization",
            output_icon,
            output_icon,
            external=True,
        )
        icons.append(output_icon)
