# Saving, loading and trimming the calculation history.
import json
from datetime import datetime, timedelta

# ============================================================
# HELPERS
# ============================================================
def prune_entries(entries, days=7, now=None):
    """Return only the well-formed entries that are newer than `days` days."""
    now = now or datetime.now()
    cutoff = now - timedelta(days=days)
    kept = []
    for entry in entries:
        try:
            stamp = datetime.fromisoformat(entry["time"])
            entry["expression"], entry["result"]  # make sure both keys exist
        except (KeyError, ValueError, TypeError):
            continue
        if stamp >= cutoff:
            kept.append(entry)
    return kept

# plain language for dates
def day_label(day, today=None):
    today = today or datetime.now().date()
    if day == today:
        return "Today"
    if day == today - timedelta(days=1):
        return "Yesterday"
    return f"{day:%a %d %b}"

# ============================================================
# HISTORY
# ============================================================
class History:
    def __init__(self, path, days=7):
        self.path = path
        self.days = days
        self.entries = self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except (OSError, ValueError):
            return []
        if not isinstance(entries, list):
            return []
        return prune_entries(entries, self.days)

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
        except OSError:
            pass  # history is a privilege, ensure it won't break

    def prune(self, now=None):
        self.entries = prune_entries(self.entries, self.days, now)

    def add(self, expression, result, now=None):
        now = now or datetime.now()
        self.entries.append({
            "time": now.isoformat(timespec="seconds"),
            "expression": expression,
            "result": result,
        })
        self.prune(now)
        self.save()

    def clear(self):
        self.entries = []
        self.save()