# Commit this session's work as three commits, merge to main, and push.
#
# Run from the repository root:
#     powershell -ExecutionPolicy Bypass -File .\finish-session.ps1
#
# It stops at the first failure and changes nothing on the remote until every local step
# has succeeded. Delete this file afterwards; it is a one-off.

$ErrorActionPreference = 'Stop'
$msg = 'C:\Users\deyao\AppData\Local\Temp\claude\D--Git-igd-capstone-2026\f980f86b-de6b-4588-846b-776c31f9385d\scratchpad'

function Step($label) { Write-Host "`n=== $label ===" -ForegroundColor Cyan }
function Check($label) { if ($LASTEXITCODE -ne 0) { throw "$label failed (exit $LASTEXITCODE)" } }

Step 'Confirming the branch'
git rev-parse --abbrev-ref HEAD
if ((git rev-parse --abbrev-ref HEAD) -ne 'lane-a/launcher-and-gate') {
    throw 'Expected to be on lane-a/launcher-and-gate.'
}

Step 'Confirming .env is not tracked'
git check-ignore -q .env
Check 'git check-ignore .env'

Step 'Running the gate'
uv run python -m packs.build --check;            Check 'packs.build --check'
uv run python scripts/build_team_tasks.py --check; Check 'build_team_tasks --check'
uv run ruff check .;                             Check 'ruff check'
uv run ruff format --check .;                    Check 'ruff format --check'
uv run mypy core modules corpus;                 Check 'mypy'
uv run pytest -q;                                Check 'pytest'

Step 'Commit 1 of 3 - repair make check'
git reset -q
git add core/contracts.py corpus/validate.py packs/build.py `
        packs/insurance_agent/schemas.py packs/iras_tax/schemas.py `
        tests/test_register_validation.py modules/__init__.py modules/_template/module.yaml `
        tools/paperbrain pyproject.toml uv.lock .python-version `
        infra/docker-compose.yml infra/.env.example
Check 'git add (1)'
git commit -F "$msg\c1.txt"
Check 'git commit (1)'

Step 'Commit 2 of 3 - the vertical build'
git add -A -- . ':!graphify-out' ':!docs/team-tasks.csv' ':!team' ':!scripts/build_team_tasks.py' ':!finish-session.ps1'
Check 'git add (2)'
git commit -F "$msg\c2.txt"
Check 'git commit (2)'

Step 'Commit 3 of 3 - examples, reviewers and the schedule'
git add docs/team-tasks.csv team scripts/build_team_tasks.py
Check 'git add (3)'
git commit -F "$msg\c3.txt"
Check 'git commit (3)'

Step 'What is about to be pushed'
git log --oneline main..HEAD
git status --short

Step 'Merging into main'
git checkout main;           Check 'git checkout main'
git merge --ff-only lane-a/launcher-and-gate; Check 'git merge --ff-only'

Step 'Pushing'
git push origin main;                          Check 'git push main'
git push origin lane-a/launcher-and-gate;      Check 'git push branch'

Write-Host "`nDone. main and lane-a/launcher-and-gate are pushed." -ForegroundColor Green
Write-Host "You can now delete finish-session.ps1." -ForegroundColor DarkGray
