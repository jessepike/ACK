SHELL := /bin/bash

.PHONY: help setup lint test format typecheck dev build run clean

help:
	@echo "Targets: setup lint typecheck test format dev build run clean"

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist build .next node_modules


setup:
{% if cookiecutter.project_type == "node_nextjs_app" %}
	{{ "pnpm" if cookiecutter.package_manager == "pnpm" else cookiecutter.package_manager }} install
{% else %}
	python -m venv .venv
	. .venv/bin/activate && python -m pip install -U pip
{% if cookiecutter.project_type == "python_fastapi_api" %}
	. .venv/bin/activate && pip install -r requirements.txt
{% elif cookiecutter.project_type == "shared_lib_python" %}
	. .venv/bin/activate && pip install -e ".[dev]"
{% else %}
	@echo "No python deps for this project type"
{% endif %}
{% endif %}

lint:
{% if cookiecutter.project_type == "node_nextjs_app" %}
	{{ "pnpm" if cookiecutter.package_manager == "pnpm" else cookiecutter.package_manager }} run lint
{% elif cookiecutter.project_type in ["python_fastapi_api", "shared_lib_python"] %}
	. .venv/bin/activate && ruff check .
{% else %}
	@echo "No lint target configured"
{% endif %}

format:
{% if cookiecutter.project_type == "node_nextjs_app" %}
	{{ "pnpm" if cookiecutter.package_manager == "pnpm" else cookiecutter.package_manager }} run format
{% elif cookiecutter.project_type in ["python_fastapi_api", "shared_lib_python"] %}
	. .venv/bin/activate && ruff format .
{% else %}
	@echo "No format target configured"
{% endif %}

typecheck:
{% if cookiecutter.project_type == "node_nextjs_app" %}
	{{ "pnpm" if cookiecutter.package_manager == "pnpm" else cookiecutter.package_manager }} run typecheck
{% elif cookiecutter.project_type in ["python_fastapi_api", "shared_lib_python"] %}
	. .venv/bin/activate && mypy .
{% else %}
	@echo "No typecheck target configured"
{% endif %}

test:
{% if cookiecutter.project_type == "node_nextjs_app" %}
	{{ "pnpm" if cookiecutter.package_manager == "pnpm" else cookiecutter.package_manager }} run test
{% elif cookiecutter.project_type in ["python_fastapi_api", "shared_lib_python"] %}
	. .venv/bin/activate && pytest -q
{% else %}
	@echo "No tests configured"
{% endif %}

dev:
{% if cookiecutter.project_type == "node_nextjs_app" %}
	{{ "pnpm" if cookiecutter.package_manager == "pnpm" else cookiecutter.package_manager }} run dev
{% elif cookiecutter.project_type == "python_fastapi_api" %}
	. .venv/bin/activate && uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
{% else %}
	@echo "No dev server for this project type"
{% endif %}

build:
{% if cookiecutter.project_type == "node_nextjs_app" %}
	{{ "pnpm" if cookiecutter.package_manager == "pnpm" else cookiecutter.package_manager }} run build
{% elif cookiecutter.project_type == "shared_lib_python" %}
	. .venv/bin/activate && python -m build
{% elif cookiecutter.project_type == "shared_lib_ts" %}
	{{ "pnpm" if cookiecutter.package_manager == "pnpm" else cookiecutter.package_manager }} run build
{% else %}
	@echo "No build target configured"
{% endif %}
