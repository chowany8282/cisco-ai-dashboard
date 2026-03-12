from pathlib import Path


def test_app_file_exists():
    assert Path("app.py").exists()


def test_requirements_exists():
    assert Path("requirements.txt").exists()
