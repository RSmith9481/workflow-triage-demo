"""Create a deterministic work queue from fictional/local task data."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


def parse_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("dates must use YYYY-MM-DD")
    return date.fromisoformat(value)


def prioritize(records, today):
    if not isinstance(records, list):
        raise ValueError("input must be a JSON array")
    seen, queue = set(), []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each task must be an object")
        task_id, title = record.get("id"), record.get("title")
        if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", task_id):
            raise ValueError("task IDs must contain 1–64 letters, digits, underscores or hyphens")
        if task_id in seen:
            raise ValueError("duplicate task ID: " + task_id)
        seen.add(task_id)
        if not isinstance(title, str) or not title.strip() or len(title) > 200 or any(ord(c) < 32 for c in title):
            raise ValueError("titles must be nonempty single-line text of at most 200 characters")
        impact, status = record.get("impact"), record.get("status")
        if impact not in ("low", "medium", "high") or status not in ("open", "done"):
            raise ValueError("invalid impact or status for " + task_id)
        due = parse_date(record.get("due"))
        if status == "done":
            continue
        days = (due - today).days
        priority = 0 if days < 0 or (impact == "high" and days <= 7) else 1 if days <= 7 else 2
        queue.append((priority, due, task_id, title.strip(), impact))
    return sorted(queue)


def markdown_text(text):
    return re.sub(r"([\\`*_{}\[\]()<>#+.!|~-])", r"\\\1", text)


def report(queue, today):
    lines = ["# Workflow Triage", "", "As of " + today.isoformat() + ". Fictional sample workflow.", ""]
    for rank, label in enumerate(("Urgent", "Soon", "Planned")):
        lines.extend(["## " + label, ""])
        tasks = [task for task in queue if task[0] == rank]
        lines.extend([f"- **{task_id}** — {markdown_text(title)} (due {due.isoformat()}; {impact} impact)" for _, due, task_id, title, impact in tasks] or ["No tasks."])
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--today", required=True, help="reproducible YYYY-MM-DD reference date")
    args = parser.parse_args()
    try:
        today = parse_date(args.today)
        records = json.loads(args.input.read_text(encoding="utf-8"))
        print(report(prioritize(records, today), today))
    except (OSError, ValueError) as error:
        print("Error: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
