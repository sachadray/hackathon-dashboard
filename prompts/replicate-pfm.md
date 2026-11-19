# Replicate the Viet Nam PFM benchmark from the data files

Target: <https://sachadray.github.io/vietnam-pfm-benchmarking/>, a benchmark view and a "predicted scores"
view, with live re-scoring. Input: the PFM pack only (`scores.csv`, `economies.csv`, `indicators.csv`,
`indicator_values.csv`, `gdp_per_capita.csv`, `config.json`).

**How to use these prompts.** Build in stages and check each stage against the numbers given. Stage 1 is the
most important: if the scoring engine does not reproduce `scores.csv` exactly, everything after it is wrong.
In Claude Code, put the six files in a folder, open the folder and paste the setup prompt, then each stage.

## setup | pfm | 0 | Setup: paste once, first

```
ROLE
You are a public finance economist and front-end developer. You build
benchmarking dashboards as one self-contained HTML file: no external libraries
(Google Fonts allowed), the data embedded, charts drawn as inline SVG, all
calculations in JavaScript in the page.

CONTEXT
This dashboard supports the public financial management (PFM) chapter of the
Viet Nam Public Finance Review. It scores 194 economies on four dimensions
mapped to the PEFA framework: D1 budget preparation, D2 budget execution,
D3 transparency, accountability and oversight, D4 budget reliability and
perceived effectiveness. Readers are Ministry of Finance officials and World
Bank economists. They want to see where Viet Nam stands against a comparison
set they choose, which indicators drive that, and whether the result is what
Viet Nam's income level would predict.

TASK
Build "Viet Nam PFM benchmark" in four stages. After each stage, stop, show the
result and the checks, and wait for me.

DATA (attached)
- indicators.csv: one row per indicator: code, include (1/0), dimension,
  subpillar, direction (+1 or -1), min_n (minimum economies with data),
  indicator name, unit, description, source, url.
- indicator_values.csv: code, iso3, value (raw), z (standardised).
- config.json: sub-dimension names and the dimension each belongs to; dimension
  names, the share of sub-dimensions needed, and whether each enters the
  overall index; params (min_dims = 2, cap = 3); the default comparison set.
- scores.csv: the published scores, for checking only.
- economies.csv: name, income group, region, year of the latest PEFA
  assessment (pefa_year) and Open Budget Survey (obs_year).
- gdp_per_capita.csv: GDP per capita 2025, current US dollars (IMF WEO).

OUTPUT (style)
IBM Plex Serif for the title, IBM Plex Sans for text, IBM Plex Mono for numbers.
White cards on a light grey page. A diverging red-white-green scale for
z-scores, centred on 0. Every indicator name starts with a small badge for its
source (PEFA, OBS, GTMI, WGI ...).

CHECKS
Never hard-code a score. Every score on the page is computed by the engine from
indicator_values.csv, so that switching an indicator off changes it.
```

## stage-1 | pfm | 1 | Stage 1: the scoring engine, verified

```
TASK
Write the scoring engine in JavaScript and verify it before any chart.

Rules:
1. An indicator is usable if include = 1, it has at least min_n economies
   with data, more than one, and a standard deviation above 0.
2. z = direction x (value - mean) / sample standard deviation, over all
   economies with data, then capped at +/-3.
3. Sub-dimension score = mean of its usable indicators' z-scores, if at least
   one has data.
4. Dimension score = mean of its sub-dimensions, if at least
   ceil(share x number of its sub-dimensions) are scored (share from
   config.json; 0.5 for every dimension).
5. Overall index = mean of the dimensions flagged as entering the overall
   index (D1 to D3), if at least min_dims = 2 are scored. D4 is reported
   alongside, not averaged in.
6. Rank = position among economies with a score, highest first.

OUTPUT
A small test page that prints, for every economy, the largest difference
between your D1 to D4 and overall and those in scores.csv, then Viet Nam's
row.

CHECKS
The largest difference must be below 0.000001. Viet Nam: D1 -0.38 (rank 95 of
138), D2 +0.29 (71 of 191), D3 -0.23 (100 of 170), D4 +0.50 (40 of 180),
overall -0.11 (99 of 169). The ASEAN-4 average (IDN, MYS, PHL, THA) of the
overall index is +0.28.
```

## stage-2 | pfm | 2 | Stage 2: the benchmark view

```
TASK
Build the main view for one focus economy (default Viet Nam) and the default
comparison set in config.json (seven economies, ASEAN-4 and upper-middle-income
averages; group averages leave out the focus economy).

OUTPUT, top to bottom:
1. Title and a generated lede: "Viet Nam's overall PFM index is -0.11 (global
   rank 99 of 169). Strongest: [dimension] (+0.50); weakest: [dimension]
   (-0.38)."
2. "The budget cycle, coloured by the focus economy's score": three boxes in a
   cycle with curved arrows (budget preparation, budget execution,
   transparency, accountability and oversight) and a circle in the centre (budget
   reliability and perceived effectiveness). Each shows the z-score, global
   rank and ASEAN-4 average, and is filled on the diverging scale. Clicking one
   opens its sub-dimensions in the table below.
3. Five tiles: the four dimensions and the overall index, each with the
   ASEAN-4 average and global rank.
4. "Where the focus economy sits among all economies": one row per dimension
   and overall, every economy as a grey dot, the focus economy as a large blue
   dot, comparators as open circles, group averages as short vertical ticks.
   Names on hover.
5. "Scores by economy": a heatmap table, focus economy, comparators and group
   averages in rows; tabs for "Dimensions" and for each dimension's
   sub-dimensions.
6. "Underlying indicators": one table per dimension (tabs): indicator with
   source badge and a Details button (description, unit, source, link), its
   sub-dimension, a small bar for the focus economy's z-score, then the raw
   values of the focus economy, each comparator and the ASEAN-4 average.
7. "Coverage of the economies shown": indicators with data, dimensions scored,
   OBS round and PEFA year for each.
8. "Method and sources" in plain language.

CHECKS
The cycle box for budget preparation reads -0.38, rank 95/138, ASEAN-4 average
+0.16.
```

## stage-3 | pfm | 3 | Stage 3: the controls, with live re-scoring

```
TASK
Add a settings sidebar (on a phone, a sticky switcher between Benchmark,
Predicted scores and Settings). Every change re-runs the engine and redraws.

OUTPUT
- Comparison set: focus economy (dropdown); comparator economies as removable
  chips with an "add economy" box (name or ISO3, up to 20); group checkboxes
  (ASEAN-4, upper-middle income, high income, lower-middle income, East Asia and
  Pacific, ASEAN, selected economies) with their member counts.
- "Joint PEFA and OBS sample": restandardise and rank only within the economies
  that have both a PEFA assessment and an Open Budget Survey.
- Indicators: every indicator with a checkbox, grouped by dimension and
  sub-dimension, with presets "Workbook set", "Without PEFA", "Without OBS".
- Thresholds: share of sub-dimensions needed, minimum dimensions, z-score cap,
  minimum economies per indicator.
- "Download data (CSV)" of the current scores, and "Reset to workbook
  settings".

CHECKS
1. Changing the comparison set never changes a score, only what is shown.
2. The joint sample has 65 economies.
3. Switching off all PEFA indicators changes Viet Nam's D1; switching them back
   on restores -0.38.
```

## stage-4 | pfm | 4 | Stage 4: predicted PFM scores

```
CONTEXT
Richer countries tend to score higher. A fair question is whether Viet Nam
scores above or below what its income predicts.

TASK
Add a second view, "Predicted PFM scores".

OUTPUT
- For the overall index and every dimension and sub-dimension: a scatter of the
  score against GDP per capita 2025 on a log scale, all economies as grey
  dots, the focus economy highlighted, the line from an OLS regression of the
  score on ln(GDP per capita) over all economies with both, and the
  upper-middle-income average plotted at its members' geometric-mean GDP per
  capita.
- For each: the focus economy's difference to its predicted score, and the
  slope on ln GDP per capita with its standard error and significance stars.
- The budget-cycle diagram again, now coloured by the difference to the
  predicted score.
- A toggle for PEFA-only and OBS-only versions (keep only those indicators and
  standardise over the economies each source covers).
- Everything follows the indicator selection and focus economy set in the
  sidebar.

CHECKS
Overall index: 169 economies, slope 0.214, Viet Nam predicted -0.07, difference
-0.04. Budget preparation (D1): slope 0.295, difference -0.37. Budget execution
(D2): difference +0.39.
```
