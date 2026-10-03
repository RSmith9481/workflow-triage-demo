# Workflow Triage Demo

An original, local automation example by **Hallvance Tech**.

> A mark of quality. A step forward.

Turn a small list of fictional maintenance tasks into a reproducible work queue. This demonstrates input validation, explicit business rules, deterministic output, and focused tests.

## Run

Requires Python 3.10 or later. No packages, credentials, or network access are needed.

```sh
python3 triage.py sample/tasks.json --today 2026-10-03
python3 -m unittest discover -s tests -v
```

Redirect stdout to save a report:

```sh
python3 triage.py sample/tasks.json --today 2026-10-03 > report.md
```

## Rules

Completed tasks are omitted. An overdue task or a high-impact task due within seven days is **urgent**. Other tasks due within seven days are **soon**. Everything else is **planned**. Sort order is priority, due date, then task ID. The date is required so repeated runs are reproducible.

Input is an array of objects with unique `id`, `title`, ISO `due` date, `impact` (`low`, `medium`, `high`), and `status` (`open`, `done`). Invalid input produces an error and a nonzero exit code. Markdown metacharacters in titles are escaped.

The sample is entirely fictional. The demo reads a local JSON file and writes a report to stdout. It does not schedule jobs, send reminders, contact services, or change task records. Priority rules are illustrative, not safety or maintenance advice.

[See selected work](https://github.com/RSmith9481/hallvance-tech-portfolio) · [Business inquiries](mailto:hallvancetech@gmail.com)
