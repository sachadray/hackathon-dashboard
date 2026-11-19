# PFM pack: how well does Viet Nam manage public money, compared with other countries?

PFM is public financial management: how a government plans its budget, spends it, reports on it and is held
to account. This pack scores 194 economies on 68 international indicators.

| File | What it holds | Size |
|---|---|---|
| `scores.csv` | **Start here.** One row per economy: the four dimension scores, the overall index and 19 sub-dimension scores | 194 rows |
| `economies.csv` | Name, income group, region, ASEAN-5 and OECD flags, year of the latest PEFA assessment and Open Budget Survey | 194 rows |
| `indicators.csv` | One row per indicator: name, unit, dimension, sub-dimension, direction, source, link | 85 rows |
| `indicator_values.csv` | One row per indicator and economy: raw `value` and standardised `z` | 9,817 rows |
| `gdp_per_capita.csv` | GDP per capita 2025, current US dollars | 192 rows |
| `config.json` | Names of the dimensions and sub-dimensions, scoring rules, default comparison set | |

## How to read a score

Every score is a **z-score**: 0 is the average of all economies with data, +1 is one standard deviation above
it. Higher is always better (indicators where lower is better have been flipped).

| Column in `scores.csv` | Dimension |
|---|---|
| `D1` | Budget preparation |
| `D2` | Budget execution |
| `D3` | Transparency, accountability and oversight |
| `D4` | Budget reliability and perceived effectiveness (reported alongside, not in the overall index) |
| `overall` | Mean of D1, D2 and D3 (needs at least two) |
| `sp_1a` … `sp_4c` | Sub-dimensions; names in `config.json` → `subpillars` |

Viet Nam (`VNM`): overall −0.11, rank 99 of 169 economies with a score. Strongest dimension: D4 (+0.50).
Weakest: D1 (−0.38).

## The default comparison set

Indonesia (`IDN`), Malaysia (`MYS`), the Philippines (`PHL`), Thailand (`THA`), Cambodia (`KHM`),
Korea (`KOR`), Japan (`JPN`), plus two group averages: **ASEAN-4** (IDN, MYS, PHL, THA) and
**upper-middle income** (from `economies.csv` → `income`). Exclude Viet Nam from group averages.

## How the scores are built (to recompute them)

1. For each indicator with `include` = 1: z = direction × (value − mean) / standard deviation over all economies
   with data, capped at ±3. (Already in `indicator_values.csv` → `z`.)
2. Sub-dimension = mean of its indicators' z-scores (at least one with data).
3. Dimension = mean of its sub-dimensions (at least half of them scored).
4. Overall = mean of D1 to D3 (at least two scored).

## Sources

PEFA Secretariat (2016-framework assessments), IBP Open Budget Survey 2025/2023, World Bank GovTech Maturity
Index 2025, Worldwide Governance Indicators, IMF World Economic Outlook October 2026, Global Tax Expenditures
Transparency Index, World Bank Global Public Procurement Database, ISORA, B-READY 2025. Full source and
licence for each indicator in `indicators.csv`.

Built from: <https://sachadray.github.io/vietnam-pfm-benchmarking/>
