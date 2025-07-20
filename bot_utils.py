import csv
import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any


def load_posts(path: str) -> List[Dict[str, Any]]:
    """Load posts configuration from the given JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def append_log(log_file: str, user: Any) -> None:
    """Append a user start record to the CSV log."""
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            getattr(user, 'username', '') or '',
            getattr(user, 'id', ''),
            getattr(user, 'first_name', '') or '',
            datetime.now(timezone.utc).isoformat(),
            ''
        ])


def update_subscription(log_file: str, user_id: int, status: str) -> None:
    """Update the subscription status for the last record of the given user."""
    rows = []
    if os.path.exists(log_file):
        with open(log_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    for row in reversed(rows):
        if len(row) >= 2 and row[1] == str(user_id) and (len(row) < 5 or row[4] == ''):
            if len(row) < 5:
                row.append(status)
            else:
                row[4] = status
            break
    with open(log_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
