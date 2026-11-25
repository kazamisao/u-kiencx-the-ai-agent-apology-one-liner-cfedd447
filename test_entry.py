"""Tests for the apology one-liner entry.

Checks the two properties the sealed gate and the judge rely on:
the program is deterministic (same bytes on every run) and the line
it writes sits inside the competition's 1-159 character window.
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run_once(out_dir: str) -> bytes:
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=out_dir)
    subprocess.run(
        [sys.executable, "-P", "-s", os.path.join(HERE, "main.py")],
        env=env,
        check=True,
    )
    with open(os.path.join(out_dir, "entry.txt"), "rb") as fh:
        return fh.read()


def test_deterministic() -> None:
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        assert run_once(a) == run_once(b), "output differs between runs"


def test_window_and_shape() -> None:
    with tempfile.TemporaryDirectory() as d:
        text = run_once(d).decode("utf-8")
    assert 1 <= len(text) <= 159, f"line is {len(text)} chars, outside 1-159"
    assert text.strip() == text and text.strip(), "line must be non-blank"
    assert "\n" not in text, "entry must be a single line"


if __name__ == "__main__":
    test_deterministic()
    test_window_and_shape()
    print("all tests passed")
