# pytest-djangoapp installation

[uv](https://docs.astral.sh/uv/) is recommended for installation, though plain `pip` works too.

## From PyPI

Add the package to a project:

```bash
uv add pytest-djangoapp
```

or with pip:

```bash
pip install pytest-djangoapp
```

## From source

Clone the repository and synchronize its development environment:

```bash
git clone https://github.com/idlesign/pytest-djangoapp pytest-djangoapp
cd pytest-djangoapp
uv sync
```

Run commands in the project environment with `uv run`.
