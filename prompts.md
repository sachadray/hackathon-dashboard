# Prompts

Copy, paste, adapt. They work in any AI assistant that can read a file and
produce an HTML page.

A good prompt is a brief with five parts:

| Part | What it tells the tool |
|---|---|
| **Reader** | Who will look at the page, and how much time they have |
| **Decision** | What they have to decide |
| **Data** | What you are giving it, and to check it before using it |
| **Design** | What goes on the screen |
| **Proof** | Source, date and method, so every number can be traced |

## The four prompts for the exercise

Use them in this order. Most people start at the third one. The first, second
and fourth are where you add value.

### 1. Explore

```
I am attaching district_jobs_toy.csv: one row per district per month for a
province with ten districts.

Profile the file before doing anything else:
- number of rows and columns, date range, list of districts
- missing values, duplicated rows, values that look impossible
- names that are spelled in more than one way

List every problem you find, with the row. Do not fix anything yet and do not
build any chart.
```

### 2. Frame

```
The province has budget to open two youth training centres. It must choose two
of the ten districts.

Using only the columns in this file:
- propose three different ways to define "a good district for a training centre"
- for each, say which columns you would use and what the definition ignores
- tell me what data is missing that a real decision would need

Do not rank the districts yet.
```

### 3. Build

```
Build a one-screen dashboard as a single self-contained HTML file.

Reader: the provincial director in charge of the decision. They have two
minutes and will read the page on a laptop.

Decision: which two of the ten districts get a youth training centre.

Data: the attached CSV. First apply these cleaning steps and tell me what you
changed: [paste the fixes you agreed in step 1].

Criteria: a district is a good choice when [paste the definition you chose in
step 2]. Use the average of the last three months.

Design:
- a headline sentence at the top that states the recommendation
- three key numbers for the province
- one chart that shows why the two districts were chosen
- one trend chart with a district selector
- a table of all ten districts so the reader can check
- no more than two colours: one for the recommended districts, grey for the rest
- no dual axes, no pie charts, no 3D

Proof: under the charts, state the source, the date range, the formula for each
number, and the cleaning steps.
```

### 4. Challenge

```
Act as a sceptical adviser to the director.

- Which three numbers on this dashboard would you check first, and how?
- Show me the calculation behind the headline, step by step, for one district.
- What is the strongest argument for choosing two different districts?
- What does this dashboard not show that the director should ask about?
```

## A real example: years of farmland left in Viet Nam

This is the brief behind `docs/land.html`.

```
Build a one-screen dashboard as a single self-contained HTML file.

Reader: a provincial finance director in Viet Nam whose province pays for
public investment with revenue from converting farmland to housing and industry.

Decision: how many years this can continue at the current pace, and which
provinces must change course first.

Data: two attached files.
- gso_provinces.json: land area by province and category (agricultural,
  homestead, specially used), thousand hectares, 2018 to 2023, from the
  National Statistics Office.
- vn_provinces.geojson: province boundaries, keyed by ISO code.
Before computing anything, look for breaks in the series and implausible
values, and tell me what you find.

Method: years left = farmland in 2023 x (1 - protected share) / annual
conversion. Annual conversion is the average yearly increase in homestead plus
specially used land between 2018 and 2023.

Design:
- a headline sentence that counts the provinces below an alert threshold and
  names the one that runs out first
- a province map shaded by years left, one colour from light to dark, darker
  meaning sooner; hovering shows the province and its number
- a ranking of the ten provinces that run out first
- three sliders: pace of conversion (0.5x to 4x), share of farmland protected
  (0 to 70 percent, default 30), alert threshold in years
- preset buttons for "current pace", "twice as fast" and "protect half"
- everything updates when a slider moves

Proof: state the formula under the charts. Name every province you excluded
and why. Give the source.
```

Follow-up prompts that improve the first result:

```
The map is hard to read. Use five bins with round thresholds (25, 50, 100, 200
years) and add a legend.
```

```
Some provinces show negative or infinite years. Explain why, then show them in
grey as "not converting" and exclude them from the ranking.
```

```
Recompute the number for Quang Ninh by hand and show each step, so I can check
it against the source table.
```

## Prompts that work for any dataset

```
Here is my dataset. Before any analysis, ask me the five questions you most
need answered to build something useful for a decision-maker.
```

```
Write the headline of this dashboard as one sentence that a busy reader could
act on. Give me three versions, from cautious to bold, and tell me what
evidence each one would need.
```

```
Here is my dashboard. Remove everything that does not help the reader make the
decision. Tell me what you removed and why.
```
