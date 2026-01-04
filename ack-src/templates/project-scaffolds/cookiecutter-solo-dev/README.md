---
type: template
description: "Cookiecutter: Solo Dev Repo Template"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# Cookiecutter: Solo Dev Repo Template

# How to run the cookiecutter template



unzip cookiecutter-solo-dev-template.zip
cd cookiecutter-solo-dev

cookiecutter .

cd <project_slug>
make setup
make dev

## Where to run from
Run `cookiecutter` from the **template root folder** that contains:
- `cookiecutter.json`
- `{{cookiecutter.project_slug}}/`
- `hooks/`

Example (after downloading/unzipping):

```bash
cd /path/to/cookiecutter-solo-dev
ls
# cookiecutter.json  hooks/  {{cookiecutter.project_slug}}/  README.md
```





This cookiecutter generates **one repo** in one of these shapes:

- `node_nextjs_app` (Node + Next.js)
- `python_fastapi_api` (Python + FastAPI)
- `shared_lib_python` (Python library)
- `shared_lib_ts` (TypeScript library)

It includes a standard repo spine (docs/scripts/infra/src/tests/config), a Makefile, version pins, `.env.example`, and optional GitHub Actions CI.

## Quickstart

```bash
pipx install cookiecutter  # or: pip install cookiecutter
cookiecutter .
```

## Conventions

- No secrets in git. Use `.env.example` + platform env vars.
- `make setup && make test` should work on a fresh clone.
- CI runs `lint`, `typecheck` (if applicable), and `tests`.

## Generated Structure (typical)

```text
repo/
  .github/workflows/
  docs/ (architecture, decisions, runbooks)
  infra/
  scripts/
  src/
  tests/
  config/
  README.md
  Makefile
  .env.example
  .gitignore
  .editorconfig
  .node-version / .python-version
```

