"""Tests for cx_Freeze.command.bdist_mac."""

from __future__ import annotations

import sys
from pathlib import Path
from subprocess import CalledProcessError

import pytest
from generate_samples import run_command

bdist_mac = pytest.importorskip(
    "cx_Freeze.command.bdist_mac", reason="macOS tests"
).bdist_mac

if sys.platform != "darwin":
    pytest.skip(reason="macOS tests", allow_module_level=True)

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_mac",
    "executables": ["hello.py"],
    "script_name": "setup.py",
    "author": "Marcelo Duarte",
    "author_email": "marcelotduarte@users.noreply.github.com",
    "url": "https://github.com/marcelotduarte/cx_Freeze/",
}
SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"


@pytest.mark.datafiles(SAMPLES_DIR / "simple")
def test_bdist_mac(datafiles: Path) -> None:
    """Test the simple sample with bdist_mac."""
    name = "hello"
    version = "0.1.2.3"
    dist_created = datafiles / "build"

    run_command(datafiles, "python setup.py bdist_mac")

    base_name = f"{name}-{version}"
    file_created = dist_created / f"{base_name}.app"
    assert file_created.is_dir(), f"{base_name}.app"


@pytest.mark.datafiles(SAMPLES_DIR / "simple")
def test_bdist_dmg(datafiles: Path, capsys) -> None:
    """Test the simple sample with bdist_dmg."""
    name = "hello"
    version = "0.1.2.3"
    dist_created = datafiles / "build"

    try:
        run_command(datafiles, "python setup.py bdist_dmg")
    except CalledProcessError as exc:
        expected_err = "hdiutil: create failed - Resource busy"
        if exc.stderr and exc.stderr.startswith(expected_err):
            pytest.xfail(
                reason=f"CalledProcessError: {exc.args[0]} - exc.stderr"
            )
        if exc.stdout and exc.stdout.startswith(expected_err):
            pytest.xfail(
                reason=f"CalledProcessError: {exc.args[0]} - exc.stdout"
            )
        captured = capsys.readouterr()
        if captured.err.startswith(expected_err):
            pytest.xfail(reason=captured.err[:-1])
        if captured.out.startswith(expected_err):
            pytest.xfail(reason=captured.out[:-1])

    base_name = f"{name}-{version}"
    file_created = dist_created / f"{base_name}.dmg"
    assert file_created.is_file(), f"{base_name}.dmg"
