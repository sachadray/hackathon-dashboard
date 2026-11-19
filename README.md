# From data to decision

Material for a 45-minute session on turning economic data into dashboards that help people decide, and on
using AI to build them. Prepared for undergraduate students at the VietLeap Hackathon (University of Economics
Ho Chi Minh City, November 2026).

**Slides:** <https://sachadray.github.io/hackathon-dashboard/>

## Hands-on exercises

Two 15-minute exercises, each built on the real data behind a published dashboard. Work in pairs with any AI
assistant that reads files ([claude.ai](https://claude.ai) works on the free plan).

**[Download both exercises: instructions, prompts and data (.zip)](https://sachadray.github.io/hackathon-dashboard/data/hands-on-exercises.zip)**
· or follow them online in the **[handout](https://sachadray.github.io/hackathon-dashboard/handout.html)**

| | Track A · Land | Track B · Public financial management |
|---|---|---|
| Question | Which provinces will run out of convertible farmland first? | How does Viet Nam compare with its neighbours, and where is the biggest gap? |
| Data | Land use for 63 provinces, 2018–2023, and a province map | Scores for 194 economies on four dimensions of the budget cycle |
| Files you need | `land_provinces.csv`, `vn_provinces.geojson` | `scores.csv`, `economies.csv` |
| Data only | [land_pack.zip](https://sachadray.github.io/hackathon-dashboard/data/land_pack.zip) · [README](docs/data/land/README.md) | [pfm_pack.zip](https://sachadray.github.io/hackathon-dashboard/data/pfm_pack.zip) · [README](docs/data/pfm/README.md) |
| Full dashboard | [Vietnam Land Brief](https://sachadray.github.io/vietnam-land/) | [Viet Nam PFM benchmark](https://sachadray.github.io/vietnam-pfm-benchmarking/) |
| 15-minute version | [example](https://sachadray.github.io/hackathon-dashboard/examples/land-15min.html) | [example](https://sachadray.github.io/hackathon-dashboard/examples/pfm-15min.html) |

## Prompts

All prompts follow six parts: role, context, task, data, output and quality checks. The
**[prompts page](https://sachadray.github.io/hackathon-dashboard/prompts.html)** has them ready to copy:

- the hands-on prompts for both tracks;
- staged prompts that rebuild each full dashboard from the data files alone, checking each stage against a known number;
- prompts for a first session in Claude Code.

The source of every prompt is in [`prompts/`](prompts/).

## Presenting the slides

Arrow keys to move, **S** for a presenter view with notes and timings, **F** for full screen, **T** to start the
15-minute timer. Slides 2 and 33 run live polls: students scan a QR code and the results update on screen.
Answers go through [ntfy.sh](https://ntfy.sh), a free public relay, are anonymous and are deleted after 12 hours
(save them with the button on the slide). To rehearse without touching the real poll, add `?topic=test1` to the
slides and poll URLs.

## Data sources

- **Land:** National Statistics Office of Viet Nam (land-use statistics); Natural Earth (province boundaries, public
  domain); Ministry of Finance, ISEAS, OECD and National Assembly Resolution 39/2021/QH15 for the fiscal figures.
- **PFM:** PEFA Secretariat, IBP Open Budget Survey, World Bank (GovTech Maturity Index, Worldwide Governance
  Indicators, Global Public Procurement Database, B-READY), IMF (World Economic Outlook, ISORA) and others; the
  source and link of each of the 85 indicators is in `indicators.csv`.

Each pack's README explains every column and the known problems in the data.

## Repository

```
docs/       the published site: slides, handout, prompts page, poll, examples and data
prompts/    the prompts, in markdown (the pages are built from these)
build/      scripts that build the data packs, the pages and the QR codes
```

To rebuild after editing a prompt: `python build/build_site.py`.
