import pathlib

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


# NOTE All Gtk dependencies and introspection files must be installed for this
# to work.
@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install("-e", ".")
    session.run(
        "pytest",
        "--doctest-modules",
        "calcleaner",
        env={"LANG": "C"},  # Force using the default strings
    )


# Requires gettext
@nox.session
def locales_update(session):
    # Extract messages in .pot
    python_files = [p.as_posix() for p in pathlib.Path("calcleaner/").glob("**/*.py")]
    ui_files = [
        p.as_posix() for p in pathlib.Path("calcleaner/data/ui").glob("*.glade")
    ]
    session.run(
        "xgettext",
        "--from-code=UTF-8",
        "-o",
        "locales/messages.pot",
        *ui_files,
        *python_files,
        external=True,
    )
    # Updates locales
    for po_file in pathlib.Path("locales").glob("*.po"):
        session.run(
            "msgmerge",
            "--update",
            "--no-fuzzy-matching",
            po_file.as_posix(),
            "locales/messages.pot",
            external=True,
        )


# Requires gettext
@nox.session
def locales_compile(session):
    LOCAL_DIR = pathlib.Path("calcleaner/data/locales")
    for po_file in pathlib.Path("locales").glob("*.po"):
        output_file = (
            LOCAL_DIR
            / po_file.name[: -len(po_file.suffix)]
            / "LC_MESSAGES"
            / "org.flozz.calcleaner.mo"
        )
        print(output_file.as_posix())
        output_file.parent.mkdir(parents=True, exist_ok=True)
        session.run(
            "msgfmt",
            po_file.as_posix(),
            "-o",
            output_file.as_posix(),
            external=True,
        )


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
