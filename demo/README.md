# PARROT family demo

This is a lightweight, browser-runnable demonstration of the PARROT user experience.

## Run
Open `demo/family-app/index.html` through a local static server. Because the page loads JSON with fetch, use a local server rather than opening the file directly.

Example:
```bash
python -m http.server 8080
```
Then open:
`http://localhost:8080/demo/family-app/`

## Synthetic family data
`family-data.json` provides five fictional household profiles corresponding to the five persona situations on proposal page 3: Sarah, Marcus, Daniel & Rachel, Priya and Jason.

The additional biographical details are deliberately illustrative and are not claims about real people. No real insurer, bank or government agency is used.

## Design intent
The demo follows the proposal's four surfaces:
- Today
- Ask
- Vault
- Packs

It also demonstrates the proposal's trust behaviour: every supported answer is paired with a source, while an unsupported question produces an explicit abstention state.

This is a UI/demo layer. It does not replace the production Next.js/LangGraph/PostgreSQL implementation already present in the repository.
