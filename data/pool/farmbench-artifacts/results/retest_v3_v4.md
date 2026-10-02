# Test-retest: v3 run vs v4 run (same prompts for these 10 tasks, temperature 0, ~20 min apart)

| model | same choice | changed |
|---|---|---|
| gemini-3.7-flash | 9/10 | terminal_carrot:plant_day24->plant_day26 |
| glm-5 | 3/5 | melon_dump:72->71; se_quadrant:never->buy_day12 |
| gemma-4-31b-it | 9/10 | opening:meta_a->default |
| gemini-2.5-flash | 6/10 | crop_choice:STRAWBERRY->WHEAT; opening:strawberry_rush->goose_farm; max_hands:hands_6->hands_8; terminal_carrot:plant_day25->off |
| gpt-5.5-2026-04-23 | 7/8 | terminal_carrot:plant_day26->plant_day27 |
| grok-4.20-0309-reasoning | 6/7 | sheep_yarn:sheep_6->sheep_4 |
| gemini-2.5-pro | 8/10 | terminal_tomato:plant_day18->plant_day16; terminal_carrot:plant_day25->plant_day24 |
| claude-opus-4-8-default | 10/10 |  |
| claude-sonnet-4-5-20250929 | 7/10 | melon_dump:72->0; sheep_yarn:sheep_4->sheep_6; max_hands:hands_4->hands_10 |
| gpt-oss-120b | 0/1 | terminal_tomato:off->plant_day16 |
| gpt-oss-20b | 6/10 | opening:goose_farm->meta_a; sheep_no_yarn:sheep_8->sheep_0; max_hands:hands_6->hands_4; terminal_tomato:plant_day18->plant_day16 |
| gemini-3.1-flash-lite-preview | 9/10 | opening:goose_farm->melon_max |
| gpt-5.4-mini-2026-03-17 | 3/10 | crop_choice:STRAWBERRY->WHEAT; opening:cautious->land_first; sheep_yarn:sheep_4->sheep_2; sheep_no_yarn:sheep_0->sheep_2; max_hands:hands_6->hands_14; |
| gpt-5.4-nano-2026-03-17 | 3/10 | melon_race_timing:10->9; crop_choice:TOMATO->WHEAT; opening:meta_a->default; sheep_yarn:sheep_4->sheep_0; max_hands:hands_6->hands_8; terminal_tomato: |
| claude-haiku-4-5-20251001 | 7/10 | melon_dump:72->0; se_quadrant:buy_day16->never; terminal_tomato:off->plant_day16 |

overall 93/131 decisions unchanged

| task | unchanged / compared |
|---|---|
| melon_dump | 11/14 |
| melon_race_timing | 12/13 |
| crop_choice | 10/13 |
| opening | 7/13 |
| sheep_yarn | 9/13 |
| sheep_no_yarn | 11/13 |
| se_quadrant | 12/14 |
| max_hands | 7/12 |
| terminal_tomato | 7/13 |
| terminal_carrot | 7/13 |
