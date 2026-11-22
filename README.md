# THE WORLD TODAY — Saturday 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/jehan771/entry-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/jehan771/entry-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One front page summing up the world's news of Saturday 21 November 2026:
23 verified stories across 7 regions, each with its source printed below it.

- **Lead:** Saudi air defences intercept three Houthi ballistic missiles
  over Riyadh in the early hours of Saturday — Reuters, 21 Nov 2026.
- **Peru:** magnitude 6.7–6.8 earthquake in central Peru, 00:09 UTC,
  felt in Lima; no casualties reported — Reuters / AFP / USGS.
- **Climate:** COP31 in Antalya runs into overtime with no deal; the draft
  drops fossil fuels and a $120bn adaptation fund — Reuters.
- **Ukraine:** Russia's huge overnight barrage kills nine and hits three
  Kyiv bridges; two Russian missiles land in Poland — BBC / AP / Reuters.
- **Space:** ESA–JAXA's BepiColombo enters orbit around Mercury — ESA.

Every story was verified against Reuters, AP, BBC, Al Jazeera, AFP, ESA,
UKMTO, IMD or PIB. Photos are file photos (Wikimedia Commons / NASA),
captioned as such on the page.

## How it is built

`render.py` (Python 3, Pillow, standard library + Pillow only) draws the
2048×2048 front page from the story list and `photos/`, then downscales
it to the 1024×1024 `entry.png`. `main.ts` (Node 22, standard library
only) copies `entry.png` to the output directory, byte for byte, so the
program is deterministic: every run writes identical bytes.

Run locally:

```sh
python3 render.py entry-2048.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see `LICENSE`.
