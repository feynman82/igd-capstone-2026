.PHONY: check dev corpus-check eval eval-quick fmt

check:
	uv run ruff check . && uv run ruff format --check . && uv run mypy core modules packs corpus && uv run pytest -q

fmt:
	uv run ruff format . && uv run ruff check --fix .

dev:
	uv run uvicorn api.main:app --reload --port 8000 & (cd web && npm run dev)

# Validate a register handed over by Lane E before anyone builds against it.
corpus-check:
	uv run python -m corpus.validate corpus/register/batch1.csv

eval:
	uv run python -m eval.run --corpus a --out eval/results

eval-quick:
	uv run python -m eval.run --corpus a --subset 25 --out /tmp/parrot-eval
