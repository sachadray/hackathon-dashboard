# From data to decision

A 45-minute session for undergraduate students at the VietLeap Hackathon (UEH, November 2026): how to turn
economic data into dashboards that help people decide, and how to use AI to build them.

Everything is served from `docs/` by GitHub Pages:

| Page | Link | What it is |
|---|---|---|
| Slides | <https://sachadray.github.io/hackathon-dashboard/> | 34 slides in three parts, with speaker notes and live polls |
| Handout | <https://sachadray.github.io/hackathon-dashboard/handout.html> | What students open for the hands-on: data, five steps, prompts to copy |
| Prompts | <https://sachadray.github.io/hackathon-dashboard/prompts.html> | Every prompt: hands-on, staged rebuilds of both example dashboards, first Claude Code session |
| Poll | `poll.html?p=start` and `poll.html?p=end` | What students see when they scan the QR codes |

## The session

| Part | Minutes | Content |
|---|---|---|
| Opening | 3 | Live poll: use of AI, dashboards, GitHub |
| 1. Dashboard explainer | 12 | Why it matters, workflow and trilemma, a definition, the four questions, anatomy, two examples (Vietnam Land Brief, Viet Nam PFM benchmark), the six-part prompt, staged prompting |
| 2. Hands-on | 18 | In pairs, 15 minutes: build a dashboard from the data behind one of the two examples |
| 3. Uses of AI | 10 | What AI changes, GitHub and Claude Code for beginners, the hackathon checkpoints, responsible use, students' value proposition |
| Close | 2 | Open-ended live poll: what they learned, impressions |

## Presenting

Open the slides link in a browser.

| Key | Action |
|---|---|
| → Space / ← | Next / previous slide |
| a number, then Enter | Jump to that slide |
| F | Full screen |
| S | Presenter view in a new window: notes with timings, next slide, elapsed time. It stays in sync with the main window. |
| T | Start or pause the 15-minute hands-on timer (slide 21); the current step lights up |
| ? | Help |

Print from the browser (landscape, background graphics on) for a PDF with one slide per page.

### The live polls

Answers go through [ntfy.sh](https://ntfy.sh), a free public relay: no account, no server of our own. Students
scan the QR code on slide 2 or 33, answer on their phone, and the slide updates within a second or two.

- **Answers are deleted after 12 hours.** Press "Save answers (CSV)" on the poll slide before closing the browser.
- **Rehearse on a separate topic** so test answers never reach the real one: add `?topic=rehearsal-anything` to
  both the slides URL and the poll URL, for example `…/hackathon-dashboard/?topic=rehearsal-1` and
  `…/poll.html?p=start&topic=rehearsal-1`. The QR codes always point at the real topic.
- **The relay is public.** Anyone who knows the topic name can read or post. Answers are anonymous, every message is
  validated before it is counted, and text is shown as plain text. Click an open answer on slide 33 to hide it on
  your screen.
- Students on the same Wi-Fi share one rate limit at the relay (by default a burst of 60 requests, then one every
  five seconds). One submission is one request. If a large room submits in the same few seconds, some phones
  wait: the page retries automatically for about 15 seconds, then asks the student to press Send again.

## The data packs

`docs/data/land/` and `docs/data/pfm/`, each with a README that explains every column, plus a zip of each.

- **Land** (from [sachadray/vietnam-land](https://sachadray.github.io/vietnam-land/)): GSO land use by province
  2018–2023 and nationally 2008–2023, Natural Earth province boundaries (public domain), and published fiscal
  figures with their sources. **Left out on purpose:** the CEIC export and the real-estate credit and Savills price
  series derived from it, which are licensed.
- **PFM** (from [sachadray/vietnam-pfm-benchmarking](https://sachadray.github.io/vietnam-pfm-benchmarking/)): the
  processed tables behind the public dashboard (scores, economies, indicators, indicator values, config) and GDP per
  capita 2025. The public dashboard already embeds the same figures.

Checked: from these files alone, the land runway reproduces the brief exactly (4 / 13 / 19 / 24 provinces by
risk tier; Quang Ninh 22 years), and recomputing the PFM scores from `indicator_values.csv` reproduces
`scores.csv` to 1e-10 (Viet Nam −0.11, rank 99 of 169).

## Rebuilding

The pages are static files. Three scripts regenerate what they embed:

```bash
python build/make_data_packs.py --land ../vietnam-land --pfm ../vietnam-pfm-benchmarking   # data packs (needs both source repos)
python build/build_site.py      # embeds data in docs/examples/ and prompts in handout.html and prompts.html
python build/make_qr.py         # QR codes (pip install segno)
```

Prompts are written once, in `prompts/*.md`; `build_site.py` copies them into the handout and prompts pages.
Edit the markdown, never the copy in the HTML.

## Layout

```
docs/                 the published site
  index.html          slides (styles and engine in assets/deck.css, assets/deck.js)
  handout.html        student handout
  prompts.html        all prompts
  poll.html           poll form for students; ?view=results shows live results full-page
  examples/           what 15 minutes can produce, one per track
  data/               the two data packs and their zips
  assets/             css, js, QR codes, screenshots
prompts/              the prompts, in markdown (single source)
build/                scripts that build the packs, the pages and the QR codes
```

## Publishing

GitHub Pages serves this repository from the `docs/` folder: Settings → Pages → Deploy from a branch →
`main`, `/docs`. A Pages site is public even when the repository is private, so `docs/` holds only what students
may see.
