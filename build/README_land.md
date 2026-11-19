# Land pack: Viet Nam's land and the revenue it raises

Four files. Everything is in thousand hectares unless the column says otherwise.

| File | What it holds | Size |
|---|---|---|
| `land_provinces.csv` | Land area by province and category, 2018, 2020, 2021, 2022, 2023 | 63 provinces × 5 categories = 315 rows |
| `land_national.csv` | Land area for the whole country by category, 2008 to 2023 | 14 years (no 2010 or 2019) |
| `land_finance.csv` | Land revenue, state revenue, GDP and the 2030 land-use plan targets, one figure per row with its source | 24 rows |
| `vn_provinces.geojson` | Province boundaries for a map, keyed by `iso` (same code as in `land_provinces.csv`) | 63 shapes |

## land_provinces.csv

| Column | Meaning |
|---|---|
| `province`, `iso`, `region` | Province name, ISO 3166-2 code (join key to the map), one of six regions |
| `category` | `total` natural area · `agri` agricultural production land (crops, mostly rice) · `forest` forestry land · `special` specially used land (industry, roads, public works) · `homestead` residential land |
| `2018` … `2023` | Area in thousand hectares |

Known problems: **Da Nang**'s specially used land falls from 44.4 to 13.9 between 2021 and 2022, a change of
definition rather than a real change, so do not compute changes for Da Nang. Binh Duong and Binh Phuoc have a
blank `agri` value in 2021 (the published figure was a duplicate). 2019 is not published.

## land_national.csv

`total`, `agriculture` (all agricultural land, including forest), `agri_production`, `agri_forestry`,
`non_agri` (everything built: homestead plus specially used plus other), `homestead`, `specially_used`, `unused`.
Two jumps (2011 and 2020) are mostly reclassifications, not real changes on the ground.

## land_finance.csv

Columns: `indicator`, `year`, `value`, `unit`, `kind` (`published` or `derived` by the author), `source`, `note`.
Key figures: land revenue reached **575.5 trillion dong in 2025**, 21.7% of state revenue and 4.48% of GDP.
The national rice-land floor is **3,500 thousand ha** (Resolution 39/2021/QH15).

## A useful formula

How many years of farmland can a province still convert at its recent pace?

```
conversion per year = (homestead + special in 2023 − homestead + special in 2018) / 5
protected share     = 3,500 / national agricultural production land in 2023   (about 30%)
years left          = agri in 2023 × (1 − protected share) / conversion per year
```

With this, Quang Ninh has about 22 years, Hai Phong 31, Bac Ninh 44.

## Sources

National Statistics Office of Viet Nam (GSO), land-use statistics. Boundaries: Natural Earth 10m admin-1
(public domain), simplified. Fiscal figures: Ministry of Finance as reported in the Vietnamese press, NSO,
ISEAS Perspective 2026/62, OECD Economic Survey of Viet Nam 2025, National Assembly Resolution 39/2021/QH15.
Provinces are the 63 that existed before the 2025 merger into 34.

Built from: <https://sachadray.github.io/vietnam-land/>
