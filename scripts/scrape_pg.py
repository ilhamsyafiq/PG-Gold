#!/usr/bin/env python3
import json, re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://publicgold.com.my/index.php?pgcode=PG01881462&route=dealer%2Fpage"
OUT = Path("data/gold.json")

def fetch_html():
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0 (compatible; PG-Gold-Tracker/1.0)"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

def extract(html):
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    m = re.search(r"GOLD\s+GAP\s+ACCOUNT\s+24K.*?RM\s*([\d,]+(?:\.\d+)?)\s*/\s*gram", text, re.I)
    if not m:
        raise RuntimeError("GAP 24K price not found on Public Gold page")
    price = float(m.group(1).replace(",", ""))
    updated = None
    u = re.search(r"Last updated\s+(\d{2}-[A-Za-z]{3}-\d{4})(?:\s+(\d{2}:\d{2}:\d{2}))?", text, re.I)
    if u:
        updated = " ".join(x for x in u.groups() if x)
    return price, updated

def main():
    html = fetch_html()
    price, source_updated = extract(html)
    today = datetime.now(timezone(timedelta(hours=8))).date().isoformat()
    data = {"source":"Public Gold","product":"GOLD GAP ACCOUNT 24K","unit":"gram","currency":"MYR","updated":today,"history":[]}
    if OUT.exists():
        try:
            data = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            pass
    history = data.get("history", [])
    history = [x for x in history if x.get("date") != today]
    history.append({"date":today,"price":round(price,2)})
    history = sorted(history, key=lambda x:x.get("date",""))[-365:]
    data.update({"source":"Public Gold","product":"GOLD GAP ACCOUNT 24K","unit":"gram","currency":"MYR","updated":today,"source_updated":source_updated,"source_url":URL,"history":history})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated GAP 24K: RM {price:.2f}/g | source update: {source_updated} | {today}")

if __name__ == "__main__":
    main()
