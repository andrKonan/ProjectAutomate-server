# server/tests/test_filepath.py
import os
import pathlib
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def find_python_files(base_dir: pathlib.Path):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def has_correct_header(filepath):
    expected_header = f"# {os.path.relpath(filepath, PROJECT_ROOT).replace(os.sep, '/')}"
    with open(filepath, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
    return first_line == expected_header

def test_collection_modifyitems():    
    missing = []
    
    for py_file in find_python_files(pathlib.Path('.')):
        if not has_correct_header(py_file):
            missing.append(py_file)

    if missing:
        raise pytest.UsageError(
            f"❌ The following files are missing a valid path header on the first line:\n" +
            "\n".join(f" - {os.path.relpath(f, PROJECT_ROOT)}" for f in missing)
        )
    