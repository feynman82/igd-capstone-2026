.PHONY: check dev packs tasks corpus-check eval eval-quick fmt

check:
	uv run python -m packs.build --check
	uv run python scripts/build_team_tasks.py --check
	uv run ruff check . && uv run ruff format --check . && uv run mypy core modules corpus && uv run pytest -q

# Regenerate schemas.py, the register column headers and the field dictionary from pack.yaml.
packs:
	uv run python -m packs.build

# Regenerate each member's task list from docs/team-tasks.csv.
tasks:
	uv run python scripts/build_team_tasks.py

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
