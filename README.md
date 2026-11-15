# From data to decision

Material for a 45-minute session at the VietLeap Hackathon: how to turn economic
data into a dashboard that helps someone decide.

## The exercise (20 minutes, in pairs)

Song Xanh is a fictional province with ten districts. It has budget for **two
youth training centres**. Which two districts should get them?

1. Download [`data/district_jobs_toy.csv`](data/district_jobs_toy.csv).
2. Open [`prompts.md`](prompts.md) and any AI assistant you already use.
3. Follow the four steps.

| Minutes | Step | What you do |
|---|---|---|
| 3 | Explore | Profile the file. Find what is wrong with it. |
| 5 | Frame | Decide what makes a district a good choice. |
| 8 | Build | One screen with a recommendation. |
| 4 | Challenge | Swap with another pair. Try to break theirs. |

The data is synthetic and has errors planted in it on purpose.

### The columns

| Column | Meaning |
|---|---|
| `month` | Month, `YYYY-MM`, January 2024 to December 2025 |
| `district` | One of ten districts |
| `working_age_pop_thousand` | Residents aged 15 to 64, thousand |
| `youth_unemployment_pct` | Unemployment rate, ages 15 to 24, percent |
| `job_postings` | New job advertisements in the month |
| `median_wage_million_vnd` | Median monthly wage, million dong |
| `training_seats` | Places available in existing training programmes |
| `training_applicants` | People who applied for those places |

## What is in this repository

| Path | What it is |
|---|---|
| `data/district_jobs_toy.csv` | The toy dataset for the exercise |
| `data/make_toy_data.py` | The script that generates it, with a fixed seed |
| `prompts.md` | Prompts for each step, plus the brief behind a real dashboard |
| `docs/index.html` | A reference answer to the exercise. Look at it after you have built yours. |
| `docs/land.html` | A real example: years of convertible farmland left in each province of Viet Nam, with a map and scenario sliders |
| `instructor/notes.md` | Run-of-show and the planted errors. Spoilers. |

Both dashboards are single HTML files with no dependencies. Download one and
open it in a browser, or serve the `docs/` folder with GitHub Pages.

## Data and sources

The exercise data is invented. The province and its districts do not exist.

`docs/land.html` uses land-use statistics by province for 2018 to 2023 from the
National Statistics Office of Viet Nam. The method and the exclusions are stated
at the bottom of the page.
