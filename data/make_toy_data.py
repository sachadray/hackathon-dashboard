"""Generate the toy dataset for the hands-on exercise.

Everything here is SYNTHETIC. Song Xanh province and its ten districts do not
exist. The numbers are drawn from the parameters below with a fixed seed, so
the file is reproducible:

    python data/make_toy_data.py

Outputs
  data/district_jobs_toy.csv   the file students work with (four planted problems)
  docs/index.html              the reference dashboard, with clean data injected
"""
import csv
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
random.seed(2026)

# name, working-age pop (thousand), youth unemployment % (start), monthly drift (pp),
# job postings per 1,000 working-age (start), monthly growth of postings,
# median wage (million VND), training seats per month, applicants per seat
DISTRICTS = [
    ("Riverside",  180,  7.5, -0.02, 6.0,  0.005,  9.8, 400, 1.1),
    ("Old Market", 150,  8.2,  0.00, 5.0,  0.002,  9.1, 350, 1.2),
    ("Harbour",    210, 13.5,  0.06, 5.5,  0.020,  8.4, 300, 2.8),
    ("Hillside",    90, 14.8,  0.03, 1.8, -0.003,  6.9, 200, 0.9),
    ("Tech Park",  240,  5.9, -0.03, 9.0,  0.015, 13.5, 600, 1.6),
    ("Lakeside",   130, 11.2, -0.05, 3.5,  0.003,  8.8, 300, 1.3),
    ("Northfield", 170, 12.6,  0.05, 4.8,  0.018,  8.0, 250, 2.5),
    ("Eastgate",   160,  8.9,  0.01, 4.2,  0.004,  8.9, 350, 1.4),
    ("Greenbelt",  110, 10.1, -0.01, 2.6,  0.001,  7.6, 250, 1.0),
    ("Uplands",     70, 16.9,  0.04, 1.2, -0.005,  6.2, 150, 0.7),
]
MONTHS = [f"{y}-{m:02d}" for y in (2024, 2025) for m in range(1, 13)]
COLS = ["month", "district", "working_age_pop_thousand", "youth_unemployment_pct",
        "job_postings", "median_wage_million_vnd", "training_seats", "training_applicants"]

clean = []
for name, pop, u0, du, p0, gp, wage, seats, ratio in DISTRICTS:
    for t, month in enumerate(MONTHS):
        unemp = u0 + du * t + random.gauss(0, 0.3)
        postings = pop * p0 * (1 + gp) ** t * random.gauss(1, 0.06)
        applicants = seats * ratio * (1 + 0.004 * t) * random.gauss(1, 0.07)
        clean.append({
            "month": month,
            "district": name,
            "working_age_pop_thousand": pop,
            "youth_unemployment_pct": round(unemp, 1),
            "job_postings": round(postings),
            "median_wage_million_vnd": round(wage * (1 + 0.004 * t) * random.gauss(1, 0.01), 1),
            "training_seats": seats,
            "training_applicants": round(applicants),
        })

# ---- the messy copy students receive: four planted problems ----
messy = [dict(r) for r in clean]
for r in messy:
    # 1. decimal-point typo: 112.0 instead of about 11.2
    if r["district"] == "Lakeside" and r["month"] == "2024-11":
        r["youth_unemployment_pct"] = round(r["youth_unemployment_pct"] * 10, 1)
    # 2. missing value
    if r["district"] == "Greenbelt" and r["month"] == "2025-07":
        r["job_postings"] = ""
    # 3. inconsistent spelling of one district
    if r["district"] == "Tech Park" and r["month"] in ("2024-05", "2024-06", "2025-02"):
        r["district"] = "Tech park"
# 4. one duplicated row
dup = next(r for r in messy if r["district"] == "Old Market" and r["month"] == "2025-03")
messy.insert(messy.index(dup) + 1, dict(dup))

with open(ROOT / "data" / "district_jobs_toy.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(messy)

# ---- inject the clean data into the reference dashboard ----
page = ROOT / "docs" / "index.html"
if page.exists():
    html = page.read_text(encoding="utf-8")
    payload = json.dumps(clean, separators=(",", ":"))
    html, n = re.subn(r"/\*DATA\*/.*?/\*END\*/", lambda m: f"/*DATA*/{payload}/*END*/", html, flags=re.S)
    assert n == 1, "data placeholder not found in docs/index.html"
    page.write_text(html, encoding="utf-8")

# ---- check the intended answer still holds ----
def last3(name, fn):
    rows = [r for r in clean if r["district"] == name][-3:]
    return sum(fn(r) for r in rows) / 3

def median(xs):
    s = sorted(xs)
    return (s[4] + s[5]) / 2

names = [d[0] for d in DISTRICTS]
need = {n: last3(n, lambda r: r["youth_unemployment_pct"]) for n in names}
opp = {n: last3(n, lambda r: r["job_postings"] / r["working_age_pop_thousand"]) for n in names}
queue = {n: last3(n, lambda r: r["training_applicants"] / r["training_seats"]) for n in names}
picks = [n for n in names if need[n] > median(need.values())
         and opp[n] > median(opp.values()) and queue[n] > median(queue.values())]
print(f"{len(messy)} rows written. Above the median on all three criteria: {picks}")
assert picks == ["Harbour", "Northfield"], picks
