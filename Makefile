.PHONY: check dev packs tasks graph graph-setup corpus-check eval eval-quick fmt

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

# Run once per clone: teaches git the union merge driver for graphify-out/graph.json,
# which .gitattributes already asks for. Without it, two people's graph updates conflict.
graph-setup:
	git config merge.graphify.driver "graphify merge-driver %O %A %B"
	git config merge.graphify.name "graphify union merge for graph.json"
	@echo "merge driver registered. Now: graphify install --platform claude && graphify hook install"

# Refresh the code graph (free, local). For docs and markdown run /graphify . in Claude Code.
graph:
	graphify update .

fmt:
	uv run ruff format . && uv run ruff check --fix .

dev:
	uv run python scripts/run_parrot.py

# Validate a register handed over by Lane E before anyone builds against it.
corpus-check:
	uv run python -m corpus.validate corpus/register/batch1.csv

eval:
	uv run python -m eval.run --corpus a --out eval/results

eval-quick:
	uv run python -m eval.run --corpus a --subset 25 --out /tmp/parrot-eval
