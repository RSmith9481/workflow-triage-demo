import unittest
from datetime import date
from triage import prioritize, report, parse_date


def task(task_id="A", due="2026-10-03", impact="medium", status="open", title="Sample task"):
    return dict(id=task_id, due=due, impact=impact, status=status, title=title)


class TriageTests(unittest.TestCase):
    today = date(2026, 10, 3)

    def test_priority_boundaries(self):
        records = [task("overdue", "2026-10-02"), task("high7", "2026-10-10", "high"), task("medium7", "2026-10-10"), task("high8", "2026-10-11", "high")]
        self.assertEqual([(x[2], x[0]) for x in prioritize(records, self.today)], [("overdue", 0), ("high7", 0), ("medium7", 1), ("high8", 2)])

    def test_done_omitted_and_input_order_irrelevant(self):
        records = [task("B"), task("A"), task("C", status="done")]
        self.assertEqual(prioritize(records, self.today), prioritize(list(reversed(records)), self.today))
        self.assertEqual([x[2] for x in prioritize(records, self.today)], ["A", "B"])

    def test_invalid_records_rejected(self):
        for records in ({}, [None], [task(), task()], [task(due="2026-02-30")], [task(status="unknown")], [task(title="bad\nline")], [task(task_id="<bad>")]):
            with self.subTest(records=records), self.assertRaises(ValueError):
                prioritize(records, self.today)

    def test_date_requires_canonical_format(self):
        for value in ("20261003", "2026-1-01", None):
            with self.assertRaises(ValueError):
                parse_date(value)

    def test_markdown_cannot_create_links_or_html(self):
        output = report(prioritize([task(title="[sample](https://example.invalid) <img> | test")], self.today), self.today)
        self.assertIn(r"\[sample\]\(https://example\.invalid\) \<img\> \| test", output)

    def test_empty_queue(self):
        self.assertEqual(report([], self.today).count("No tasks."), 3)


if __name__ == "__main__":
    unittest.main()
