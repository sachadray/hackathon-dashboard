"""Build the two student data packs from the source repositories.

    python build/make_data_packs.py --land ../vietnam-land --pfm ../vietnam-pfm-benchmarking

Writes docs/data/land/ and docs/data/pfm/ (CSV, GeoJSON, JSON and a README each)
plus a zip of each pack. Only openly sourced series are copied:

  land  GSO land-use statistics (province 2018-2023, national 2008-2023),
        Natural Earth boundaries (public domain), and published fiscal figures
        (Ministry of Finance, NSO, ISEAS, OECD, Resolution 39/2021/QH15).
        Left out on purpose: the CEIC export (data/VNM land use and price.xlsx)
        and the real-estate credit and Savills price series derived from it.
  pfm   the processed dashboard tables, which the public dashboard already
        embeds, plus GDP per capita 2025 (IMF WEO) taken from that same page.
"""
import argparse
import csv
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "data"


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def land(src):
    out = OUT / "land"
    out.mkdir(parents=True, exist_ok=True)
    G = json.loads((src / "site/data/gso_provinces.json").read_text())
    N = json.loads((src / "site/data/national.json").read_text())
    F = json.loads((src / "site/data/fiscal.json").read_text())
    geo = json.loads((src / "site/data/vn_provinces.geojson").read_text())

    years = [str(y) for y in G["meta"]["years"]]
    cats = {"total": "Total natural area", "agri": "Agricultural production land",
            "forest": "Forestry land", "special": "Specially used land", "homestead": "Homestead (residential) land"}

    # 1. provinces, one row per province and category, one column per year
    rows = []
    for p in G["provinces"]:
        for c, label in cats.items():
            v = p["values"].get(c, {})
            rows.append([p["name"], p["iso"], p["region"], c, label] + [("" if v.get(y) is None else v[y]) for y in years])
    write_csv(out / "land_provinces.csv", ["province", "iso", "region", "category", "category_label"] + years, rows)

    # 2. national series, land categories only (credit and price series left out)
    ncols = ["total", "agriculture", "agri_production", "agri_forestry", "non_agri", "homestead",
             "specially_used", "unused"]
    write_csv(out / "land_national.csv", ["year"] + ncols,
              [[y] + [N["land"][y].get(c, "") for c in ncols] for y in sorted(N["land"], key=int)])

    # 3. published fiscal and planning figures, one fact per row with its source
    S = dict(F["sources"])
    # the "prior" source points at a file in the private repository; name it for students instead
    S["prior"] = ("Earlier land-finance note by the author (unpublished); its own sources: MONRE land-area "
                  "statistics 2023, Ministry of Finance final accounts, provincial tax offices")
    facts = []
    def add(ind, year, val, unit, rec, note=None):
        facts.append([ind, year, val, unit, rec.get("kind", ""), S.get(rec.get("source"), rec.get("source", "")),
                      note if note is not None else rec.get("note", "")])
    for r in F["revenue_series"]["rows"]:
        add("land_revenue", r["year"], r["revenue"], "VND trillion", r)
        if r.get("pct_budget") is not None:
            add("land_revenue_share_of_state_revenue", r["year"], r["pct_budget"], "percent", r, "")
    for r in F["budget_revenue_total"]:
        add("state_budget_revenue", r["year"], r["value"], "VND trillion", r)
    g = F["gdp"]
    add("gdp_nominal", 2025, g["nominal_2025_vnd_tn"]["value"], "VND trillion", g["nominal_2025_vnd_tn"])
    add("gdp_real_growth", 2025, g["real_growth_2025_pct"]["value"], "percent", g["real_growth_2025_pct"])
    add("land_revenue_share_of_gdp", 2025, g["land_revenue_pct_gdp_2025"]["value"], "percent", g["land_revenue_pct_gdp_2025"])
    t = F["target_vs_outturn_2025"]
    add("land_revenue_target", 2025, t["target"], "VND trillion", t)
    P = F["land_use_plan"]
    add("rice_land_floor", 2030, P["rice_land_floor_kha"]["value"], "thousand ha", P["rice_land_floor_kha"])
    add("non_agri_land_target_original", 2030, P["non_agri_target_2030_kha"]["value"], "thousand ha", P["non_agri_target_2030_kha"])
    add("non_agri_land_target_adjusted", 2030, P["non_agri_target_2030_adjusted_kha"]["value"], "thousand ha", P["non_agri_target_2030_adjusted_kha"])
    for p in F["provinces_2025"]:
        v = p.get("land_use_fees", p.get("land_revenue"))
        add("province_land_revenue_" + p["iso"], 2025, v, "VND trillion", p, (p["name"] + ". " + p.get("note", "")).strip())
    write_csv(out / "land_finance.csv", ["indicator", "year", "value", "unit", "kind", "source", "note"], facts)

    # 4. boundaries, with the province name added for convenience
    names = {p["iso"]: p["name"] for p in G["provinces"]}
    for f in geo["features"]:
        f["properties"] = {"iso": f["properties"]["iso"], "name": names.get(f["properties"]["iso"], "")}
    (out / "vn_provinces.geojson").write_text(json.dumps(geo, separators=(",", ":")))
    return out


def pfm(src):
    out = OUT / "pfm"
    out.mkdir(parents=True, exist_ok=True)
    d = src / "data/processed/dashboard"
    for f in ["economies.csv", "scores.csv", "indicators.csv", "indicator_values.csv", "config.json"]:
        shutil.copy(d / f, out / f)
    page = (src / "docs/index.html").read_text(encoding="utf-8")
    m = re.search(r'"gdp":(\{[^}]*\})', page)
    gdp = json.loads(m.group(1))
    write_csv(out / "gdp_per_capita.csv", ["iso3", "gdp_per_capita_usd_2025"], sorted(gdp.items()))
    return out


def zip_pack(folder, name):
    z = OUT / name
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(folder.iterdir()):
            zf.write(f, f"{folder.name}/{f.name}")
    return z


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--land", type=Path, required=True)
    ap.add_argument("--pfm", type=Path, required=True)
    a = ap.parse_args()
    lo, po = land(a.land.resolve()), pfm(a.pfm.resolve())
    for folder in (lo, po):
        shutil.copy(ROOT / "build" / f"README_{folder.name}.md", folder / "README.md")
    zip_pack(lo, "land_pack.zip")
    zip_pack(po, "pfm_pack.zip")
    print("land:", sorted(p.name for p in lo.iterdir()))
    print("pfm: ", sorted(p.name for p in po.iterdir()))
