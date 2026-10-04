import json,re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

URL="https://publicgold.com.my/index.php?pgcode=PG01881462&route=dealer%2Fpage"
OUT=Path("data/gold.json")

r=requests.get(URL,headers={"User-Agent":"Mozilla/5.0"},timeout=30)
r.raise_for_status()
soup=BeautifulSoup(r.text,"html.parser")
text=" ".join(soup.stripped_strings)

# Public Gold page currently exposes the GAP price in the section:
# GOLD GAP ACCOUNT 24K ... RM xxx / gram
m=re.search(r"GOLD\s+GAP\s+ACCOUNT\s+24K.*?RM\s*([\d,]+(?:\.\d+)?)\s*/\s*gram",text,re.I)
if not m:
    # fallback: search a nearby HTML block
    node=soup.find(string=re.compile(r"GOLD GAP ACCOUNT 24K",re.I))
    area=node.parent.parent.get_text(" ",strip=True) if node else text
    m=re.search(r"RM\s*([\d,]+(?:\.\d+)?)\s*/\s*gram",area,re.I)
if not m:
    raise RuntimeError("GAP price not found. Public Gold page structure may have changed.")

price=float(m.group(1).replace(",",""))
tz=timezone(timedelta(hours=8))
now=datetime.now(tz)
obj=json.loads(OUT.read_text()) if OUT.exists() else {"updated":None,"source":"Public Gold","history":[]}

# GAP price changes daily; keep one latest observation per calendar date.
today=now.strftime("%Y-%m-%d")
history=[x for x in obj.get("history",[]) if x.get("date")!=today]
history.append({"date":today,"price":price})
history=sorted(history,key=lambda x:x["date"])[-730:]

obj.update({"updated":now.isoformat(),"source":"Public Gold","history":history})
OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
print(f"PG GAP: RM {price:.2f}/g; {today}")
