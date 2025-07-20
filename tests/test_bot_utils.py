import json
from types import SimpleNamespace
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bot_utils import load_posts, append_log, update_subscription


def test_load_posts(tmp_path):
    posts = [{"id": 1, "media": ["file.jpg"], "text": "hi"}]
    p = tmp_path / "posts.json"
    p.write_text(json.dumps(posts, ensure_ascii=False))
    assert load_posts(str(p)) == posts


def test_append_and_update(tmp_path):
    log_file = tmp_path / "stats.csv"
    # write header
    log_file.write_text("username,user_id,first_name,start_time,subscribed\n")
    user = SimpleNamespace(username="test", id=1, first_name="Test")
    append_log(str(log_file), user)
    update_subscription(str(log_file), 1, "yes")
    lines = log_file.read_text().splitlines()
    assert lines[1].endswith(',yes')
