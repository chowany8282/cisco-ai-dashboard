# Setup (recommended)

## 1) Python 3.11

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

## 2) Install

```bash
pip install -U pip
pip install -r requirements.txt
```

## 3) Secrets

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then fill real API keys
```

## 4) Run

```bash
streamlit run app.py
```

## 5) Test

```bash
ruff check .
pytest -q
```
