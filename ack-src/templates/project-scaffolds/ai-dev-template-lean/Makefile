.PHONY: python node sanity

python:
	cd python && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && python src/smoke.py

node:
	cd node && pnpm install && pnpm dev

sanity:
	./scripts/sanity.sh
