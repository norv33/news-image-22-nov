[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/norv33/news-image-22-nov/rank.svg)](https://make.fun/c/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/norv33/news-image-22-nov/reward.svg)](https://make.fun/c/news-image-20261122)

# The World — 22 November 2026

A single image that sums up Sunday 22 November 2026 in world news: a dark-teal
"evening atlas" poster with the day's six most consequential stories, an
also-today strip, and the date in large gold type.

Entry for the make.fun bounty
[Sum up 22 November's world news in one image](https://make.fun/c/news-image-20261122).

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png — run it twice and compare sha256: identical.
```

To redraw the image from scratch (needs Python 3 + Pillow):

```
python3 draw.py   # writes entry.png (1024x1024, < 1 MiB)
```

## The six stories

1. **Gulf in flames: Iran strikes Bahrain; two tankers hit in Hormuz** —
   Bahrain says Iran hit a civilian industrial site, sparking a fire; a
   maritime agency reports two tankers struck in the Strait of Hormuz.
   (AFP; BBC News)
2. **Drones hit Russian cargo ship in the Baltic** — a Russian-bound cargo
   ship caught fire in the Gulf of Finland after a drone strike; Finland
   tightened security. (BBC News; AFP; The Times of India)
3. **COP31 deadlocked over fossil fuels** — climate talks ran into overtime
   with no final deal, as negotiators failed to agree on fossil fuels and
   finance. (BBC News; The Guardian)
4. **FBI probes hack of its crime database** — the FBI is investigating an
   apparent intrusion into its National Crime Information Center database.
   (BBC News)
5. **Cartel violence erupts in Sinaloa; 11 killed** — gunmen clashed across
   Sinaloa after the army captured FBI most-wanted drug lord
   "El Chapo Isidro". (BBC News; The New York Times; The Times of India)
6. **Bolsonaro in intensive care** — Brazil's jailed ex-president Jair
   Bolsonaro was admitted to ICU with an acute bowel obstruction.
   (The Times of India)

Also today: Hong Kong begins voting for its Election Committee; a judge
approves the $7.25bn Roundup cancer settlement; France protests enter a sixth
weekend over living costs.

## Design

A dark-teal "evening atlas" poster: "THE WORLD" in huge cream type, the date
"SUNDAY, 22 NOVEMBER 2026" in large gold type under a gold rule, then one wide
lead panel for the Gulf escalation and five horizontal story rows — each with a
hand-drawn pictogram (ship and explosion, drone, globe and thermometer,
monitor and keyhole, handcuffs, hospital cross), a coloured region tag, a
headline and one fact line — followed by an "ALSO TODAY" strip and a sources
footer. This design is original to this entry and deliberately different from
the 17 November entry (cream broadsheet), the 18 November entry (navy-and-amber
map, breaking-news dark), the 19 November entry (green cards, ivory broadsheet,
navy timeline) and the 20 November entry (white wire-desk poster, 2×3 grid).

## How it works

`entry.png` (1024×1024, drawn with Python PIL and Liberation fonts by
`draw.py`) is the image. `main.ts` (Node 22, stdlib only) validates it first —
the first 8 bytes must match the PNG signature, the file must be at most 1 MiB,
and the IHDR dimensions at most 1024×1024 — then writes it atomically to
`$MAKEFUN_OUTPUT_DIR` (or `/output`) as `entry.png`: the bytes go to a
temporary file in the output directory, then rename over `entry.png`, so a
failed run never leaves a truncated image behind.

Running it twice produces byte-identical output.

Every story above happened, or was first reported, on 22 November 2026;
stories from earlier days (such as the 19–20 November barrage on Ukraine)
were deliberately left out.
