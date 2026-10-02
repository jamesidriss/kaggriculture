| model | score | sanity (3) | exact (5) | sim (7) | flags pool / SE / fib / refill |
|---|---|---|---|---|---|
| gemini-3.7-flash | 0.902 | 1.00 | 0.94 | 0.83 | 8 / 1 / 3 / 9 |
| gpt-6-astra | 0.863 | 1.00 | 1.00 | 0.71 | 2 / 1 / 0 / 10 |
| gemma-4-31b-it | 0.860 | 1.00 | 0.99 | 0.71 | 7 / 1 / 2 / 5 |
| claude-opus-5-default | 0.858 | 1.00 | 1.00 | 0.69 | 12 / 1 / 7 / 6 |
| gemini-3.8-flash | 0.839 | 1.00 | 0.99 | 0.66 | 7 / 1 / 3 / 9 |
| claude-sonnet-5-default | 0.839 | 1.00 | 0.99 | 0.66 | 8 / 1 / 3 / 4 |
| gemini-2.5-flash | 0.806 | 1.00 | 0.75 | 0.76 | 5 / 1 / 2 / 5 |
| glm-5 | 0.806 | 0.89 | 0.99 | 0.64 | 9 / 1 / 3 / 8 |
| gpt-5.5-2026-04-23 | 0.797 | 1.00 | 0.99 | 0.57 | 9 / 1 / 3 / 11 |
| gemini-2.5-pro | 0.785 | 1.00 | 0.99 | 0.54 | 8 / 2 / 3 / 8 |
| claude-opus-4-8-default | 0.737 | 0.67 | 0.76 | 0.75 | 7 / 1 / 4 / 7 |
| grok-4.20-0309-reasoning | 0.725 | 1.00 | 0.99 | 0.42 | 11 / 0 / 3 / 6 |
| gpt-oss-20b | 0.722 | 1.00 | 0.72 | 0.61 | 3 / 1 / 2 / 1 |
| claude-sonnet-4-5-20250929 | 0.712 | 0.56 | 0.71 | 0.79 | 10 / 1 / 2 / 5 |
| gpt-5.4-mini-2026-03-17 | 0.646 | 0.83 | 0.60 | 0.60 | 6 / 1 / 1 / 1 |
| gemini-3.1-flash-lite-preview | 0.549 | 0.56 | 0.54 | 0.56 | 4 / 1 / 1 / 5 |
| gpt-oss-120b | 0.515 | 0.67 | 0.60 | 0.39 | 6 / 1 / 4 / 4 |
| gpt-5.4-nano-2026-03-17 | 0.400 | 0.28 | 0.15 | 0.63 | 9 / 1 / 1 / 7 |
| claude-haiku-4-5-20251001 | 0.398 | 0.33 | 0.54 | 0.33 | 9 / 1 / 2 / 4 |
| deepseek-r1-0528 | 0.000 | 0.00 | 0.00 | 0.00 | 0 / 0 / 0 / 0 |
| grok-4.6 | 0.000 | 0.00 | 0.00 | 0.00 | 0 / 0 / 0 / 0 |

| task | gemini-3.7-flash | gpt-6-astra | gemma-4-31b-it | claude-opus-5-default | gemini-3.8-flash | claude-sonnet-5-default | gemini-2.5-flash | glm-5 | gpt-5.5-2026-04-23 | gemini-2.5-pro | claude-opus-4-8-default | grok-4.20-0309-reasoning | gpt-oss-20b | claude-sonnet-4-5-20250929 | gpt-5.4-mini-2026-03-17 | gemini-3.1-flash-lite-preview | gpt-oss-120b | gpt-5.4-nano-2026-03-17 | claude-haiku-4-5-20251001 | deepseek-r1-0528 | grok-4.6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hire_math | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 | 0.50 | 0.00 | 1.00 | 0.50 | 0.00 | 0.00 | 0.00 |
| feed_or_lose | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| fertilizer_melon | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.67 | 1.00 | 0.67 | 0.00 | 0.33 | 1.00 | 0.00 | 0.00 |
| melon_dump | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| melon_race_timing | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| wool_lot | 0.72 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.63 | 1.00 | 1.00 | 1.00 | 0.56 | 1.00 | 0.29 | 0.56 | 0.56 | 0.38 | 1.00 | 0.44 | 0.38 | 0.00 | 0.00 |
| milk_front_run | 0.97 | 1.00 | 0.97 | 1.00 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.26 | 0.97 | 0.31 | 0.97 | 0.10 | 0.31 | 0.00 | 0.00 | 0.31 | 0.00 | 0.00 |
| crop_choice | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.16 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 1.00 | 1.00 | 0.33 | 1.00 | 0.00 | 0.00 |
| opening | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.16 | 0.54 | 1.00 | 0.00 | 0.00 | 0.16 | 0.00 | 0.00 |
| sheep_yarn | 1.00 | 1.00 | 0.00 | 0.92 | 0.78 | 0.78 | 0.40 | 0.78 | 1.00 | 0.92 | 0.40 | 0.92 | 0.40 | 0.40 | 0.78 | 0.00 | 0.00 | 0.40 | 0.40 | 0.00 | 0.00 |
| sheep_no_yarn | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 |
| se_quadrant | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| max_hands | 0.89 | 0.99 | 0.99 | 0.99 | 0.89 | 0.89 | 0.99 | 0.72 | 0.99 | 0.89 | 0.89 | 0.99 | 0.89 | 0.99 | 0.89 | 0.89 | 0.72 | 1.00 | 0.72 | 0.00 | 0.00 |
| terminal_tomato | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 1.00 | 1.00 | 0.95 | 0.00 | 0.95 | 0.95 | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| terminal_carrot | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |

| task | gemini-3.7-flash | gpt-6-astra | gemma-4-31b-it | claude-opus-5-default | gemini-3.8-flash | claude-sonnet-5-default | gemini-2.5-flash | glm-5 | gpt-5.5-2026-04-23 | gemini-2.5-pro | claude-opus-4-8-default | grok-4.20-0309-reasoning | gpt-oss-20b | claude-sonnet-4-5-20250929 | gpt-5.4-mini-2026-03-17 | gemini-3.1-flash-lite-preview | gpt-oss-120b | gpt-5.4-nano-2026-03-17 | claude-haiku-4-5-20251001 | deepseek-r1-0528 | grok-4.6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hire_math (choice) | [1, | [1, | [1, | [1, | [1, | [1, | [1, | [1, | [1, | [1, | [4, | [1, | [1, | [2, | [2, | [4, | [1, | [1, | [2, | None | None |
| feed_or_lose (choice) | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['A', | ['C', | ['C', | None | None |
| fertilizer_melon (choice) | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | [6, | None | [6, | [6, | None | None |
| melon_dump (choice) | 72 | 71 | 72 | 72 | 72 | 72 | 72 | 72 | 72 | 72 | 72 | 71 | 72 | 0 | 72 | 0 | 72 | 0 | 72 | None | None |
| melon_race_timing (choice) | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 10 | 10 | 10 | None | None |
| wool_lot (choice) | [4, | [0, | [0, | [0, | [0, | [0, | [8, | [0, | [0, | [0, | [10, | [0, | [13, | [10, | [10, | [13, | [0, | [12, | [13, | None | None |
| milk_front_run (choice) | [24, | [21, | [24, | [20, | [24, | [24, | [24, | [24, | [24, | [24, | [6, | [24, | [4, | [24, | [4, | [4, | None | [1, | [4, | None | None |
| crop_choice (choice) | STRAWBERRY | STRAWBERRY | STRAWBERRY | STRAWBERRY | STRAWBERRY | STRAWBERRY | WHEAT | STRAWBERRY | STRAWBERRY | STRAWBERRY | STRAWBERRY | STRAWBERRY | STRAWBERRY | STRAWBERRY | TOMATO | STRAWBERRY | STRAWBERRY | TOMATO | STRAWBERRY | None | None |
| opening (choice) | goose_farm | goose_farm | goose_farm | meta_a | goose_farm | goose_farm | goose_farm | strawberry_rush | meta_a | meta_a | meta_a | meta_a | melon_max | default | land_first | goose_farm | meta_a | meta_a | default | None | None |
| sheep_yarn (choice) | sheep_8 | sheep_8 | sheep_0 | sheep_6 | sheep_4 | sheep_4 | sheep_2 | sheep_4 | sheep_8 | sheep_6 | sheep_2 | sheep_6 | sheep_2 | sheep_2 | sheep_4 | sheep_0 | sheep_0 | sheep_2 | sheep_2 | None | None |
| sheep_no_yarn (choice) | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_2 | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_0 | sheep_2 | sheep_0 | sheep_0 | None | None |
| se_quadrant (choice) | buy_day12 | buy_day12 | buy_day12 | buy_day12 | buy_day12 | buy_day12 | buy_day12 | buy_day12 | buy_day12 | buy_day12 | never | buy_day12 | buy_day12 | never | buy_day12 | never | buy_day12 | buy_day16 | buy_day16 | None | None |
| max_hands (choice) | hands_8 | hands_10 | hands_10 | hands_10 | hands_8 | hands_8 | hands_10 | hands_6 | hands_10 | hands_8 | hands_8 | hands_10 | hands_8 | hands_10 | hands_8 | hands_8 | hands_6 | hands_12 | hands_6 | None | None |
| terminal_tomato (choice) | plant_day16 | plant_day16 | plant_day16 | plant_day16 | plant_day16 | plant_day16 | plant_day16 | plant_day16 | plant_day18 | plant_day18 | plant_day16 | off | plant_day16 | plant_day16 | plant_day18 | off | plant_day18 | plant_day18 | off | None | None |
| terminal_carrot (choice) | plant_day24 | plant_day26 | plant_day24 | plant_day24 | plant_day26 | plant_day24 | plant_day24 | plant_day24 | plant_day26 | plant_day26 | plant_day24 | plant_day27 | plant_day24 | plant_day24 | off | off | plant_day24 | plant_day24 | off | None | None |
