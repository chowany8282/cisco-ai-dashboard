from pathlib import Path

try:
    import tomllib  # py311+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


def test_secrets_example_exists_and_keys_present():
    path = Path(".streamlit/secrets.toml.example")
    assert path.exists()

    data = tomllib.loads(path.read_text(encoding="utf-8"))
    for key in ("API_KEY_LOG", "API_KEY_SPEC", "API_KEY_OS"):
        assert key in data
