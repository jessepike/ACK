# {{cookiecutter.project_name}}

Repo type: `{{cookiecutter.project_type}}`

## Standard commands

```bash
make setup
make lint
make typecheck
make test
make dev
```

## Secrets
- Use `.env.example` as the contract.
- Never commit real `.env` files.

{% if cookiecutter.project_type == "node_nextjs_app" %}
## Node + Next.js

### Prereqs
- Node {{cookiecutter.node_version}}
- {{cookiecutter.package_manager}}

### Run
```bash
make dev
```

{% elif cookiecutter.project_type == "python_fastapi_api" %}
## Python + FastAPI

### Prereqs
- Python {{cookiecutter.python_version}}

### Run
```bash
make dev
```

### Health
- `GET /healthz`

{% elif cookiecutter.project_type == "shared_lib_python" %}
## Shared library (Python)
This repo produces a reusable Python package.

{% elif cookiecutter.project_type == "shared_lib_ts" %}
## Shared library (TypeScript)
This repo produces a reusable TS package.

{% endif %}


## Enterprise add-ons
This template includes placeholders for:
- docs/threat-model/
- docs/sla-slo/
- observability/
- security/
