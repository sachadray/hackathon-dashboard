# Hands-on prompts (15 minutes)

<!-- Each "## " heading below is one prompt. The build script turns this file into
     the copy-paste cards on handout.html and prompts.html. Keep the format:
     "## id | track | step | title", then the prompt text in a fenced block. -->

## template | all | 0 | The six parts of a good prompt

```
ROLE
Who should the AI be? Name a job, not a personality.
"You are a public finance economist who builds dashboards for ministry officials."

CONTEXT
What does it need to know that is not in the data? Who is the reader, what do
they already know, why does it matter now?

TASK
The one thing to produce, and the question or decision it serves.

DATA
Which files, what one row means, the units, the known problems, and any formula
it must use.

OUTPUT
The format (one HTML file, a table, 200 words) and exactly what goes on the screen.

QUALITY CHECKS
How to test the data before trusting it: do the parts add up to the totals?
Which assumptions did it make, and do they reproduce a value you already know
(calibration)? Where do two datasets disagree?
```

## land-1 | land | 1 | Explore the files (2 min)

```
ROLE
You are a careful data analyst.

CONTEXT
I am a student preparing a dashboard on land use in Viet Nam for a provincial
finance director. I have not looked at these files yet.

TASK
Before building anything, help me understand the attached files.

DATA
land_provinces.csv and vn_provinces.geojson (attached).

OUTPUT
For each file: what one row (or feature) represents, the columns and units, the
years covered, the number of missing values, and anything that looks wrong.
Then suggest three questions a decision-maker could answer with these files.
No charts yet. Under 250 words.

CHECKS
Tell me which column in the CSV matches the map, and whether every province in
the CSV has a shape in the map.
```

## land-2 | land | 2 | Build the dashboard (6 min)

```
ROLE
You are a data analyst and web developer who builds clear, one-screen
dashboards for government officials.

CONTEXT
Provinces in Viet Nam raise much of their own revenue by converting farmland
into housing, industry and roads. Each hectare can be converted only once, and
about 30% of farmland (the national rice-land floor) is protected by law. The
reader is a provincial finance director with two minutes, who wants to know how
long this source of revenue can last.

TASK
Build a dashboard that answers: "Which provinces will run out of convertible
farmland first, and how sensitive is that to the pace of conversion?"

DATA
- land_provinces.csv: land area by province and category, thousand hectares,
  2018 to 2023. Categories: agri (agricultural production land), special
  (specially used land), homestead (residential land), forest, total.
- vn_provinces.geojson: province boundaries, joined to the CSV on the column iso.
Method:
- conversion per year = (homestead + special in 2023 - homestead + special in 2018) / 5
- protected share = 30%
- years left = agri in 2023 x (1 - protected share) / conversion per year
Leave out Da Nang (break in its data). Provinces with no positive conversion
are "not converting".

OUTPUT
One self-contained HTML file with no external libraries, on one screen:
1. A headline sentence at the top that states the answer with numbers.
2. A map of the provinces coloured by years left, in four risk bands: under 50,
   50 to 100, 100 to 200, over 200 years; grey for no data. Hovering shows the
   province and its value.
3. A bar chart of the 10 provinces with the fewest years left.
4. Two sliders: pace of conversion (0.5x to 3x the recent pace) and protected
   share (0% to 70%). The headline, map and chart update as they move.
5. A footnote with the method and the source (National Statistics Office of
   Viet Nam).

QUALITY CHECKS
Before the dashboard:
1. Check that agri + forest + special + homestead never exceed total for any
   province, and report any province where they do.
2. State the assumptions you used (the 30% protected share, the 2018-2023
   pace) and calibrate: print the five provinces with the fewest years left.
   Quang Ninh should be about 22 years. If yours differs, explain why.
3. Flag inconsistencies: Da Nang's break, and any blank values.
```

## land-3 | land | 3 | Improve it: pick one (3 min)

```
Make the headline change with the sliders, and always state numbers in it.

Add one sentence under the title, "How to read it", for a reader who has never
seen this map.

Add a third slider, an alert threshold in years, and count the provinces under
it in the headline.

Remove anything that does not help the director decide. Tell me what you
removed and why.

Check that the colours can be told apart by a colour-blind reader and on a
projector. Fix them if not.
```

## land-4 | land | 4 | Check it (2 min)

```
Show me, step by step, how you computed the years left for Quang Ninh, starting
from its rows in land_provinces.csv. Then list two ways this dashboard could
mislead a reader, and fix the more serious one.
```

## pfm-1 | pfm | 1 | Explore the files (2 min)

```
ROLE
You are a careful data analyst.

CONTEXT
I am a student preparing a dashboard on public financial management (PFM): how
governments prepare, execute and report on their budgets. I have not looked at
these files yet.

TASK
Before building anything, help me understand the attached files.

DATA
scores.csv and economies.csv (attached).

OUTPUT
For each file: what one row represents, the columns and what they measure, the
number of economies, the missing values, and anything that looks unusual.
Explain in two sentences what a z-score is and how to read a score of -0.4.
Then suggest three questions a ministry could answer with these files.
No charts yet. Under 250 words.

CHECKS
Tell me how many economies have an overall score, and Viet Nam's (VNM) overall
score.
```

## pfm-2 | pfm | 2 | Build the dashboard (6 min)

```
ROLE
You are a public finance economist and data-visualisation designer.

CONTEXT
Viet Nam's Ministry of Finance wants to know where its public financial
management is strong or weak compared with its neighbours. The reader is a
senior official with two minutes. They know the budget process well but are not
statisticians.

TASK
Build a dashboard that answers: "How does Viet Nam compare with its neighbours,
and where is the biggest gap?"

DATA
- scores.csv: one row per economy (iso3). Columns D1 Budget preparation,
  D2 Budget execution, D3 Transparency, accountability and oversight,
  D4 Budget reliability and perceived effectiveness, and overall. All are
  z-scores: 0 is the average of all economies with data, +1 is one standard
  deviation above it, higher is better.
- economies.csv: economy names, income group and region.
Comparison set: Viet Nam (VNM) against Indonesia, Malaysia, the Philippines,
Thailand, Cambodia, Korea and Japan, plus two averages: ASEAN-4 (IDN, MYS, PHL,
THA) and upper-middle income. Leave Viet Nam out of both averages.

OUTPUT
One self-contained HTML file with no external libraries, on one screen:
1. A headline sentence: Viet Nam's overall score and global rank, its strongest
   and its weakest dimension.
2. Five tiles (D1 to D4 and overall): Viet Nam's score, the ASEAN-4 average and
   the global rank.
3. A dot plot with one row per dimension: every economy as a small grey dot,
   Viet Nam large and coloured, the seven comparators as open circles named on
   hover, the ASEAN-4 average as a short vertical tick.
4. A table of Viet Nam and the comparators by dimension, cells coloured from red
   (below 0) through white to green (above 0), values shown with their sign.
5. A dropdown to change the focus economy; everything updates.
6. A footnote explaining z-scores and naming the sources.

QUALITY CHECKS
Before the dashboard:
1. Check that overall equals the mean of D1, D2 and D3 for every economy, and
   that scores.csv and economies.csv list the same economies.
2. State the assumptions (z-scores; group averages leave out Viet Nam) and
   calibrate: print Viet Nam's five scores and its rank on the overall index,
   ranking only economies with a score. Expected: overall -0.11, rank 99 of
   169. If yours differs, explain why.
3. Flag economies with missing scores.
```

## pfm-3 | pfm | 3 | Improve it: pick one (3 min)

```
Make the headline name the single largest gap between Viet Nam and the ASEAN-4
average, in words a minister would use.

When the reader clicks a dimension, show its sub-dimension scores (columns
sp_1a to sp_4c in scores.csv; names are in config.json).

Add a toggle that replaces the seven comparators with all upper-middle-income
economies.

Remove anything that does not help the official decide. Tell me what you
removed and why.

Check that the red-green scale can be read by a colour-blind reader. If not,
switch to blue-orange and say so in the legend.
```

## pfm-4 | pfm | 4 | Check it (2 min)

```
Show me, step by step, how Viet Nam's overall score and rank were computed from
scores.csv. Then list two ways this dashboard could mislead a reader (for
example about what a z-score of 0 means), and fix the more serious one.
```
