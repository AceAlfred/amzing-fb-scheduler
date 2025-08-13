import os
import csv
import time
import json
import requests
from datetime import datetime
from dateutil import parser as dtparser
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()

GRAPH_VERSION = "v19.0"
API_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"

PAGE_ID = os.environ.get("FB_PAGE_ID")
ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")

CSV_PATH = "amzing_fb_schedule.csv"

def iso_to_unix_utc(iso_str: str) -> int:
    dt = dtparser.isoparse(iso_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("Europe/Stockholm"))
    return int(dt.astimezone(ZoneInfo("UTC")).timestamp())

def schedule_post(message: str, scheduled_iso: str) -> dict:
    url = f"{API_BASE}/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "published": "false",
        "scheduled_publish_time": str(iso_to_unix_utc(scheduled_iso)),
        "access_token": ACCESS_TOKEN,
    }
    resp = requests.post(url, data=payload, timeout=30)
    try:
        data = resp.json()
    except json.JSONDecodeError:
        data = {"error": f"Non-JSON response: {resp.text}"}
    if not resp.ok:
        raise RuntimeError(f"API error {resp.status_code}: {data}")
    return data

def main():
    if not PAGE_ID or not ACCESS_TOKEN:
        raise SystemExit("❌ Saknar FB_PAGE_ID eller FB_PAGE_ACCESS_TOKEN i .env")

    successes, failures = 0, 0
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            message = row.get("message", "").strip()
            scheduled_iso = row.get("scheduled_time_iso", "").strip()
            if not message or not scheduled_iso:
                print("⚠️ Hoppar över rad utan message/scheduled_time_iso")
                continue

            try:
                time.sleep(0.5)
                result = schedule_post(message, scheduled_iso)
                post_id = result.get("id", "OK")
                print(f"✅ Schemalagd: {scheduled_iso} — {post_id}")
                successes += 1
            except Exception as e:
                print(f"❌ Misslyckades för {scheduled_iso}: {e}")
                failures += 1

    print(f"\n📊 Klart. Lyckade: {successes}, Misslyckade: {failures}")

if __name__ == "__main__":
    main()
