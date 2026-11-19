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


TRACKS = [
    ("land", "Track A · Land", "Which provinces will run out of convertible farmland first?",
     "A provincial finance director", ["land_provinces.csv", "vn_provinces.geojson"]),
    ("pfm", "Track B · PFM", "How does Viet Nam compare with its neighbours, and where is the biggest gap?",
     "A Ministry of Finance official", ["scores.csv", "economies.csv"]),
]
STEPS = [(1, "Explore the files", 2), (2, "Build the dashboard", 6), (3, "Improve it: pick one line", 3), (4, "Check it, then share it", 3)]


def exercises_zip():
    """One download with both hands-on exercises: instructions, prompts and data."""
    import zipfile
    P = {p["id"]: p for p in all_prompts()["handson"]["prompts"]}
    md = ["# Hands-on exercises: build a dashboard in 15 minutes", "",
          "Work in pairs on one laptop. Pick one track. Open an AI assistant that reads files "
          "(claude.ai works on the free plan), attach the two files listed for your track, and paste "
          "the prompts below in order. Online version: https://sachadray.github.io/hackathon-dashboard/handout.html", "",
          "| Minutes | Step |", "|---|---|", "| 1 | Set up: open the assistant, attach the two files |"]
    md += [f"| {m} | {title} |" for _, title, m in STEPS]
    md += ["", "## The six parts of a good prompt", "", "```", P["template"]["text"], "```", ""]
    for key, name, q, reader, files in TRACKS:
        md += [f"## {name}", "", f"**Question:** {q}", "", f"**Reader:** {reader}", "",
               f"**Attach:** `{key}/{files[0]}` and `{key}/{files[1]}`. Every column is explained in `{key}/README.md`.", ""]
        for n, title, m in STEPS:
            md += [f"### {n}. {title} ({m} min)", "", "```", P[f"{key}-{n}"]["text"], "```", ""]
    md += ["## If something goes wrong", "",
           "- The dashboard does not appear in the chat: ask \"Give me the complete HTML file\", save it as `dashboard.html` and open it in a browser.",
           "- The map is empty: ask it to check the join between `iso` in the CSV and `iso` in the GeoJSON.",
           "- The numbers differ from the known value: ask for the calculation step by step for Quang Ninh, or for Viet Nam.", ""]
    out = DOCS / "data" / "hands-on-exercises.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("hands-on-exercises/EXERCISES.md", "\n".join(md))
        for key in ("land", "pfm"):
            for f in sorted((DOCS / "data" / key).iterdir()):
                z.write(f, f"hands-on-exercises/{key}/{f.name}")


if __name__ == "__main__":
    land_example()
    pfm_example()
    prompt_pages()
    exercises_zip()
    print("site built")
