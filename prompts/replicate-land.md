# Replicate the Vietnam Land Brief from the data files

Target: <https://sachadray.github.io/vietnam-land/>, three panels with no long scroll.
Input: the land pack only (`land_national.csv`, `land_provinces.csv`, `land_finance.csv`,
`vn_provinces.geojson`).

**How to use these prompts.** A dashboard this size is too much for one prompt: you cannot check it. Build it
in stages, and check each stage against a number you already know before moving on. Paste the setup prompt
once, then one stage at a time. In Claude Code, put the four data files in a folder, open the folder, and
paste. In a chat assistant, attach the files with the setup prompt.

## setup | land | 0 | Setup: paste once, first

```
ROLE
You are a senior economist and front-end developer. You build policy
dashboards as a single self-contained HTML file: no external libraries (Google
Fonts allowed), the data embedded in the file, every chart drawn as inline SVG.

CONTEXT
Viet Nam's state owns all land and sells the right to use it, usually when
farmland is reclassified for housing, industry or roads. In 2025 land revenue
reached 575.5 trillion dong, 21.7% of state revenue and 4.48% of GDP, and
provinces keep it for capital spending. A hectare can be charged for only once.
The readers are Ministry of Finance and provincial officials, and economists.
They want three things: what the country's land is made of, which provinces are
closest to running out of farmland they can convert, and what the revenue
arithmetic implies.

TASK
Build "Vietnam Land Brief": three panels switched by tabs at the top right,
with no long scroll: 01 What the land is, 02 Land at risk, 03 Scenarios. We will
build it in four stages. After each stage, stop, show me the result and the
checks, and wait for me.

DATA (attached)
- land_national.csv: national land area by category, thousand ha, 2008-2023
  (no 2010 or 2019). The 2011 and 2020 jumps are reclassifications.
- land_provinces.csv: 63 provinces x 5 categories (total, agri = agricultural
  production land, forest, special = specially used, homestead), thousand ha,
  2018, 2020-2023. Da Nang's specially used land has a definitional break in
  2022: exclude Da Nang from every change measure.
- land_finance.csv: land revenue, state revenue, GDP 2025 (12,847.6 trillion
  dong, real growth 8.02%), the rice-land floor (3,500 thousand ha) and the 2030
  plan targets for non-agricultural land (4,896.48 original, 5,840.14 revised).
- vn_provinces.geojson: province boundaries, joined on iso.

OUTPUT (style for every stage)
IBM Plex Serif for titles, IBM Plex Sans for text, IBM Plex Mono for numbers and
small capitals labels. Pale green-grey page, white cards with hairline borders.
Blue for agricultural land, orange for built land, grey for unused. Each panel
opens with a two-sentence lede with the key numbers in bold. Every chart has a
"Reading it" line underneath. Sources at the bottom of each panel.

CHECKS
Never invent a number. Every figure on the page must come from the files or
from a formula I give you.
```

## stage-1 | land | 1 | Stage 1: the numbers, before any chart

```
TASK
Compute and print these tables. No HTML yet.

1. National, 2023: total area (expect 33.13 million ha) and the shares of
   agricultural (84.4%), non-agricultural (12.0%) and unused land (3.5%; it was
   14.3% in 2008).
2. Change 2008 to 2023 by category, thousand ha: crop land (agri_production)
   +2,229; forest +649; specially used +468; homestead +150; unused -3,560.
3. For every province:
   - conversion rate = (homestead + special in 2023 - same in 2018) / 5
   - protected share = 3,500 / national agri_production in 2023 (expect 30.05%)
   - years left (runway) = agri 2023 x (1 - protected share) / conversion rate
   - expansion rate = conversion rate / (homestead + special in 2018), % a year
   - non-farm share = (homestead + special) / total, 2023, %
   - farmland share = agri / total, 2023, %
   - most exposed = above the median on both non-farm share and expansion rate
4. Risk tiers by runway: critical under 50 years, high 50-100, moderate
   100-200, ample over 200, no runway when it cannot be computed.

CHECKS
Expect 4 critical (Quang Ninh 22, Hai Phong 31, Bac Ninh 44, Hung Yen 49),
13 high, 19 moderate, 24 ample, and 3 with no runway (Da Nang excluded; Lai Chau
and Ca Mau show no net conversion). If any number differs, stop and explain.
```

## stage-2 | land | 2 | Stage 2: panel 01, What the land is

```
TASK
Build panel 01 from the stage 1 numbers.

OUTPUT
- Lede: "Viet Nam has 33.1 million hectares. Five-sixths of it is farmed or
  forested, an eighth is built on, and the slice that was once spare has nearly
  vanished: unused land fell from 14.3% of the country in 2008 to 3.5% in 2023."
- Four tiles: total land area; agricultural 84.4%; non-agricultural 12.0%
  (with the change since 2008); unused 3.5% (was 14.3% in 2008).
- A donut of the 2023 inventory (agricultural, non-agricultural, unused) with
  the total in the centre and a legend giving the hectares.
- A stacked area chart of the composition 2008-2023 (crop land, forest land,
  other agricultural, non-agricultural, unused). The years are unevenly spaced:
  draw the x-axis to scale, and mark the 2015 and 2020 inventories with dashed
  lines and a note that those steps are definitional.
- A line chart of built (non-agricultural) land against the 2030 plan: the
  actual series, the original target 4,896 and the revised target 5,840 as
  dashed lines, and an annotation comparing the actual pace with the pace
  needed to reach 5,840 by 2030.
- Horizontal diverging bars: "Where the 15 years went", change 2008-2023 by
  category, unused land in red.

CHECKS
The needed pace should be about 265 thousand ha a year ((5,840 - 3,985) / 7).
```

## stage-3 | land | 3 | Stage 3: panel 02, Land at risk

```
TASK
Build panel 02: which provinces are closest to running out of convertible
farmland.

OUTPUT
- Lede: depletion is a provincial problem, not a national one; four provinces
  run out inside 50 years.
- Left column, "Map series": six thumbnail maps (Depletion risk, Years of
  farmland left, Expansion rate, Non-farm share, Farmland share, Most exposed).
  Clicking one shows it in the main map.
- Middle: the main map. Depletion risk uses the four tier colours (red,
  orange, yellow, green) plus light grey for no runway, with a legend that
  counts the provinces in each tier. The continuous measures use six quantile
  bins of one hue. "Most exposed" highlights the provinces above both medians.
- Right: "Shortest runway first": a thin stacked bar of the tier shares, then
  every province ranked by runway as a thin bar with its value. Hovering a
  province highlights it on the map and in the list; clicking pins it.
- Notes: "How the runway is built" (the formula in words, and that it is a pace
  indicator, not a forecast) and "Withheld" (Da Nang, Lai Chau, Ca Mau, and that
  these are the 63 provinces before the 2025 merger). Boundaries: Natural Earth.

CHECKS
Hover Quang Ninh: 22 years, critical. The legend counts must read 4, 13, 19,
24, 3.
```

## stage-4 | land | 4 | Stage 4: panel 03, Scenarios

```
CONTEXT
Land revenue is an identity: R(t) = D(t) x p(t), revenue equals hectares
converted times the price each fetches. Fix any two and the third follows.

TASK
Build panel 03 with three scenarios as tabs. Use these definitions exactly:
- K = convertible stock = farmland x (1 - protected share); S(t) = what is left
- R0 = 575.5 trillion dong (2025); D0 = R0 / p0; gamma = real GDP growth 8.02%
- Scenario 1, revenue target: R(t) = R0 (1+g)^t; p(t) = p0; D(t) = R(t) / p0
- Scenario 2, conversion quota: D(t) = Q; p(t) = p0; R(t) = Q x p0
- Scenario 3, revenue target with price adjusting:
  p(t) = p0 (D(t)/D0)^(-1/e) (1+gamma)^t (K/S(t))^theta, which gives
  D(t) = [ R(t) / (p0 D0^(1/e) (1+gamma)^t (K/S(t))^theta) ]^(e/(e-1))
- In every scenario D(t) cannot exceed S(t); when land runs out, revenue is the
  residual D x p. Horizon: 100 years from 2025.
- Revenue as % of GDP uses GDP 2025 = 12,847.6 trillion growing at gamma.

OUTPUT
- Left: the equation box for the active scenario, then sliders: revenue growth
  (-4 to 16% a year, default 8), price per hectare in the first year (3 to 60
  billion dong, default 32.5), conversion quota (2 to 120 thousand ha a year,
  default 17.8), price elasticity e (1.2 to 4, default 2), scarcity premium
  theta (0 to 1.5, default 0.5), protected farmland (0 to 70%, default 30), and
  "Apply the test to": Viet Nam or one province (a province's revenue is the
  national figure times its share of national conversion). Grey out the
  sliders the active scenario does not use.
- Right: a chain of four numbers (ha converted 2025, ha converted 2045,
  revenue % of GDP in 2045, years to the floor), one sentence reading the
  result, four small charts (convertible farmland left, converted each year,
  price per hectare, revenue % of GDP with the 2025 level dashed) and a table
  "All three at these settings".

CHECKS
At the defaults, nationally: scenario 1 converts 17.7k ha in 2025 and 82.5k ha
in 2045, revenue 4.46% of GDP in 2045, 48 years to the floor. Scenario 2:
17.8k ha in 2045, 0.96% of GDP, more than 100 years. Scenario 3: 16.8k ha,
4.46% of GDP, more than 100 years.
```

## stage-5 | land | 5 | Stage 5: finish and review

```
TASK
Review the whole page as a sceptical reader would.

OUTPUT
1. Make it work on a phone: the tabs stay visible and the panels stack.
2. Make the tabs work with the keyboard.
3. List every number on the page with the file and formula it comes from, and
   flag any that you cannot trace.
4. Tell me the three weakest points of the argument the page makes, in one
   sentence each.
```
