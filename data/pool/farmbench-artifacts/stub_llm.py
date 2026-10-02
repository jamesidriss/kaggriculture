"""Local-only stub LLM for FarmBench: answers each task from stub_answers_<mode>.json (mode: naive | best | mixed).
Never used on Kaggle. It reads the task id from the prompt ("task id: <id>")."""
import json, os, re
from kaggle_benchmarks import actors
from kaggle_benchmarks.llm_messages import LLMMessage

HERE = os.path.dirname(os.path.abspath(__file__))
NAIVE = {
    "hire_math": {"hire_more": 0, "extra_cost": 0}, "feed_or_lose": {"feed": ["C", "D", "E"]},
    "fertilizer_melon": {"units_with_fertilizer": 7, "units_without_fertilizer": 6, "age_first_full_with_fertilizer": 10},
    "melon_dump": {"sell_now": 0}, "melon_race_timing": {"harvest_day": 10},
    "wool_lot": {"day27": 30, "day28": 0, "day29": 0}, "milk_front_run": {"units_per_hour": [0] * 23 + [24]},
    "crop_choice": {"crop": "NONE"},
    "opening": {"option": "cautious"}, "sheep_yarn": {"value": 0}, "sheep_no_yarn": {"value": 0},
    "se_quadrant": {"option": "never"}, "max_hands": {"value": 2},
    "terminal_tomato": {"value": -1}, "terminal_carrot": {"value": -1},
}


class StubLLM(actors.LLMChat):
    def __init__(self, mode="naive"):
        super().__init__(name=f"stub-{mode}")
        self.mode = mode
        self.answers = dict(NAIVE)
        p = os.path.join(HERE, f"stub_answers_{mode}.json")
        if os.path.exists(p):
            self.answers.update(json.load(open(p)))

    def invoke(self, messages, tools=None, **kw):
        text = "\n".join(str(getattr(m, "content", m)) for m in messages)
        m = re.search(r"task id: ([a-z_0-9]+)", text)
        tid = m.group(1) if m else None
        ans = dict(self.answers.get(tid, {}))
        ans.setdefault("rationale", f"stub {self.mode} answer for {tid}")
        return LLMMessage(sender=self, content=json.dumps(ans))
