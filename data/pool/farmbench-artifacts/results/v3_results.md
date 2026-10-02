# FarmBench v3 run (26 Sep 2026, task version 3, 16 models) — saved from the collector output before v4 overwrote results/

| model | score | sanity (3) | exact (5) | sim (7) | flags pool / SE / fib / refill |
|---|---|---|---|---|---|
| gemini-3.7-flash | 0.902 | 1.00 | 0.94 | 0.83 | 8 / 1 / 3 / 11 |
| glm-5 | 0.897 | 1.00 | 0.80 | 0.92 | 10 / 1 / 2 / 7 |
| gemma-4-31b-it | 0.860 | 1.00 | 0.99 | 0.71 | 6 / 2 / 1 / 6 |
| gemini-2.5-flash | 0.788 | 1.00 | 0.87 | 0.64 | 4 / 1 / 2 / 6 |
| gpt-5.5-2026-04-23 | 0.743 | 1.00 | 1.00 | 0.45 | 7 / 1 / 3 / 6 |
| grok-4.20-0309-reasoning | 0.727 | 1.00 | 1.00 | 0.42 | 9 / 1 / 5 / 8 |
| gemini-2.5-pro | 0.720 | 1.00 | 0.83 | 0.52 | 9 / 1 / 1 / 5 |
| claude-opus-4-8-default | 0.704 | 0.56 | 0.73 | 0.75 | 9 / 1 / 4 / 6 |
| claude-sonnet-4-5-20250929 | 0.694 | 0.44 | 0.77 | 0.75 | 8 / 1 / 2 / 7 |
| gpt-oss-120b | 0.675 | 1.00 | 0.66 | 0.54 | 3 / 1 / 2 / 1 |
| gpt-oss-20b | 0.607 | 0.67 | 0.68 | 0.53 | 6 / 1 / 3 / 4 |
| gemini-3.1-flash-lite-preview | 0.549 | 0.56 | 0.54 | 0.56 | 5 / 0 / 1 / 6 |
| gpt-5.4-mini-2026-03-17 | 0.521 | 0.50 | 0.57 | 0.49 | 5 / 1 / 1 / 4 |
| gpt-5.4-nano-2026-03-17 | 0.440 | 0.11 | 0.35 | 0.64 | 8 / 1 / 2 / 7 |
| claude-haiku-4-5-20251001 | 0.368 | 0.22 | 0.47 | 0.36 | 11 / 1 / 2 / 5 |
| deepseek-r1-0528 | 0.000 | 0.00 | 0.00 | 0.00 | 0 / 0 / 0 / 0 (all ResponseParsingError / 429) |

Per-task scores (columns in the order of the table above, DeepSeek last):

| task | g3.7f | glm5 | gemma | g2.5f | gpt5.5 | grok | g2.5p | opus | sonnet | oss120 | oss20 | g3.1lite | 5.4mini | 5.4nano | haiku | dsr1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hire_math | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 0.00 | 0.00 |
| feed_or_lose | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| fertilizer_melon | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 0.33 | 1.00 | 1.00 | 0.67 | 1.00 | 0.33 | 0.67 | 0.00 |
| melon_dump | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| melon_race_timing | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| wool_lot | 0.72 | 1.00 | 1.00 | 0.56 | 1.00 | 1.00 | 1.00 | 0.65 | 0.56 | 1.00 | 0.38 | 0.38 | 0.56 | 0.44 | 0.56 | 0.00 |
| milk_front_run | 0.97 | 0.00 | 0.97 | 0.81 | 1.00 | 1.00 | 0.97 | 0.00 | 0.31 | 0.31 | 0.00 | 0.31 | 0.31 | 0.00 | 0.64 | 0.00 |
| crop_choice | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.16 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 0.16 | 0.00 |
| opening | 1.00 | 1.00 | 0.00 | 0.00 | 0.16 | 0.00 | 0.00 | 0.00 | 0.16 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| sheep_yarn | 1.00 | 0.78 | 1.00 | 1.00 | 1.00 | 0.92 | 0.00 | 0.40 | 0.78 | 0.92 | 0.00 | 0.00 | 0.78 | 0.78 | 0.78 | 0.00 |
| sheep_no_yarn | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| se_quadrant | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| max_hands | 0.89 | 0.72 | 0.99 | 0.72 | 0.99 | 0.99 | 0.89 | 0.89 | 0.33 | 0.89 | 0.72 | 0.89 | 0.72 | 0.72 | 0.72 | 0.00 |
| terminal_tomato | 0.95 | 0.95 | 0.95 | 0.95 | 0.00 | 0.00 | 1.00 | 0.95 | 0.95 | 0.00 | 1.00 | 0.00 | 0.95 | 1.00 | 0.00 | 0.00 |
| terminal_carrot | 1.00 | 1.00 | 1.00 | 0.78 | 0.00 | 0.00 | 0.78 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |

Choices (same column order):

| task | g3.7f | glm5 | gemma | g2.5f | gpt5.5 | grok | g2.5p | opus | sonnet | oss120 | oss20 | g3.1lite | 5.4mini | 5.4nano | haiku |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hire_math (hands, $) | 1,8 | 1,8 | 1,8 | 1,8 | 1,8 | 1,8 | 1,8 | 4,48 | 2,21 | 1,8 | 2 | 4 | 4 | 4 | 2 |
| feed_or_lose | ABC | ABC | ABC | ABC | ABC | ABC | ABC | ABC | ABC | ABC | ABC | ABC | ABC | CDE | CDE |
| melon_dump | 72 | 72 | 72 | 72 | 71 | 72 | 72 | 72 | 72 | 0 | 72 | 0 | 72 | 72 | 72 |
| melon_race_timing | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 10 | 10 | 10 |
| wool_lot (day 27 first) | 4,13,13 | 0,0,30 | 0,0,30 | 10,10,10 | 0,0,30 | 0,0,30 | 0,0,30 | 8,9,13 | 10,10,10 | 0,0,30 | 13,13,4 | 13,.. | 10,10,10 | 12,.. | 10,10,10 |
| milk_front_run (hour 0) | 24 | none | 24 | 8 | 21 | 20 | 24 | 2/h | 4/h | 4/h | 1/h | 4/h | 4/h | 1/h | 6 |
| crop_choice | STRAW | STRAW | STRAW | STRAW | STRAW | STRAW | WHEAT | STRAW | STRAW | STRAW | STRAW | STRAW | STRAW | TOMATO | WHEAT |
| opening | goose | goose | meta_a | straw_rush | default | meta_a | cautious | meta_a | default | melon_max | goose | goose | cautious | meta_a | melon_max |
| sheep_yarn | 8 | 4 | 8 | 8 | 8 | 6 | 0 | 2 | 4 | 6 | 0 | 0 | 4 | 4 | 4 |
| sheep_no_yarn | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| se_quadrant | d12 | never | d12 | d12 | d12 | d12 | d12 | never | never | d12 | d12 | never | d12 | d16 | d16 |
| max_hands | 8 | 6 | 10 | 6 | 10 | 10 | 8 | 8 | 4 | 8 | 6 | 8 | 6 | 6 | 6 |
| terminal_tomato | d16 | d16 | d16 | d16 | none | off | d18 | d16 | d16 | off | d18 | off | d16 | d18 | off |
| terminal_carrot | d24 | d24 | d24 | d25 | d26 | d26 | d25 | d24 | d24 | d24 | d24 | off | d27 | d24 | off |

Counts (15 models with a completed run): hire_math correct 8; feed 12; fertilizer all-three 10; melon_dump sell-all 13;
race day 9: 12; wool hold-to-end 6; milk hour-0 dump 5, drip 7; crop strawberry 12; opening goose 4 / meta_a 4;
sheep_yarn 4–8: 11, zero: 3; sheep_no_yarn zero: 14; SE never: 4, buy: 11; max_hands 6: 6, 8: 5, 10: 3, 4: 1;
tomato d16/d18: 10, off/none: 5; carrot d24/25: 10.
