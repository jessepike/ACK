import shutil
from pathlib import Path

ptype = "{{cookiecutter.project_type}}"
pm = "{{cookiecutter.package_manager}}"

root = Path(".")

def rm(path):
    p = root / path
    if p.is_dir():
        shutil.rmtree(p, ignore_errors=True)
    elif p.exists():
        p.unlink()

# Always keep docs/, scripts/, infra/, config/, tests/, src/
# Remove irrelevant skeletons

if ptype != "node_nextjs_app":
    rm("package.json")
    rm("pnpm-lock.yaml")
    rm("package-lock.json")
    rm("yarn.lock")
    rm("next.config.js")
    rm("tsconfig.json")
    rm("src/pages")
    rm("src/app_next")
    rm("src/components")
    rm("src/styles")
    rm("public")
    rm(".eslintrc.json")
    rm(".prettierrc")
    rm("jest.config.js")

if ptype not in ("python_fastapi_api", "shared_lib_python"):
    rm("pyproject.toml")
    rm("requirements.txt")
    rm("src/app.py")
    rm("src/__init__.py")
    rm("tests/test_health.py")

# Lockfile cleanup
if ptype == "node_nextjs_app":
    # Keep only the chosen package manager lockfile
    if pm != "pnpm":
        rm("pnpm-lock.yaml")
    if pm != "npm":
        rm("package-lock.json")
    if pm != "yarn":
        rm("yarn.lock")

# If user said no CI, remove workflow
if "{{cookiecutter.use_github_actions_ci}}" != "yes":
    rm(".github")

# If user said no ADR, remove decisions dir
if "{{cookiecutter.include_adr}}" != "yes":
    rm("docs/decisions")

from pathlib import Path
if "{{cookiecutter.use_docker}}" != "yes":
    p = Path("Dockerfile")
    if p.exists():
        p.unlink()
