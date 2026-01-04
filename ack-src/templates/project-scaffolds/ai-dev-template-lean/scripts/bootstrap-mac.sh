#!/usr/bin/env bash
set -euo pipefail

brew bundle

fnm install 20 || true
fnm default 20 || true

echo "Recommended Python: pyenv install 3.12.1 && pyenv global 3.12.1"
