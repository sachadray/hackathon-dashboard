"""Inject data and prompts into the pages under docs/.

    python build/build_site.py

Run after build/make_data_packs.py. It reads only files inside this repository:
the data packs in docs/data/ and the prompt files in prompts/.
  - docs/examples/land-15min.html  <- province land data and boundaries
  - docs/examples/pfm-15min.html   <- scores and economy names
  - docs/prompts.html, docs/handout.html <- every prompt, as copy-paste cards
"""
import csv
import html
import json
import re
from pathlib import Path

from prompts_lib import all_prompts

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def inject(path, key, payload):
    page = path.read_text(encoding="utf-8")
    page, n = re.subn(rf"/\*{key}\*/.*?/\*END_{key}\*/",
                      lambda m: f"/*{key}*/{payload}/*END_{key}*/", page, flags=re.S)
    assert n == 1, f"{key} placeholder not found in {path.name}"
    path.write_text(page, encoding="utf-8")


def num(x):
    return None if x in ("", None) else float(x)


def land_example():
    rows = list(csv.DictReader(open(DOCS / "data/land/land_provinces.csv", encoding="utf-8")))
    prov = {}
    for r in rows:
        p = prov.setdefault(r["iso"], {"name": r["province"], "iso": r["iso"], "region": r["region"], "v": {}})
        p["v"][r["category"]] = r
    out = []
    for iso, p in prov.items():
        v = p["v"]
        excluded = iso == "VN-DN"  # definitional break in specially used land, 2021-2022
        built = lambda y: num(v["homestead"][y]) + num(v["special"][y])
        out.append({"name": p["name"], "iso": iso, "region": p["region"], "agri": num(v["agri"]["2023"]),
                    "conv": None if excluded else round((built("2023") - built("2018")) / 5, 4), "excluded": excluded})
    geo = json.loads((DOCS / "data/land/vn_provinces.geojson").read_text())
    page = DOCS / "examples/land-15min.html"
    inject(page, "PROV", json.dumps(out, separators=(",", ":"), ensure_ascii=False))
    inject(page, "GEO", json.dumps({"features": geo["features"]}, separators=(",", ":")))


def pfm_example():
    econ = {r["iso3"]: r for r in csv.DictReader(open(DOCS / "data/pfm/economies.csv", encoding="utf-8"))}
    out = []
    for r in csv.DictReader(open(DOCS / "data/pfm/scores.csv", encoding="utf-8")):
        out.append({"iso3": r["iso3"], "economy": r["economy"], "income": econ[r["iso3"]]["income"],
                    **{k: (None if num(r[k]) is None else round(num(r[k]), 4)) for k in ["D1", "D2", "D3", "D4", "overall"]}})
    inject(DOCS / "examples/pfm-15min.html", "SCORES", json.dumps(out, separators=(",", ":"), ensure_ascii=False))


def prompt_pages():
    data = all_prompts()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    for name in ["prompts.html", "handout.html"]:
        page = DOCS / name
        if page.exists():
            inject(page, "PROMPTS", payload)


if __name__ == "__main__":
    land_example()
    pfm_example()
    prompt_pages()
    print("site built")
