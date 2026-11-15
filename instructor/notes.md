# Instructor notes

Spoilers for the exercise. Students should not read this before the session.

## Run-of-show, 45 minutes

| Clock | Part |
|---|---|
| 0:00 to 17:00 | Slides 1 to 15: why it matters, workflow and trilemma, what AI changes, what a dashboard is, three examples, prompts |
| 17:00 to 37:00 | Hands-on, slides 16 and 17 |
| 37:00 to 45:00 | Slides 18 to 21: hackathon, responsible use, value proposition, close |

Per-slide timings are in the speaker notes of the deck.

## Before the session

- Check students can reach the repository and download the CSV. If the Wi-Fi is
  weak, bring the file on a USB stick or share it in the group chat.
- Open `docs/index.html` and `docs/land.html` in two browser tabs.
- Ask students to sit in pairs, one laptop per pair.

## Hands-on, minute by minute

**0 to 3, Explore.** Students run prompt 1. Ask the room what they found. There
are four planted problems:

| Problem | Where | Sensible fix |
|---|---|---|
| Duplicated row | Old Market, 2025-03 | Drop one copy |
| Decimal-point typo | Lakeside, 2024-11, youth unemployment above 100 percent | Divide by ten, or drop the value |
| Missing value | Greenbelt, 2025-07, `job_postings` is blank | Leave it out of the average, do not fill with zero |
| Inconsistent name | "Tech park" in three rows, "Tech Park" elsewhere | Harmonise the spelling |

Teaching point: an assistant asked to "make a dashboard" will often chart the
112 percent unemployment rate without comment, and may show eleven districts.
Asking it to profile first is what catches this.

**3 to 8, Frame.** Students run prompt 2 and choose a definition. Ask two pairs
to state theirs. Expect two camps:

- *Need only:* highest youth unemployment. Picks Uplands and Hillside.
- *Need and opportunity:* high unemployment, and jobs to train people for.
  Picks Harbour and Northfield.

Neither is wrong. They answer different questions, and the director has to say
which one they are asking. This is the data-method-question trilemma in small.

**8 to 16, Build.** Students run prompt 3 with their own cleaning steps and
criteria. Walk around. The common problems: no headline sentence, too many
charts, a dual axis, colours without meaning.

**16 to 20, Challenge.** Pairs swap laptops. Each asks the other: what is your
recommendation, and which number should I check first? Then show
`docs/index.html`.

## The reference answer

The reference dashboard recommends **Harbour and Northfield**: the only two
districts above the provincial median on all three tests, using the average of
the last three months.

| Test | Measure |
|---|---|
| Need | Youth unemployment |
| Opportunity | Job postings per 1,000 working-age residents |
| Demand for training | Applicants per training seat |

Uplands and Hillside have the highest unemployment but few vacancies, and their
existing training seats are not full. A centre there may still be the right
choice if the goal is equity. Let students argue it.

## Regenerating the data

```bash
python data/make_toy_data.py
```

The script uses a fixed seed, rewrites the CSV, injects the clean data into
`docs/index.html`, and fails if the intended answer no longer holds.
