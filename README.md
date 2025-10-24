# Investing Research Dashboard

A restored working copy of my full-stack market operations workspace: structured research data, automation scripts, and the visual dashboard that I review each trading session. The repo keeps the source data (`master-plan/master-plan.md`), rendered dashboard (`master-plan/research-dashboard.html`), guides, and helper tooling in one place so it is easy to see **what the project is** and ship updates to GitHub.

## Core Components

| Path | Purpose |
|------|---------|
| `master-plan/master-plan.md` | Source-of-truth YAML + Markdown that drives every dashboard panel.
| `master-plan/research-dashboard.html` | Static HTML/JS dashboard generated from the plan; open in a browser for the full UI.
| `master-plan/README.md` | Deep dive on the dashboard workflow plus backup/archival instructions.
| `Toolbox/` | Centralized instructions, prompt libraries, and long-form workflows referenced by the daily plan.
| `scripts/` | Python helpers/automation (scrapers, sync jobs, templated updates).
| `Journal/`, `Research/`, `Tickers/`, `Trading/` | Supporting research notes, trade journals, and ticker-level studies that feed the plan.

Everything else (archives, backups, alternate dashboards) lives under `master-plan/archive` so the latest working files stay light.

## Quick Start

1. **Preview the dashboard**
   ```bash
   # from repo root
   python -m http.server 9000
   # then open http://localhost:9000/master-plan/research-dashboard.html
   ```
   Opening the file directly in a browser also works because it is a self-contained HTML bundle.

2. **Edit the data**
   - Update `master-plan/master-plan.md` to change sentiment cards, metrics, action items, etc.
   - The HTML reads the YAML front matter, so once you save the `.md` file, refresh the browser to see changes.

3. **Run automations (optional)**
   ```bash
   # regenerate dashboards or ingest new data
   python scripts/automation/run_workflow.py YYYY-MM-DD
   python scripts/automation/run_intraday_update.py YYYY-MM-DD
   ```
   These scripts push fresh research inputs into `master-plan.md` before you publish.

## Daily Use Workflow

- **Morning (30–45 min):** execute the full research workflow (`How to use_MP.txt`), sync datasets, and regenerate the dashboard.
- **Intraday (2–3 min):** quick sentiment + level refresh via `run_intraday_update.py` and a light edit to the planner section.
- **End of Day (10 min):** log trades inside `Journal/`, archive the day’s plan (`master-plan/archive/2025-10/`), and capture any lessons in `Toolbox` instructions.

## Backups & Restore Notes

- Every save drops timestamped backups beside the live files (`master-plan.md.backup`, `research-dashboard.html.safe_backup`).
- Historical copies live in `master-plan/archive/` organized by date so a restore is just copying the desired snapshot back into place.
- After restoring, review `git status`, confirm both the `.md` and `.html` versions represent the date you just recovered, then commit.

## Publishing Checklist

1. Verify `master-plan/master-plan.md` and `master-plan/research-dashboard.html` show the same `dashboard.pageTitle` date.
2. Open the HTML locally to ensure charts, tabs, and timelines render without console errors.
3. Stage all modified files plus any new backups you want tracked.
4. Commit with a message like `docs: restore research dashboard snapshot` and push to GitHub.

This README now documents the restored project so future commits clearly describe what lives in this repo.
