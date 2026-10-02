"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent

import base64,zlib,json
_DATA=json.loads(zlib.decompress(base64.b85decode(__import__('publication_assets').value('observed_56713902_009_010'))))
def _router(obs,step,state):
    if 'route'not in state:state['route']=0
    if step%24==0:
        f=obs['farms'][int(obs['player'])];fields=[z.get('animal',z.get('crop',''))if isinstance(z,dict)else'L'if z=='LOCKED'else''for rr in f['tiles']for z in rr];shops=obs['town']['unlocked_shops'];scores=[]
        for i,r in enumerate(_DATA):
            snap=r['states'][str(step)];mismatch=sum(a!=b for a,b in zip(fields,snap['fields']));distance=sum(abs(shops.count(s)-snap['shops'].count(s))for s in set(shops+snap['shops']))
            # A route cannot silently move or replace live livestock.
            if any(a in('COW','SHEEP','GOOSE')and a!=b for a,b in zip(fields,snap['fields'])):continue
            if fields.count('L')!=snap['fields'].count('L'):continue
            scores.append((mismatch*10+distance,i!=state['route'],i))
        if scores:state['route']=min(scores)[2]
    return state['route']

_TG_START=144

_TG_UNIT_NS={'__name__':'sep30_task_unit_model'}
exec(__import__('publication_assets').source('policies/observed_56713902_009_011.py', 'text'),_TG_UNIT_NS)
"""Execute public expert task intents against the live farm, not recorded moves."""
_TG_OBS=None
_TG_STATE={}
_SC29_TG_REPORT=dict(goals=0,completed=0,repairs=0,resource_waits=0,terminal_returns=0,wait_reasons={})

def _tg_walk(pos,target):
    x,y=pos;tx,ty=target
    if x!=tx:return ['EAST'if x<tx else'WEST']
    if y!=ty:return ['SOUTH'if y<ty else'NORTH']
    return None

def _tg_home(pos):return min(((4,4),(5,4),(4,5),(5,5)),key=lambda xy:abs(pos[0]-xy[0])+abs(pos[1]-xy[1]))

def _tg_goal(obs,actor,goals,st,seeds,shed):
    p=int(obs['player']);farm=obs['farms'][p];pr=obs['private'];pos=tuple(([farm['farmer']]+farm['hands'])[actor]);inv=pr['inventories'][actor];step=int(obs['step']);home=_tg_home(pos);distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    if any(inv.values())and step>=717-distance:
        _SC29_TG_REPORT['terminal_returns']+=1;return _tg_walk(pos,home)or['DROP']
    index=st['index'].get(actor,0)
    while index<len(goals):
        target,command,gid,dependency=goals[index];target=tuple(target);op=command[0]
        if dependency>=0 and dependency not in st['done'] and dependency not in st['pending_done']:return _tg_walk(pos,target)or['PASS']
        tile=farm['tiles'][target[1]][target[0]];animal=isinstance(tile,dict)and 'animal'in tile;plant=isinstance(tile,dict)and tile.get('kind')=='PLANT';complete=False;valid=True;cmd=list(command)
        if op=='WATER':complete=not plant or tile.get('watered_today')
        elif op=='HARVEST':complete=not isinstance(tile,dict)or tile.get('yield_units',0)<=0 or(plant and step//24-tile['planted_day']<{'WHEAT':2,'CARROT':2,'MELON':10,'STRAWBERRY':10,'TOMATO':8}[tile['crop']])
        elif op=='FEED':complete=not animal or tile.get('fed_today');valid=inv.get('WHEAT',0)>0
        elif op=='CARE':complete=not animal or tile.get('cared_today')
        elif op=='COLLECT_FERTILIZER':complete=not animal or not tile.get('fertilizer_available')
        elif op=='FERTILIZE':complete=not plant or tile.get('fertilized_until_day',-1)>=int(obs['step'])//24+2;valid=inv.get('FERTILIZER',0)>0
        elif op=='PLANT':
            complete=plant or animal;valid=seeds.get(command[1],0)>0
            if not valid:st['seed_requests'][command[1]]=st['seed_requests'].get(command[1],0)+1
            if isinstance(tile,dict)and tile.get('kind')=='WEED':
                if pos!=target:return _tg_walk(pos,target)
                _SC29_TG_REPORT['repairs']+=1;return ['DIG']
            if tile=='LOCKED':valid=False
        elif op in('BUILD_COOP','BUILD_PASTURE'):
            complete=isinstance(tile,dict)and tile.get('kind')in('COOP','PASTURE')or plant or animal
            if isinstance(tile,dict)and tile.get('kind')=='WEED':
                if pos!=target:return _tg_walk(pos,target)
                _SC29_TG_REPORT['repairs']+=1;return ['DIG']
            if tile=='LOCKED':valid=False
        elif op=='DIG':complete=tile is None or tile=='LOCKED'or animal
        elif op=='PICKUP':
            item=command[1];wanted=command[2]if len(command)>2 else 1
            if item in('WHEAT','FERTILIZER'):
                operation='FEED'if item=='WHEAT'else'FERTILIZE'
                wanted=max(0,sum(g[1][0]==operation for g in goals[index+1:])-inv.get(item,0))
                if wanted==0:complete=True
            qty=min(wanted,shed.get(item,0));valid=qty>0
            if not valid and wanted>0:st['requests'][item]=st['requests'].get(item,0)+wanted
            if valid:cmd=['PICKUP',item,qty]
        elif op=='PLACE':
            item=command[1]
            if item in ANIMAL_STRUCTURE:
                complete=animal;valid=inv.get(item,0)>0
                if tile is None and pos==target:_SC29_TG_REPORT['repairs']+=1;return ['BUILD_'+ANIMAL_STRUCTURE[item]]
            else:
                complete=inv.get(item,0)<=0;cmd=['PLACE',item,min(command[2]if len(command)>2 else 1,inv.get(item,0))]
        elif op=='DROP':complete=not any(inv.values())
        else:complete=True
        if complete:st['done'].add(gid);index+=1;st['index'][actor]=index;continue
        if op=='FEED'and not valid:
            if tile.get('consecutive_unfed',0)==0:
                st['done'].add(gid);index+=1;st['index'][actor]=index;continue
            if pos!=home:return _tg_walk(pos,home)
            q=min(shed.get('WHEAT',0),sum(g[1][0]=='FEED'for g in goals[index:]))
            if q:shed['WHEAT']-=q;return ['PICKUP','WHEAT',q]
        if pos!=target:return _tg_walk(pos,target)
        if not valid:
            _SC29_TG_REPORT['resource_waits']+=1
            reason=op+(':'+str(command[1])if len(command)>1 else'');wr=_SC29_TG_REPORT['wait_reasons'];wr[reason]=wr.get(reason,0)+1
            # Fertilizer is optional; do not let it starve mandatory watering.
            if op=='FERTILIZE'or op=='PICKUP'and command[1]=='FERTILIZER':st['done'].add(gid);index+=1;st['index'][actor]=index;continue
            return ['PASS']
        if op=='PLANT':
            # A new plant must receive water before midnight. Its watering goal
            # follows immediately in the observed intent sequence.
            if step%24>=23:return ['PASS']
            seeds[cmd[1]]-=1
        if op=='PICKUP':shed[cmd[1]]-=cmd[2]
        st['index'][actor]=index+1;st['pending_done'].add(gid);_SC29_TG_REPORT['completed']+=1;return cmd
    if any(inv.values()):return _tg_walk(pos,home)or['DROP']
    return ['PASS']

_TG_NATIVE_ROUTE=Chassis._route_action

def _tg_route_action(self,route,step):
    action=_TG_NATIVE_ROUTE(self,route,step)
    if step<_TG_START or step%24<6:return action
    obs=dict(_TG_OBS);p=int(obs['player']);obs['farms']=list(obs['farms']);obs['farms'][p]=copy.deepcopy(obs['farms'][p]);obs['private']=copy.deepcopy(obs['private']);day=step//24;st=_TG_STATE.get(p)
    if st is None or st['day']!=day or step==0:
        st=dict(day=day,index={},done=set(),pending_done=set(),requests={},seed_requests={});_TG_STATE[p]=st
        _SC29_TG_REPORT['goals']+=sum(len(g)for g in _DATA[route]['tasks'][day])
    st['done'].update(st['pending_done']);st['pending_done'].clear()
    st['requests']={};st['seed_requests']={}
    goals=_DATA[route]['tasks'][day];farm=obs['farms'][p];seeds=dict(obs['private']['seeds']);shed=dict(obs['private']['shed']);commands=[]
    for actor in range(1+len(farm['hands'])):
        command=_tg_goal(obs,actor,goals[actor]if actor<len(goals)else[],st,seeds,shed);commands.append(command)
        _TG_UNIT_NS['_apply_unit_action'](farm,obs['private'],actor,command,10,day,24,100)
        seeds=dict(obs['private']['seeds']);shed=dict(obs['private']['shed'])
    action['farmer']=commands[0];action['hands']=commands[1:]
    market=[list(o)for o in action.get('market',[])];reserved={}
    for actor,queue in enumerate(goals):
        if actor>=len(obs['private']['inventories']):continue
        for item,operation in [('WHEAT','FEED'),('FERTILIZER','FERTILIZE')]:
            need=sum(g[1][0]==operation for g in queue[st['index'].get(actor,0):]);need=max(0,need-obs['private']['inventories'][actor].get(item,0));reserved[item]=reserved.get(item,0)+need
    for item,need in reserved.items():
        available=max(0,shed.get(item,0)-need)
        for order in market:
            if order[:2]==['SELL',item]:order[2]=min(order[2],available);available-=order[2]
    for item,q in st['requests'].items():
        already=sum(o[2]for o in market if len(o)>2 and o[:2]==['BUY_PRODUCT',item]);q=max(0,min(q,100-sum(shed.values()))-already)
        price=obs['market']['prices'].get(item,ANIMAL_COST.get(item,0));op='BUY_ANIMAL'if item in ANIMAL_COST else'BUY_PRODUCT'
        if q and len(market)<10 and farm['money']>q*(price+10)+20:market.append([op,item,q])
    for item,q in st['seed_requests'].items():
        already=sum(o[2]for o in market if len(o)>2 and o[:2]==['BUY_SEED',item]);q=max(0,q-already)
        if q and len(market)<10 and farm['money']>q*SEED_PRICE[item]+20:market.append(['BUY_SEED',item,q])
    if step%24<8:
        need=max(0,len(goals)-1-len(farm['hands'])-sum(o[:1]==['HIRE']for o in market))
        while need and len(market)<10:
            n=int(farm['hires_today'])+sum(o[:1]==['HIRE']for o in market)
            if farm['money']<_fib(n)+20:break
            market.append(['HIRE']);need-=1
    action['market']=market;return action

Chassis._route_action=_tg_route_action
_PROXY=make_agent({i:r['actions']for i,r in enumerate(_DATA)},router=_router,front_run=False,sell_lead=True,budget_guard=True,room_guard=True,clamp_sells=True,dead_stock=True,terminal_liquidation=True,weed_repair=False)
def sep30_task_graph_agent(obs,configuration=None):
    global _TG_OBS
    _TG_OBS=obs
    return _PROXY(obs,configuration)

_BR30_ARM=0
"""Counterfactual daily project options with observable-state descriptors."""
_BR30_ENTRY=[v for v in list(globals().values())if callable(v)][-1]
_BR30_ROUTER=_PROXY.chassis.router
_SC29_BRANCH_REPORT={'decisions':[]}
_BR30_SIGNATURES={}
for _j,_r in enumerate(_DATA):
 _BR30_SIGNATURES[_j]=tuple(tuple(_r['states'][str(t)]['fields'])for t in(168,192,216))
def _br30_features(obs):
 p=int(obs['player']);items=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER');shops=('BAKERY','BRUNCH_SPOT','FARMERS_MARKET','ICE_CREAM_SHOP','PET_CAFE','PIZZA_SHOP','SMOOTHIE_SHOP','YARN_STORE');x=[obs['farms'][p]['money']/1000,obs['farms'][1-p]['money']/1000]
 x += [obs['market']['prices'][i]for i in items];x += [obs['market']['inventory'][i]-10000 for i in items];x += [obs['town']['unlocked_shops'].count(i)for i in shops]
 for player in(p,1-p):
  fields=[t.get('animal',t.get('crop',''))if isinstance(t,dict)else''for row in obs['farms'][player]['tiles']for t in row];x +=[fields.count(i)for i in('COW','SHEEP','GOOSE','WHEAT','CARROT','TOMATO','STRAWBERRY','MELON')]
 return x

def _br30_action_features(route):
 x=[]
 for t in(168,192,216):
  fields=_DATA[route]['states'][str(t)]['fields'];x.extend(fields.count(i)for i in('COW','SHEEP','GOOSE','WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','L'))
 return x

def _br30_options(obs,state,parent):
 p=int(obs['player']);f=obs['farms'][p];fields=[z.get('animal',z.get('crop',''))if isinstance(z,dict)else'L'if z=='LOCKED'else''for row in f['tiles']for z in row];shops=obs['town']['unlocked_shops'];scored=[]
 for i,r in enumerate(_DATA):
  snap=r['states']['144']
  if any(a in('COW','SHEEP','GOOSE')and a!=b for a,b in zip(fields,snap['fields']))or fields.count('L')!=snap['fields'].count('L'):continue
  distance=sum(a!=b for a,b in zip(fields,snap['fields']))*10+sum(abs(shops.count(s)-snap['shops'].count(s))for s in set(shops+snap['shops']));scored.append((distance,i))
 options=[parent];seen={_BR30_SIGNATURES[parent]}
 for _,i in sorted(scored):
  if _BR30_SIGNATURES[i]not in seen:options.append(i);seen.add(_BR30_SIGNATURES[i])
 return options[:4]


import math as _PROJECT_MATH
_PROJECT_MODEL=__import__('publication_assets').value('observed_56713902_009_012')
def _br30_choose(features,options):
 m=_PROJECT_MODEL;descriptors=[_br30_action_features(i) for i in options];vectors=[features+o+[a-b for a,b in zip(o,descriptors[0])] for o in descriptors];predictions=[]
 for member in m['members']:
  values=[]
  for x in vectors:
   z=[(v-mu)/sd for v,mu,sd in zip(x,m['mean'],m['std'])]
   h=[_PROJECT_MATH.tanh(sum(a*b for a,b in zip(w,z))+bias) for w,bias in zip(member['w1'],member['b1'])]
   values.append(sum(a*b for a,b in zip(member['w2'],h))+member['b2'])
  predictions.append([v-values[0] for v in values])
 scores=[]
 for i in range(len(options)):
  vs=[v[i] for v in predictions];mean=sum(vs)/len(vs);sd=(sum((v-mean)**2 for v in vs)/max(1,len(vs)-1))**.5
  scores.append(mean-m['risk']*sd+m['logprior'][i])
 return max(range(len(scores)),key=lambda i:scores[i])

def _br30_router(obs,step,state):
 parent=_BR30_ROUTER(obs,step,state)
 if step!=144:return parent
 options=_br30_options(obs,state,parent);x=_br30_features(obs);arm=_br30_choose(x,options);choice=options[arm];_SC29_BRANCH_REPORT['decisions'].append(dict(step=step,features=x,options=options,option_features=[_br30_action_features(i)for i in options],chosen=choice,arm=arm))
 state['route']=choice;return choice
_PROXY.chassis.router=_br30_router
final_sep30_branch_entry=_BR30_ENTRY

_SC29_EXEC_REPORT=_PROXY.chassis.diagnostics

_MT30_BASE=[v for v in list(globals().values())if callable(v)][-1]
import math
import itertools as _cxd_it

_R37_MARKET_PARAMS = {'WHEAT': {'base': 25, 'I0': 10000, 'T': 400, 'below_func': 'sqrt', 'below_target': 0.8, 'above_func': 'log', 'above_target': 0.2}, 'CARROT': {'base': 35, 'I0': 10000, 'T': 450, 'below_func': 'hinge', 'below_target': 1.0, 'above_func': 'sqrt', 'above_target': 0.7}, 'TOMATO': {'base': 60, 'I0': 10000, 'T': 200, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'sqrt', 'above_target': 0.6}, 'STRAWBERRY': {'base': 120, 'I0': 10000, 'T': 100, 'below_func': 'sqrt', 'below_target': 0.7, 'above_func': 'linear', 'above_target': 1.6}, 'MELON': {'base': 250, 'I0': 10000, 'T': 300, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.6}, 'EGG': {'base': 50, 'I0': 10000, 'T': 332, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'log', 'above_target': 0.2}, 'MILK': {'base': 160, 'I0': 10000, 'T': 122, 'below_func': 'sqrt', 'below_target': 0.6, 'above_func': 'linear', 'above_target': 1.6}, 'WOOL': {'base': 200, 'I0': 10000, 'T': 105, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.2}, 'FERTILIZER': {'base': 100, 'I0': 10000, 'T': 200, 'below_func': 'linear', 'below_target': 0.4, 'above_func': 'linear', 'above_target': 0.4}}
_R37_PRICE_FLOOR = 1
_R37_HINGE_GAIN = 8.0
def _r37_shape(func, x, T=None):
    x = max(0.0, x)
    if func == "linear": return x
    if func == "sq":     return x * x
    if func == "sqrt":   return math.sqrt(x)
    if func == "log":    return math.log(1.0 + x)
    if func == "log10":  return math.log10(1.0 + x)
    if func == "hinge":
        # Degenerates to linear if T is missing or non-positive.
        if not T or T <= 0:
            return x
        u = x / T
        return u + _R37_HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x
def _r37_market_price(item, inventory, params=None):
    """Floor at _R37_PRICE_FLOOR."""
    p = (params or _R37_MARKET_PARAMS)[item]
    base = p["base"]
    I0 = p["I0"]
    T = p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _r37_shape(f, T, T)
        price = base + amp * _r37_shape(f, I0 - inventory, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _r37_shape(f, T, T)
        price = base - amp * _r37_shape(f, inventory - I0, T)
    return max(_R37_PRICE_FLOOR, int(round(price)))
def _v44y_price(item, inventory, params):
    return _r37_market_price(item, inventory, params)
def _v44y_params(obs):
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for k, patch in (obs['market'].get('params') or {}).items():
        if k in params and isinstance(patch, dict): params[k].update(patch)
    return params
def _v44y_lockstep(orders_me, orders_opp, inv0, stock_me, stock_opp, params):
    """Replay the engine's per-slot / per-unit lockstep for SELL and BUY_PRODUCT orders (money-unbounded).
    Returns (revenue_me, revenue_opp)."""
    inv = dict(inv0); stock = [dict(stock_me), dict(stock_opp)]; rev = [0.0, 0.0]
    queues = [list(orders_me), list(orders_opp)]
    for i in range(max(len(queues[0]), len(queues[1]))):
        rem = [None, None]
        for p in (0, 1):
            if i < len(queues[p]):
                o = queues[p][i]
                if o and len(o) >= 3 and o[0] in ('SELL', 'BUY_PRODUCT') and o[1] in params:
                    try: n = int(o[2])
                    except Exception: n = 0
                    if n > 0: rem[p] = [o[0], o[1], n]
        guard = 0
        while True:
            guard += 1
            if guard > 5000: break
            quoted = [None, None]
            for p in (0, 1):
                r = rem[p]
                if r is None or r[2] <= 0: continue
                if r[0] == 'SELL':
                    quoted[p] = ('SELL', r[1], _v44y_price(r[1], inv[r[1]], params))
                elif r[1] in ('WHEAT', 'FERTILIZER'):
                    quoted[p] = ('BUY_PRODUCT', r[1], _v44y_price(r[1], inv[r[1]] - 1, params))
                else:
                    rem[p] = None
            if quoted[0] is None and quoted[1] is None: break
            committed = False
            for p in (0, 1):
                q = quoted[p]
                if q is None: continue
                op, item, price = q
                if op == 'SELL':
                    if stock[p].get(item, 0) <= 0:
                        rem[p] = None; continue
                    stock[p][item] -= 1; rev[p] += price
                    if price > 1: inv[item] += 1
                else:
                    stock[p][item] = stock[p].get(item, 0) + 1; rev[p] -= price; inv[item] -= 1
                rem[p][2] -= 1; committed = True
            if not committed: break
    return rev[0], rev[1]
def _v44y_factor_margin(opp, inv0, stock, params):
    # EXP298: cache independent item schedules, preserving the donor's exact search/ties.
    # The donor model has no shared cash/capacity constraint; per-item revenues add.
    cache = {}
    opp_schedules = {}
    for i, order in enumerate(opp):
        if order and len(order) >= 3 and order[0] in ('SELL', 'BUY_PRODUCT') and order[1] in params:
            item = order[1]
            padded = opp_schedules.setdefault(item, [[] for _ in opp])
            padded[i] = order
    def margin(cand):
        schedules = {item: [] for item in opp_schedules}
        for i, order in enumerate(cand):
            if order and len(order) >= 3 and order[0] in ('SELL', 'BUY_PRODUCT') and order[1] in params:
                schedules.setdefault(order[1], []).append((i, order[0], int(order[2])))
        total = 0.0
        for item, schedule in schedules.items():
            key = (item, tuple(schedule))
            value = cache.get(key)
            if value is None:
                mine = [[] for _ in cand]
                for i, op, n in schedule: mine[i] = [op, item, n]
                theirs = opp_schedules.get(item, [[] for _ in opp])
                a, b = _v44y_lockstep(mine, theirs, {item: inv0[item]},
                                      {item: stock.get(item, 0)}, {item: stock.get(item, 0)},
                                      {item: params[item]})
                value = a - b
                cache[key] = value
            total += value
        return total
    return margin
_CXD_FIXED = ('HIRE', 'BUY_SEED', 'BUY_ANIMAL', 'BUY_LAND')
_CXD_BUDGET = 800
_CXD_REPORT = {'cxd_turns': 0, 'cxd_gain': 0.0, 'cxd_evals': 0, 'cxd_budget_hits': 0, 'cxd_errors': 0}
_CXD_MODELS = []
_CXD_PARENT_ORDERS = []
def _cxd_candidates(orders, slots, sells, fixed):
    """Orderings of `sells` over `slots`, fixed-price orders filling the rest in their own order."""
    for positions in _cxd_it.permutations(slots, len(sells)):
        out = list(orders)
        rest = [i for i in slots if i not in positions]
        for i, order in zip(positions, sells):
            out[i] = order
        for i, order in zip(rest, fixed):
            out[i] = order
        yield out
def _cxd_reorder(obs, action):
    market = action.get('market') or []
    if len(market) < 2:
        return action
    orders = [list(o) if isinstance(o, (list, tuple)) else o for o in market]
    bought = {o[1] for o in orders if o and len(o) > 1 and o[0] == 'BUY_PRODUCT'}
    slots, sells, fixed = [], [], []
    for i, o in enumerate(orders):
        if not o:
            continue
        if o[0] in _CXD_FIXED:
            slots.append(i); fixed.append(o)
        elif o[0] == 'SELL' and len(o) > 1 and o[1] not in bought:
            slots.append(i); sells.append(o)
    if not sells or len(slots) < 2:
        return action
    params = _v44y_params(obs)
    stock = {k: max(0, int(v)) for k, v in projected_shed(action, FarmView(obs)).items()}
    inv0 = {k: int(v) for k, v in obs['market']['inventory'].items()}
    _CXD_PARENT_ORDERS[:] = [list(o) for o in orders if o]
    models = [m for m in _CXD_MODELS if m] or [orders]
    margins = [_v44y_factor_margin(m, inv0, stock, params) for m in models]

    def margin(cand):
        return min(f(cand) for f in margins)
    base = best = margin(orders)
    best_orders = None
    evals = 0
    for cand in _cxd_candidates(orders, slots, sells, fixed):
        if cand == orders:
            continue
        evals += 1
        if evals > _CXD_BUDGET:
            _CXD_REPORT['cxd_budget_hits'] += 1
            break
        value = margin(cand)
        if value > best + 0.5:
            best, best_orders = value, cand
    _CXD_REPORT['cxd_evals'] += evals
    if best_orders is None:
        return action
    _CXD_REPORT['cxd_turns'] += 1
    _CXD_REPORT['cxd_gain'] += best - base
    return dict(action, market=best_orders)
_SC29_MODE='population'
_SC29_ORIG_CXD = _cxd_reorder
_SC29_REPORT = dict(turns=0, changed=0, errors=0, forecast_gain=0.0)
def _sc29_assignment(obs, action, models):
    orders = [list(o) if o else [] for o in (action.get('market') or [])]
    bought = {o[1] for o in orders if len(o)>1 and o[0]=='BUY_PRODUCT'}
    slots=[]; sells=[]; fixed=[]
    for i,o in enumerate(orders):
        if not o: continue
        if o[0] in _CXD_FIXED: slots.append(i); fixed.append((i,o))
        elif len(o)>2 and o[0]=='SELL' and o[1] not in bought:
            slots.append(i); sells.append(o)
    if not sells or len(slots)<2 or len({o[1]for o in sells})!=len(sells):return orders,0.0
    params=_v44y_params(obs);stock={k:max(0,int(v))for k,v in projected_shed(action,FarmView(obs)).items()};inv={k:int(v)for k,v in obs['market']['inventory'].items()}
    weights=[]
    for sale in sells:
        item=sale[1];values=[]
        if item not in params:return orders,0.0
        for slot in slots:
            mine=[[]for _ in orders];mine[slot]=sale;value=0.0
            for model in models:
                theirs=[o if len(o)>2 and o[0]in('SELL','BUY_PRODUCT')and o[1]==item else [] for o in model]
                a,b=_v44y_lockstep(mine,theirs,{item:inv[item]},{item:stock.get(item,0)},{item:stock.get(item,0)},{item:params[item]})
                value+=(a-b)/len(models)
            values.append(value)
        weights.append(values)
    # Only sale identities occupy the subset state; fixed orders remain in their original relative order.
    dp={0:(0.0,[])}
    for pos,slot in enumerate(slots):
        nxt={}
        for mask,(v,path)in dp.items():
            f=pos-mask.bit_count()
            if f<len(fixed):
                old=fixed[f][0]
                # Do not advance a capital/labour purchase ahead of the parent's cash availability.
                if slot>=old:
                    cand=(v,path+[('f',f)])
                    if mask not in nxt or v>nxt[mask][0]:nxt[mask]=cand
            for k in range(len(sells)):
                if mask>>k&1:continue
                m=mask|(1<<k);val=v+weights[k][pos]
                if m not in nxt or val>nxt[m][0]+1e-9:nxt[m]=(val,path+[('s',k)])
        dp=nxt
    terminal=dp.get((1<<len(sells))-1)
    if terminal is None:return orders,0.0
    best,path=terminal;out=[list(o)for o in orders]
    for slot,(kind,k)in zip(slots,path):out[slot]=list(sells[k]if kind=='s'else fixed[k][1])
    original=sum(weights[k][slots.index(next(i for i,o in enumerate(orders)if o is sale or o==sale))]for k,sale in enumerate(sells))
    return (out,best-original)if best>original+0.5 else (orders,0.0)
def _cxd_reorder(obs,action):
    if int(obs['step'])==0:
        _SC29_REPORT.update(turns=0,changed=0,errors=0,forecast_gain=0.0)
    parent=_SC29_ORIG_CXD(obs,action)
    if int(obs['step'])<144:return parent
    try:
        raw=[list(o)if o else []for o in action.get('market')or[]]
        if _SC29_MODE=='exact':models=[raw]
        elif _SC29_MODE=='response':models=[parent.get('market')or[]]
        else:
            models=[raw,parent.get('market')or[]]
            # Fictitious-play style restricted population: best responses to empirical mixtures.
            for _ in range(4):
                response,_gain=_sc29_assignment(obs,action,models)
                if response not in models:models.append(response)
                else:break
        out,gain=_sc29_assignment(obs,parent,models)
        _SC29_REPORT['turns']+=1
        if gain>0 and out!=parent.get('market'):
            _SC29_REPORT['changed']+=1;_SC29_REPORT['forecast_gain']+=gain
            return dict(parent,market=out)
    except Exception:
        _SC29_REPORT['errors']+=1
    return parent

_MT30_PARENT=[v for v in list(globals().values())if callable(v)][-1]
def FarmView(obs):
 return _View(obs,int(obs['player']),_PROXY.chassis.cfg)
def projected_shed(action,view):
 return _PROXY.chassis._projected_shed(action,view)
_SC29_MT_REPORT={'calls':0,'errors':0}
def sep30_market_transfer_entry(obs,configuration=None):
 action=_MT30_BASE(obs,configuration)
 if int(obs['step'])<144:return action
 try:
  _SC29_MT_REPORT['calls']+=1
  return _cxd_reorder(obs,action)
 except Exception:
  _SC29_MT_REPORT['errors']+=1
  return action


_EP30_ENTRY=[v for v in list(globals().values())if callable(v)][-1]
_EP30_NEURAL=_br30_choose
_EP30_TABLE={(tuple(context),tuple(action)):(n,total)for context,action,n,total in json.loads(zlib.decompress(base64.b85decode(__import__('publication_assets').value('observed_56713902_009_013'))))}
_SC29_EP_REPORT={'empirical':0,'neural':0,'disagreements':0}
def _br30_choose(features,options):
 descriptors=[_br30_action_features(i)for i in options];context=tuple(features[20:44]+descriptors[0]);values=[_EP30_TABLE.get((context,tuple(v)),(0,0.))for v in descriptors[1:]]
 parent=_EP30_NEURAL(features,options)
 if not values or min(n for n,total in values)<4:
  _SC29_EP_REPORT['neural']+=1
  return parent
 scores=[0.]+[total/(n+4)for n,total in values];chosen=max(range(len(scores)),key=lambda i:scores[i]);_SC29_EP_REPORT['empirical']+=1;_SC29_EP_REPORT['disagreements']+=chosen!=parent
 return chosen
final_sep30_supported_policy_entry=_EP30_ENTRY
