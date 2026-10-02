# Composite candidate: mature HybridOpening base + mixed-market singleton inventory accounting fix.
# Strategy: Use the inspected Pipe-16 HybridOpening controller. Reassign idle workers during the first three days to plant, water and harvest one temporary wheat crop, then restore the planned pasture and deliver the wheat. Preserve the public Metav4 production and market controller. This is attributed reuse, and its stronger public source still needs live confirmation. Disable optional environment-dependent external library loading so the archive is self-contained.
# Local packaging modifications, 2026-09-20. Original attribution retained.
# Kaggriculture submission v9/3: public V39 (Apache-2.0, notices below) plus the v9 layers
# RACEPX gate, RACE (reservation from step 192, horizon 40 / margin 12), COURIER, CARROT and HERD
# appended at the end of this file.
# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
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


import base64
import json
import zlib
# EXP239 native schedules: Yusuke Hayashi (yhay81), Shop Router 0913.
# https://www.kaggle.com/code/yhay81/shop-router-0913
# Ahmed Berat Ozer: V39 prefix/terminal, shared-action encoding and controllers.
_R108_DATA=json.loads(zlib.decompress(base64.b85decode(__import__('publication_assets').value('observed_56713902_001_002'))))
_ROUTES={int(k):[_R108_DATA['actions'][i] for i in ids] for k,ids in _R108_DATA['routes'].items()}
_R108_SHOP_ROUTES={tuple(r['shops']):r['route'] for r in _R108_DATA['shops']}
del _R108_DATA
_SETTINGS={'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': False, 'front_run': False}

# EXP241: fixed two-policy choice, learned with five whole-team held-out folds.
# The full-fit tree and all five fold trees use only first-two-shop YARN_STORE count.
# V39 handles yarn-specialized worlds; EXP240 handles the other shop combinations.
_R110_OLD_SHOPS=__import__('publication_assets').value('observed_56713902_001_003')

_V92_TABLE={('BAKERY', 'YARN_STORE'): 9, ('BRUNCH_SPOT', 'YARN_STORE'): 9, ('FARMERS_MARKET', 'YARN_STORE'): 9, ('ICE_CREAM_SHOP', 'YARN_STORE'): 9, ('PET_CAFE', 'YARN_STORE'): 9, ('PIZZA_SHOP', 'YARN_STORE'): 9, ('SMOOTHIE_SHOP', 'YARN_STORE'): 9, ('YARN_STORE', 'BAKERY'): 9, ('YARN_STORE', 'BRUNCH_SPOT'): 9, ('YARN_STORE', 'FARMERS_MARKET'): 9, ('YARN_STORE', 'ICE_CREAM_SHOP'): 9, ('YARN_STORE', 'PET_CAFE'): 9, ('YARN_STORE', 'PIZZA_SHOP'): 9, ('YARN_STORE', 'SMOOTHIE_SHOP'): 9, ('YARN_STORE', 'YARN_STORE'): 9}

_V93_ROUTE_BY_RIVAL = {(229.0, 9989): 128}
def _router(observation,step,state):
    if step==2:
        try:
            _rv=observation['farms'][1-int(observation['player'])]
            state['rkey']=(round(float(_rv['money']),3), int(observation['market']['inventory']['WHEAT']))
        except Exception:
            state['rkey']=None
    if step>=144 and not state.get('day6'):
        shops=tuple((_get(_get(observation,'town',{}),'unlocked_shops',[]) or [])[:2])
        use_new=shops.count('YARN_STORE')<=0
        state['expert']='EXP240' if use_new else 'V39'
        state['route']=_R108_SHOP_ROUTES.get(shops,100) if use_new else _R110_OLD_SHOPS.get(shops,0)
        state['route']=_V92_TABLE.get(shops,state['route'])
        if 'YARN_STORE' in shops and state.get('rkey') in _V93_ROUTE_BY_RIVAL:
            state['route']=_V93_ROUTE_BY_RIVAL[state['rkey']]
        state['day6']=True
    if step>=648 and not state.get('day27'):
        state['route']=2
        state['day27']=True
    return state.get('route',0)

_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 30], ['SELL', 'WHEAT', 30]]
for _r42_tape in _ROUTES.values():
    _r42_tape[0]=dict(_r42_tape[0],market=[list(o) for o in _R42_OPENING])
del _r42_tape
_IMPL=make_agent(_ROUTES,router=_router,**_SETTINGS)
_IMPL.chassis.diagnostics['terminal_rescue_errors']=0

def agent(observation,configuration=None):
    try:
        action=_IMPL(observation,configuration)
        pass
        return action
    except Exception:
        return {'farmer':['PASS'],'hands':[],'market':[]}

_SHOP_PARENT=agent
del agent

def agent(observation,configuration=None):
    action=_SHOP_PARENT(observation,configuration)
    try:
        if _step_of(observation)>=718:
            view=_View(observation,_int(_get(observation,'player',0)),_IMPL.chassis.cfg)
            units=[]
            for i,pos in enumerate(view.positions):
                units.append(['DROP'] if _shed_adjacent(pos,view.board) and view.inv(i) else ['PASS'])
            action={'farmer':units[0],'hands':units[1:],'market':[]}
            projected=_IMPL.chassis._projected_shed(action,view)
            action['market']=[['SELL',item,projected.get(item,0)] for item in PRODUCTS if projected.get(item,0)>0]
            action['market'].sort(key=lambda o:-view.prices.get(o[1],0)*o[2])
    except Exception:
        _IMPL.chassis.diagnostics['terminal_rescue_errors'] += 1
    return action

# EXP-154 modifications: Ahmed Berat Ozer; public capabilities credited below.
# Dmitrii Gluzdov Seven Turn Rescue and Kaggle engine contributors, Apache-2.0.

_UNIT_NS={"__name__":"v28_own_unit_model"}
exec(__import__('publication_assets').source('policies/observed_56713902_001_004.py', 'text'),_UNIT_NS)
_PLANNER_NS=dict(_UNIT_NS)
exec(__import__('publication_assets').source('policies/observed_56713902_001_005.py', 'text'),_PLANNER_NS)
# EXP-154 integration by Ahmed Berat Ozer, derived from Dmitrii Gluzdov E182.
# The preserved v27 parent is simulated on a private shadow only at step 712.
_PRE_TERMINAL_AGENT=agent
del agent
_TERMINAL_PLANS={}
_TERMINAL_PREVIOUS={}
_UPGRADE_STATS={'planning_calls':0,'accepted':0,'changed_steps':0,'aborted':0,'shadow_declines':0,'errors':0,'max_planning_ms':0.0}
_TERMINAL_SEARCH_MODE = 'expanded_256'  # Options: 'as_is', 'expanded_256', 'disabled'

def _parent_liquidate(farm, private, prices):
    # Exactly v27's final projected DROP ordering, in the planner's private state.
    view=_View({'player':0,'farms':[farm],'private':private,'market':{'prices':prices}},0,_IMPL.chassis.cfg)
    commands=[['DROP'] if _shed_adjacent(pos,view.board) and view.inv(i) else ['PASS'] for i,pos in enumerate(view.positions)]
    action={'farmer':commands[0],'hands':commands[1:],'market':[]}
    stock=_IMPL.chassis._projected_shed(action,view)
    action['market']=[['SELL',item,stock.get(item,0)] for item in PRODUCTS if stock.get(item,0)>0]
    action['market'].sort(key=lambda o:-view.prices.get(o[1],0)*o[2])
    return action

_PLANNER_NS['shop_liquidation']=_parent_liquidate

def _shadow_terminal(obs,config):
    seat=int(obs['player']);chassis=_IMPL.chassis
    state=chassis.players.get(seat)
    if not state or state.get('last_step')!=711 or state.get('route')!=2:
        return None
    # No delayed weed/structure intervention may depend on an unmodeled future.
    if state.get('pending'):
        return None
    shadow=copy.copy(chassis);shadow.players=copy.deepcopy(chassis.players)
    shadow.diagnostics={k:0 for k in chassis.diagnostics}
    projected=copy.deepcopy(obs);baseline=[];states=[]
    for step in range(712,719):
        projected['step']=step;projected['day']=step//24;projected['hour']=step%24
        states.append(copy.deepcopy(shadow.players[seat]))
        action=shadow.act(projected,config)
        if step==718:
            action=_parent_liquidate(projected['farms'][seat],projected['private'],projected['market']['prices'])
        else:
            market=action.get('market',[])
            if len(market)!=9 or {o[1] for o in market}!=set(PRODUCTS) or any(o[0]!='SELL' or len(o)!=3 or type(o[2]) is not int or o[2]<100 for o in market):
                return None
        if any(shadow.diagnostics.values()):return None
        run=_PLANNER_NS['simulate'](projected,config,[action])
        if run['actions'][0]!=action:return None
        baseline.append(action)
        run['farm']['money']=projected['farms'][seat]['money']
        projected['farms'][seat]=run['farm'];projected['private']=run['private']
    return baseline,states

def agent(observation,configuration=None):
    try:
        step=int(observation['step']);seat=int(observation['player'])
    except Exception:
        return _PRE_TERMINAL_AGENT(observation,configuration)
    previous=_TERMINAL_PREVIOUS.get(seat)
    if step==0 or (previous is not None and step<=previous):_TERMINAL_PLANS.pop(seat,None)
    _TERMINAL_PREVIOUS[seat]=step
    plan=_TERMINAL_PLANS.get(seat)
    if plan and plan.get('accepted') and 712<=step<=718:
        if previous!=step-1:plan.update(abandoned=True,reason='nonconsecutive callback')
        try:
            result=_PLANNER_NS['terminal_action'](observation,configuration,plan['baseline'][step-712],plan)
            if plan.get('abandoned'):
                if not plan.get('abort_counted'):
                    plan['abort_counted']=True;_UPGRADE_STATS['aborted']+=1
                if not plan.get('deviated'):
                    _IMPL.chassis.players[seat]=copy.deepcopy(plan['parent_states_before'][step-712])
                    _TERMINAL_PLANS.pop(seat,None)
                    return _PRE_TERMINAL_AGENT(observation,configuration)
            _UPGRADE_STATS['changed_steps']+=int(result!=plan['baseline'][step-712])
            return result
        except Exception:
            _UPGRADE_STATS['errors']+=1
            if plan.get('deviated'):
                try:return _PLANNER_NS['_recover_observed'](observation,configuration,plan['baseline'][step-712],plan)
                except Exception:return _parent_liquidate(observation['farms'][seat],observation['private'],observation['market']['prices'])
    if step!=712:return _PRE_TERMINAL_AGENT(observation,configuration)
    if _TERMINAL_SEARCH_MODE == 'disabled':
        return _PRE_TERMINAL_AGENT(observation,configuration)
    _UPGRADE_STATS['planning_calls']+=1
    try:shadow=_shadow_terminal(observation,configuration)
    except (ValueError,KeyError,TypeError,IndexError):shadow=None
    if shadow is None:
        _UPGRADE_STATS['shadow_declines']+=1
        return _PRE_TERMINAL_AGENT(observation,configuration)
    baseline,states=shadow
    actual=_PRE_TERMINAL_AGENT(observation,configuration)
    if actual!=baseline[0]:
        _UPGRADE_STATS['shadow_declines']+=1;return actual
    try:
        if _TERMINAL_SEARCH_MODE == 'expanded_256':
            plan=_PLANNER_NS['plan_terminal'](observation,configuration,baseline,max_simulations=256,passes=2,proposals_per_actor=12)
        else:
            plan=_PLANNER_NS['plan_terminal'](observation,configuration,baseline,max_simulations=64,passes=1,proposals_per_actor=4)
        _UPGRADE_STATS['max_planning_ms']=max(_UPGRADE_STATS['max_planning_ms'],plan.get('planning_ms',0.0))
        if not plan.get('accepted'):return actual
        plan['parent_states_before']=states;_TERMINAL_PLANS[seat]=plan
        _UPGRADE_STATS['accepted']+=1
        result=_PLANNER_NS['terminal_action'](observation,configuration,actual,plan)
        _UPGRADE_STATS['changed_steps']+=int(result!=actual)
        return result
    except Exception:
        _UPGRADE_STATS['errors']+=1;return actual

agent.telemetry=_UPGRADE_STATS

# EXP-154: aurax7 Reactive v2 day-end storage guard, adapted to our v27 view.
_PRE_ROOM_AGENT=agent
del agent
_ROOM_STATS={'changed_turns':0,'added_units':0,'errors':0}
def agent(observation,configuration=None):
    action=_PRE_ROOM_AGENT(observation,configuration)
    try:
        step=_step_of(observation)
        if step%24!=23:return action
        view=_View(observation,_int(_get(observation,'player',0)),_IMPL.chassis.cfg)
        carried=sum(max(0,int(n)) for inv in view.invs for n in inv.values())
        needed=sum(view.shed.values())+carried-99
        if needed<=0:return action
        planned={}
        for o in action.get('market',[]):
            if o and o[0]=='SELL' and len(o)>=3:planned[o[1]]=planned.get(o[1],0)+max(0,int(o[2]))
        result=copy.deepcopy(action);added=0
        for item in sorted(PRODUCTS,key=lambda it:-int(view.prices.get(it,0))):
            qty=min(needed,max(0,view.shed.get(item,0)-planned.get(item,0)))
            if qty<=0:continue
            if len(result['market'])>=10:break
            result['market'].append(['SELL',item,qty]);needed-=qty;added+=qty
            if needed<=0:break
        if added:_ROOM_STATS['changed_turns']+=1;_ROOM_STATS['added_units']+=added
        return result
    except Exception:
        _ROOM_STATS['errors']+=1;return action

agent.telemetry=_ROOM_STATS

# Incorporated upstream attribution and change notice:
# E182 Shop0909 + terminal physical closure (modified 2026-09-09)
# 
# The active public parent is Yusuke Hayashi's yhay81/shop-router-0909 v3.
# router_parent.py and actions.json are exact original bytes, not newly authored
# routes. The parent credits aurax7's Reactive Router for sale timing and shed
# projection; that attribution remains in router_parent.py. Original payload
# LICENSE.txt is preserved unchanged (Apache License 2.0 text); it contains no
# named copyright grantor and no separate NOTICE was supplied. No additional
# ownership, endorsement, or upstream replay-data rights claim is made.
# 
# Local changes: separate main.py/policy.py adapter; bounded start712 planner
# copied from frozen E180/S78 and modified for seven callbacks, exact Shop final
# liquidation, strict positive physical delivery/sale gain, and observation guards.
# unit_model.py is an unchanged frozen E180 copy of Kaggle's extracted semantics.
# The following original E180 notice is retained verbatim for attribution history.
# Its references to Thomas files describe E180, not files supplied in this Shop
# package: no Thomas tapes, trees or policy are included here.
# 
# ----- Original E180 notice -----
# Kaggriculture: Last-Mile Harvest Planner
# Attribution and change notice
# 
# Thomas Tschinkel is the author of the parent public state-router policy and its
# published decision trees and action-route data. Source: Kaggriculture: 93.8% Win
# Rate Public State Router, notebook version 3, scriptVersionId 347936183:
# https://www.kaggle.com/code/thomastschinkel/kaggriculture-93-8-win-rate-public-state-router?scriptVersionId=347936183
# The public notebook identifies its license as Apache License, Version 2.0.
# Original published main.py SHA-256:
# b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522
# 
# Changes to that source for this distribution: compressed route/tree literals
# were decoded into readable tapes.json and trees.json; a read-only planned_action
# helper was added; descriptive headers and local data loading were adapted.
# The original parent feature extraction, tree traversal and agent behavior are
# retained. These public routes are not claimed as newly authored or trained by
# the notebook distributor.
# 
# unit_model.py contains deterministic unit-action and crop-decay definitions
# extracted from Kaggle's kaggle-environments 1.32.7 Kaggriculture engine, licensed
# under Apache License, Version 2.0. Credit: Kaggle and the kaggle-environments
# contributors. Project: https://github.com/Kaggle/kaggle-environments
# Source file: kaggle_environments/envs/kaggriculture/kaggriculture.py
# Source SHA-256:
# bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
# The extracted unit/decay definitions are not a newly authored game engine;
# market price dynamics and the full interpreter are not part of this module.
# 
# Additional work in this distribution: a bounded last-nine-action collection
# and delivery planner, observation guards and recovery, a settings-consuming
# factory and entry point, standalone examples, and deterministic packaging.
# The full Apache License, Version 2.0 is included as LICENSE.txt.
# No endorsement by Thomas Tschinkel or Kaggle is implied.
# 
# Data provenance limitation: Thomas's source refers to public replay data and
# an upstream provenance.json. That original episode-level manifest, replay IDs
# and individual replay-author identities were not supplied with the public
# notebook/output used here. No names or episode lineage have been invented.
# Notebook-level licensing does not independently establish the missing underlying
# replay-data rights chain. The package supplies usable readable routes, not a
# reproducible reconstruction of their original collection or training process.
# 
# Packaging note: source inputs described as byte-exact above are
# normalized to UTF-8/LF text with a final newline in this standalone
# notebook package. Route JSON values and parent policy behavior are unchanged.

# Final public-entry guard; measured separately and compared on captured observations.
_V28_CORE=agent
del agent
_IMPL.chassis.diagnostics['v28_entry_errors']=0
def agent(observation,configuration=None):
    try:
        return _V28_CORE(observation,configuration)
    except Exception:
        _IMPL.chassis.diagnostics['v28_entry_errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_ROOM_STATS

# EXP-155: prvsiyan V221B finite tomato investment, adapted by Ahmed Berat Ozer.
# Original public source is retained under research24/public; Apache-2.0.
MAX_ORDERS=10
class FarmView(_View):
    def __init__(self,obs):super().__init__(obs,int(obs['player']),_IMPL.chassis.cfg)
    def inventory(self,actor):return self.inv(actor)
def projected_shed(action,view):return _IMPL.chassis._projected_shed(action,view)

CROP_MIN_PRICE=70

# V219: a finite late tomato investment with dedicated, observed workers.
_V219_PARENT = agent
del agent
_V219_FERTILIZE = True  # Builder changes only this flag for the ablation.
_V219_STATES = {}
_V219_REPORT = {'commitments': 0, 'hire_requests': 0, 'confirmed_workers': 0,
                'hire_shortfalls': 0, 'plant_requests': 0, 'confirmed_plants': 0,
                'water_requests': 0, 'fertilize_requests': 0, 'harvest_requests': 0,
                'confirmed_harvest_units': 0, 'drop_requests': 0,
                'tomato_sale_requests': 0, 'budget_declines': 0, 'lost_plants': 0}


def _v219_fib(n):
    a, b = 1, 1
    for _ in range(n): a, b = b, a+b
    return a


def _v219_native_day(native, day):
    tape = _IMPL.chassis.routes[native['route']]
    return tape[day*24:min((day+1)*24,719)]


def _v219_qualifies(obs, native):
    farm=obs['farms'][obs['player']]
    if len(farm['tiles']) != 10 or set(farm['unlocked_quadrants']) != {'NW','NE','SW'}:
        return False
    if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:
        return False
    if sum(s in ('PIZZA_SHOP','FARMERS_MARKET') for s in obs['town']['unlocked_shops']) < 3:
        return False
    if any(farm['tiles'][y][x] != 'LOCKED' for y in (5,6) for x in range(5,10)):
        return False
    if obs['private']['seeds'].get('TOMATO',0) or obs['private']['shed'].get('TOMATO',0):
        return False
    if any(isinstance(t,dict) and t.get('crop')=='TOMATO' for row in farm['tiles'] for t in row):
        return False
    # The investment uses spare land and new worker indices. Avoid taking over
    # any native tomato or land purchase obligation on the known own schedule.
    for tape in _IMPL.chassis.routes.values():
        for a in tape[432:719]:
            if any(o and o[0]=='BUY_LAND' for o in a.get('market',[])):return False
            if any(c==['PLANT','TOMATO'] for c in [a.get('farmer')]+a.get('hands',[])):return False
    return True


def _v219_walk(pos, target):
    x,y=pos;tx,ty=target
    if x != tx:return ['EAST' if x < tx else 'WEST']
    if y != ty:return ['SOUTH' if y < ty else 'NORTH']
    return None


def _v219_home(pos):
    return min(((4,4),(5,4),(4,5),(5,5)),key=lambda p:abs(pos[0]-p[0])+abs(pos[1]-p[1]))


def _v219_request(obs, action, state, native):
    step=int(obs['step']);day=step//24;offset=step%24
    farm=obs['farms'][obs['player']];private=obs['private']
    # If the planting-day transaction could not complete, abandon investment.
    # Later purchases would miss the finite day26..29 production window.
    if not state.get('committed') and day!=18:return action
    if state.get('requested_day')==day:return action
    planned=_v219_native_day(native,day)
    # EXP240: committed crops must wait for the native worker indices.
    # New schedules finish native hiring at hour4 or6. The existing two/three
    # crop-worker groups can still water/harvest their ten cells by midnight.
    # Initial investment stays within hour3; ordinary schedules are unchanged.
    latest_hire=max((i for i,a in enumerate(planned) if any(o and o[0]=='HIRE' for o in a.get('market',[]))),default=-1)
    deadline=6 if state.get('committed') and 3<latest_hire<=6 else 3
    if offset>deadline:return action
    remaining=planned[offset+1:]
    if any(o and o[0]=='HIRE' for a in remaining for o in a.get('market',[])):
        return action
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in action['market'])
    expected=max(len(a.get('hands',[])) for a in planned)
    if len(farm['hands'])+parent_hires != expected:return action
    fertilizer=bool(_V219_FERTILIZE and day in (24,27) and _r79_tomato_fertilizer_worthwhile(obs,action))
    # One watering tour: at most 2 entry moves + 9 between tiles + 10 waters.
    # A hire request by hour2 leaves at least21 callbacks after confirmation.
    crop_workers=1 if day in (19,20,21,22,23,25) and offset<=2 else (3 if 26<=day<=28 else 2)
    labor=_r53_labor_assignment(obs,action,fertilizer)
    if labor is not None:crop_workers=labor['workers']
    count=crop_workers+int(fertilizer and day==27 and labor is None)
    extra=[]
    if not state.get('committed'):
        extra += [['BUY_LAND'],['BUY_SEED','TOMATO',10]]
    fertilizer_quantity=_r70_parent_fert_qty(obs,action,planned,offset) if fertilizer else 0
    if fertilizer:extra.append(['BUY_PRODUCT','FERTILIZER',fertilizer_quantity])
    extra += [['HIRE'] for _ in range(count)]
    if len(action['market'])+len(extra)>MAX_ORDERS:return action
    # No assumed sale proceeds. Reserve 3,000 for parent obligations and price
    # movement; the qualification separately requires 12,000 initial liquidity.
    budget=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+count))
    if not state.get('committed'):budget+=4500
    if fertilizer:budget+=fertilizer_quantity*(obs['market']['prices']['FERTILIZER']+5)
    for order in action['market']:
        if not order:continue
        if order[0]=='BUY_PRODUCT':budget+=int(order[2])*(int(obs['market']['prices'][order[1]])+10)
        elif order[0]=='BUY_ANIMAL':budget+=int(order[2])*{'COW':400,'SHEEP':500,'GOOSE':300}[order[1]]
        elif order[0]=='BUY_SEED':budget+=int(order[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[order[1]]
    if farm['money']<budget+3000:
        _V219_REPORT['budget_declines']+=1;return action
    state['pending']={'step':step,'first_actor':expected+1,'count':count,'crop_workers':crop_workers,'fertilizer':fertilizer,'labor':labor}
    if labor is not None:
        _R53_LABOR_REPORT['labor_requests']+=1;_R53_LABOR_REPORT['labor_hires_avoided']+=1;_R53_LABOR_REPORT['labor_day'+str(day)]+=1
    state['requested_day']=day
    _V219_REPORT['hire_requests']+=count
    if not state.get('committed'):
        state['committed']=True;_V219_REPORT['commitments']+=1
    changed=copy.deepcopy(action);changed['market']+=extra
    return changed


def _v219_worker(obs, state, actor, role):
    day=int(obs['step'])//24;step=int(obs['step']);view=FarmView(obs)
    pos=tuple(view.positions[actor]);inv=view.inventory(actor)
    targets=role['targets']
    # Actual cargo differences, observed on the next callback, verify harvests.
    previous=state['last_work'].get(actor)
    if previous and previous['step']==step-1 and previous['command']==['HARVEST']:
        _V219_REPORT['confirmed_harvest_units']+=max(0,int(inv.get('TOMATO',0))-previous['tomatoes'])
    if role.get('needs_fertilizer') and not role.get('loaded'):
        home=_v219_home(pos)
        walk=_v219_walk(pos,home)
        if walk:return walk
        desired=role.get('fertilizer_quantity',10 if role['kind']=='fertilizer' else 5)
        if inv.get('FERTILIZER',0)>=desired:role['loaded']=True
        elif role.get('pickup_requested'):
            # Never spend repeated turns waiting for stock that was not bought.
            role['loaded']=True;role['fertilizer_available']=int(inv.get('FERTILIZER',0))
        elif view.shed.get('FERTILIZER',0)>=desired:
            role['pickup_requested']=True;return ['PICKUP','FERTILIZER',desired]
        else:role['loaded']=True
    todo=[]
    for target in targets:
        x,y=target;tile=view.tiles[y][x]
        tomato=isinstance(tile,dict) and tile.get('crop')=='TOMATO'
        if tomato and target not in state['seen_plants']:
            state['seen_plants'].add(target);_V219_REPORT['confirmed_plants']+=1
        if target in state['seen_plants'] and not tomato and target not in state['lost']:
            state['lost'].add(target);_V219_REPORT['lost_plants']+=1
        command=None
        if role['kind']=='fertilizer':
            if tomato and tile.get('fertilized_until_day',-1)<day+2 and inv.get('FERTILIZER',0)>0:
                command=['FERTILIZE']
        elif day==18 and not tomato:
            if tile is None and obs['private']['seeds'].get('TOMATO',0)>0:command=['PLANT','TOMATO']
            elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif tomato:
            # No later production follows the final day, so watering then would
            # consume time needed to harvest and deliver the final cargo.
            if day<29 and not tile.get('watered_today'):command=['WATER']
            elif role.get('needs_fertilizer') and tile.get('fertilized_until_day',-1)<day+2 and inv.get('FERTILIZER',0)>0:
                command=['FERTILIZE']
            elif tile.get('yield_units',0)>0:command=['HARVEST']
        if command:todo.append((target,command))
    # Final return has priority once only the exact distance plus DROP remains.
    home=_v219_home(pos);distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    if step>=718-distance and inv.get('TOMATO',0):
        return _v219_walk(pos,home) or ['PLACE','TOMATO',int(inv.get('TOMATO',0))]
    if todo:
        target,command=min(todo,key=lambda v:(abs(pos[0]-v[0][0])+abs(pos[1]-v[0][1]),targets.index(v[0])))
        return _v219_walk(pos,target) or command
    if inv.get('TOMATO',0):return _v219_walk(pos,home) or ['PLACE','TOMATO',int(inv['TOMATO'])]
    if any(inv.values()):return _v219_walk(pos,home) or ['DROP']
    return ['PASS']


def agent(observation, configuration=None):
    action=_V219_PARENT(observation,configuration)
    step=int(observation['step']);player=int(observation['player']);day=step//24
    state=_V219_STATES.get(player)
    if state is None or step<=state['last_step']:
        state={'last_step':step,'day':-1,'workers':{},'last_work':{},'seen_plants':set(),'lost':set(),
               'targets':[(x,y) for y in (5,6) for x in range(5,10)]}
        _V219_STATES[player]=state
    state['last_step']=step
    native=_IMPL.chassis.players[player]
    if step==432:state['eligible']=_v219_qualifies(observation,native)
    if not state.get('eligible') or day<18:return action
    if state['day']!=day:
        state['day']=day;state['workers']={};state['last_work']={}
    farm=observation['farms'][player]
    pending=state.pop('pending',None)
    if pending:
        if len(farm['hands'])+1 >= pending['first_actor']+pending['count'] and 'SE' in farm['unlocked_quadrants']:
            for index in range(pending['count']):
                fertilizer_worker=index==pending['crop_workers']
                if fertilizer_worker:targets=state['targets']
                elif pending['crop_workers']==1:targets=state['targets']
                elif pending['crop_workers']==2:targets=state['targets'][index*5:index*5+5]
                else:targets=[[(5,5),(6,5),(7,5)],[(8,5),(9,5),(9,6),(8,6)],[(5,6),(6,6),(7,6)]][index]
                state['workers'][pending['first_actor']+index]={'kind':'fertilizer' if fertilizer_worker else 'crop','targets':targets,
                    'needs_fertilizer':pending['fertilizer'] and (day==24 or fertilizer_worker)}
                if pending.get('labor') is not None:
                    role=state['workers'][pending['first_actor']+index]
                    role['targets']=[tuple(p) for p in pending['labor']['paths'][index]]
                    role['needs_fertilizer']=pending['labor']['fertilizer'];role['fertilizer_quantity']=len(role['targets'])
                    if tuple(farm['hands'][pending['first_actor']+index-1])!=tuple(pending['labor']['spawns'][index]):_R53_LABOR_REPORT['labor_spawn_errors']+=1
                    if index==0:_R53_LABOR_REPORT['labor_confirmed']+=1
            _V219_REPORT['confirmed_workers']+=pending['count']
        else:_V219_REPORT['hire_shortfalls']+=pending['count']
    action=_v219_request(observation,action,state,native)
    if state['workers']:
        commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
        commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
        for actor,role in state['workers'].items():
            if actor>=len(commands):continue
            command=_v219_worker(observation,state,actor,role)
            commands[actor]=command
            name={'PLANT':'plant_requests','WATER':'water_requests','FERTILIZE':'fertilize_requests',
                  'HARVEST':'harvest_requests','DROP':'drop_requests'}.get(command[0])
            if name:_V219_REPORT[name]+=1
            state['last_work'][actor]={'step':step,'command':command,'tomatoes':observation['private']['inventories'][actor].get('TOMATO',0)}
        action=copy.deepcopy(action);action['farmer'],action['hands']=commands[0],commands[1:]
    if state.get('committed') and len(action['market'])<MAX_ORDERS and not any(o[:2]==['SELL','TOMATO'] for o in action['market']):
        quantity=projected_shed(action,FarmView(observation)).get('TOMATO',0)
        if quantity>0:
            action=copy.deepcopy(action);action['market'].append(['SELL','TOMATO',quantity])
            _V219_REPORT['tomato_sale_requests']+=quantity
    return action


agent.telemetry=_V219_REPORT

# V221B: labor-only ablation of frozen V219G; not yet publicly scored.


# Crop workers own their final routes after commitment. A private parent shadow
# does not contain these obligations, so terminal rescue must abstain there.
_ORIGINAL_SHADOW_TERMINAL=_shadow_terminal
def _shadow_terminal(obs,config):
    if _V219_STATES.get(int(obs['player']),{}).get('committed'):return None
    return _ORIGINAL_SHADOW_TERMINAL(obs,config)

APPLY_TIMING=False

_EXPERIMENT_PARENT=agent
del agent
_V219_REPORT['extra_fertilizer_days']=0
_V219_REPORT['reordered_market_turns']=0
_V219_REPORT['errors']=0
def agent(observation,configuration=None):
    try:
        action=_EXPERIMENT_PARENT(observation,configuration)
        if APPLY_TIMING and int(observation['step'])>=144:action=_v224_sales_first(action)
        return action
    except Exception:
        _V219_REPORT['errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_V219_REPORT

def _v224_sales_first(action):
    original=action.get('market',[])[:MAX_ORDERS]
    orders=[list(o) for o in original if o and (o[0] in ('HIRE','BUY_LAND') or (len(o)>=3 and int(o[2])>0))]
    for index in range(len(orders)):
        order=orders[index]
        if order[0]!='SELL':continue
        cursor=index
        while cursor>0:
            previous=orders[cursor-1]
            if previous[0]=='SELL':break
            if previous[0] in ('BUY_PRODUCT','BUY_ANIMAL') and previous[1]==order[1]:break
            orders[cursor-1],orders[cursor]=orders[cursor],orders[cursor-1]
            cursor-=1
    if orders==original:return action
    _V219_REPORT['reordered_market_turns']+=1
    changed=copy.deepcopy(action);changed['market']=orders
    return changed
_ORDER_PARENT=agent
del agent

def agent(observation,configuration=None):
    try:
        action=_ORDER_PARENT(observation,configuration)
        if int(observation["step"])>=144:action=_v224_sales_first(action)
        return action
    except Exception:
        _V219_REPORT["errors"]+=1
        return {"farmer":["PASS"],"hands":[],"market":[]}
agent.telemetry=_V219_REPORT

_V31_CORE=agent
del agent
_IMPL.chassis.diagnostics['production_errors']=0
_IMPL.chassis.diagnostics['v31_entry_errors']=0
def agent(observation,configuration=None):
    before=_V219_REPORT['errors']
    try:
        action=_V31_CORE(observation,configuration)
        _IMPL.chassis.diagnostics['production_errors']+=_V219_REPORT['errors']-before
        return action
    except Exception:
        _IMPL.chassis.diagnostics['v31_entry_errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_V219_REPORT

# Apache-2.0; later cattle transfer from prvsiyan, Moon (2026-09-10).
# Bounded livestock substitution; confirm owned animals before redirecting workers.
_V231_PARENT=agent
_V231_CAP=4
_V231_STATES={}
_V231_REPORT={}

def _v231_new_state():
    return {'last':-1,'confirmed':0,'reserved':0,'pending_buy':None,
            'carrying':{},'pending_places':[],'sites':{},'milk_credit':0,
            'requested':0,'failed_purchase_units':0,'picked':0,'placed':0,
            'failed_placements':0,'extra_milk_harvested':0,'extra_milk_sale_requests':0}

def _v231_controller(obs,action,state,cap):
    step=int(obs['step']);seat=int(obs['player']);farm=obs['farms'][seat]
    private=obs['private'];shed=private['shed'];inventories=private['inventories']
    positions=[farm['farmer'],*farm['hands']]
    pending=state['pending_buy']
    if pending is not None:
        gained=max(0,int(shed.get('COW',0))-pending['before'])
        confirmed=min(pending['quantity'],gained)
        state['confirmed']+=confirmed;state['reserved']+=confirmed
        state['failed_purchase_units']+=pending['quantity']-confirmed
        state['pending_buy']=None
    for pending in state['pending_places']:
        x,y=pending['site'];tile=farm['tiles'][y][x]
        if (isinstance(tile,dict) and tile.get('animal')=='COW'
                and tile.get('placed_day')==pending['day']):
            state['sites'][(x,y)]=pending['day'];state['placed']+=1
            actor=pending['actor'];state['carrying'][actor]=max(0,state['carrying'].get(actor,0)-1)
        else:state['failed_placements']+=1
    state['pending_places']=[]
    state['last']=step
    result=copy.deepcopy(action)
    workers=[result.get('farmer') or ['PASS'],*(result.get('hands') or [])]
    seen_harvest=set();cow_available=int(shed.get('COW',0));occupied=set()
    for actor,work in enumerate(workers[:len(positions)]):
        inventory=inventories[actor] if actor<len(inventories) else {}
        x,y=positions[actor];tile=farm['tiles'][y][x];site=(x,y)
        if (work==['HARVEST'] and site in state['sites'] and site not in seen_harvest
                and isinstance(tile,dict) and tile.get('animal')=='COW'
                and tile.get('placed_day')==state['sites'][site]):
            units=max(0,int(tile.get('yield_units',0)))
            state['milk_credit']+=units;state['extra_milk_harvested']+=units
            seen_harvest.add(site)
        if len(work)>=2 and work[:2]==['PICKUP','SHEEP']:
            quantity=max(0,int(work[2]) if len(work)>2 else 1)
            center=len(farm['tiles'])//2
            if (quantity and state['reserved']>=quantity and cow_available>=quantity
                    and x in (center-1,center) and y in (center-1,center)
                    and not any(inventory.get(a,0) for a in ('COW','SHEEP','GOOSE'))):
                work[1]='COW';state['reserved']-=quantity;cow_available-=quantity
                state['carrying'][actor]=state['carrying'].get(actor,0)+quantity
                state['picked']+=quantity
        if (len(work)>=2 and work[:2]==['PLACE','SHEEP']
                and state['carrying'].get(actor,0)>0 and inventory.get('COW',0)>0
                and isinstance(tile,dict) and tile.get('kind')=='PASTURE'
                and 'animal' not in tile and site not in occupied):
            work[1]='COW'
            state['pending_places'].append({'actor':actor,'site':site,'day':step//24})
        if (len(work)>=2 and work[0]=='PLACE' and work[1] in ('COW','SHEEP','GOOSE')
                and inventory.get(work[1],0)>0):occupied.add(site)
    result['farmer'],result['hands']=workers[0],workers[1:]
    market=result.get('market',[])
    animal_orders=[o for o in market if len(o)>=3 and o[0]=='BUY_ANIMAL']
    shops=obs['town']['unlocked_shops'];prices=obs['market']['prices']
    counts={'COW':0,'SHEEP':0}
    for line in farm['tiles']:
        for tile in line:
            if isinstance(tile,dict) and tile.get('animal') in counts:counts[tile['animal']]+=1
    cargo=sum(int(inv.get(a,0)) for inv in inventories for a in ('COW','SHEEP','GOOSE'))
    stock_animals=sum(int(shed.get(a,0)) for a in ('COW','SHEEP','GOOSE'))
    milk_shops=sum(shop in ('PIZZA_SHOP','ICE_CREAM_SHOP','SMOOTHIE_SHOP') for shop in shops)
    if (216<=step<=227 and len(shops)>=3 and state['confirmed']<cap and not state['reserved']
            and not any(state['carrying'].values()) and not state['pending_places']
            and not cargo and not stock_animals and len(animal_orders)==1
            and animal_orders[0][1]=='SHEEP' and milk_shops>=2 and 'YARN_STORE' not in shops
            and int(prices.get('MILK',0))>=int(prices.get('WOOL',0))
            and counts['COW']>=4 and counts['SHEEP']>=2):
        order=animal_orders[0];quantity=int(order[2])
        if 1<=quantity<=2 and quantity<=cap-state['confirmed']:
            order[1]='COW';state['requested']+=quantity
            state['pending_buy']={'before':int(shed.get('COW',0)),'quantity':quantity}
    # Sell only additional physically harvested production at an existing sale slot.
    if state['milk_credit']>0:
        stock=projected_shed(result,FarmView(obs))
        total_planned=sum(max(0,int(o[2])) for o in market if len(o)>=3 and o[:2]==['SELL','MILK'])
        extra=min(state['milk_credit'],max(0,int(stock.get('MILK',0))-total_planned))
        if extra:
            for order in market:
                if len(order)>=3 and order[:2]==['SELL','MILK'] and int(order[2])>0:
                    order[2]=int(order[2])+extra
                    state['milk_credit']-=extra;state['extra_milk_sale_requests']+=extra
                    break
    result['market']=market
    return result

def agent(observation,configuration=None):
    step=int(observation['step']);seat=int(observation['player'])
    state=_V231_STATES.get(seat)
    if state is None or step<=state['last']:
        state=_V231_STATES[seat]=_v231_new_state()
    action=_V231_PARENT(observation,configuration)
    action=_v231_controller(observation,action,state,_V231_CAP)
    _V231_REPORT.clear();_V231_REPORT.update(_V231_PARENT.telemetry)
    for name in ('confirmed','reserved','requested','failed_purchase_units','picked','placed',
                 'failed_placements','extra_milk_harvested','extra_milk_sale_requests','milk_credit'):
        _V231_REPORT['cattle_'+name]=state[name]
    _V231_REPORT['cattle_carried_pending']=sum(state['carrying'].values())
    return action

agent.telemetry=_V231_REPORT


# EXP-167, adapted from Dmitrii Gluzdov's Two Coins, One Sheep (Apache-2.0).
# Reserve only physically available stock after the final parent worker actions.
_R36_SALE_PARENT=agent
_R36_NATIVE_LEAD=Chassis._sell_lead
_R36_NATIVE_SUPPRESS=Chassis._apply_suppression
_R36_SALE_REPORT={}

def _r36_native_lead(self,action,view,projected,route,step,next_sup):
    if step<288 or step>=696:
        return _R36_NATIVE_LEAD(self,action,view,projected,route,step,next_sup)

def _r36_suppress(action,state,step):
    _R36_NATIVE_SUPPRESS(action,state,step)
    due=state.get('r36_debts',{}).pop(step,{})
    for order in action.get('market',[]):
        if len(order)>=3 and order[0]=='SELL':
            removed=min(max(0,int(order[2])),due.get(order[1],0))
            order[2]-=removed
            due[order[1]]=due.get(order[1],0)-removed

Chassis._sell_lead=_r36_native_lead
Chassis._apply_suppression=staticmethod(_r36_suppress)

def _r36_reserve(obs,action):
    step=int(obs['step'])
    # The final planner forecasts its own parent, so keep its full window native.
    if not 192<=step<696:return action
    native=_IMPL.chassis.players[int(obs['player'])]
    tape=_IMPL.chassis.routes[native['route']]
    _v9_hz=_V9_ITEM_HZ.get(int(obs['player']))
    end=min(695,step+(max(_v9_hz.values()) if _v9_hz else _R37_HORIZONS.get(int(obs['player']),2)))
    if end<=step:return action
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    view=FarmView(obs)
    # This projection intentionally abstains on ambiguous animal depot returns.
    if any(len(c)>1 and c[0]=='PLACE' and c[1] in ANIMAL_STRUCTURE
           and view.inv(i).get(c[1],0)>0 for i,c in enumerate(commands[:len(view.positions)])):
        return action
    stock=projected_shed(action,view)
    market=action.get('market',[])
    blocked={o[1] for o in market if len(o)>1 and o[0] in ('SELL','BUY_PRODUCT')}
    blocked.update(c[1] for c in commands if len(c)>1 and c[0]=='PICKUP')
    blocked.update(c[1] for queue in native['pending'].values() for pos,c in queue
                   if len(c)>1 and c[0]=='PICKUP')
    debts=native['sell_state'].setdefault('r36_debts',{})
    for item in PRODUCTS:
        if item in blocked or view.prices.get(item,0)<2:continue
        available=max(0,int(stock.get(item,0)))
        if not available or len(market)>=10:continue
        reservations=[]
        item_end=min(end,step+_v9_hz[item]) if _v9_hz and item in _v9_hz else end
        for due_step in range(step+1,item_end+1):
            future=tape[due_step]
            work=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
            if any(len(c)>1 and c[:2]==['PICKUP',item] for c in work):break
            if any(len(o)>1 and o[:2]==['BUY_PRODUCT',item] for o in future.get('market',[])):break
            planned=sum(max(0,int(o[2])) for o in future.get('market',[]) if len(o)>=3 and o[:2]==['SELL',item])
            amount=min(available,max(0,planned-debts.get(due_step,{}).get(item,0)))
            if amount:
                reservations.append((due_step,amount));available-=amount
            if not available:break
        qty=sum(q for _,q in reservations)
        if qty:
            market.append(['SELL',item,qty])
            for due,q in reservations:
                debt=debts.setdefault(due,{})
                debt[item]=debt.get(item,0)+q
            _R36_SALE_REPORT['sale_reserved_units']+=qty
            _R36_SALE_REPORT['sale_reservations']+=1
    return action

def agent(observation,configuration=None):
    if int(observation.get('step',0))==0:
        _R36_SALE_REPORT.update(sale_reserved_units=0,sale_reservations=0,sale_errors=0)
    action=_R36_SALE_PARENT(observation,configuration)
    try:
        if configuration is None or all(configuration.get(k,v)==v for k,v in
            [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
            action=_r36_reserve(observation,action)
            if int(observation['step'])>=288:action=_v224_sales_first(action)
    except Exception:
        _R36_SALE_REPORT['sale_errors']=_R36_SALE_REPORT.get('sale_errors',0)+1
    _R36_SALE_REPORT.update(_R36_SALE_PARENT.telemetry)
    return action

agent.telemetry=_R36_SALE_REPORT

# Ensure the Kaggle-selected final callable is the exported policy.
agent = globals().pop("agent")


# Public capability transfer: lucifer19; Flexon is the same Two Coins asset set.
# Apache-2.0; exact functions from Kaggle kaggle-environments 1.32.7.
# https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture
import math
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

def _r37_similarity(observation):
    """Empty tiles cannot make two unrelated production layouts look alike."""
    farms = observation['farms']
    own, rival = farms[observation['player']], farms[1-observation['player']]
    if own['unlocked_quadrants'] != rival['unlocked_quadrants']:
        return 0.0
    matches = total = 0
    for a, b in zip([t for row in own['tiles'] for t in row],
                    [t for row in rival['tiles'] for t in row]):
        sa = (a.get('crop'), a.get('animal')) if isinstance(a, dict) else (None, None)
        sb = (b.get('crop'), b.get('animal')) if isinstance(b, dict) else (None, None)
        if sa != (None, None) or sb != (None, None):
            total += 1
            matches += sa == sb
    return matches / total if total >= 8 else 0.0


def _r37_quote_priority(observation, order, stock):
    """Revenue exposed to a small rival batch, not nominal headline revenue."""
    item = order[1]
    quantity = min(max(0, int(order[2])), stock.get(item, 0))
    if not quantity or item not in _R37_MARKET_PARAMS:
        return 0.0
    inventory = observation['market']['inventory'][item]
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for k, patch in observation['market'].get('params', {}).items():
        if k in params:
            params[k].update(patch)
    rival = observation['farms'][1-observation['player']]
    crop_item = item if item in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON') else None
    animal = {'EGG':'GOOSE','MILK':'COW','WOOL':'SHEEP'}.get(item)
    standing = sum(max(0, int(t.get('yield_units', 0))) for row in rival['tiles'] for t in row
                   if isinstance(t, dict) and
                   ((crop_item is not None and t.get('crop') == crop_item) or
                    (animal is not None and t.get('animal') == animal)))
    # Public fields do not reveal the rival shed. Eight units are a scenario,
    # not a recovered hidden quantity; visible ripe yield increases the stress.
    batch = min(24, max(8, standing))
    now = sum(_r37_market_price(item, inventory+j, params) for j in range(quantity))
    later = sum(_r37_market_price(item, inventory+batch+j, params) for j in range(quantity))
    return now-later


def _r37_reorder_sales(observation, action):
    """Keep quantities and purchase barriers; rank distinct contiguous sales."""
    stock = projected_shed(action, FarmView(observation))
    orders = [list(o) for o in action['market']]
    start = 0
    while start < len(orders):
        if orders[start][0] != 'SELL':
            start += 1
            continue
        end = start
        while end < len(orders) and orders[end][0] == 'SELL':
            end += 1
        block = orders[start:end]
        if len({o[1] for o in block}) == len(block):
            orders[start:end] = sorted(block, key=lambda o: _r37_quote_priority(observation, o, stock), reverse=True)
        start = end
    if orders != action['market']:
        _R37_STATS['quote_reordered_turns'] += 1
        action = dict(action, market=orders)
    return action



# EXP175: bounded public cash-response probe inspired by leoprovorov,
# Two Coins Mirror Counter v1 (Apache-2.0). No hidden rival inventory.
_R44_PROBES={}
_R44_REPORT=dict(probe_matches=0,probe_four_turn_calls=0,probe_errors=0)

def _r44_before(obs):
    player=int(obs['player']);step=int(obs['step'])
    st=_R44_PROBES.get(player)
    if st is None or step<=st['step']:
        st=_R44_PROBES[player]={'step':-1,'money':None,'probe':0,'matched':False}
    if step==0:_R44_REPORT.update(probe_matches=0,probe_four_turn_calls=0,probe_errors=0)
    money=tuple(float(obs['farms'][i]['money']) for i in (player,1-player))
    if st['money'] is not None and st['probe']>=100 and _r37_similarity(obs)>=.90:
        own=money[0]-st['money'][0];rival=money[1]-st['money'][1]
        if own>0 and rival>0 and abs(own-rival)<=max(5.0,.05*st['probe']):
            if not st['matched']:_R44_REPORT['probe_matches']+=1
            st['matched']=True
    st.update(step=step,money=money,probe=0)
    return st

def _r44_after(obs,action,st):
    step=int(obs['step']);player=int(obs['player'])
    if not 336<=step<648 or st['matched']:return
    # Positive all-sale probes avoid mistaking equal spending for preemption.
    if not action['market'] or any(o and o[0]!='SELL' for o in action['market']):return
    debts=_IMPL.chassis.players[player]['sell_state'].get('r36_debts',{})
    own=debts.get(step+3,{})
    if own:st['probe']=sum(max(0,int(n))*int(obs['market']['prices'].get(item,0)) for item,n in own.items())

_R37_ADAPTIVE = True
_R37_QUOTE = True
# EXP-168: adapted from lucifer19 / Harvest Nocturne, Apache-2.0.
# All rivalry features use public occupied tiles; no private rival inventory.
_R37_PARENT = agent
_R37_PLAYERS = {}
_R37_HORIZONS = {}
_V9_ITEM_HZ = {}
_R37_REPORT = {}
_R37_STATS = dict(quote_reordered_turns=0, three_turn_calls=0, nocturne_errors=0)
del agent

def agent(observation, configuration=None):
    player, step = int(observation['player']), int(observation['step'])
    state = _R37_PLAYERS.get(player)
    if state is None or step <= state['step']:
        state = _R37_PLAYERS[player] = {'step': -1, 'streak': 0}
    if step == 0:
        _R37_STATS.update(quote_reordered_turns=0, three_turn_calls=0, nocturne_errors=0)
    state['step'] = step
    _R37_HORIZONS[player] = 2
    probe_state=_r44_before(observation)
    try:
        if _R37_ADAPTIVE and step < 648:
            state['streak'] = state['streak'] + 1 if _r37_similarity(observation) >= .90 else 0
            if 336 <= step < 648 and state['streak'] >= 6:
                _R37_HORIZONS[player] = 3
                _R37_STATS['three_turn_calls'] += 1
    except Exception:
        _R37_STATS['nocturne_errors'] += 1
    if _R37_HORIZONS[player]==3 and probe_state['matched']:
        _R37_HORIZONS[player]=4
        _R44_REPORT['probe_four_turn_calls']+=1
    # EXP179: four-turn reservation; retain stock, debt and purchase barriers.
    if 288 <= step < 696:_R37_HORIZONS[player] = 4
    action = _R37_PARENT(observation, configuration)
    _r44_after(observation,action,probe_state)
    if _R37_QUOTE and step >= 288:
        try:
            action = _r37_reorder_sales(observation, action)
        except Exception:
            _R37_STATS['nocturne_errors'] += 1
    _R37_REPORT.update(getattr(_R37_PARENT, 'telemetry', {}))
    _R37_REPORT.update(_R37_STATS)
    _R37_REPORT.update(_R44_REPORT)
    return action

agent.telemetry = _R37_REPORT

# Export guard: normal decisions stay identical to the frozen screened policy.
_RELEASE_PARENT=agent
_RELEASE_REPORT={}
_RELEASE_ERRORS=0
del agent

def agent(observation,configuration=None):
    global _RELEASE_ERRORS
    try:
        result=_RELEASE_PARENT(observation,configuration)
    except Exception:
        _RELEASE_ERRORS+=1
        count=0
        try:
            count=min(64,len(observation['farms'][int(observation['player'])]['hands']))
        except Exception:
            pass
        result={'farmer':['PASS'],'hands':[['PASS'] for _ in range(count)],'market':[]}
    _RELEASE_REPORT.update(getattr(_RELEASE_PARENT,'telemetry',{}))
    _RELEASE_REPORT['release_errors']=_RELEASE_ERRORS
    return result

agent.telemetry=_RELEASE_REPORT
agent=globals().pop('agent')

# Adapted from prvsiyan / The Soil Remembers Rain, Apache-2.0.
# V233: bounded, financed six-sheep SE discovery investment.
_V233_PARENT=agent
del agent
_V233_STATES={}
_V233_REPORT=dict(sheep_commit_requests=0,sheep_committed=0,sheep_hire_requests=0,
    sheep_workers_confirmed=0,sheep_hire_shortfalls=0,sheep_budget_declines=0,
    sheep_capacity_declines=0,sheep_purchase_shortfalls=0,sheep_feed_buy_requests=0,
    sheep_wool_harvested=0,sheep_fert_collected=0,sheep_extra_wool_sales=0,
    sheep_extra_fert_sales=0,sheep_rescue_feed_requests=0)

def _v233_eligible(obs,native):
    farm=obs['farms'][obs['player']];prices=obs['market']['prices']
    if len(farm['tiles'])!=10 or set(farm['unlocked_quadrants'])!={'NW','NE','SW'}:return False
    if obs['town']['unlocked_shops'].count('YARN_STORE')<2 or prices['WOOL']<220 or prices['WHEAT']>45:return False
    if any(farm['tiles'][y][x]!='LOCKED' for y in (5,6) for x in range(5,8)):return False
    if obs['private']['shed'].get('SHEEP',0) or any(i.get('SHEEP',0) for i in obs['private']['inventories']):return False
    for day in range(12,30):
        for a in _v219_native_day(native,day):
            if any(o and (o[0]=='BUY_LAND' or o[:2]==['BUY_ANIMAL','SHEEP']) for o in a.get('market',[])):return False
            if any(c and c[0] in ('PICKUP','PLACE') and len(c)>1 and c[1]=='SHEEP' for c in [a.get('farmer')]+a.get('hands',[])):return False
    return True

def _v233_request(obs,action,state,native):
    step=int(obs['step']);day=step//24;hour=step%24
    # EXP242: preserve native indices while servicing already committed sheep.
    if state.get('requested_day')==day:return action
    committed=state.get('committed')
    if not committed and (hour>(3 if day==11 else 1) or day not in (11,12) or not _v233_eligible(obs,native)):return action
    planned=_v219_native_day(native,day)
    deadline=2 if committed else (3 if day==11 else 1)
    if committed:
        last_native_hire=max((h for h,a in enumerate(planned) if any(o and o[0]=='HIRE' for o in a.get('market',[]))),default=0)
        if 2<last_native_hire<=6:deadline=6
    if hour>deadline:return action
    if any(o and o[0]=='HIRE' for a in planned[hour+1:] for o in a.get('market',[])):return action
    farm=obs['farms'][obs['player']];market=action.get('market',[])
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in market)
    expected=max(len(a.get('hands',[])) for a in planned)
    if len(farm['hands'])+parent_hires!=expected:return action
    initial=not state.get('committed')
    extra=([['BUY_LAND'],['BUY_ANIMAL','SHEEP',6]] if initial else [])+[['BUY_PRODUCT','WHEAT',6],['HIRE'],['HIRE']]
    if len(market)+len(extra)>MAX_ORDERS:return action
    stock=projected_shed(action,FarmView(obs))
    incoming=6+6*initial
    budget=7000*initial+6*(int(obs['market']['prices']['WHEAT'])+10)
    budget+=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+2))
    for o in market:
        if not o:continue
        if o[0]=='BUY_LAND':return action
        if o[0]=='BUY_PRODUCT':
            incoming+=int(o[2]);budget+=int(o[2])*(int(obs['market']['prices'][o[1]])+10)
        elif o[0]=='BUY_ANIMAL':
            incoming+=int(o[2]);budget+=int(o[2])*{'SHEEP':500,'COW':400,'GOOSE':300}[o[1]]
        elif o[0]=='BUY_SEED':budget+=int(o[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[o[1]]
    if sum(stock.values())+incoming>100:
        _V233_REPORT['sheep_capacity_declines']+=1;return action
    if farm['money']<budget+(3000 if initial else 1000):
        _V233_REPORT['sheep_budget_declines']+=1;return action
    state['requested_day']=day
    state['pending']={'first':expected+1,'initial':initial}
    _V233_REPORT['sheep_hire_requests']+=2;_V233_REPORT['sheep_feed_buy_requests']+=6
    if initial:_V233_REPORT['sheep_commit_requests']+=1
    result=copy.deepcopy(action);result['market']=market+extra
    return result

def _v233_worker(obs,actor,targets):
    farm=obs['farms'][obs['player']];private=obs['private'];step=int(obs['step'])
    pos=tuple(farm['hands'][actor-1]);inv=private['inventories'][actor]
    access=((4,4),(5,4),(4,5),(5,5))
    home=min(access,key=lambda p:(abs(pos[0]-p[0])+abs(pos[1]-p[1]),p))
    distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    cargo=[item for item in ('WOOL','FERTILIZER') if inv.get(item,0)]
    if cargo and step%24 >= (22 if step//24==29 else 23)-distance:
        return _v219_walk(pos,home) or ['PLACE',cargo[0],inv[cargo[0]]]
    missing=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP') for x,y in targets)
    if missing and not inv.get('SHEEP',0) and private['shed'].get('SHEEP',0):
        return _v219_walk(pos,home) or ['PICKUP','SHEEP',min(missing,private['shed']['SHEEP'])]
    hungry=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('fed_today')) for x,y in targets)
    if hungry and not inv.get('WHEAT',0) and private['shed'].get('WHEAT',0):
        return _v219_walk(pos,home) or ['PICKUP','WHEAT',min(hungry,private['shed']['WHEAT'])]
    tasks=[]
    for target in targets:
        x,y=target;tile=farm['tiles'][y][x];command=None
        if tile is None:command=['BUILD_PASTURE']
        elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif isinstance(tile,dict) and tile.get('kind')=='PASTURE' and not tile.get('animal'):
            if inv.get('SHEEP',0):command=['PLACE','SHEEP']
        elif isinstance(tile,dict) and tile.get('animal')=='SHEEP':
            if not tile['fed_today'] and inv.get('WHEAT',0):command=['FEED']
            elif not tile['cared_today']:command=['CARE']
            elif tile['yield_units']:command=['HARVEST']
            elif tile['fertilizer_available']:command=['COLLECT_FERTILIZER']
        if command:tasks.append((abs(pos[0]-x)+abs(pos[1]-y),targets.index(target),target,command))
    if tasks:
        _,_,target,command=min(tasks);return _v219_walk(pos,target) or command
    if cargo:return _v219_walk(pos,home) or ['PLACE',cargo[0],inv[cargo[0]]]
    return ['PASS']

def _v234_rescue(obs,action,state):
    if not state['workers'] or int(obs['step'])%24>14:return action
    orders=action.get('market',[])
    if len(orders)>=MAX_ORDERS:return action
    if any(o and (o[0] in ('HIRE','BUY_LAND','BUY_ANIMAL','BUY_PRODUCT','BUY_SEED') or (len(o)>1 and o[1]=='WHEAT')) for o in orders):return action
    farm=obs['farms'][obs['player']];private=obs['private'];hungry=carried=0
    commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
    for actor,targets in state['workers'].items():
        command=commands[actor]
        if command==['FEED'] or command[:2]==['PICKUP','WHEAT']:return action
        carried+=private['inventories'][actor].get('WHEAT',0)
        hungry+=sum(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP' and not farm['tiles'][y][x].get('fed_today') for x,y in targets)
    stock=projected_shed(action,FarmView(obs))
    shortage=hungry-carried-stock.get('WHEAT',0)
    if not 0<shortage<=6 or state.get('rescue_today',0)+shortage>6:return action
    quote=int(obs['market']['prices']['WHEAT'])
    if quote<1 or farm['money']<1000+shortage*(quote+10) or sum(stock.values())+shortage>100:return action
    result=copy.deepcopy(action);result['market'].append(['BUY_PRODUCT','WHEAT',shortage])
    state['rescue_today']=state.get('rescue_today',0)+shortage
    _V233_REPORT['sheep_rescue_feed_requests']+=shortage
    return result

def agent(observation,configuration=None):
    action=_V233_PARENT(observation,configuration)
    step=int(observation['step']);player=int(observation['player']);day=step//24
    state=_V233_STATES.get(player)
    if state is None or step<=state['last_step']:
        state={'last_step':step,'day':-1,'workers':{},'work':{},'credit':{'WOOL':0,'FERTILIZER':0}}
        _V233_STATES[player]=state
    state['last_step']=step
    if configuration is not None and any(configuration.get(k,v)!=v for k,v in
        (('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10))):return action
    if day<11:return action
    farm=observation['farms'][player];private=observation['private']
    if state['day']!=day:state['day']=day;state['workers']={};state['work']={};state['rescue_today']=0
    for actor,previous in state['work'].items():
        if previous['step']!=step-1 or actor>=len(private['inventories']):continue
        item={'HARVEST':'WOOL','COLLECT_FERTILIZER':'FERTILIZER'}.get(previous['command'][0])
        if item:
            gained=max(0,private['inventories'][actor].get(item,0)-previous['inventory'].get(item,0))
            state['credit'][item]+=gained
            _V233_REPORT['sheep_wool_harvested' if item=='WOOL' else 'sheep_fert_collected']+=gained
    pending=state.pop('pending',None)
    if pending:
        funded='SE' in farm['unlocked_quadrants'] and (not pending['initial'] or private['shed'].get('SHEEP',0)>=6)
        if not funded:_V233_REPORT['sheep_purchase_shortfalls']+=1
        elif len(farm['hands'])<pending['first']+pending.get('count',2)-1:_V233_REPORT['sheep_hire_shortfalls']+=1
        else:
            if pending.get('count',2)==1:
                state['workers'][pending['first']]=list(pending['targets'])
                _SL_REPORT['confirmed']+=1
            else:
                for i in range(2):state['workers'][pending['first']+i]=[(x,5+i) for x in range(5,8)]
            _V233_REPORT['sheep_workers_confirmed']+=pending.get('count',2)
            if pending['initial']:state['committed']=True;_V233_REPORT['sheep_committed']+=1
    action=_v233_request(observation,action,state,_IMPL.chassis.players[player])
    if not state.get('committed'):return action
    result=copy.deepcopy(action)
    commands=[result.get('farmer') or ['PASS']]+list(result.get('hands') or [])
    commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
    state['work']={}
    for actor,targets in state['workers'].items():
        command=_v233_worker(observation,actor,targets);commands[actor]=command
        state['work'][actor]={'step':step,'command':command,'inventory':dict(private['inventories'][actor])}
    result['farmer'],result['hands']=commands[0],commands[1:]
    result=_v234_rescue(observation,result,state)
    stock=projected_shed(result,FarmView(observation))
    for item in ('WOOL','FERTILIZER'):
        scheduled=sum(int(o[2]) for o in result['market'] if o[:2]==['SELL',item])
        count=min(state['credit'][item],max(0,stock.get(item,0)-scheduled))
        if count and len(result['market'])<MAX_ORDERS:
            result['market'].append(['SELL',item,count]);state['credit'][item]-=count
            _V233_REPORT['sheep_extra_wool_sales' if item=='WOOL' else 'sheep_extra_fert_sales']+=count
    return result

_R46_SHEEP_AGENT=agent
_R46_SHADOW_PARENT=_shadow_terminal
_R46_REPORT={}
def _shadow_terminal(obs,config):
    if _V233_STATES.get(int(obs['player']),{}).get('committed'):return None
    return _R46_SHADOW_PARENT(obs,config)
del agent
def agent(observation,configuration=None):
    try:
        if int(observation.get('step',-1))==0:
            for k in _V233_REPORT:_V233_REPORT[k]=0
        result=_R46_SHEEP_AGENT(observation,configuration)
    except Exception:
        _R46_REPORT['sheep_overlay_errors']=_R46_REPORT.get('sheep_overlay_errors',0)+1
        result={'farmer':['PASS'],'hands':[],'market':[]}
    _R46_REPORT.update(getattr(_V233_PARENT,'telemetry',{}))
    _R46_REPORT.update(_V233_REPORT)
    return result
agent.telemetry=_R46_REPORT
agent=globals().pop('agent')

# EXP182: finite-harvest wheat/carrot input planner; original adaptation.
_R51_INPUT_PARENT=agent
_R51_INPUT_STATES={}
_R51_INPUT_REPORT={}
_R51_INPUT_MAX_WORKERS=2
_R51_INPUT_CROPS={'WHEAT':(2,4,6),'CARROT':(2,3,4)}

def _r51_input_forecast(obs,route,expected):
    step=int(obs['step']);day=step//24;farm=obs['farms'][obs['player']]
    pos=[list(farm['farmer'])]+[list(p) for p in farm['hands'][:expected]];targets={}
    for y,line in enumerate(farm['tiles']):
        for x,tile in enumerate(line):
            if not isinstance(tile,dict) or tile.get('crop') not in _R51_INPUT_CROPS:continue
            item=tile['crop'];first,last,cap=_R51_INPUT_CROPS[item]
            if 1<=day-tile['planted_day']<last:
                targets[(x,y)]={'crop':item,'birth':tile['planted_day'],'yield':tile['yield_units'],
                    'until':tile.get('fertilized_until_day',-1),'watered':tile.get('watered_today',False),'water':[],'harvest':None,'first':first,'last':last,'cap':cap}
    access=((4,4),(5,4),(4,5),(5,5));seen=set()
    # Native continuation ends before the reactive terminal closure planner.
    for t in range(step,min(712,(day+4)*24)):
        tape=_IMPL.chassis.routes[2 if t>=648 else route];a=tape[t]
        for actor,c in enumerate([a.get('farmer') or ['PASS'],*(a.get('hands') or [])][:len(pos)]):
            if not c:continue
            xy=tuple(pos[actor]);target=targets.get(xy)
            if target is not None and target['harvest'] is None:
                if c[0]=='WATER' and (t//24,xy) not in seen:
                    seen.add((t//24,xy))
                    if not(t//24==day and target['watered']) and target['first']<=t//24-target['birth']<=target['last']:target['water'].append(t)
                if c[0]=='HARVEST':target['harvest']=t
            if c[0] in MOVES:
                dx,dy=MOVES[c[0]];pos[actor]=[max(0,min(9,pos[actor][0]+dx)),max(0,min(9,pos[actor][1]+dy))]
        for o in a.get('market',[]):
            if o and o[0]=='HIRE':
                counts={p:sum(tuple(q)==p for q in pos) for p in access}
                pos.append(list(min(access,key=lambda p:(counts[p],access.index(p)))))
        if (t+1)%24==0:pos=[[4,4]]
    return targets

def _r51_input_gain(target,arrival,day):
    if target['harvest'] is None or target['harvest']<=arrival:return 0
    extra=sum(arrival<t<=target['harvest'] and day<=t//24<=day+2 and t//24>target['until'] for t in target['water'])
    baseline=target['yield']+sum(2 if t//24<=target['until'] else 1 for t in target['water'])
    return max(0,min(extra,target['cap']-baseline))

def _r51_input_path(obs,targets,action,index):
    step=int(obs['step']);day=step//24
    ready,start=_r62_input_start(obs,action,index)
    prices={p:max(1,int(obs['market']['prices'][p])-2) for p in ('WHEAT','CARROT')}
    fertilizer=max(1,_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-16)+2)
    # Tuple: penalized value, gross value, next free turn, position, path, used,
    # wheat units, carrot units. No state reads from the rival's private farm.
    beam=[(0,0,ready,start,(),frozenset(),0,0)]
    best=None
    for depth in range(8):
        expanded=[]
        for score,gross,now,pos,path,used,wheat,carrot in beam:
            for xy,target in targets.items():
                if xy in used:continue
                arrival=now+abs(pos[0]-xy[0])+abs(pos[1]-xy[1])
                if arrival>=day*24+23:continue
                gain=_r51_input_gain(target,arrival,day)
                if not gain:continue
                item=target['crop'];new_gross=gross+gain*prices[item]
                new_path=path+((xy[0],xy[1],item,target['birth']),)
                expanded.append((new_gross-1.5*fertilizer*len(new_path),new_gross,arrival+1,xy,new_path,
                                 used|{xy},wheat+(gain if item=='WHEAT' else 0),carrot+(gain if item=='CARROT' else 0)))
        if not expanded:break
        expanded.sort(key=lambda s:(-s[0],-s[1],s[2],s[4]))
        beam=expanded[:8]
        if depth>=2:
            candidate=beam[0]
            if best is None or (-candidate[0],-candidate[1],candidate[2],candidate[4])<(-best[0],-best[1],best[2],best[4]):best=candidate
    if best is None:return [],{'WHEAT':0,'CARROT':0}
    return list(best[4]),{'WHEAT':best[6],'CARROT':best[7]}

def _r51_input_control(obs,action,state):
    step=int(obs['step']);day=step//24;hour=step%24;player=int(obs['player']);farm=obs['farms'][player];private=obs['private']
    native=_IMPL.chassis.players[player]
    if state.get('day')!=day:state.update(day=day,workers={},pending=None,placed=[])
    for x,y in state['placed']:
        tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('fertilized_until_day',-1)>=day+2:_R51_INPUT_REPORT['input_confirmed_applications']+=1
        else:_R51_INPUT_REPORT['input_application_errors']+=1
    state['placed']=[]
    if state.get('pending'):
        pending=state.pop('pending')
        for actor,plan in pending.items():
            if len(farm['hands'])>=actor:state['workers'][actor]=plan;_R51_INPUT_REPORT['input_confirmed_hires']+=1
            else:_R51_INPUT_REPORT['input_hire_errors']+=1
    if state['workers']:
        changed=copy.deepcopy(action)
        for actor,plan in state['workers'].items():
            inv=private['inventories'][actor];pos=tuple(farm['hands'][actor-1]);cmd=['PASS']
            if not plan['loaded']:
                stock=projected_shed(changed,FarmView(obs));q=min(plan['quantity'],max(0,stock.get('FERTILIZER',0)))
                if q and _shed_adjacent(pos,10):
                    cmd=['PICKUP','FERTILIZER',q];plan['loaded']=True;_R51_INPUT_REPORT['input_loaded_units']+=q
                    if q<plan['quantity']:_R51_INPUT_REPORT['input_stock_shortfalls']+=plan['quantity']-q
            elif inv.get('FERTILIZER',0):
                while plan['path']:
                    x,y,crop,birth=plan['path'][0];tile=farm['tiles'][y][x]
                    if not isinstance(tile,dict) or tile.get('crop')!=crop or tile.get('planted_day')!=birth or tile.get('fertilized_until_day',-1)>=day+2:
                        plan['path'].pop(0);continue
                    cmd=_v219_walk(pos,(x,y)) or ['FERTILIZE']
                    if cmd==['FERTILIZE']:state['placed'].append((x,y));plan['path'].pop(0);_R51_INPUT_REPORT['input_application_requests']+=1
                    break
            changed['hands'][actor-1]=cmd
        return changed
    if hour not in (1,2,3) or not 12<=day<=28:return action
    planned=_v219_native_day(native,day);expected=max(len(a.get('hands',[])) for a in planned)
    if any(o and o[0]=='HIRE' for a in planned[hour:] for o in a.get('market',[])) or native['pending']:return action
    parents=[_V219_STATES.get(player,{}),_V233_STATES.get(player,{})]
    # A parent may retry after a full market queue; its headcount must remain native.
    if day in (12,18) or any(p.get('committed') and p.get('requested_day')!=day for p in parents):return action
    if any(p.get('pending') for p in parents) or any(o and o[0]=='HIRE' for o in action.get('market',[])):return action
    owned=set(range(1,expected+1))
    for p in parents:
        actors=set(p.get('workers',{}))
        if owned&actors:return action
        owned|=actors
    if owned!=set(range(1,len(farm['hands'])+1)):return action
    targets=_r51_input_forecast(obs,native['route'],expected);plans=[];total_q=0;total_cost=0;all_units={'WHEAT':0,'CARROT':0}
    stock=projected_shed(action,FarmView(obs));purchases=sum(max(0,int(o[2])) for o in action.get('market',[]) if len(o)>2 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    # Units act before market orders. Preserve the native next-turn pickup,
    # after the current parent's actual sales/purchases, before buying tour inputs.
    available=max(0,stock.get('FERTILIZER',0))
    for o in action.get('market',[]):
        if len(o)>=3 and o[:2]==['SELL','FERTILIZER']:available=max(0,available-max(0,int(o[2])))
        elif len(o)>=3 and o[:2]==['BUY_PRODUCT','FERTILIZER']:available+=max(0,int(o[2]))
    next_native=planned[hour+1];native_pickups=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in [next_native.get('farmer') or ['PASS'],*(next_native.get('hands') or [])] if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
    topup=max(0,native_pickups-available)
    plans,total_q,total_cost,all_units=_r68_joint_plans(obs,action,targets,stock,purchases,topup)
    if not plans:return action
    state['pending']={len(farm['hands'])+1+i:plan for i,plan in enumerate(plans)}
    _R51_INPUT_REPORT['input_hire_requests']+=len(plans);_R51_INPUT_REPORT['input_purchase_requests']+=total_q+topup
    _R51_INPUT_REPORT['input_forecast_wheat']+=all_units['WHEAT'];_R51_INPUT_REPORT['input_forecast_carrot']+=all_units['CARROT']
    changed=copy.deepcopy(action);changed['market'] += [['BUY_PRODUCT','FERTILIZER',total_q+topup]]+[['HIRE'] for _ in plans];return changed

def agent(observation,configuration=None):
    try:
        step=int(observation['step']);player=int(observation['player']);state=_R51_INPUT_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R51_INPUT_STATES[player]={'step':-1}
            _R51_INPUT_REPORT.update(input_hire_requests=0,input_confirmed_hires=0,input_hire_errors=0,input_purchase_requests=0,
                input_loaded_units=0,input_stock_shortfalls=0,input_application_requests=0,input_confirmed_applications=0,
                input_application_errors=0,input_errors=0,input_forecast_wheat=0,input_forecast_carrot=0)
        state['step']=step;action=_R51_INPUT_PARENT(observation,configuration)
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
            action=_r51_input_control(observation,action,state)
        _R51_INPUT_REPORT.update(getattr(_R51_INPUT_PARENT,'telemetry',{}));return action
    except Exception:
        _R51_INPUT_REPORT['input_errors']=_R51_INPUT_REPORT.get('input_errors',0)+1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_R51_INPUT_REPORT
agent=globals().pop('agent')

# EXP182: project the final hour's actual worker actions before automatic deposit.
_R51_WAREHOUSE_PARENT=agent
_R51_WAREHOUSE_REPORT={}

def _r51_close_warehouse(obs,action):
    step=int(obs['step']);day=step//24
    if step%24!=23 or not 12<=day<=28:return action
    # No speculative product purchase/worker count model: these hours abstain.
    if any(o and o[0] not in ('SELL',) for o in action.get('market',[])):return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={k for k,q in demand.items() if q>private['seeds'].get(k,0)}
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:c=['PASS']
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    post=dict(private['shed'])
    for o in action.get('market',[]):
        if len(o)>=3 and o[0]=='SELL':post[o[1]]=max(0,post.get(o[1],0)-max(0,int(o[2])))
    needed=sum(post.values())+sum(max(0,q) for inv in private['inventories'] for q in inv.values())-100
    if needed<=0:return action
    result=copy.deepcopy(action);orders=result['market']
    # Grain and fertilizer have native input obligations; other products do not.
    # Additional commodity sales are bounded by actual post-action physical stock.
    for item in sorted((p for p in PRODUCTS if p not in ('WHEAT','FERTILIZER')),key=lambda p:-obs['market']['prices'].get(p,0)):
        qty=min(needed,post.get(item,0))
        if not qty:continue
        existing=next((o for o in orders if len(o)>=3 and o[:2]==['SELL',item]),None)
        if existing is not None:existing[2]=max(0,int(existing[2]))+qty
        elif len(orders)<10:orders.append(['SELL',item,qty])
        else:continue
        needed-=qty;post[item]-=qty;_R51_WAREHOUSE_REPORT['warehouse_extra_sales']+=qty
        if needed<=0:break
    if needed>0:
        native=_IMPL.chassis.players[int(obs['player'])];reserve=0
        for t in range(step+1,719):
            future=_IMPL.chassis.routes[2 if t>=648 else native['route']][t]
            for c in [future.get('farmer') or ['PASS'],*(future.get('hands') or [])]:
                if len(c)>1 and c[:2]==['PICKUP','WHEAT']:reserve+=max(0,int(c[2]) if len(c)>2 else 1)
            if any(len(o)>1 and o[:2]==['BUY_PRODUCT','WHEAT'] for o in future.get('market',[])):break
        incoming=sum(max(0,inv.get('WHEAT',0)) for inv in private['inventories'])
        others=sum(q for p,q in post.items() if p!='WHEAT')+sum(max(0,q) for inv in private['inventories'] for p,q in inv.items() if p!='WHEAT')
        # Even if every other carried item deposits first, this grain reserve fits.
        qty=min(needed,post.get('WHEAT',0),max(0,post.get('WHEAT',0)+incoming-reserve)) if 100-others>=reserve else 0
        existing=next((o for o in orders if len(o)>=3 and o[:2]==['SELL','WHEAT']),None)
        if qty and (existing is not None or len(orders)<10):
            if existing is not None:existing[2]=max(0,int(existing[2]))+qty
            else:orders.append(['SELL','WHEAT',qty])
            needed-=qty;_R51_WAREHOUSE_REPORT['warehouse_extra_sales']+=qty
    _R51_WAREHOUSE_REPORT['warehouse_projected_unresolved']+=max(0,needed)
    if result!=action:_R51_WAREHOUSE_REPORT['warehouse_changed_turns']+=1
    return result

def agent(observation,configuration=None):
    result=_R51_WAREHOUSE_PARENT(observation,configuration)
    try:
        if int(observation['step'])==0:_R51_WAREHOUSE_REPORT.update(warehouse_changed_turns=0,warehouse_extra_sales=0,warehouse_projected_unresolved=0,warehouse_errors=0)
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):result=_r51_close_warehouse(observation,result)
    except Exception:_R51_WAREHOUSE_REPORT['warehouse_errors']=_R51_WAREHOUSE_REPORT.get('warehouse_errors',0)+1
    _R51_WAREHOUSE_REPORT.update(getattr(_R51_WAREHOUSE_PARENT,'telemetry',{}));return result
agent.telemetry=_R51_WAREHOUSE_REPORT
agent=globals().pop('agent')

from itertools import permutations as _r53_permutations
_R53_LABOR_REPORT=dict(labor_requests=0,labor_hires_avoided=0,labor_spawn_errors=0,labor_confirmed=0,labor_day26=0,labor_day27=0,labor_day28=0)

def _r53_labor_assignment(obs,action,fertilizer):
    step=int(obs['step']);day=step//24;farm=obs['farms'][obs['player']]
    if day not in (26,27,28) or step%24>2:return None
    # Do not preempt a later price-gated fertilizer request with a smaller unfertilized team.
    if day==27 and not fertilizer:return None
    count=3 if fertilizer else 2
    positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    for i,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(positions)]):
        if c and c[0] in MOVES:
            dx,dy=MOVES[c[0]];positions[i]=[max(0,min(9,positions[i][0]+dx)),max(0,min(9,positions[i][1]+dy))]
    access=((4,4),(5,4),(4,5),(5,5));spawns=[]
    native_hires=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
    for i in range(native_hires+count):
        chosen=min(access,key=lambda p:(sum(tuple(q)==p for q in positions),access.index(p)));positions.append(list(chosen))
        if i>=native_hires:spawns.append(chosen)
    groups=(((5,5),(6,5),(7,5),(8,5)),((9,5),(9,6),(8,6)),((5,6),(6,6),(7,6))) if fertilizer else (tuple((x,5) for x in range(5,10)),tuple((x,6) for x in range(5,10)))
    choices=[];remaining=23-step%24
    for assignment in _r53_permutations(groups):
        costs=[]
        for start,path in zip(spawns,assignment):
            distance=abs(start[0]-path[0][0])+abs(start[1]-path[0][1])
            distance+=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(path,path[1:]))
            distance+=min(abs(path[-1][0]-x)+abs(path[-1][1]-y) for x,y in access)
            costs.append(distance+(3 if fertilizer else 2)*len(path)+1+int(fertilizer))
        if max(costs)<=remaining:choices.append((max(costs),sum(costs),assignment))
    if not choices:return None
    _,_,assignment=min(choices)
    return dict(paths=assignment,spawns=spawns,remaining=remaining,workers=count,fertilizer=fertilizer)

_R53_LABOR_PARENT=agent
def agent(observation,configuration=None):
    if isinstance(observation,dict) and observation.get('step')==0:
        for k in _R53_LABOR_REPORT:_R53_LABOR_REPORT[k]=0
    result=_R53_LABOR_PARENT(observation,configuration)
    _R53_LABOR_COMBINED.update(getattr(_R53_LABOR_PARENT,'telemetry',{}));_R53_LABOR_COMBINED.update(_R53_LABOR_REPORT)
    return result
_R53_LABOR_COMBINED={}
agent.telemetry=_R53_LABOR_COMBINED
agent=globals().pop('agent')

# EXP193: deterministic HIRE spawn after native unit actions, then next-turn pickup.
def _r62_input_start(obs,action,index):
    farm=obs['farms'][obs['player']]
    positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    for actor,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(positions)]):
        if c and c[0] in MOVES:
            dx,dy=MOVES[c[0]]
            positions[actor]=[max(0,min(9,positions[actor][0]+dx)),max(0,min(9,positions[actor][1]+dy))]
    access=((4,4),(5,4),(4,5),(5,5))
    native_hires=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
    for _ in range(native_hires+index+1):
        chosen=min(access,key=lambda p:(sum(tuple(q)==p for q in positions),access.index(p)))
        positions.append(list(chosen))
    return int(obs['step'])+2,chosen

agent=globals().pop('agent')

def _r68_joint_plans(obs,action,targets,stock,purchases,topup):
    farm=obs['farms'][obs['player']];choices=[]
    for mode,first_crop in enumerate((None,'WHEAT','CARROT')):
        remaining=dict(targets);plans=[];total_q=0;total_cost=0;total_value=0
        all_units={'WHEAT':0,'CARROT':0}
        for i in range(_R51_INPUT_MAX_WORKERS):
            subset={xy:t for xy,t in remaining.items() if t['crop']==first_crop} if i==0 and first_crop else remaining
            path,units=_r51_input_path(obs,subset,action,i);q=len(path)
            if q<3 or len(action.get('market',[]))+2+i>10 or sum(stock.values())+purchases+total_q+q+topup>95:break
            quote=_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-total_q-q-topup)
            cost=(q+(topup if i==0 else 0))*(quote+2)+_v219_fib(int(farm['hires_today'])+i)
            value=sum(n*max(1,_r37_market_price(item,obs['market']['inventory'][item]+all_units[item]+n)-2) for item,n in units.items())
            if value<1.5*cost+50 or farm['money']<total_cost+cost+3000:break
            plans.append({'path':path,'quantity':q,'loaded':False});total_q+=q;total_cost+=cost;total_value+=value
            for item,n in units.items():all_units[item]+=n
            for x,y,_,_ in path:remaining.pop((x,y),None)
        score=(total_value-total_cost,total_value,-total_cost,-len(plans),-mode)
        choices.append((score,plans,total_q,total_cost,all_units))
    _,plans,total_q,total_cost,all_units=max(choices,key=lambda v:v[0])
    return plans,total_q,total_cost,all_units

agent=globals().pop('agent')

_R70_STATES={}
_R70_REPORT={}

def _r70_parent_fert_qty(obs,action,planned,offset):
    stock=dict(projected_shed(action,FarmView(obs)))
    for order in action.get('market',[]):
        if len(order)<3:continue
        op,item,quantity=order[:3];quantity=max(0,int(quantity))
        if op=='SELL':stock[item]=max(0,stock.get(item,0)-quantity)
        elif op in ('BUY_PRODUCT','BUY_ANIMAL'):
            stock[item]=stock.get(item,0)+min(quantity,max(0,100-sum(stock.values())))
    next_action=planned[offset+1] if offset+1<len(planned) else {}
    commands=[next_action.get('farmer') or ['PASS'],*(next_action.get('hands') or [])]
    native_need=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in commands if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
    quantity=max(10,10+native_need-max(0,stock.get('FERTILIZER',0)))
    if quantity>max(0,100-sum(stock.values())):
        _R70_REPORT['parent_input_capacity_declines']+=1
        return 10
    if quantity>10:
        _R70_REPORT['parent_input_guard_turns']+=1
        _R70_REPORT['parent_input_guard_extra_units']+=quantity-10
    return quantity

def _r70_before(obs):
    player=int(obs['player']);step=int(obs['step']);state=_R70_STATES.get(player)
    if state is None or step<=state['step']:
        state=_R70_STATES[player]={'step':-1,'pending':[],'roles':set()}
        _R70_REPORT.update(parent_input_guard_turns=0,parent_input_guard_extra_units=0,
            parent_input_requests=0,parent_input_confirmed=0,parent_input_shortfalls=0,
            parent_input_errors=0,parent_input_capacity_declines=0)
    state['step']=step
    for request in state['pending']:
        actor,quantity,old=request
        actual=max(0,int(obs['private']['inventories'][actor].get('FERTILIZER',0))-old)
        _R70_REPORT['parent_input_confirmed']+=min(quantity,actual)
        _R70_REPORT['parent_input_shortfalls']+=max(0,quantity-actual)
    state['pending']=[]
    return state

def _r70_after(obs,action,state):
    player=int(obs['player']);day=int(obs['step'])//24
    for actor,role in _V219_STATES.get(player,{}).get('workers',{}).items():
        if not role.get('needs_fertilizer'):continue
        key=(day,actor);inv=obs['private']['inventories'][actor].get('FERTILIZER',0)
        if key not in state['roles']:
            state['roles'].add(key)
            desired=role.get('fertilizer_quantity',10 if role['kind']=='fertilizer' else 5)
            if role.get('loaded') and not role.get('pickup_requested') and inv<desired:
                _R70_REPORT['parent_input_shortfalls']+=desired-inv
        command=action.get('hands',[])[actor-1] if actor<=len(action.get('hands',[])) else ['PASS']
        if len(command)>1 and command[:2]==['PICKUP','FERTILIZER']:
            quantity=max(0,int(command[2]) if len(command)>2 else 1)
            _R70_REPORT['parent_input_requests']+=quantity
            state['pending'].append((actor,quantity,int(inv)))

_R70_PARENT=agent

def agent(observation,configuration=None):
    state=None
    try:state=_r70_before(observation)
    except Exception:_R70_REPORT['parent_input_errors']=_R70_REPORT.get('parent_input_errors',0)+1
    result=_R70_PARENT(observation,configuration)
    try:
        if state is not None:_r70_after(observation,result,state)
    except Exception:_R70_REPORT['parent_input_errors']=_R70_REPORT.get('parent_input_errors',0)+1
    _R70_REPORT.update(getattr(_R70_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R70_REPORT
agent=globals().pop('agent')

def _r79_tomato_fertilizer_worthwhile(obs,action):
    if obs['market']['prices']['FERTILIZER']<=30:return True
    farm=obs['farms'][obs['player']];day=int(obs['step'])//24;bonus=0
    for y in (5,6):
        for x in range(5,10):
            tile=farm['tiles'][y][x]
            if not isinstance(tile,dict) or tile.get('crop')!='TOMATO':continue
            birth=tile['planted_day'];until=tile.get('fertilized_until_day',-1)
            bonus+=sum(until<d and 8<=d+1-birth<=11 for d in range(day,day+3))
    if not bonus:return False
    inventory=obs['market']['inventory']
    price=max(1,_r37_market_price('TOMATO',inventory['TOMATO']+bonus+10)-2)
    fertilizer=max(1,_r37_market_price('FERTILIZER',inventory['FERTILIZER']-10)+2)
    native_hires=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
    extra_labor=_v219_fib(int(farm['hires_today'])+native_hires+3)
    return bonus*price>=2*(10*fertilizer+extra_labor)+100

agent=globals().pop('agent')

# EXP216: original adaptation of economic feed and fertilizer-sale concepts.
# Conceptual credit: Steven Lee Hans, "Lord Momo Returns", September12 snapshot.
_R85_FEED = True
_R85_FERT = True
_R85_PARENT = agent
_R85_STATES = {}
_R85_REPORT = {}
_FEED_TERMINAL_CUT = 'universal'
_FEED_ANIMAL_DAYS = {'GOOSE': (4, 1), 'COW': (8, 2), 'SHEEP': (6, 3)}

def _r85_feed(obs, action):
    step=int(obs['step']);day=step//24
    if not 10<=day<=28 or step%24>21:return action
    player=int(obs['player']);native=_IMPL.chassis.players[player]
    tape=_v219_native_day(native,day)
    expected=max(len(a.get('hands',[])) for a in tape)
    farm=obs['farms'][player];positions=[farm['farmer'],*farm['hands']]
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    prices=obs['market']['prices'];changed=False
    for actor,command in enumerate(commands[:expected+1]):
        if command!=['FEED'] or actor>=len(positions):continue
        tile=_tile_at(farm['tiles'],positions[actor])
        if not isinstance(tile,dict) or tile.get('animal') not in ('GOOSE','COW','SHEEP'):continue
        if tile.get('fed_today'):continue
        if int(obs['private']['inventories'][actor].get('WHEAT',0))<=0:continue
        if _FEED_TERMINAL_CUT != 'as_is':
            first, interval = _FEED_ANIMAL_DAYS[tile['animal']]
            first += int(tile['placed_day'])
            if _FEED_TERMINAL_CUT == 'universal':
                next_prod = first
                if next_prod <= day:
                    next_prod += ((day - next_prod) // interval + 1) * interval
                if next_prod > 29:
                    commands[actor] = ['PASS']
                    changed = True
                    _R85_REPORT['feed_skips'] += 1
                    continue
            elif _FEED_TERMINAL_CUT == 'day28_only':
                produces_day29 = (29 >= first and (29 - first) % interval == 0)
                if day == 28 and not produces_day29:
                    commands[actor] = ['PASS']
                    changed = True
                    _R85_REPORT['feed_skips'] += 1
                    continue
        if int(tile.get('consecutive_unfed',0))!=0:continue
        if int(obs['private']['inventories'][actor].get('WHEAT',0))<=0:continue
        item={'GOOSE':'EGG','COW':'MILK','SHEEP':'WOOL'}[tile['animal']]
        bonus=_r88_feed_bonus_cost(tile,day)
        if bonus*(float(prices[item])+5)*1.25>=float(prices['WHEAT']):continue
        if not _r86_next_feed(obs,positions[actor]):continue
        commands[actor]=['PASS'];changed=True
        _R85_REPORT['feed_skips']+=1
    if not changed:return action
    result=copy.deepcopy(action);result['farmer'],result['hands']=commands[0],commands[1:]
    return result

def _r85_reserve(obs, state):
    step=int(obs['step']);player=int(obs['player']);native=_IMPL.chassis.players[player]
    route=native['route'];key=(route,step)
    cache=state.setdefault('native_reserves',{})
    if route not in cache:
        # Backward recurrence preserves field-before-market order within a turn.
        reserve=[0]*720
        for t in range(718,-1,-1):
            a=_IMPL.chassis.routes[2 if t>=648 else route][t]
            pickup=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in [a.get('farmer') or ['PASS'],*(a.get('hands') or [])] if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
            purchase=sum(max(0,int(o[2])) for o in a.get('market',[]) if len(o)>2 and o[:2]==['BUY_PRODUCT','FERTILIZER'])
            reserve[t]=pickup+max(0,reserve[t+1]-purchase)
        cache[route]=reserve
    dedicated=0
    for parent in (_V219_STATES.get(player,{}),_V233_STATES.get(player,{})):
        for actor,role in parent.get('workers',{}).items():
            if not isinstance(role,dict) or not role.get('needs_fertilizer') or role.get('loaded'):continue
            desired=role.get('fertilizer_quantity',10 if role.get('kind')=='fertilizer' else 5)
            carried=obs['private']['inventories'][actor].get('FERTILIZER',0)
            dedicated+=max(0,desired-carried)
        pending=parent.get('pending') or {}
        if pending.get('fertilizer'):dedicated+=10
    inputs=_R51_INPUT_STATES.get(player,{})
    for actor,plan in {**inputs.get('workers',{}),**(inputs.get('pending') or {})}.items():
        if not plan.get('loaded'):dedicated+=max(0,int(plan['quantity']))
    return max(14,cache[route][min(719,step+1)]+dedicated)

def _r85_fertilizer(obs, action, state):
    step=int(obs['step']);day=step//24
    if not 6<=day<=28:return action
    market=action.get('market',[])
    if len(market)>=MAX_ORDERS or any(o and o[0]!='SELL' for o in market):return action
    stock=projected_shed(action,FarmView(obs))
    held=max(0,int(stock.get('FERTILIZER',0)))
    sold=sum(max(0,int(o[2])) for o in market if len(o)>2 and o[:2]==['SELL','FERTILIZER'])
    extra=held-sold-_r85_reserve(obs,state)
    if extra<=0:return action
    result=copy.deepcopy(action);result['market'].append(['SELL','FERTILIZER',extra])
    _R85_REPORT['fert_sale_turns']+=1;_R85_REPORT['fert_sale_units']+=extra
    return result

def agent(observation, configuration=None):
    result=_R85_PARENT(observation,configuration)
    try:
        step=int(observation['step']);player=int(observation['player'])
        state=_R85_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R85_STATES[player]={'step':-1}
            _R85_REPORT.update(feed_skips=0,fert_sale_turns=0,fert_sale_units=0,economic_overlay_errors=0)
        state['step']=step
        if configuration is not None and any(configuration.get(k,v)!=v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):return result
        if _R85_FEED:result=_r85_feed(observation,result)
        if _R85_FERT:result=_r85_fertilizer(observation,result,state)
        if step%24==23:result=_r51_close_warehouse(observation,result)
    except Exception:
        _R85_REPORT['economic_overlay_errors']=_R85_REPORT.get('economic_overlay_errors',0)+1
    _R85_REPORT.update(getattr(_R85_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R85_REPORT
agent=globals().pop('agent')

# EXP217: planned next-day service is required before discretionary feed cuts.
_R86_FEED_CACHE = {}

def _r86_next_feed(obs, target):
    step=int(obs['step']);day=step//24
    if day==28:return True  # No second dawn follows before game termination.
    player=int(obs['player']);native=_IMPL.chassis.players[player]
    tomorrow=day+1;route=2 if tomorrow>=27 else native['route'];key=(route,tomorrow)
    if key not in _R86_FEED_CACHE:
        positions=[(4,4)];wheat=[0];access=((4,4),(5,4),(4,5),(5,5));feeds=set()
        for hour in range(24):
            a=_IMPL.chassis.routes[route][tomorrow*24+hour]
            commands=[a.get('farmer') or ['PASS'],*(a.get('hands') or [])]
            for actor,command in enumerate(commands[:len(positions)]):
                if not command:continue
                pos=positions[actor];op=command[0]
                if op in MOVES:
                    dx,dy=MOVES[op];positions[actor]=(max(0,min(9,pos[0]+dx)),max(0,min(9,pos[1]+dy)))
                elif command[:2]==['PICKUP','WHEAT'] and pos in access:
                    wheat[actor]+=max(0,int(command[2]) if len(command)>2 else 1)
                elif op=='FEED' and wheat[actor]>0:
                    wheat[actor]-=1
                    if hour<=21:feeds.add(pos)
                elif op=='DROP' and pos in access:wheat[actor]=0
                elif command[:2]==['PLACE','WHEAT'] and pos in access:
                    wheat[actor]=max(0,wheat[actor]-max(0,int(command[2]) if len(command)>2 else 1))
            for order in a.get('market',[]):
                if order and order[0]=='HIRE':
                    chosen=min(access,key=lambda p:(positions.count(p),access.index(p)))
                    positions.append(chosen);wheat.append(0)
        _R86_FEED_CACHE[key]=frozenset(feeds)
    return tuple(target) in _R86_FEED_CACHE[key]

agent=globals().pop('agent')

# EXP219: charge care credits only when this feeding decision can affect them.
_R88_PHASE = True
_R88_HORIZON = True
_R88_ANIMAL_DAYS = {'GOOSE': (4, 1), 'COW': (8, 2), 'SHEEP': (6, 3)}


def _r88_feed_bonus_cost(tile, day):
    first, interval = _R88_ANIMAL_DAYS[tile['animal']]
    first += int(tile['placed_day'])
    tomorrow = day + 1
    produces = tomorrow >= first and (tomorrow - first) % interval == 0
    pending = max(0, int(tile.get('pending_care_bonus', 0)))
    if _R88_PHASE and not produces:
        pending = 0  # It remains banked on non-production dawns.
    care = 1  # Conservative: charge one possible CARE even if not yet observed.
    if _R88_HORIZON:
        # Today's care is added AFTER tomorrow's production; its first possible
        # payout is a later production dawn, which must occur before game end.
        next_use = first
        if next_use <= tomorrow:
            next_use += ((tomorrow - next_use) // interval + 1) * interval
        if next_use > 29:
            care = 0
    return pending + care


agent = globals().pop('agent')

# EXP226: retain physical grain for two complete days before trimming a buy.
_R95_PARENT = agent
_R95_REPORT = {}
_R95_RESERVES = {}

def _r95_reserve(obs):
    step=int(obs['step']);player=int(obs['player'])
    native=_IMPL.chassis.players[player];route=native['route']
    key=(route,step)
    if key not in _R95_RESERVES:
        demand=6  # Physical buffer beyond every scheduled pickup and sale.
        for t in range(step+1,min(719,step+49)):
            a=_IMPL.chassis.routes[2 if t>=648 else route][t]
            for c in [a.get('farmer') or ['PASS'],*(a.get('hands') or [])]:
                if c[:2]==['PICKUP','WHEAT']:
                    demand+=max(0,int(c[2]) if len(c)>2 else 1)
            for o in a.get('market',[]):
                if len(o)>2 and o[:2]==['SELL','WHEAT']:
                    demand+=max(0,int(o[2]))
        _R95_RESERVES[key]=demand
    demand=_R95_RESERVES[key]
    # Reserve full feed for a possible southeast sheep commitment. Do not
    # rely on its future discretionary buy, eligibility, or existing cargo.
    if obs['town']['unlocked_shops'].count('YARN_STORE')>=2:
        demand+=6*len({t//24 for t in range(step+1,step+49) if t//24>=12})
    return demand

def _r95_replenish(obs,action):
    step=int(obs['step'])
    if not 10<=step//24<=11:return action
    orders=action.get('market') or []
    if not any(len(o)>2 and o[:2]==['BUY_PRODUCT','WHEAT'] and int(o[2])>0 for o in orders):return action
    # Preserve all same-turn grain trading/arbitrage sequences unchanged.
    if any(o[:2]==['SELL','WHEAT'] for o in orders):return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,step//24,24,100)
    held=max(0,int(private['shed'].get('WHEAT',0)))
    reserve=_r95_reserve(obs);result=None;removed=0
    for i,o in enumerate(orders):
        if len(o)<3 or o[:2]!=['BUY_PRODUCT','WHEAT']:continue
        quantity=max(0,int(o[2]));retained=min(quantity,max(0,reserve-held))
        held+=retained
        if retained<quantity:
            if result is None:result=copy.deepcopy(action)
            result['market'][i][2]=retained  # Zero keeps every later order slot.
            removed+=quantity-retained
    if result is None:return action
    _R95_REPORT['replenishment_trim_turns']+=1
    _R95_REPORT['replenishment_trim_units']+=removed
    return result

def agent(observation,configuration=None):
    result=_R95_PARENT(observation,configuration)
    try:
        if int(observation['step'])==0:
            _R95_REPORT.update(replenishment_trim_turns=0,replenishment_trim_units=0,replenishment_errors=0)
        if configuration is not None and any(configuration.get(k,v)!=v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):return result
        result=_r95_replenish(observation,result)
    except Exception:
        _R95_REPORT['replenishment_errors']=_R95_REPORT.get('replenishment_errors',0)+1
    _R95_REPORT.update(getattr(_R95_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R95_REPORT
agent=globals().pop('agent')

# EXP231: protect inputs using funded current orders without unassigned cash padding from observed physical resources.
_R97_PARENT=agent
_R97_REPORT={}
_R97_LAST={}

def _r97_market_stock(shed,orders):
    stock=dict(shed);buys={};sales={}
    for index,order in enumerate(orders):
        if len(order)<3:continue
        op,item,n=order[:3];n=max(0,int(n))
        if op=='SELL':
            q=min(n,max(0,stock.get(item,0)));stock[item]=stock.get(item,0)-q;sales[index]=q
        elif op in ('BUY_PRODUCT','BUY_ANIMAL'):
            q=min(n,max(0,100-sum(stock.values())));stock[item]=stock.get(item,0)+q;buys[index]=q
    return stock,buys,sales

def _r97_delivery(stock,private,night):
    stock=dict(stock);lost={}
    if night:
        for inv in private['inventories']:
            for item,q in inv.items():
                q=max(0,int(q));take=min(q,max(0,100-sum(stock.values())))
                stock[item]=stock.get(item,0)+take
                if q>take:lost[item]=lost.get(item,0)+q-take
    return stock,lost

def _r97_budget(obs,orders):
    farm=obs['farms'][obs['player']];cost=0;hires=int(farm['hires_today'])
    # At most ten 100-unit purchases per opponent turn. The additional 1000
    # own units give an intentionally conservative upper bound on buy quotes.
    prices={p:_r37_market_price(p,obs['market']['inventory'][p]-2000) for p in ('WHEAT','FERTILIZER')}
    for order in orders:
        if not order:continue
        op=order[0]
        if op=='HIRE':cost+=_v219_fib(hires);hires+=1
        elif op=='BUY_LAND':cost+=4000
        elif len(order)>2:
            item=order[1];q=max(0,int(order[2]))
            if op=='BUY_PRODUCT':cost+=q*prices[item]
            elif op=='BUY_ANIMAL':cost+=q*{'GOOSE':300,'COW':400,'SHEEP':500}[item]
            elif op=='BUY_SEED':cost+=q*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[item]
    return cost<=farm['money']  # No current sale proceeds are assumed.

def _r97_supply(obs,action):
    step=int(obs['step']);player=int(obs['player']);day=step//24
    if not 144<=step<695:return action
    native=_IMPL.chassis.players[player]
    future=_IMPL.chassis.routes[2 if step+1>=648 else native['route']][step+1]
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    following=_IMPL.chassis.routes[2 if step+2>=648 else native['route']][step+2]
    next_orders=future.get('market') or []
    prefund=0
    if len(next_orders)==10 and not any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in next_orders):
        later=[following.get('farmer') or ['PASS'],*(following.get('hands') or [])]
        demand=lambda cs:sum(max(0,int(c[2]) if len(c)>2 else 1) for c in cs if c[:2]==['PICKUP','WHEAT'])
        if demand(later):prefund=demand(commands)+demand(later)
    if not prefund and not any(c[:2]==['PICKUP','WHEAT'] for c in commands):return action
    orders=action.get('market') or []
    if len(orders)>10 or not _r97_budget(obs,orders):
        _R97_REPORT['supply_budget_declines']+=1;return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][player],obs['private'])
    for actor,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])];night=step%24==23
    access=((4,4),(5,4),(4,5),(5,5))
    if night:positions=[(4,4)]
    else:
        for order in orders:
            if order and order[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    need=sum(max(0,int(c[2]) if len(c)>2 else 1) for pos,c in zip(positions,commands) if pos in access and c[:2]==['PICKUP','WHEAT'])
    need=max(need,prefund)
    if not need:return action
    original_stock,original_buys,_=_r97_market_stock(private['shed'],orders)
    original_final,original_loss=_r97_delivery(original_stock,private,night)
    if original_final.get('WHEAT',0)>=need:return action
    result=copy.deepcopy(action);proposed=result['market'];blocked=False
    def project(candidate):
        stock,buys,sales=_r97_market_stock(private['shed'],candidate)
        final,loss=_r97_delivery(stock,private,night)
        safe=all(buys.get(i,0)>=q for i,q in original_buys.items()) and all(q<=original_loss.get(item,0) for item,q in loss.items())
        return final,sales,safe
    # Hold an existing grain sale first. Preserve all order indices and every
    # originally funded buy; no extra overnight overflow may be introduced.
    for index in range(len(proposed)-1,-1,-1):
        if proposed[index][:2]!=['SELL','WHEAT']:continue
        final,sales,safe=project(proposed);shortage=max(0,need-final.get('WHEAT',0))
        if not shortage:break
        sold=sales.get(index,0)
        if not sold:continue
        old=proposed[index][2];proposed[index][2]=max(0,sold-shortage)
        after,_,safe=project(proposed)
        if not safe or after.get('WHEAT',0)<=final.get('WHEAT',0):proposed[index][2]=old
    final,_,safe=project(proposed);shortage=max(0,need-final.get('WHEAT',0))
    if shortage:
        last_sale=max((i for i,o in enumerate(proposed) if o[:2]==['SELL','WHEAT']),default=-1)
        index=next((i for i in range(len(proposed)-1,last_sale,-1) if proposed[i][:2]==['BUY_PRODUCT','WHEAT']),None)
        if index is not None:proposed[index][2]=max(0,int(proposed[index][2]))+shortage
        elif len(proposed)<10:proposed.append(['BUY_PRODUCT','WHEAT',shortage])
        else:_R97_REPORT['supply_slot_declines']+=1;return action
    final,_,safe=project(proposed)
    if not safe or final.get('WHEAT',0)<need:
        _R97_REPORT['supply_capacity_declines']+=1;return action
    if not _r97_budget(obs,proposed):
        _R97_REPORT['supply_budget_declines']+=1;return action
    if prefund:
        _R97_REPORT['supply_prefund_changes']+=1
        _R97_REPORT['supply_prefund_units']+=max(0,final.get('WHEAT',0)-original_final.get('WHEAT',0))
    if step<288:
        _R97_REPORT['supply_early_changes']+=1
        _R97_REPORT['supply_early_units']+=max(0,final.get('WHEAT',0)-original_final.get('WHEAT',0))
    _R97_REPORT['supply_guard_changes']+=1
    _R97_REPORT['supply_grain_protected']+=final.get('WHEAT',0)-original_final.get('WHEAT',0)
    _R97_REPORT['supply_buy_units']+=sum(max(0,int(o[2])) for o in proposed if o[:2]==['BUY_PRODUCT','WHEAT'])-sum(max(0,int(o[2])) for o in orders if o[:2]==['BUY_PRODUCT','WHEAT'])
    return result

def agent(observation,configuration=None):
    result=_R97_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step'])
        if player not in _R97_LAST or step<=_R97_LAST[player]:
            _R97_REPORT.update(supply_guard_changes=0,supply_grain_protected=0,supply_buy_units=0,supply_early_changes=0,supply_early_units=0,supply_prefund_changes=0,supply_prefund_units=0,supply_slot_declines=0,supply_capacity_declines=0,supply_budget_declines=0,supply_errors=0)
        _R97_LAST[player]=step
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)]):result=_r97_supply(observation,result)
    except Exception:_R97_REPORT['supply_errors']=_R97_REPORT.get('supply_errors',0)+1
    _R97_REPORT.update(getattr(_R97_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R97_REPORT
agent=globals().pop('agent')


# ---------------------------------------------------------------------------
# v9 COURIER: deliver premium cargo before midnight and sell it the same day.
#
# Roughly 40% of the tape's strawberries and milk are still in workers' hands
# when the day ends; the engine drops them into the shed *after* the market,
# so every sibling of this policy sells them the next morning.  No town draw
# happens between hour 20 and the next dawn's market, so an evening sale gets
# the morning's quote a day earlier than a rival who waits for the auto-drop.
#
# From hour V9_COURIER_FROM_HOUR, a tape worker carrying premium goods whose
# every remaining command today is a PASS or a move (moves are free: workers
# respawn at the shed at dawn) walks to the nearest shed-access tile, drops,
# and the delivered units are offered in the first market slot.
# ---------------------------------------------------------------------------
V9_COURIER_ITEMS = ("STRAWBERRY", "MILK", "WOOL", "MELON")
V9_COURIER_FROM_HOUR = 12
_V9_COURIER_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
_V9_COURIER_IDLE = frozenset({"PASS", "NORTH", "SOUTH", "EAST", "WEST", "DROP"})
_V9_COURIER = {}
_V9_COURIER_REPORT = dict(courier_trips=0, courier_units=0, courier_errors=0)


def _v9_courier_walk(pos, target):
    x, y = pos
    tx, ty = target
    return ([["EAST"]] * max(0, tx - x) + [["WEST"]] * max(0, x - tx)
            + [["SOUTH"]] * max(0, ty - y) + [["NORTH"]] * max(0, y - ty))


def _v9_courier_plan(tape, unit, pos, commands, step, end):
    """Walk-and-drop route for an idle tape worker, or None if it has work left today."""
    if commands[unit] and commands[unit][0] not in _V9_COURIER_IDLE:
        return None
    for t in range(step + 1, end + 1):
        a = tape[t] if t < len(tape) else {}
        units = [a.get("farmer") or ["PASS"]] + list(a.get("hands") or [])
        command = units[unit] if unit < len(units) else ["PASS"]
        if command and command[0] not in _V9_COURIER_IDLE:
            return None
    target = min(_V9_COURIER_ACCESS, key=lambda a: abs(a[0] - pos[0]) + abs(a[1] - pos[1]))
    walk = _v9_courier_walk(pos, target)
    return walk + [["DROP"]] if len(walk) <= end - step else None


def _v9_courier(obs, action, st):
    step = int(obs["step"])
    player = int(obs["player"])
    if step >= 718 or step % 24 < V9_COURIER_FROM_HOUR:
        return action
    day = step // 24
    if st.get("day") != day:
        st["day"] = day
        st["plans"] = {}
    native = _IMPL.chassis.players.get(player)
    if not native or native.get("route") not in _IMPL.chassis.routes:
        return action
    tape = _IMPL.chassis.routes[native["route"]]
    farm = obs["farms"][player]
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]
    inventories = obs["private"]["inventories"]
    commands = [list(action.get("farmer") or ["PASS"])] + [list(c) for c in (action.get("hands") or [])]
    commands += [["PASS"]] * (len(positions) - len(commands))
    end = day * 24 + 23
    plans = st["plans"]
    # Only tape workers: overlay-dedicated hands are appended after the tape's crew.
    crew = 1 + max(len(tape[t].get("hands") or []) for t in range(day * 24, min(len(tape), end + 1)))
    delivered = {}
    changed = False
    for unit, pos in enumerate(positions[:crew]):
        inventory = inventories[unit] if unit < len(inventories) else {}
        cargo = {k: int(v) for k, v in inventory.items() if k in V9_COURIER_ITEMS and int(v) > 0}
        plan = plans.get(unit)
        if plan is None:
            if not cargo or native.get("pending", {}).get(unit):
                continue
            route = _v9_courier_plan(tape, unit, pos, commands, step, end)
            if route is None:
                continue
            plan = plans[unit] = {"route": route, "start": step}
            _V9_COURIER_REPORT["courier_trips"] += 1
        index = step - plan["start"]
        if index >= len(plan["route"]):
            continue
        command = plan["route"][index]
        if command == ["DROP"]:
            if pos not in _V9_COURIER_ACCESS:
                plans[unit] = {"route": [], "start": step}
                continue
            for item, n in cargo.items():
                delivered[item] = delivered.get(item, 0) + n
        commands[unit] = command
        changed = True
    if not changed:
        return action
    result = dict(action)
    result["farmer"], result["hands"] = commands[0], commands[1:]
    if delivered:
        market = [list(o) for o in action.get("market") or []]
        prices = obs["market"]["prices"]
        for item, n in sorted(delivered.items(), key=lambda kv: -int(prices.get(kv[0], 0)) * kv[1]):
            if int(prices.get(item, 0)) < 2:
                continue
            existing = next((o for o in market if o and o[0] == "SELL" and len(o) >= 3 and o[1] == item), None)
            if existing is not None:
                existing[2] = int(existing[2]) + n
                market.remove(existing)
                market.insert(0, existing)
            elif len(market) < MAX_ORDERS:
                market.insert(0, ["SELL", item, n])
            _V9_COURIER_REPORT["courier_units"] += n
        result["market"] = market
    return result


_V9_COURIER_PARENT = agent


def agent(observation, configuration=None):
    player, step = int(observation["player"]), int(observation["step"])
    st = _V9_COURIER.get(player)
    if st is None or step <= st["step"]:
        st = _V9_COURIER[player] = {"step": -1}
        if step == 0:
            _V9_COURIER_REPORT.update(courier_trips=0, courier_units=0, courier_errors=0)
    st["step"] = step
    action = _V9_COURIER_PARENT(observation, configuration)
    try:
        return _v9_courier(observation, action, st)
    except Exception:
        _V9_COURIER_REPORT["courier_errors"] += 1
        return action


agent.telemetry = _V9_COURIER_REPORT
agent = globals().pop("agent")


# ---------------------------------------------------------------------------
# v9 CARROT: plant carrots instead of wheat when the carrot book pays for it.
#
# The tape replants wheat on the same short cycle a carrot needs (water daily,
# harvest at age 2-4), so the swap keeps every worker's schedule intact.  A
# watered wheat plant yields 4 and a carrot 3, for $10 more seed, so the swap
# only pays once the carrot quote clears V9_CARROT_RATIO x the wheat quote --
# which pet cafes and farmers markets make happen by draining the hinge book.
# Wheat is also feed, so the swap stops while the shed holds less than
# V9_CARROT_WHEAT_RESERVE wheat.
# ---------------------------------------------------------------------------
V9_CARROT_RATIO = 1.8
V9_CARROT_FIRST_DAY = 10
V9_CARROT_LAST_DAY = 23
V9_CARROT_WHEAT_RESERVE = 40
V9_CARROT_BOOM_RATIO = 3.5   # from this ratio the feed reserve is bought instead of grown
V9_CARROT_BOOM_RESERVE = 10
_V9_CARROT_REPORT = dict(carrot_swaps=0, carrot_seed_swaps=0, carrot_errors=0)


def _v9_carrot(obs, action, st):
    step = int(obs["step"])
    day = step // 24
    prices = obs["market"]["prices"]
    private = obs["private"]
    commands = [list(action.get("farmer") or ["PASS"])] + [list(c) for c in (action.get("hands") or [])]
    market = [list(o) for o in action.get("market") or []]
    changed = False
    if st.get("tiles"):
        # swapped carrots die at the start of age 4, but the wheat tape may harvest at age 4:
        # harvest them on the age-3 watering visit instead
        _farm = obs["farms"][int(obs["player"])]
        _pos = [_farm["farmer"]] + list(_farm["hands"])
        for _i, c in enumerate(commands[:len(_pos)]):
            if c != ["WATER"]:
                continue
            _p = tuple(_pos[_i])
            if st["tiles"].get(_p) != day - 3:
                continue
            _t = _farm["tiles"][_p[1]][_p[0]]
            if isinstance(_t, dict) and _t.get("crop") == "CARROT" and int(_t.get("planted_day", -9)) == day - 3 and int(_t.get("yield_units", 0)) > 0:
                commands[_i] = ["HARVEST"]
                changed = True
                _V9_CARROT_REPORT["carrot_rescues"] = _V9_CARROT_REPORT.get("carrot_rescues", 0) + 1
    wheat_held = int(private["shed"].get("WHEAT", 0)) + sum(int(i.get("WHEAT", 0)) for i in private["inventories"])
    ratio = int(prices.get("CARROT", 0)) / max(1, int(prices.get("WHEAT", 99)))
    boom = ratio >= V9_CARROT_BOOM_RATIO
    reserve = V9_CARROT_BOOM_RESERVE if boom else V9_CARROT_WHEAT_RESERVE
    if boom and V9_CARROT_FIRST_DAY <= day <= V9_CARROT_LAST_DAY and wheat_held < V9_CARROT_WHEAT_RESERVE:
        # Carrots are worth several wheat each: buy the feed the swap no longer grows.
        topup = V9_CARROT_WHEAT_RESERVE - wheat_held
        budget = float(obs["farms"][int(obs["player"])]["money"]) - 1500
        qty = min(topup, int(budget // max(1, int(prices.get("WHEAT", 99)) + 5)))
        if qty > 0 and len(market) < MAX_ORDERS and not any(o[:2] == ["BUY_PRODUCT", "WHEAT"] for o in market if len(o) >= 2):
            market.append(["BUY_PRODUCT", "WHEAT", qty])
            changed = True
    if (V9_CARROT_FIRST_DAY <= day <= V9_CARROT_LAST_DAY and wheat_held >= reserve
            and ratio >= V9_CARROT_RATIO):
        carrot_seeds = int(private["seeds"].get("CARROT", 0)) - sum(1 for c in commands if c[:2] == ["PLANT", "CARROT"])
        _farm = obs["farms"][int(obs["player"])]
        _pos = [_farm["farmer"]] + list(_farm["hands"])
        for _i, c in enumerate(commands):
            if c[:2] == ["PLANT", "WHEAT"] and carrot_seeds > 0:
                c[1] = "CARROT"
                carrot_seeds -= 1
                changed = st["swapped"] = True
                _V9_CARROT_REPORT["carrot_swaps"] += 1
                if _i < len(_pos):
                    st.setdefault("tiles", {})[tuple(_pos[_i])] = day
        for o in market:
            if len(o) >= 3 and o[:2] == ["BUY_SEED", "WHEAT"]:
                o[1] = "CARROT"
                changed = st["swapped"] = True
                _V9_CARROT_REPORT["carrot_seed_swaps"] += int(o[2])
    result = dict(action)
    result["farmer"], result["hands"], result["market"] = commands[0], commands[1:], market
    if st.get("swapped") and day < 24:
        # Swapped carrots have no planned sale on the tape before its own carrot days.
        stock = projected_shed(result, FarmView(obs)).get("CARROT", 0)
        selling = sum(int(o[2]) for o in market if len(o) >= 3 and o[:2] == ["SELL", "CARROT"])
        if stock > selling and len(market) < MAX_ORDERS and int(prices.get("CARROT", 0)) >= 2:
            market.insert(0, ["SELL", "CARROT", stock - selling])
            changed = True
    return result if changed else action


_V9_CARROT = {}


_V9_CARROT_PARENT = agent


def agent(observation, configuration=None):
    player, step = int(observation["player"]), int(observation["step"])
    st = _V9_CARROT.get(player)
    if st is None or step <= st["step"]:
        st = _V9_CARROT[player] = {"step": -1}
        if step == 0:
            _V9_CARROT_REPORT.update(carrot_swaps=0, carrot_seed_swaps=0, carrot_errors=0)
    st["step"] = step
    action = _V9_CARROT_PARENT(observation, configuration)
    try:
        return _v9_carrot(observation, action, st)
    except Exception:
        _V9_CARROT_REPORT["carrot_errors"] += 1
        return action


agent.telemetry = _V9_CARROT_REPORT
agent = globals().pop("agent")


# ---------------------------------------------------------------------------
# v9 HERD: raise the tape's day-10 geese as sheep or cows when the draw pays.
#
# A cared goose lays 2 eggs a day into a $50 book; a cared sheep grows 4 wool
# every 3 days into a $200 book, a cow 3 milk every 2 days into a $160 book.
# The tape handles its geese exactly like pasture animals (build, pick up,
# place, feed, care, collect fertilizer, harvest), so swapping the species at
# the first goose purchase keeps every worker's schedule.  Wool needs a yarn
# store to hold its price and milk needs pizza / ice cream / smoothie shops;
# egg shops keep the geese.  The swapped herd's extra product has no planned
# sale on the tape, so anything beyond the tape's remaining planned sales is
# sold as it reaches the shed.
# ---------------------------------------------------------------------------
V9_HERD_MIN_WOOL = 150         # wool quote needed to swap to sheep
V9_HERD_MIN_MILK = 150         # milk quote needed to swap to cows
V9_HERD_MAX_EGG_SHOPS = 1         # sheep swap: at most this many BAKERY + BRUNCH_SPOT
V9_HERD_MAX_EGG_SHOPS_COW = 0  # cow swap: at most this many
V9_HERD_MIN_MILK_SHOPS = 3      # cow swap: at least this many PIZZA / ICE_CREAM / SMOOTHIE
_V9_HERD_PRODUCT = {"SHEEP": "WOOL", "COW": "MILK"}
_V9_HERD = {}
_V9_HERD_REPORT = dict(herd_species="", herd_rewrites=0, herd_extra_sold=0, herd_errors=0)


def _v9_herd_choose(obs):
    shops = obs["town"]["unlocked_shops"]
    prices = obs["market"]["prices"]
    egg_shops = sum(s in ("BAKERY", "BRUNCH_SPOT") for s in shops)
    if (egg_shops <= V9_HERD_MAX_EGG_SHOPS and "YARN_STORE" in shops
            and int(prices.get("WOOL", 0)) >= V9_HERD_MIN_WOOL):
        return "SHEEP"
    milk_shops = sum(s in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP") for s in shops)
    if (egg_shops <= V9_HERD_MAX_EGG_SHOPS_COW and milk_shops >= V9_HERD_MIN_MILK_SHOPS
            and int(prices.get("MILK", 0)) >= V9_HERD_MIN_MILK):
        return "COW"
    return None


def _v9_herd(obs, action, st):
    step = int(obs["step"])
    orders = action.get("market") or []
    if st.get("species") is None and not st.get("decided"):
        if step >= 216 and any(len(o) >= 2 and o[:2] == ["BUY_ANIMAL", "GOOSE"] for o in orders):
            st["decided"] = True
            st["species"] = _v9_herd_choose(obs)
            _V9_HERD_REPORT["herd_species"] = st["species"] or ""
    species = st.get("species")
    if not species:
        return action
    product = _V9_HERD_PRODUCT[species]
    commands = [list(action.get("farmer") or ["PASS"])] + [list(c) for c in (action.get("hands") or [])]
    market = [list(o) for o in orders]
    for c in commands:
        if c and c[0] == "BUILD_COOP":
            c[0] = "BUILD_PASTURE"
            _V9_HERD_REPORT["herd_rewrites"] += 1
        elif len(c) >= 2 and c[0] in ("PICKUP", "PLACE") and c[1] == "GOOSE":
            c[1] = species
            _V9_HERD_REPORT["herd_rewrites"] += 1
    rewritten = []
    for o in market:
        if len(o) >= 3 and o[:2] == ["BUY_ANIMAL", "GOOSE"]:
            rewritten.append(["BUY_ANIMAL", species, o[2]])
        elif len(o) >= 2 and o[:2] == ["SELL", "EGG"] and not any(isinstance(t_, dict) and t_.get("animal") == "GOOSE" for r_ in obs["farms"][int(obs["player"])]["tiles"] for t_ in r_):
            continue
        else:
            rewritten.append(o)
    result = dict(action)
    result["farmer"], result["hands"], result["market"] = commands[0], commands[1:], rewritten
    player = int(obs["player"])
    native = _IMPL.chassis.players.get(player)
    if native and native.get("route") in _IMPL.chassis.routes and step < 718:
        stock = projected_shed(result, FarmView(obs)).get(product, 0)
        selling = sum(int(o[2]) for o in rewritten if len(o) >= 3 and o[:2] == ["SELL", product])
        planned = _IMPL.chassis.future_sells(native["route"], product, step + 1)
        extra = stock - selling - planned
        if extra > 0 and len(rewritten) < MAX_ORDERS and int(obs["market"]["prices"].get(product, 0)) >= 2:
            rewritten.insert(0, ["SELL", product, extra])
            _V9_HERD_REPORT["herd_extra_sold"] += extra
    return result


_V9_HERD_PARENT = agent


def agent(observation, configuration=None):
    player, step = int(observation["player"]), int(observation["step"])
    st = _V9_HERD.get(player)
    if st is None or step <= st["step"]:
        st = _V9_HERD[player] = {"step": -1}
        if step == 0:
            _V9_HERD_REPORT.update(herd_species="", herd_rewrites=0, herd_extra_sold=0, herd_errors=0)
    st["step"] = step
    action = _V9_HERD_PARENT(observation, configuration)
    try:
        return _v9_herd(observation, action, st)
    except Exception:
        _V9_HERD_REPORT["herd_errors"] += 1
        return action


agent.telemetry = _V9_HERD_REPORT
agent = globals().pop("agent")


# ---------------------------------------------------------------------------
# v9 FERT: spend carried fertilizer on young wheat and carrots.
#
# Workers that tend animals carry collected fertilizer back to the shed, where
# the tape sells it into a book that falls from $55 on day 14 to $10 by day 27.
# On a short crop the same unit is worth far more: a watered wheat plant ends at
# 4 units, but fertilized for its yield window it caps at 6.  A worker that
# carries fertilizer and is about to water a wheat or carrot plant one day
# after planting (watered on planting day, not yet fertilized) fertilizes it
# instead; the tape waters it again on the following days.  Fertilizer the
# worker's own tape commands still spend today is left alone, and the layer only
# acts from day 16, once the fertilizer book is worth less than two wheat.
# ---------------------------------------------------------------------------
V9_FERT_CROPS = ("WHEAT", "CARROT")
V9_FERT_AGES = (1,)
V9_FERT_FIRST_DAY = 14
_V9_FERT_REPORT = dict(fert_applied=0, fert_errors=0)


def _v9_fert(obs, action):
    step = int(obs["step"])
    day = step // 24
    if day < V9_FERT_FIRST_DAY or step >= 700:
        return action
    player = int(obs["player"])
    farm = obs["farms"][player]
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]
    inventories = obs["private"]["inventories"]
    commands = [list(action.get("farmer") or ["PASS"])] + [list(c) for c in (action.get("hands") or [])]
    changed = False
    native = _IMPL.chassis.players.get(player)
    tape = _IMPL.chassis.routes.get(native.get("route")) if native else None
    planned = {}
    if tape is not None:
        # fertilizer this worker's own tape commands still spend today
        for t in range(step, min(len(tape), day * 24 + 24)):
            a = tape[t] or {}
            for u, c in enumerate([a.get("farmer") or ["PASS"]] + list(a.get("hands") or [])):
                if c and c[0] == "FERTILIZE":
                    planned[u] = planned.get(u, 0) + 1
    carried = {}
    targeted = set()
    for unit, command in enumerate(commands[:len(positions)]):
        if not command or command[0] != "WATER":
            continue
        x, y = positions[unit]
        tile = farm["tiles"][y][x]
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("crop") in V9_FERT_CROPS):
            continue
        if (day - int(tile["planted_day"])) not in V9_FERT_AGES or tile.get("watered_today"):
            continue
        if int(tile.get("consecutive_unwatered", 1)) != 0 or int(tile.get("fertilized_until_day", -1)) >= day:
            continue
        have = carried.setdefault(unit, int((inventories[unit] if unit < len(inventories) else {}).get("FERTILIZER", 0))
                                  - planned.get(unit, 0))
        if have <= 0 or (x, y) in targeted:
            continue
        commands[unit] = ["FERTILIZE"]
        carried[unit] = have - 1
        targeted.add((x, y))
        changed = True
        _V9_FERT_REPORT["fert_applied"] += 1
    if not changed:
        return action
    result = dict(action)
    result["farmer"], result["hands"] = commands[0], commands[1:]
    return result


_V9_FERT_PARENT = agent


def agent(observation, configuration=None):
    if int(observation["step"]) == 0:
        _V9_FERT_REPORT.update(fert_applied=0, fert_errors=0)
    action = _V9_FERT_PARENT(observation, configuration)
    try:
        return _v9_fert(observation, action)
    except Exception:
        _V9_FERT_REPORT["fert_errors"] += 1
        return action


agent.telemetry = _V9_FERT_REPORT
agent = globals().pop("agent")


# ---------------------------------------------------------------------------
# v9 OPENING: a cash-safe step-0 wheat trade.
#
# Every route tape opens with a wheat round trip
#     step 0: BUY 13, BUY 30, SELL 30      step 1: SELL 13, BUY 5   (net +5)
# and then runs days 0-9 with only ~$6 of cash slack (minimum at step 32).
# The round trip wins cash from rivals whose own opening buys into it, but
# against openings that dump wheat in the same slots (e.g. BUY 43 / SELL 20 /
# SELL 22 or BUY 30 / SELL all) it ends step 1 up to $75 short; the day-1
# wheat and hire orders then fail, the herd goes unfed, and by days 5-8 the
# strawberry seed orders fail too (18-21 plants instead of 33, -20k..-65k).
#
# Replacing it with BUY 10, SELL 5 at step 0 (still net +5, nothing at
# step 1) leaves >= $1,050 after step 1 against all 6,648 recorded openings
# in the metav2 / M&M replays (exact market simulation, build/v9/opensim.py),
# and $2 more than the round trip against the V38/V39 tape lineage.
# ---------------------------------------------------------------------------
V9_OPENING_STEP0 = (("BUY_PRODUCT", "WHEAT", 20), ("SELL", "WHEAT", 15))
V9_OPENING_TAPE = ((("BUY_PRODUCT", "WHEAT", 13), ("BUY_PRODUCT", "WHEAT", 30), ("SELL", "WHEAT", 30)),
                   (("SELL", "WHEAT", 13), ("BUY_PRODUCT", "WHEAT", 5)))


def _v9_opening(obs, action):
    step = int(obs["step"])
    if step > 1:
        return action
    native = _IMPL.chassis.players.get(int(obs["player"]))
    if not native or native.get("route") not in _IMPL.chassis.routes:
        return action
    market = [list(o) for o in action.get("market") or []]
    wheat = [o for o in market if len(o) >= 3 and o[0] in ("BUY_PRODUCT", "SELL") and o[1] == "WHEAT"]
    if tuple((o[0], o[1], int(o[2])) for o in wheat) != V9_OPENING_TAPE[step]:
        return action  # the tape's opening was changed upstream; leave it alone
    rest = [o for o in market if o not in wheat]
    result = dict(action)
    result["market"] = ([list(o) for o in V9_OPENING_STEP0] if step == 0 else []) + rest
    return result


_V9_OPENING_PARENT = agent


def agent(observation, configuration=None):
    action = _V9_OPENING_PARENT(observation, configuration)
    try:
        return _v9_opening(observation, action)
    except Exception:
        return action


agent = globals().pop("agent")




# ---------------------------------------------------------------------------
# v9/2 PREDICT: forecast the rival's premium sales from a library of recorded
# streams and sell our planned lots just before theirs.
#
# Each turn the rival's executed sales are recovered exactly like RACE does
# (inventory delta + town draw - own sales).  Library streams with the same
# first two shops are scored against the rival's recovered sale ticks of the last
# 240 turns; when most of the best TOP streams sell >= K units of a product in the
# next two turns, our tape's planned sales of that product within H turns are
# sold now.
# ---------------------------------------------------------------------------
import json as _v92_json, os as _v92_os, zlib as _v92_zlib, base64 as _v92_b64
_V92_P_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "EGG", "MELON")
_V92_P_USE = ('MILK', 'WOOL', 'STRAWBERRY')
_V92_P_H = 48
_V92_P_K = 4
_V92_P_TOP = 1
_V92_P_EVERY = 3
_V92_EP = None          # panel: current episode (library excludes same-parity episodes)
_V92_P_LIB = None
_V92_P = {}
_V92_P_REPORT = dict(pred_units=0, pred_fires=0, pred_errors=0, pred_rejects=0)
_V92_P_MODE = 'as_is'  # 'as_is', 'score_gate', 'disabled'
_V92_P_MIN_SCORE = 5.0  # minimum matching score required to trust forecast



_V92_P_BLOB = __import__('publication_assets').value('observed_56713902_001_006')
_V92_P_INDEX = [(0, 24351), (24351, 23453), (47804, 25995), (73799, 23384), (97183, 16234), (113417, 17537), (130954, 22124), (153078, 11768), (164846, 22007), (186853, 18184), (205037, 21673), (226710, 16105), (242815, 17743), (260558, 25579), (286137, 19595), (305732, 14257), (319989, 21574), (341563, 20658), (362221, 21185), (383406, 31913), (415319, 18530), (433849, 25386), (459235, 22171), (481406, 19768), (501174, 21173), (522347, 17644), (539991, 29906), (569897, 26025), (595922, 18397), (614319, 32350), (646669, 15249), (661918, 16105), (678023, 16332), (694355, 20165), (714520, 15688), (730208, 22362), (752570, 15957), (768527, 23124), (791651, 16137), (807788, 14851), (822639, 18035), (840674, 23725), (864399, 19752), (884151, 13858), (898009, 29738), (927747, 27298), (955045, 14888), (969933, 26842), (996775, 18337), (1015112, 18811), (1033923, 16243), (1050166, 12205), (1062371, 16791), (1079162, 18399), (1097561, 27007), (1124568, 19223), (1143791, 27568), (1171359, 15692), (1187051, 18199), (1205250, 14269), (1219519, 27888), (1247407, 19941), (1267348, 20908), (1288256, 31571)]
_V92_P_RAW = None


def _v92_p_lib():
    global _V92_P_LIB, _V92_P_RAW
    if _V92_P_LIB is None:
        _V92_P_LIB = {}
    return _V92_P_LIB


def _v92_p_pair(shops):
    lib = _v92_p_lib()
    if shops in lib:
        return lib[shops]
    global _V92_P_RAW
    names = ['BAKERY', 'BRUNCH_SPOT', 'FARMERS_MARKET', 'ICE_CREAM_SHOP', 'PET_CAFE', 'PIZZA_SHOP', 'SMOOTHIE_SHOP', 'YARN_STORE']
    out = []
    if len(shops) == 2 and shops[0] in names and shops[1] in names:
        if _V92_P_RAW is None:
            _V92_P_RAW = _v92_zlib.decompress(_v92_b64.b85decode(_V92_P_BLOB))
        start, length = _V92_P_INDEX[names.index(shops[0]) * 8 + names.index(shops[1])]
        raw = _V92_P_RAW; pos = start
        n = raw[pos] | raw[pos + 1] << 8; pos += 2
        for _ in range(n):
            m = raw[pos] | raw[pos + 1] << 8; pos += 2
            ev = {}; last = 0
            for _ in range(m):
                d = raw[pos]; pos += 1
                if d == 255:
                    t = raw[pos] | raw[pos + 1] << 8; pos += 2
                else:
                    t = last + d
                ev[(t, raw[pos])] = raw[pos + 1]; pos += 2; last = t
            out.append((-1, ev))
    lib[shops] = out
    return out


def _v92_p_update(obs, st):
    player, step = int(obs["player"]), int(obs["step"])
    race = _V9_RACE.get(player) or {}
    prev = race.get("prev")
    if not prev or prev["step"] != step - 1:
        return
    inv = obs["market"]["inventory"]
    draw = _v9_town_draw(prev["shops"], prev["step"])
    for i, item in enumerate(_V92_P_ITEMS):
        if prev["prices"].get(item, 0) <= 3:
            continue
        sold = inv[item] - prev["inventory"][item] + draw.get(item, 0) - prev["own"].get(item, 0)
        if sold >= 2:
            st["obs"][(step - 1, i)] = sold


def _v92_p_forecast(obs, st):
    step = int(obs["step"])
    shops = tuple(obs["town"]["unlocked_shops"][:2])
    cands = _v92_p_pair(shops)
    if _V92_EP is not None:
        cands = [c for c in cands if c[0] % 2 != _V92_EP % 2]
    seen = st["obs"]
    lo = step - 240
    scored = []
    recent = [(tt, i) for (tt, i) in seen if tt >= lo]
    for ep, ev in cands:
        m = f = 0
        for (tt, i), q in ev.items():
            if lo <= tt < step - 1:
                if (tt, i) in seen or (tt - 1, i) in seen or (tt + 1, i) in seen:
                    m += 1
                else:
                    f += 1
        miss = sum(1 for (tt, i) in recent if (tt, i) not in ev and (tt - 1, i) not in ev and (tt + 1, i) not in ev)
        scored.append((m - 0.5 * f - 0.5 * miss, ev))
    scored.sort(key=lambda x: -x[0])
    if _V92_P_MODE == 'score_gate':
        if not scored or scored[0][0] < _V92_P_MIN_SCORE:
            _V92_P_REPORT['pred_rejects'] += 1
            return []
    return [ev for _, ev in scored[:_V92_P_TOP]]


def _v92_predict(obs, action, st):
    if _V92_P_MODE == 'disabled':
        return action
    step = int(obs["step"])
    _v92_p_update(obs, st)
    if step < 150 or step >= 700:
        return action
    if step % _V92_P_EVERY == 0 or "best" not in st:
        st["best"] = _v92_p_forecast(obs, st)
    best = st["best"]
    if not best:
        return action
    native = _IMPL.chassis.players.get(int(obs["player"]))
    if not native or native.get("route") not in _IMPL.chassis.routes:
        return action
    tape = _IMPL.chassis.routes[native["route"]]
    market = [list(o) for o in action.get("market") or []]
    already = {o[1] for o in market if len(o) > 1 and o[0] in ("SELL", "BUY_PRODUCT")}
    stock = projected_shed(action, FarmView(obs))
    changed = False
    for i, item in enumerate(_V92_P_ITEMS):
        if item not in _V92_P_USE or item in already or len(market) >= MAX_ORDERS:
            continue
        votes = sum(1 for ev in best if ev.get((step + 1, i), 0) + ev.get((step + 2, i), 0) >= _V92_P_K)
        if votes < 1:
            continue
        ours = 0
        for t in range(step + 1, min(len(tape), step + _V92_P_H + 1)):
            ours += sum(min(100, int(o[2])) for o in (tape[t] or {}).get("market") or []
                        if len(o) >= 3 and o[0] == "SELL" and o[1] == item)
        qty = min(int(stock.get(item, 0)), ours)
        if qty > 0:
            market.insert(0, ["SELL", item, qty])
            _V92_P_REPORT["pred_units"] += qty
            _V92_P_REPORT["pred_fires"] += 1
            changed = True
    if not changed:
        return action
    result = dict(action)
    result["market"] = market[:MAX_ORDERS]
    return result


_V92_P_PARENT = agent


def agent(observation, configuration=None):
    player, step = int(observation["player"]), int(observation["step"])
    st = _V92_P.get(player)
    if st is None or step <= st["step"]:
        st = _V92_P[player] = {"step": -1, "obs": {}}
        if step == 0:
            _V92_P_REPORT.update(pred_units=0, pred_fires=0, pred_errors=0, pred_rejects=0)
    st["step"] = step
    action = _V92_P_PARENT(observation, configuration)
    try:
        return _v92_predict(observation, action, st)
    except Exception:
        _V92_P_REPORT["pred_errors"] += 1
        return action


agent.telemetry = _V92_P_REPORT
agent = globals().pop("agent")



# ---------------------------------------------------------------------------
# v9/2 PREDICT2: forecast the rival's premium sales from the whole library of
# recorded streams (every shop pair) and sell our planned lots just before theirs.
#
# Rival sales are recovered each turn like RACE (inventory delta + town draw - own
# sales).  Every library stream keeps an incremental score over the whole game:
#   matched ticks - PF * unmatched library ticks - PM * unmatched rival sales
# (+-1 turn tolerance, MILK / WOOL / STRAWBERRY).  The per-sale miss term is the same
# for every stream except those with a nearby tick, so the argmax is maintained from
# an inverted (tick, item) -> streams index.  When the best stream sells >= K units of
# a product in the next two turns, the tape's planned sales of it within H turns are
# sold now.
# ---------------------------------------------------------------------------
import json as _v92_json, os as _v92_os
_V92_Q_ITEMS = ("MILK", "WOOL", "STRAWBERRY")
_V92_Q_H = 48
_V92_Q_K = 4
_V92_Q_PF = 1.0
_V92_Q_PM = 0.5
_V92_Q_CACHE = {}
_V92_Q = {}
_V92_Q_REPORT = dict(pred_units=0, pred_fires=0, pred_errors=0)


def _v92_q_streams():
    """List of (ep, {(tick, item_index): qty}) over MILK/WOOL/STRAWBERRY (item index into _V92_Q_ITEMS)."""
    if "streams" not in _V92_Q_CACHE:
        path = None  # Frozen offline build: no environment-dependent external library.
        out = []
        if path:
            for x in _v92_json.load(open(path)):
                ev = {(t, i): q for t, i, q in x["ev"] if i <= 2}
                if ev:
                    out.append((x["ep"], ev))
        _V92_Q_CACHE["streams"] = out
    return _V92_Q_CACHE["streams"]


def _v92_q_index(parity):
    key = ("index", parity)
    if key not in _V92_Q_CACHE:
        evs = [ev for ep, ev in _v92_q_streams() if parity is None or ep % 2 != parity]
        index = {}
        for c, ev in enumerate(evs):
            for k in ev:
                index.setdefault(k, []).append(c)
        _V92_Q_CACHE[key] = (evs, index)
    return _V92_Q_CACHE[key]


def _v92_q_new_state():
    parity = None if _V92_EP is None else _V92_EP % 2
    evs, index = _v92_q_index(parity)
    n = len(evs)
    return {"step": -1, "obs": {}, "evs": evs, "index": index, "m": [0] * n, "f": [0] * n, "near": [0] * n,
            "score": [0.0] * n, "best": 0 if n else None, "done": 150}


def _v92_q_update(obs, st):
    player, step = int(obs["player"]), int(obs["step"])
    race = _V9_RACE.get(player) or {}
    prev = race.get("prev")
    seen = st["obs"]
    if prev and prev["step"] == step - 1:
        inv = obs["market"]["inventory"]
        draw = _v9_town_draw(prev["shops"], prev["step"])
        for i, item in enumerate(_V92_Q_ITEMS):
            if prev["prices"].get(item, 0) <= 3:
                continue
            sold = inv[item] - prev["inventory"][item] + draw.get(item, 0) - prev["own"].get(item, 0)
            if sold >= 2:
                seen[(step - 1, i)] = sold
    evs, index = st["evs"], st["index"]
    if not evs:
        return
    m, f, near, score = st["m"], st["f"], st["near"], st["score"]
    best = st["best"]
    rescan = False
    # finalize ticks up to step-2 (their +-1 neighbourhood of observations is known)
    while st["done"] <= step - 2:
        tau = st["done"]
        st["done"] += 1
        for i in range(3):
            hit = (tau, i) in seen or (tau - 1, i) in seen or (tau + 1, i) in seen
            for c in index.get((tau, i), ()):
                if hit:
                    m[c] += 1
                    score[c] += 1.0
                else:
                    f[c] += 1
                    score[c] -= _V92_Q_PF
                    if c == best:
                        rescan = True
            if (tau, i) in seen:
                touched = set(index.get((tau - 1, i), ())) | set(index.get((tau, i), ())) | set(index.get((tau + 1, i), ()))
                for c in touched:
                    near[c] += 1
                    score[c] += _V92_Q_PM
                    if score[c] > score[best]:
                        best = c
            for c in index.get((tau, i), ()):
                if score[c] > score[best]:
                    best = c
    if rescan:
        best = max(range(len(score)), key=score.__getitem__)
    st["best"] = best


def _v92_predict2(obs, action, st):
    step = int(obs["step"])
    _v92_q_update(obs, st)
    if step < 150 or step >= 700 or st["best"] is None:
        return action
    ev = st["evs"][st["best"]]
    native = _IMPL.chassis.players.get(int(obs["player"]))
    if not native or native.get("route") not in _IMPL.chassis.routes:
        return action
    tape = _IMPL.chassis.routes[native["route"]]
    market = [list(o) for o in action.get("market") or []]
    already = {o[1] for o in market if len(o) > 1 and o[0] in ("SELL", "BUY_PRODUCT")}
    stock = None
    changed = False
    for i, item in enumerate(_V92_Q_ITEMS):
        if item in already or len(market) >= MAX_ORDERS:
            continue
        if ev.get((step + 1, i), 0) + ev.get((step + 2, i), 0) < _V92_Q_K:
            continue
        ours = 0
        for t in range(step + 1, min(len(tape), step + _V92_Q_H + 1)):
            ours += sum(min(100, int(o[2])) for o in (tape[t] or {}).get("market") or []
                        if len(o) >= 3 and o[0] == "SELL" and o[1] == item)
        if stock is None:
            stock = projected_shed(action, FarmView(obs))
        qty = min(int(stock.get(item, 0)), ours)
        if qty > 0:
            market.insert(0, ["SELL", item, qty])
            _V92_Q_REPORT["pred_units"] += qty
            _V92_Q_REPORT["pred_fires"] += 1
            changed = True
    if not changed:
        return action
    result = dict(action)
    result["market"] = market[:MAX_ORDERS]
    return result


_V92_Q_PARENT = agent


def agent(observation, configuration=None):
    player, step = int(observation["player"]), int(observation["step"])
    st = _V92_Q.get(player)
    if st is None or step <= st["step"]:
        st = _V92_Q[player] = _v92_q_new_state()
    st["step"] = step
    action = _V92_Q_PARENT(observation, configuration)
    try:
        return _v92_predict2(observation, action, st)
    except Exception:
        _V92_Q_REPORT["pred_errors"] += 1
        return action


agent.telemetry = _V92_Q_REPORT
agent = globals().pop("agent")

# ---------------------------------------------------------------------------
# v9 RACE: fit the sale-reservation horizon to the rival's observed sale lead.
#
# Premium books crash within ~60 units of glut, so the first seller of a lot
# takes the price and the second sells into the crash.  The parent reserves
# planned tape sales a fixed four turns ahead; any deeper fixed horizon beats
# it head-to-head, but selling earlier than necessary gives away town-demand
# recovery against a rival that does not race.
#
# Everything here is public.  Each turn the rival's executed sales are
#
#   rival_sold[p] = inventory'[p] - inventory[p] + town_draw[p] - own_sold[p]
#
# (exact above the $1 floor, where sales never enter inventory).  When the
# rival sells a product while we still hold stock that our tape sells later,
# and the sale is not a late fill of our previous lot, the turns until our next
# planned sale are the rival's lead.  One horizon serves every product:
#
#   horizon = clamp(largest lead seen + RACE_MARGIN, RACE_DEFAULT, RACE_MAX)
#
# and it also lifts the parent's 72-turn block bound (patched into the
# parent's reservation by the release builder).
#
# v9/2: the shipped horizon is 40 turns with a 12-turn margin (was 6 and 4).
# Mirrors are the ladder's real opponent, and the premium books are first-come
# races, so reserve depth is the whole decision.  Against the 6/4 build the new
# setting wins 73-7 (+308) over 80 mirror games; against the shipped 32/12 build
# it wins 74-6 (+358).  Deeper is not better: 44/12 beats 40 head to head but
# drops the shallow-baseline record to 65-15, and 48/12 (a constant 48) falls to
# 14-26 against it, because a horizon past the rival's next lot gives up
# town-demand recovery for nothing.  The frozen top-30 stream panel is unchanged
# inside its noise (52.2% / +2,797 over 178 games vs 52.8% / +2,929 at 32/12) and
# the public field still goes 8-0.
#
# v9/2b: the reservation window starts at step 192 (day 8) instead of 288 (day 12),
# a one-line change in the parent's `_r36_reserve` gate made by the release builder.
# The herd's first milk and wool lots land on days 8-11 and the same-day sale
# reservation is what takes their price before a rival's lot lands; the two middle
# days of the tape's own schedule give that up.  Three fresh mirror blocks against
# the step-288 build: 32-0 (+147), 30-2 (+11), 30-2 (+10); and against the shallow
# 6/4 baseline the new build is if anything stronger, not weaker: 28-4 (+556) vs
# 28-4 (+406), 29-3 (+272), 31-1 (+359) vs 31-1 (+349).  Per-item horizons instead of
# one global horizon change nothing once the window starts at 192 (28 of 32 games
# identical), so the one-line gate is the whole change.
# ---------------------------------------------------------------------------
_RACE_HORIZON_MODE = 'conditional'  # options: 'as_is' (40, 48), 'conditional' (shop-demand aware), 'hz_12' (12, 24)
if _RACE_HORIZON_MODE == 'hz_24':
    V9_RACE_DEFAULT = 24
    V9_RACE_MAX = 36
elif _RACE_HORIZON_MODE == 'hz_12':
    V9_RACE_DEFAULT = 12
    V9_RACE_MAX = 24
else:
    V9_RACE_DEFAULT = 40
    V9_RACE_MAX = 48
V9_RACE_MARGIN = 12
V9_RACE_GAP = 3            # a sale this soon after our previous planned lot is a late fill
V9_RACE_WINDOW = 30        # turns of tape searched for planned sales around a rival sale
V9_RACE_ITEMS = ("CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL")
_V9_SHOP_ITEMS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_V9_RACE = {}
_V9_RACE_REPORT = dict(rival_sales=0, leads=0, race_errors=0)


def _v9_town_draw(shops, step):
    """Units each shop instance and the town centre remove after `step`'s market."""
    draw = dict.fromkeys(V9_RACE_ITEMS, 0)
    if step % 4 == 0:
        for shop in shops:
            items = _V9_SHOP_ITEMS.get(shop, ())
            for item in items:
                if item in draw:
                    draw[item] += 2 if len(items) == 1 else 1
    if step % 24 == 0:
        for item in draw:
            draw[item] += 1
    return draw


def _v9_planned_sells(tape, item, step):
    """Turns within V9_RACE_WINDOW of `step` at which the tape sells `item`."""
    out = []
    for t in range(max(0, step - V9_RACE_WINDOW), min(len(tape), step + V9_RACE_WINDOW + 1)):
        if any(o and o[0] == "SELL" and len(o) >= 3 and o[1] == item and int(o[2]) > 0
               for o in tape[t].get("market") or []):
            out.append(t)
    return out


def _v9_race_update(obs, st):
    """Recover last turn's rival sales and record the leads that prove racing."""
    prev = st["prev"]
    step = int(obs["step"])
    if not prev or prev["step"] != step - 1:
        return
    native = _IMPL.chassis.players.get(int(obs["player"]))
    if not native or native.get("route") not in _IMPL.chassis.routes:
        return
    tape = _IMPL.chassis.routes[native["route"]]
    inventory = obs["market"]["inventory"]
    draw = _v9_town_draw(prev["shops"], prev["step"])
    t = prev["step"]
    for item in V9_RACE_ITEMS:
        if prev["prices"].get(item, 0) <= 3:
            continue
        sold = inventory[item] - prev["inventory"][item] + draw[item] - prev["own"].get(item, 0)
        if sold < 2:
            continue
        _V9_RACE_REPORT["rival_sales"] += 1
        if prev["left"].get(item, 0) <= 0:
            continue
        planned = _v9_planned_sells(tape, item, t)
        after = [s for s in planned if s >= t]
        before = [s for s in planned if s < t]
        if not after or (before and t - before[-1] < V9_RACE_GAP):
            continue
        st["lead"] = max(st["lead"], after[0] - t)
        _V9_RACE_REPORT["leads"] += 1


_V9_RACE_PARENT = agent


def agent(observation, configuration=None):
    player, step = int(observation["player"]), int(observation["step"])
    st = _V9_RACE.get(player)
    if st is None or step <= st["step"]:
        st = _V9_RACE[player] = {"step": -1, "lead": -V9_RACE_MARGIN, "prev": None}
        if step == 0:
            _V9_RACE_REPORT.update(rival_sales=0, leads=0, race_errors=0)
    st["step"] = step
    try:
        _v9_race_update(observation, st)
        if _RACE_HORIZON_MODE == 'conditional':
            base_hz = min(V9_RACE_MAX, max(V9_RACE_DEFAULT, st["lead"] + V9_RACE_MARGIN))
            fast_hz = min(24, max(12, st["lead"] + V9_RACE_MARGIN))
            shops = observation.get("town", {}).get("unlocked_shops", [])
            _V9_ITEM_HZ[player] = {
                item: fast_hz if sum(1 for s in shops if item in _V9_SHOP_ITEMS.get(s, ())) >= 2 else base_hz
                for item in V9_RACE_ITEMS
            }
        else:
            horizon = min(V9_RACE_MAX, max(V9_RACE_DEFAULT, st["lead"] + V9_RACE_MARGIN))
            _V9_ITEM_HZ[player] = dict.fromkeys(V9_RACE_ITEMS, horizon)
    except Exception:
        _V9_RACE_REPORT["race_errors"] += 1
        _V9_ITEM_HZ.pop(player, None)
    action = _V9_RACE_PARENT(observation, configuration)
    try:
        stock = projected_shed(action, FarmView(observation))
        own = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in V9_RACE_ITEMS:
                n = min(max(0, int(o[2])), max(0, stock.get(o[1], 0) - own.get(o[1], 0)))
                own[o[1]] = own.get(o[1], 0) + n
        st["prev"] = {"step": step, "inventory": dict(observation["market"]["inventory"]),
                      "prices": dict(observation["market"]["prices"]), "own": own,
                      "left": {item: stock.get(item, 0) - own.get(item, 0) for item in V9_RACE_ITEMS},
                      "shops": list(observation["town"]["unlocked_shops"])}
    except Exception:
        _V9_RACE_REPORT["race_errors"] += 1
        st["prev"] = None
    return action


agent.telemetry = _V9_RACE_REPORT
agent = globals().pop("agent")


# ---------------------------------------------------------------------------
# v9 RACEPX: lead-sell a planned lot early only while its book is not glutted.
#
# The engine prices a product off the market inventory: below I0 the quote is above
# base, above I0 it is below.  The lead sale moves a lot one turn ahead of the tape's
# own plan, which is what takes the price when both sides hold the same lot -- but
# when the book is already above I0 the same units only fetch a lower price, and the
# town drain between the two turns is not enough to pay for it.
#
# Measured against the frozen top-20 streams the shipped build realizes below-base
# prices on exactly the products it floods (strawberry $107-123 vs a $120 base, milk
# $98-107 vs $160, wool $129-139 vs $200, melon $212 vs $250, fertilizer $43 vs $100)
# and above base on the ones the town drains (wheat $38 vs $25, carrot $54 vs $35,
# tomato $125 vs $60, egg $52 vs $50).
#
# This layer keeps the lead sale for products quoted at or above base + MARGIN and
# leaves the rest to the tape's own schedule.  The reservation (`_r36_reserve`) is
# untouched, so the RACE horizon still governs how far ahead lots may be pulled.
#
# Evidence (v9/3): mirror against the shipped build 35-13 (+220) over 48 fresh games;
# against the 6/4 ancestor 41-7 (+620) where the shipped build is 45-3 (+449); frozen
# top-20 panel 69/120 (+3,586) against 66/120 (+3,364); second panel 63/120 (+2,264)
# against 63/120 (+1,882); public field pool unchanged (14-2 vs cdb and fh11, 16-0
# vs fa103/fa141/fa238/wd14).
# ---------------------------------------------------------------------------
V9_RACEPX_BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
                  "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}
V9_RACEPX_MARGIN = 0
_v9_racepx_report = dict(racepx_skipped=0, racepx_sold=0, racepx_errors=0)
_V9_RACEPX_LEAD = Chassis._sell_lead


def _v9_racepx_lead(self, action, view, projected, route, step, next_sup):
    prices = view.prices
    blocked = {i for i in V9_RACEPX_BASE
               if prices.get(i, 0) <= V9_RACEPX_BASE[i] + V9_RACEPX_MARGIN}
    if not blocked:
        _v9_racepx_report["racepx_sold"] += 1
        return _V9_RACEPX_LEAD(self, action, view, projected, route, step, next_sup)
    nxt = step + 1
    unlock_period = 3 * self.cfg["turns_per_day"]
    if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
        return
    tape = self.routes[route]
    future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
    planned = {}
    for o in future.get("market") or []:
        if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
            planned[o[1]] = planned.get(o[1], 0) + max(0, int(o[2]))
    already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
    for item in PRODUCTS:
        if item in blocked or item in already or planned.get(item, 0) <= 0:
            continue
        qty = min(projected.get(item, 0), planned[item])
        if qty <= 0 or prices.get(item, 0) < self.cfg["min_sell_price"]:
            continue
        if not self._add_sell(action, item, qty, self.cfg["max_orders"], merge=False):
            break
        projected[item] -= qty
        next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        _v9_racepx_report["racepx_skipped"] += 1
    if next_sup["suppress"]:
        next_sup["due_step"] = nxt


_V9_RACEPX_PARENT = agent
Chassis._sell_lead = _v9_racepx_lead


def agent(observation, configuration=None):
    if int(observation["step"]) == 0:
        _v9_racepx_report.update(racepx_skipped=0, racepx_sold=0, racepx_errors=0)
    try:
        return _V9_RACEPX_PARENT(observation, configuration)
    except Exception:
        _v9_racepx_report["racepx_errors"] += 1
        return {"farmer": ["PASS"], "hands": [], "market": []}


agent.telemetry = _v9_racepx_report
agent = globals().pop("agent")


# ---------------------------------------------------------------------------
# v9 RACEGATE: the same glut gate for the *reservation* (the 40-turn pull-forward).
#
# `_r36_reserve` moves tape-planned sales up to the RACE horizon forward, item by
# item.  RACEPX only gated the one-turn lead sale; this layer gates the reservation
# too: an item whose quote is at or below its base price is left to the tape's own
# schedule.  The debt ledger is untouched for the items that are still reserved, so
# suppression stays consistent.
#
# Evidence: see README (v9/3 round).
# ---------------------------------------------------------------------------
V9_RACEGATE_BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
                    "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}
V9_RACEGATE_MARGIN = 0
_v9_racegate_report = dict(racegate_reserved_units=0, racegate_errors=0)
_V9_RACEGATE_RESERVE = _r36_reserve


def _r36_reserve(obs, action):
    step = int(obs["step"])
    if not 192 <= step < 696:
        return action
    prices = obs["market"]["prices"]
    glutted = {i for i in V9_RACEGATE_BASE
               if prices.get(i, 0) <= V9_RACEGATE_BASE[i] + V9_RACEGATE_MARGIN}
    if not glutted:
        return _V9_RACEGATE_RESERVE(obs, action)
    native = _IMPL.chassis.players[int(obs["player"])]
    tape = _IMPL.chassis.routes[native["route"]]
    _v9_hz = _V9_ITEM_HZ.get(int(obs["player"]))
    end = min(695, step + (max(_v9_hz.values()) if _v9_hz else _R37_HORIZONS.get(int(obs["player"]), 2)))
    if end <= step:
        return action
    commands = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
    view = FarmView(obs)
    if any(len(c) > 1 and c[0] == "PLACE" and c[1] in ANIMAL_STRUCTURE
           and view.inv(i).get(c[1], 0) > 0 for i, c in enumerate(commands[:len(view.positions)])):
        return action
    stock = projected_shed(action, view)
    market = action.get("market", [])
    blocked = {o[1] for o in market if len(o) > 1 and o[0] in ("SELL", "BUY_PRODUCT")}
    blocked.update(c[1] for c in commands if len(c) > 1 and c[0] == "PICKUP")
    blocked.update(c[1] for queue in native["pending"].values() for pos, c in queue
                   if len(c) > 1 and c[0] == "PICKUP")
    debts = native["sell_state"].setdefault("r36_debts", {})
    for item in PRODUCTS:
        if item in blocked or item in glutted or view.prices.get(item, 0) < 2:
            continue
        available = max(0, int(stock.get(item, 0)))
        if not available or len(market) >= 10:
            continue
        reservations = []
        item_end = min(end, step + _v9_hz[item]) if _v9_hz and item in _v9_hz else end
        for due_step in range(step + 1, item_end + 1):
            future = tape[due_step]
            work = [future.get("farmer") or ["PASS"], *(future.get("hands") or [])]
            if any(len(c) > 1 and c[:2] == ["PICKUP", item] for c in work):
                break
            if any(len(o) > 1 and o[:2] == ["BUY_PRODUCT", item] for o in future.get("market", [])):
                break
            planned = sum(max(0, int(o[2])) for o in future.get("market", [])
                          if len(o) >= 3 and o[:2] == ["SELL", item])
            amount = min(available, max(0, planned - debts.get(due_step, {}).get(item, 0)))
            if amount:
                reservations.append((due_step, amount))
                available -= amount
            if not available:
                break
        qty = sum(q for _, q in reservations)
        if qty:
            market.append(["SELL", item, qty])
            for due, q in reservations:
                debt = debts.setdefault(due, {})
                debt[item] = debt.get(item, 0) + q
            _R36_SALE_REPORT["sale_reserved_units"] += qty
            _R36_SALE_REPORT["sale_reservations"] += 1
            _v9_racegate_report["racegate_reserved_units"] += qty
    return action


_V9_RACEGATE_PARENT = agent


def agent(observation, configuration=None):
    if int(observation["step"]) == 0:
        _v9_racegate_report.update(racegate_reserved_units=0, racegate_errors=0)
    try:
        return _V9_RACEGATE_PARENT(observation, configuration)
    except Exception:
        _v9_racegate_report["racegate_errors"] += 1
        return {"farmer": ["PASS"], "hands": [], "market": []}


agent.telemetry = _v9_racegate_report
agent = globals().pop("agent")


# ==== layer ctrtable.py 
_P_ctrtable_336053 = agent

# ---------------------------------------------------------------------------
# v9/3 CTRTABLE: rival-specific early wheat counters.
# Under the BUY 20 | SELL 15 opening, a rival tape's turn-2 observation (rival money, market wheat)
# identifies it exactly.  For known cash-tight tapes we trade alongside their own early wheat orders
# in the same market slots (checked unique over 4,604 recorded games):
#   feel the agi (979.0, 9989): steps 7-8  BUY 5 slot 0, SELL 5 slot 1
#   Mother-Goose (33.0, 9990): step 3      BUY 20 slot 0, SELL 20 slot 1
# ---------------------------------------------------------------------------
CT_TABLE = {
    (979.0, 9989): ((7, 0, ("BUY_PRODUCT", "WHEAT", 5)), (7, 1, ("SELL", "WHEAT", 5)),
                    (8, 0, ("BUY_PRODUCT", "WHEAT", 5)), (8, 1, ("SELL", "WHEAT", 5))),
    (33.0, 9990): ((3, 0, ("BUY_PRODUCT", "WHEAT", 20)), (3, 1, ("SELL", "WHEAT", 20))),
}
_CT = {}
_CT_REPORT = dict(ct_fired=0, ct_errors=0)


def _ct_apply(obs, action, st):
    step = int(obs["step"])
    if step == 2:
        rival = obs["farms"][1 - int(obs["player"])]
        st["plan"] = CT_TABLE.get((round(float(rival["money"]), 3), int(obs["market"]["inventory"]["WHEAT"])))
        if st["plan"]:
            _CT_REPORT["ct_fired"] += 1
    plan = st.get("plan")
    if not plan:
        return action
    items = sorted((slot, list(o)) for t, slot, o in plan if t == step)
    if not items:
        return action
    market = [list(o) for o in action.get("market") or []]
    for slot, o in items:
        while len(market) < slot:
            market.append(["SELL", "WHEAT", 0])
        market.insert(slot, o)
    result = dict(action)
    result["market"] = market[:MAX_ORDERS]
    return result


def agent(observation, configuration=None):
    player, step = int(observation["player"]), int(observation["step"])
    st = _CT.get(player)
    if st is None or step <= st["step"]:
        st = _CT[player] = {"step": -1}
    st["step"] = step
    action = _P_ctrtable_336053(observation, configuration)
    try:
        return _ct_apply(observation, action, st)
    except Exception:
        _CT_REPORT["ct_errors"] += 1
        return action


agent.telemetry = _CT_REPORT
agent = globals().pop("agent")


# ==== layer overflow.py 
_P_overflow_338343 = agent

# ---------------------------------------------------------------------------
# v9/3 OVERFLOW (ported from public V43 R148, Ahmed Berat Ozer, Apache-2.0):
# at hour 23 the workers' cargo drops into a 100-unit shed; cargo that does not fit
# is destroyed.  Sell exactly the shed stock that the destroyed cargo would replace,
# so the complete post-dawn stock vector is unchanged and the sold units are extra.
# ---------------------------------------------------------------------------
_OV_REPORT = dict(ov_turns=0, ov_units=0, ov_errors=0)


def _ov_fields(obs, action):
    farm, private = _PLANNER_NS['_clone_state'](obs['farms'][obs['player']], obs['private'])
    commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    demand = {}
    for c in commands:
        if len(c) > 1 and c[0] == 'PLANT':
            demand[c[1]] = demand.get(c[1], 0) + 1
    blocked = {p for p, n in demand.items() if n > private['seeds'].get(p, 0)}
    for actor, c in enumerate(commands[:len(private['inventories'])]):
        if len(c) > 1 and c[0] == 'PLANT' and c[1] in blocked:
            continue
        _PLANNER_NS['_apply_unit_action'](farm, private, actor, c, 10, int(obs['step']) // 24, 24, 100)
    return farm, private


def _ov_same(a, b):
    return all(int(a.get(p, 0)) == int(b.get(p, 0)) for p in set(a) | set(b))


def _ov_apply(obs, action):
    if int(obs['step']) % 24 != 23:
        return action
    orders = action.get('market') or []
    if len(orders) >= 10 or not _r97_budget(obs, orders):
        return action
    _, private = _ov_fields(obs, action)
    stock, _, _ = _r97_market_stock(private['shed'], orders)
    original, loss = _r97_delivery(stock, private, True)
    if not loss:
        return action
    remaining = max(0, 100 - sum(stock.values()))
    tail = []
    for bag in private['inventories']:
        for item, n in bag.items():
            n = max(0, int(n)); take = min(n, remaining); remaining -= take
            if n > take:
                tail.extend([item] * (n - take))
    released = {}; best = None
    for item in tail:
        released[item] = released.get(item, 0) + 1
        if item not in obs['market']['prices'] or released[item] > stock.get(item, 0):
            break
        if len(orders) + len(released) > 10:
            break
        proposed = list(orders) + [['SELL', p, n] for p, n in released.items()]
        after, _, _ = _r97_market_stock(private['shed'], proposed)
        final, _ = _r97_delivery(after, private, True)
        if _ov_same(original, final):
            best = (proposed, dict(released))
    if best is None:
        return action
    _OV_REPORT['ov_turns'] += 1
    _OV_REPORT['ov_units'] += sum(best[1].values())
    return dict(action, market=best[0])


def agent(observation, configuration=None):
    action = _P_overflow_338343(observation, configuration)
    try:
        return _ov_apply(observation, action)
    except Exception:
        _OV_REPORT['ov_errors'] += 1
        return action


agent.telemetry = _OV_REPORT
agent = globals().pop("agent")


# One-worker non-harvest service for the inherited six-sheep project.
# All feeding and care are mandatory. Optional fertilizer collection only uses
# leftover time; setup, wool harvests, and late-start days keep the old crew.
_SL_REQUEST = _v233_request
_SL_WORKER = _v233_worker
_SL_REPORT = dict(compact_days=0, confirmed=0, collect=0)
_SL_TILES = ((5,5),(6,5),(7,5),(7,6),(6,6),(5,6))


def _sl_dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])


def _sl_path(pos,targets):
    return min(_r53_permutations(targets),key=lambda path:(_sl_dist(pos,path[0])+sum(_sl_dist(a,b) for a,b in zip(path,path[1:])),path)) if targets else ()


def _v233_request(obs,action,state,native):
    result=_SL_REQUEST(obs,action,state,native)
    pending=state.get('pending')
    if result is action or not pending or pending['initial']:
        return result
    farm=obs['farms'][obs['player']];hour=int(obs['step'])%24
    tiles=[farm['tiles'][y][x] for x,y in _SL_TILES]
    if not all(isinstance(t,dict) and t.get('animal')=='SHEEP' and t.get('yield_units',0)==0 for t in tiles):
        return result
    # Exact spawn after native commands/hires, and a full feed pickup turn.
    ready,spawn=_r62_input_start(obs,action,0)
    path=_sl_path(spawn,_SL_TILES)
    travel=_sl_dist(spawn,path[0])+sum(_sl_dist(a,b) for a,b in zip(path,path[1:]))
    mandatory=sum(not t.get('fed_today') for t in tiles)+sum(not t.get('cared_today') for t in tiles)
    available=min((int(obs['step'])//24+1)*24,719)-ready
    if travel+mandatory>available:
        return result
    # Collection can be interleaved along the essential route. Charge the
    # discarded fertilizer against the saved wage, including final delivery.
    native_hires=sum(o and o[0]=='HIRE' for o in action.get('market',[]))
    saved=_v219_fib(farm['hires_today']+native_hires+1)
    delivery=_sl_dist(path[-1],_v219_home(path[-1]))+1 if int(obs['step'])//24==29 else 0
    possible=max(0,min(6,available-travel-mandatory-delivery))
    if saved<=(6-possible)*obs['market']['prices']['FERTILIZER']:
        return result
    out=copy.deepcopy(result)
    assert out['market'][-2:]==[['HIRE'],['HIRE']]
    out['market'].pop()
    pending.update(count=1,targets=path)
    _V233_REPORT['sheep_hire_requests']-=1
    _SL_REPORT['compact_days']+=1
    return out


def _v233_worker(obs,actor,targets):
    if len(targets)!=6:
        return _SL_WORKER(obs,actor,targets)
    farm=obs['farms'][obs['player']];private=obs['private'];step=int(obs['step'])
    pos=tuple(farm['hands'][actor-1]);inv=private['inventories'][actor]
    needed=[];hungry=0
    for target in targets:
        x,y=target;t=farm['tiles'][y][x]
        if not isinstance(t,dict) or t.get('animal')!='SHEEP':
            return _SL_WORKER(obs,actor,targets)
        if not t['fed_today']:hungry+=1
        if not t['fed_today'] or not t['cared_today']:needed.append(target)
    home=_v219_home(pos)
    if hungry>inv.get('WHEAT',0):
        return _v219_walk(pos,home) or ['PICKUP','WHEAT',min(hungry,private['shed'].get('WHEAT',0))]
    if needed:
        path=_sl_path(pos,needed)
        current=farm['tiles'][pos[1]][pos[0]]
        if pos in targets and isinstance(current,dict) and current.get('fed_today') and current.get('cared_today') and current.get('fertilizer_available'):
            travel=_sl_dist(pos,path[0])+sum(_sl_dist(a,b) for a,b in zip(path,path[1:]))
            work=sum(not farm['tiles'][y][x]['fed_today'] for x,y in path)+sum(not farm['tiles'][y][x]['cared_today'] for x,y in path)
            delivery=_sl_dist(path[-1],_v219_home(path[-1]))+1 if step//24==29 else 0
            remaining=min((step//24+1)*24,719)-step
            if 1+travel+work+delivery<=remaining:
                _SL_REPORT['collect']+=1
                return ['COLLECT_FERTILIZER']
        target=path[0];t=farm['tiles'][target[1]][target[0]]
        return _v219_walk(pos,target) or (['FEED'] if not t['fed_today'] else ['CARE'])
    # Essential work is complete. Collect what can still reach the shed on
    # the final day; on earlier days the normal midnight deposit is sufficient.
    remaining=719-step if step//24==29 else 24-step%24
    tasks=[]
    for target in targets:
        t=farm['tiles'][target[1]][target[0]]
        if not t.get('fertilizer_available'):continue
        dist=_sl_dist(pos,target)
        ret=_sl_dist(target,_v219_home(target))+1 if step//24==29 else 0
        if dist+1+ret<=remaining:tasks.append((dist,tuple(target)))
    if tasks:
        _,target=min(tasks)
        command=_v219_walk(pos,target) or ['COLLECT_FERTILIZER']
        _SL_REPORT['collect']+=command==['COLLECT_FERTILIZER']
        return command
    if inv.get('FERTILIZER',0):
        return _v219_walk(pos,home) or ['PLACE','FERTILIZER',inv['FERTILIZER']]
    return ['PASS']


agent=globals().pop('agent')


# v9/4 VE: commit the six-sheep expansion on day 11 when two of the first three
# shops are yarn stores. The melon sale lands on day 11, and sheep placed that
# day produce on days 17, 20, 23, 26 and 29 instead of 18, 21, 24 and 27: a
# fifth wool harvest for one more day of feed and labour.
# Day 11 waits until the tape's own land purchase (hour 1) and only ignores a
# native sheep that the tape itself picks up later today (units act before the
# market, and the project's hands spawn a step after its purchase). It commits
# only when cash also covers every purchase the tape still plans through day 12
# (its day-11 strawberry seeds above all); otherwise day 12 decides as before.
_VE_ELIGIBLE = _v233_eligible
_VE_REPORT = dict(ve_day11_checks=0, ve_day11_budget_declines=0, ve_day11_ok=0)
_VE_SEED = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
_VE_ANIMAL = {'SHEEP': 500, 'COW': 400, 'GOOSE': 300}


def _v233_eligible(obs, native):
    step = int(obs['step'])
    if step // 24 != 11:
        return _VE_ELIGIBLE(obs, native)
    tape = _IMPL.chassis.routes[native['route']]
    private = obs['private']
    held = int(private['shed'].get('SHEEP', 0)) + sum(int(i.get('SHEEP', 0)) for i in private['inventories'])
    pickups = 0
    for t in range(step, 12 * 24):
        for c in [tape[t].get('farmer')] + tape[t].get('hands', []):
            if c and c[0] == 'PICKUP' and len(c) > 1 and c[1] == 'SHEEP':
                pickups += int(c[2]) if len(c) > 2 else 1
    if held > pickups:
        return False
    clean = dict(private, shed=dict(private['shed'], SHEEP=0),
                 inventories=[{k: v for k, v in i.items() if k != 'SHEEP'} for i in private['inventories']])
    if not _VE_ELIGIBLE(dict(obs, private=clean), native):
        return False
    _VE_REPORT['ve_day11_checks'] += 1
    prices = obs['market']['prices']
    spend = 0
    hires = {}
    for t in range(step + 1, min(len(tape), 13 * 24)):
        for o in tape[t].get('market', []):
            if not o:
                continue
            if o[0] == 'BUY_LAND' or o[:2] == ['BUY_ANIMAL', 'SHEEP']:
                return False
            if o[0] == 'BUY_SEED':
                spend += int(o[2]) * _VE_SEED.get(o[1], 100)
            elif o[0] == 'BUY_PRODUCT':
                spend += int(o[2]) * (int(prices.get(o[1], 50)) + 10)
            elif o[0] == 'BUY_ANIMAL':
                spend += int(o[2]) * _VE_ANIMAL.get(o[1], 500)
            elif o[0] == 'HIRE':
                d = t // 24
                spend += _v219_fib(hires.get(d, 0))
                hires[d] = hires.get(d, 0) + 1
    if obs['farms'][obs['player']]['money'] < 7000 + 3000 + spend:
        _VE_REPORT['ve_day11_budget_declines'] += 1
        return False
    _VE_REPORT['ve_day11_ok'] += 1
    return True


agent.telemetry = _VE_REPORT
agent = globals().pop('agent')


# v9/4 VT: the sheep expansion's last two days.
# No refresh follows day 29, so feeding, caring and buying feed that day are
# worthless: only wool already grown is worth a hand. Day 29 hires nothing when
# no sheep holds wool, and otherwise one harvest-only hand that delivers the
# wool before the final market. A care on day 28 adds to the bonus after the
# last production refresh has already consumed it, so day-28 hands skip CARE.
_VT_REQUEST = _v233_request
_VT_WORKER = _v233_worker
_VT_RESCUE = _v234_rescue
_VT_REPORT = dict(vt_no_hire_days=0, vt_single_harvest_days=0, vt_skipped_care=0)
_VT_TILES = ((5, 5), (6, 5), (7, 5), (5, 6), (6, 6), (7, 6))


def _vt_wool_tiles(obs):
    farm = obs['farms'][obs['player']]
    return [xy for xy in _VT_TILES if isinstance(farm['tiles'][xy[1]][xy[0]], dict)
            and farm['tiles'][xy[1]][xy[0]].get('animal') == 'SHEEP' and farm['tiles'][xy[1]][xy[0]].get('yield_units', 0) > 0]


def _v233_request(obs, action, state, native):
    result = _VT_REQUEST(obs, action, state, native)
    if result is action or int(obs['step']) // 24 != 29 or not state.get('committed'):
        return result
    pending = state.get('pending')
    if not pending or pending.get('initial'):
        return result
    wool = _vt_wool_tiles(obs)
    extra = result['market'][len(action.get('market', [])):]
    if not wool:
        state.pop('pending', None)
        _V233_REPORT['sheep_hire_requests'] -= sum(o == ['HIRE'] for o in extra)
        _V233_REPORT['sheep_feed_buy_requests'] -= 6
        _VT_REPORT['vt_no_hire_days'] += 1
        return action
    out = copy.deepcopy(action)
    out['market'] = list(out.get('market', [])) + [['HIRE']]
    _V233_REPORT['sheep_hire_requests'] -= sum(o == ['HIRE'] for o in extra) - 1
    _V233_REPORT['sheep_feed_buy_requests'] -= 6
    pending.update(count=1, targets=_sl_path(_r62_input_start(obs, action, 0)[1], wool))
    _VT_REPORT['vt_single_harvest_days'] += 1
    return out


def _v233_worker(obs, actor, targets):
    step = int(obs['step'])
    day = step // 24
    if day not in (28, 29):
        return _VT_WORKER(obs, actor, targets)
    farm = obs['farms'][obs['player']]
    private = obs['private']
    pos = tuple(farm['hands'][actor - 1])
    inv = private['inventories'][actor]
    home = _v219_home(pos)
    distance = abs(pos[0] - home[0]) + abs(pos[1] - home[1])
    cargo = [item for item in ('WOOL', 'FERTILIZER') if inv.get(item, 0)]
    last = 717 if day == 29 else day * 24 + 23
    if cargo and step >= last - distance:
        return _v219_walk(pos, home) or ['PLACE', cargo[0], inv[cargo[0]]]
    sheep = [(x, y) for x, y in targets if isinstance(farm['tiles'][y][x], dict) and farm['tiles'][y][x].get('animal') == 'SHEEP']
    tasks = []
    if day == 28:
        hungry = sum(not farm['tiles'][y][x]['fed_today'] for x, y in sheep)
        if hungry and not inv.get('WHEAT', 0) and private['shed'].get('WHEAT', 0):
            return _v219_walk(pos, home) or ['PICKUP', 'WHEAT', min(hungry, private['shed']['WHEAT'])]
    for x, y in sheep:
        tile = farm['tiles'][y][x]
        command = None
        if day == 28 and not tile['fed_today'] and inv.get('WHEAT', 0):
            command = ['FEED']
        elif tile['yield_units']:
            command = ['HARVEST']
        elif day == 28 and tile['fertilizer_available']:
            command = ['COLLECT_FERTILIZER']
        if day == 28 and not tile['cared_today'] and command is None:
            _VT_REPORT['vt_skipped_care'] += 1
        if command:
            tasks.append((abs(pos[0] - x) + abs(pos[1] - y), (x, y), command))
    if tasks:
        _, target, command = min(tasks)
        return _v219_walk(pos, target) or command
    if cargo:
        return _v219_walk(pos, home) or ['PLACE', cargo[0], inv[cargo[0]]]
    return ['PASS']


def _v234_rescue(obs, action, state):
    if int(obs['step']) // 24 == 29:
        return action
    return _VT_RESCUE(obs, action, state)


agent.telemetry = _VT_REPORT
agent = globals().pop('agent')


# ---------------------------------------------------------------------------
# CARROT2 layer: carrot instead of wheat when the carrot book pays. Own implementation.
# Built by tools/claude_build_carrot.py (derivation there).
# ---------------------------------------------------------------------------
_CA_FROM = 6
_CA_TO = 28
_CA_MARGIN = -5.0
_CA_DROP = 0.0
_CA_BUFFER = 8
_CA_FEED_DAYS = 1
_CA_CASH = 800
_CA_RESCUE = True
_CA_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
_CA_CROP = {"WHEAT": (4, 6), "CARROT": (3, 4)}
_CA_STATE = {}
_CA_REPORT = {"ca_swaps": 0, "ca_rescues": 0, "ca_harvested": 0, "ca_sold": 0, "ca_seed_bought": 0,
              "ca_wheat_seed_saved": 0, "ca_carrot_seed_saved": 0, "ca_feed_block": 0, "ca_errors": 0,
              "ca_min_wheat": 999}


def _ca_tape(seat, t):
    native = _IMPL.chassis.players.get(seat)
    if not native or t > 719:
        return {}
    tape = _IMPL.chassis.routes[2 if t >= 648 else native["route"]]
    return tape[t] if t < len(tape) and isinstance(tape[t], dict) else {}


def _ca_spawn(positions, board):
    half = board // 2
    access = [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]
    occ = {a: 0 for a in access}
    for p in positions:
        if tuple(p) in occ:
            occ[tuple(p)] += 1
    return list(min(access, key=lambda a: (occ[a], access.index(a))))


def _ca_visits(obs, action, pos, t_end, start=None):
    """Non-move commands issued on tile ``pos`` from this step (with ``action``) until ``t_end``."""
    seat = int(obs["player"])
    step = int(obs["step"])
    farm = obs["farms"][seat]
    board = len(farm["tiles"])
    half = board // 2
    positions = [list(farm["farmer"])] + [list(h) for h in farm["hands"]]
    out = []
    for t in range(step, min(t_end, 719) + 1):
        act = action if t == step else _ca_tape(seat, t)
        units = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        for i in range(len(positions)):
            cmd = units[i] if i < len(units) and units[i] else ["PASS"]
            if cmd[0] in _CA_MOVES:
                dx, dy = _CA_MOVES[cmd[0]]
                nx, ny = positions[i][0] + dx, positions[i][1] + dy
                if 0 <= nx < board and 0 <= ny < board:
                    positions[i] = [nx, ny]
            elif tuple(positions[i]) == pos and (start is None or t >= start):
                out.append((t, i, cmd[0]))
        for _ in range(sum(1 for o in (act.get("market") or []) if o and o[0] == "HIRE")):
            positions.append(_ca_spawn(positions, board))
        if t % 24 == 23:
            positions = [[half - 1, half - 1]]
    return out


def _ca_decays(mls, a, b):
    """Decay events at steps s in [max(a, mls), b) with (s - mls) even."""
    a = max(a, mls)
    if b <= a:
        return 0
    first = a if (a - mls) % 2 == 0 else a + 1
    return 0 if first >= b else (b - 1 - first) // 2 + 1


def _ca_yield_path(crop, planted, visits, y0=1, fert_until=-1, watered_day=-1, now_step=0):
    """Return (harvest_units, best_rescue_units, rescue_step) for a crop following ``visits``.
    ``y0`` is the yield observed at ``now_step`` (decay before that step already included)."""
    myd, cap = _CA_CROP[crop]
    lo = (myd + 1) // 2
    mls = (planted + myd + 1) * 24
    y = y0
    best_rescue, rescue_t = 0, None
    for t, i, op in visits:
        day = t // 24
        age = day - planted
        dec = _ca_decays(mls, now_step, t)
        now = y - dec
        if now <= 0 and t > mls:
            return 0, best_rescue, rescue_t
        if op == "HARVEST":
            return (max(0, now) if age >= 2 else 0), best_rescue, rescue_t
        if op in ("PLANT", "DIG", "BUILD_COOP", "BUILD_PASTURE"):
            return 0, best_rescue, rescue_t
        if age >= 2 and now > best_rescue and t > now_step:
            best_rescue, rescue_t = now, t
        if op == "WATER" and lo <= age <= myd and day != watered_day:
            watered_day = day
            y = min(cap, y + (2 if fert_until >= day else 1))
    return 0, best_rescue, rescue_t


def _ca_wheat_total(obs):
    priv = obs["private"]
    return int(priv["shed"].get("WHEAT", 0)) + sum(int(inv.get("WHEAT", 0)) for inv in priv["inventories"])


def _ca_feed_need(seat, step, days):
    need = 0
    for t in range(step, min(719, step + 24 * days) + 1):
        act = _ca_tape(seat, t)
        units = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        need += sum(1 for c in units if c and c[0] == "FEED")
    return need


_CA_PARENT = agent
del agent


def agent(observation, configuration=None):
    action = _CA_PARENT(observation, configuration)
    try:
        step = int(observation["step"])
        seat = int(observation["player"])
        st = _CA_STATE.get(seat)
        if step == 0 or st is None or step <= st["step"]:
            st = _CA_STATE[seat] = {"step": -1, "tiles": {}, "spare_wheat": 0, "spare_carrot": 0, "credit": 0}
            if step == 0:
                _CA_REPORT.update(ca_swaps=0, ca_rescues=0, ca_harvested=0, ca_sold=0, ca_seed_bought=0,
                                  ca_wheat_seed_saved=0, ca_carrot_seed_saved=0, ca_feed_block=0,
                                  ca_errors=0, ca_min_wheat=999)
        st["step"] = step
        if not isinstance(action, dict) or step > 717:
            return action
        day = step // 24
        farm = observation["farms"][seat]
        tiles = farm["tiles"]
        priv = observation["private"]
        prices = observation["market"]["prices"]
        p_c, p_w = int(prices.get("CARROT", 0)), int(prices.get("WHEAT", 0))
        positions = [tuple(farm["farmer"])] + [tuple(h) for h in farm["hands"]]
        units = [list(action.get("farmer") or ["PASS"])] + [list(c) for c in (action.get("hands") or [])]
        market = [list(o) for o in (action.get("market") or [])]
        changed = False
        if _CA_FROM <= day <= _CA_TO + 4:
            _CA_REPORT["ca_min_wheat"] = min(_CA_REPORT["ca_min_wheat"], _ca_wheat_total(observation))
        # 1. bookkeeping + rescue of swapped carrots
        for pos, planted in list(st["tiles"].items()):
            tile = tiles[pos[1]][pos[0]]
            if not (isinstance(tile, dict) and tile.get("crop") == "CARROT" and int(tile.get("planted_day", -9)) == planted):
                st["tiles"].pop(pos, None)
                continue
            here = [i for i, p in enumerate(positions) if p == pos and i < len(units)]
            if not here:
                continue
            i = here[0]
            cmd = units[i]
            yu = int(tile.get("yield_units", 0))
            if cmd and cmd[0] == "HARVEST":
                if day - planted >= 2 and yu > 0:
                    st["credit"] += yu
                    _CA_REPORT["ca_harvested"] += yu
                    st["tiles"].pop(pos, None)
                continue
            if not _CA_RESCUE or (cmd and cmd[0] in _CA_MOVES) or day - planted < 2 or yu <= 0:
                continue
            visits = _ca_visits(observation, action, pos, (planted + 5) * 24)
            harvest, later, _ = _ca_yield_path("CARROT", planted, visits, y0=yu,
                                               fert_until=int(tile.get("fertilized_until_day", -1)),
                                               watered_day=day if tile.get("watered_today") else -1,
                                               now_step=step)
            if yu > max(harvest, later):
                units[i] = ["HARVEST"]
                st["credit"] += yu
                _CA_REPORT["ca_harvested"] += yu
                _CA_REPORT["ca_rescues"] += 1
                st["tiles"].pop(pos, None)
                changed = True
        # 2. swaps
        pays_now = 3 * (p_c - _CA_DROP) - 20 > 4 * p_w - 10 + _CA_MARGIN
        if _CA_FROM <= day <= _CA_TO and pays_now:
            seeds_c = min(st["spare_carrot"],
                          int(priv["seeds"].get("CARROT", 0)) - sum(1 for c in units if c[:2] == ["PLANT", "CARROT"]))
            wheat_ok = None
            for i, cmd in enumerate(units):
                if cmd[:2] != ["PLANT", "WHEAT"] or i >= len(positions) or seeds_c <= 0:
                    continue
                pos = positions[i]
                if tiles[pos[1]][pos[0]] is not None:
                    continue
                if wheat_ok is None:
                    wheat_ok = _ca_wheat_total(observation) >= _ca_feed_need(seat, step, _CA_FEED_DAYS)
                if not wheat_ok:
                    _CA_REPORT["ca_feed_block"] += 1
                    break
                visits = _ca_visits(observation, action, pos, (day + 6) * 24, start=step + 1)
                wu, _, _ = _ca_yield_path("WHEAT", day, visits)
                ch, cr, _ = _ca_yield_path("CARROT", day, visits)
                cu = max(ch, cr if _CA_RESCUE else 0)
                if cu * (p_c - _CA_DROP) - 20 > wu * p_w - 10 + _CA_MARGIN:
                    units[i] = ["PLANT", "CARROT"]
                    seeds_c -= 1
                    st["spare_carrot"] -= 1
                    st["tiles"][pos] = day
                    st["spare_wheat"] += 1
                    _CA_REPORT["ca_swaps"] += 1
                    changed = True
        # 3. seeds
        new_market = []
        for o in market:
            if len(o) >= 3 and o[0] == "BUY_SEED" and o[1] in ("WHEAT", "CARROT"):
                key = "spare_wheat" if o[1] == "WHEAT" else "spare_carrot"
                cut = min(int(o[2]), st[key])
                if cut > 0:
                    st[key] -= cut
                    _CA_REPORT["ca_wheat_seed_saved" if o[1] == "WHEAT" else "ca_carrot_seed_saved"] += cut
                    changed = True
                    if int(o[2]) - cut <= 0:
                        continue
                    o = [o[0], o[1], int(o[2]) - cut]
            new_market.append(o)
        market = new_market
        if _CA_FROM <= day <= _CA_TO - 1 and pays_now and len(market) < 10:
            have = int(priv["seeds"].get("CARROT", 0)) - sum(1 for c in units if c[:2] == ["PLANT", "CARROT"])
            buying = sum(int(o[2]) for o in market if len(o) >= 3 and o[:2] == ["BUY_SEED", "CARROT"])
            q = _CA_BUFFER - have - buying
            if q > 0 and int(farm.get("money", 0)) >= _CA_CASH + 20 * q:
                market.append(["BUY_SEED", "CARROT", q])
                st["spare_carrot"] += q
                _CA_REPORT["ca_seed_bought"] += q
                changed = True
        # 4. sell credited carrots
        if st["credit"] > 0 and p_c >= 2 and len(market) < 10:
            view_action = {"farmer": units[0], "hands": units[1:], "market": market}
            stock = int(projected_shed(view_action, FarmView(observation)).get("CARROT", 0))
            selling = sum(int(o[2]) for o in market if len(o) >= 3 and o[:2] == ["SELL", "CARROT"])
            q = min(st["credit"], stock - selling)
            if q > 0:
                market.insert(0, ["SELL", "CARROT", q])
                st["credit"] -= q
                _CA_REPORT["ca_sold"] += q
                changed = True
        if changed:
            action = dict(action)
            action["farmer"] = units[0]
            action["hands"] = units[1:]
            action["market"] = market[:10]
    except Exception:
        _CA_REPORT["ca_errors"] += 1
    return action


agent.telemetry = _CA_REPORT
agent = globals().pop('agent')


# ---------------------------------------------------------------------------
# ORDERPRI2 layer: sales ordered by the rival's estimated sellable stock. Own implementation.
# Built by tools/claude_build_orderpri2.py (derivation there).
# ---------------------------------------------------------------------------
_OR2_CAP = 30
_OR2_SN_K = 0
_OR2_SN_H = 24
_OR2_SLOT_H = 6
_OR2_SLOT_MARGIN = 20.0
_OR2_SN_ITEMS = ("MILK", "STRAWBERRY", "WOOL", "MELON", "EGG")
_OR2_ITEMS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL")
_OR2_ONGOING = ("TOMATO", "STRAWBERRY")
_OR2_ANIMAL = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}
_OR2_SHOPS = {"BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
              "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
              "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
              "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
              "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY")}
_OR2_STATE = {}
_OR2_REPORT = {"or2_reordered": 0, "or2_changed_vs_v39": 0, "or2_rival_harvest": 0, "or2_rival_sold": 0,
               "or2_errors": 0}


def _or2_draw(shops, step):
    draw = {}
    if step % 4 == 0:
        for name in shops:
            products = _OR2_SHOPS.get(name, ())
            for item in products:
                draw[item] = draw.get(item, 0) + (2 if len(products) == 1 else 1)
    if step % 24 == 0:
        for item in _OR2_ITEMS:
            draw[item] = draw.get(item, 0) + 1
    return draw


def _or2_tiles(farm):
    out = {}
    for y, row in enumerate(farm["tiles"]):
        for x, t in enumerate(row):
            if not isinstance(t, dict):
                continue
            if t.get("kind") == "PLANT" and t.get("crop"):
                out[(x, y)] = ("P", t["crop"], int(t.get("planted_day", -1)), int(t.get("yield_units", 0)))
            elif t.get("animal") in _OR2_ANIMAL:
                out[(x, y)] = ("A", _OR2_ANIMAL[t["animal"]], int(t.get("placed_day", -1)), int(t.get("yield_units", 0)))
    return out


def _or2_exposure(observation, item, qty, batch):
    if qty <= 0 or batch <= 0 or item not in _R37_MARKET_PARAMS:
        return 0.0
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for k, patch in (observation["market"].get("params") or {}).items():
        if k in params:
            params[k].update(patch)
    inv = int(observation["market"]["inventory"][item])
    return float(sum(_r37_market_price(item, inv + j, params) - _r37_market_price(item, inv + batch + j, params)
                     for j in range(qty)))


_OR2_PARENT = agent
del agent


def agent(observation, configuration=None):
    action = _OR2_PARENT(observation, configuration)
    try:
        step = int(observation["step"])
        seat = int(observation["player"])
        st = _OR2_STATE.get(seat)
        if step == 0 or st is None or step <= st.get("step", -1):
            st = _OR2_STATE[seat] = {"step": -1, "stock": {i: 0 for i in _OR2_ITEMS}, "prev": None}
            if step == 0:
                for k in _OR2_REPORT:
                    _OR2_REPORT[k] = 0
        rival = observation["farms"][1 - seat]
        tiles = _or2_tiles(rival)
        inv_now = {i: int(observation["market"]["inventory"].get(i, 0)) for i in _OR2_ITEMS}
        prev = st["prev"]
        if prev and prev["step"] == step - 1:
            stock = st["stock"]
            for pos, old in prev["tiles"].items():
                kind, item, born, y = old
                if y <= 0:
                    continue
                new = tiles.get(pos)
                got = 0
                if kind == "P" and item not in _OR2_ONGOING:
                    if (new is None and not _OR2_WEED(rival, pos)) or (new is not None and new[2] != born):
                        got = y
                elif new is not None and new[0] == kind and new[1] == item and new[2] == born and new[3] < y:
                    if step % 24 != 0:
                        got = y - new[3]
                    elif new[3] == 0:
                        got = y
                if got > 0:
                    stock[item] = stock.get(item, 0) + got
                    _OR2_REPORT["or2_rival_harvest"] += got
            draw = _or2_draw(prev["shops"], prev["step"])
            for item in _OR2_ITEMS:
                if prev["prices"].get(item, 0) <= 1:
                    continue
                moved = inv_now[item] - prev["inv"][item] + draw.get(item, 0) - prev["own"].get(item, 0)
                if moved > 0:
                    stock[item] = max(0, stock.get(item, 0) - moved)
                    _OR2_REPORT["or2_rival_sold"] += moved
        own = {}
        if isinstance(action, dict):
            orders = [list(o) for o in (action.get("market") or [])]
            proj = dict(projected_shed(action, FarmView(observation)))
            if _OR2_SN_K > 0 and 24 <= step < 694:
                native = _IMPL.chassis.players.get(seat)
                debts = native["sell_state"].setdefault("r36_debts", {}) if native else None
                for item in _OR2_SN_ITEMS:
                    if debts is None or int(st["stock"].get(item, 0)) < _OR2_SN_K:
                        continue
                    if int(observation["market"]["prices"].get(item, 0)) < 2 or len(orders) >= 10:
                        continue
                    if any(len(o) >= 2 and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and o[1] == item for o in orders):
                        continue
                    selling = sum(max(0, int(o[2])) for o in orders if len(o) >= 3 and o[0] == "SELL" and o[1] == item)
                    avail = int(proj.get(item, 0)) - selling
                    take = 0
                    for t in range(step + 1, min(694, step + _OR2_SN_H) + 1):
                        if take >= avail:
                            break
                        tape = _IMPL.chassis.routes[2 if t >= 648 else native["route"]]
                        act = tape[t] if t < len(tape) and isinstance(tape[t], dict) else {}
                        planned = sum(max(0, int(o[2])) for o in (act.get("market") or [])
                                      if len(o) >= 3 and o[0] == "SELL" and o[1] == item)
                        planned -= debts.get(t, {}).get(item, 0)
                        q = min(planned, avail - take)
                        if q > 0:
                            debts.setdefault(t, {})[item] = debts.get(t, {}).get(item, 0) + q
                            take += q
                    if take > 0:
                        for o in orders:
                            if len(o) >= 3 and o[0] == "SELL" and o[1] == item:
                                o[2] = int(o[2]) + take
                                break
                        else:
                            orders.append(["SELL", item, take])
                        _OR2_REPORT["or2_sellnow"] = _OR2_REPORT.get("or2_sellnow", 0) + take
                        action = dict(action)
                        action["market"] = orders
            if _OR2_SLOT_H > 0 and 288 <= step < 694 and len(orders) >= 10:
                native = _IMPL.chassis.players.get(seat)
                debts = native["sell_state"].setdefault("r36_debts", {}) if native else None
                sells = [o for o in orders if len(o) >= 3 and o[0] == "SELL"]
                selling_items = {o[1] for o in sells}
                bought_items = {o[1] for o in orders if len(o) >= 2 and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL")}
                best = None
                for item in _OR2_SN_ITEMS:
                    if debts is None or item in selling_items or item in bought_items:
                        continue
                    avail = int(proj.get(item, 0))
                    if avail <= 0 or int(observation["market"]["prices"].get(item, 0)) < 2:
                        continue
                    plan, take = [], 0
                    for t in range(step + 1, min(694, step + _OR2_SLOT_H) + 1):
                        if take >= avail:
                            break
                        tape = _IMPL.chassis.routes[2 if t >= 648 else native["route"]]
                        act = tape[t] if t < len(tape) and isinstance(tape[t], dict) else {}
                        planned = sum(max(0, int(o[2])) for o in (act.get("market") or [])
                                      if len(o) >= 3 and o[0] == "SELL" and o[1] == item)
                        q = min(planned - debts.get(t, {}).get(item, 0), avail - take)
                        if q > 0:
                            plan.append((t, q))
                            take += q
                    if take <= 0:
                        continue
                    b = min(_OR2_CAP, int(st["stock"].get(item, 0)))
                    value = _or2_exposure(observation, item, take, max(1, b))
                    if best is None or value > best[0]:
                        best = (value, item, take, plan)
                if best is not None and sells:
                    def sval(o):
                        q = min(max(0, int(o[2])), max(0, int(proj.get(o[1], 0))))
                        return _or2_exposure(observation, o[1], q, max(1, min(_OR2_CAP, int(st["stock"].get(o[1], 0)))))
                    weakest = min(sells, key=sval)
                    if best[0] > sval(weakest) + _OR2_SLOT_MARGIN and weakest[1] not in ("WHEAT", "FERTILIZER")                             or best[0] > sval(weakest) + _OR2_SLOT_MARGIN and int(weakest[2]) <= 2:
                        # drop the weakest sale; give its booked debts back (nearest due first)
                        refund = max(0, int(weakest[2]))
                        for t in range(step + 1, step + 49):
                            if refund <= 0:
                                break
                            owed = debts.get(t, {}).get(weakest[1], 0)
                            back = min(owed, refund)
                            if back > 0:
                                debts[t][weakest[1]] = owed - back
                                refund -= back
                        orders.remove(weakest)
                        orders.append(["SELL", best[1], best[2]])
                        for t, q in best[3]:
                            debts.setdefault(t, {})[best[1]] = debts.get(t, {}).get(best[1], 0) + q
                        _OR2_REPORT["or2_slot_swaps"] = _OR2_REPORT.get("or2_slot_swaps", 0) + 1
                        action = dict(action)
                        action["market"] = orders
            left = dict(proj)
            movable, fixed, bought = [], [], set()
            for idx, o in enumerate(orders):
                if len(o) >= 2 and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL"):
                    bought.add(o[1])
                if len(o) >= 3 and o[0] == "SELL" and int(o[2]) > 0 and o[1] not in bought:
                    movable.append((idx, o))
                else:
                    fixed.append((idx, o))
            if movable and step >= 1:
                def score(io):
                    item, qty = io[1][1], min(int(io[1][2]), max(0, int(proj.get(io[1][1], 0))))
                    b = min(_OR2_CAP, int(st["stock"].get(item, 0)))
                    return (-_or2_exposure(observation, item, qty, b),
                            -_r37_quote_priority(observation, io[1], proj), io[0])
                scored = sorted(movable, key=score)
                new = [o for _, o in scored] + [o for _, o in fixed]
                if new != orders:
                    v39 = sorted(movable, key=lambda io: (-_r37_quote_priority(observation, io[1], proj), io[0]))
                    if [o for _, o in v39] != [o for _, o in scored]:
                        _OR2_REPORT["or2_changed_vs_v39"] += 1
                    _OR2_REPORT["or2_reordered"] += 1
                    action = dict(action)
                    action["market"] = new
                    orders = new
            for o in orders[:10]:
                if len(o) >= 3 and o[0] == "SELL" and o[1] in _OR2_ITEMS:
                    got = min(max(0, int(o[2])), max(0, int(left.get(o[1], 0))))
                    left[o[1]] = left.get(o[1], 0) - got
                    own[o[1]] = own.get(o[1], 0) + got
        st["prev"] = {"step": step, "tiles": tiles, "inv": inv_now, "own": own,
                      "prices": dict(observation["market"]["prices"]),
                      "shops": list((observation.get("town") or {}).get("unlocked_shops") or [])}
        st["step"] = step
    except Exception:
        _OR2_REPORT["or2_errors"] += 1
    return action


def _OR2_WEED(farm, pos):
    t = farm["tiles"][pos[1]][pos[0]]
    return isinstance(t, dict) and t.get("kind") == "WEED"


agent.telemetry = _OR2_REPORT
agent = globals().pop('agent')


# ---------------------------------------------------------------------------
# CAPHARV layer: harvest animals that would overflow tonight. Own implementation.
# Built by tools/claude_build_capharv.py (derivation there).
# ---------------------------------------------------------------------------
_CH_SHED = 90
_CH_SELL = True
_CH_ANIMALS = {"GOOSE": ("EGG", 4, 4, 1), "COW": ("MILK", 6, 8, 2), "SHEEP": ("WOOL", 6, 6, 3)}
_CH_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
_CH_STATE = {}
_CH_REPORT = {"ch_collect_swaps": 0, "ch_care_swaps": 0, "ch_saved": 0, "ch_sold": 0, "ch_shed_block": 0,
              "ch_errors": 0}


def _ch_tape(seat, t):
    native = _IMPL.chassis.players.get(seat)
    if not native or t > 719:
        return {}
    tape = _IMPL.chassis.routes[2 if t >= 648 else native["route"]]
    return tape[t] if t < len(tape) and isinstance(tape[t], dict) else {}


def _ch_visits_today(obs, action):
    """{pos: [(t, op)]} for non-move commands from the next step to the end of today."""
    seat = int(obs["player"])
    step = int(obs["step"])
    farm = obs["farms"][seat]
    board = len(farm["tiles"])
    half = board // 2
    access = [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]
    positions = [list(farm["farmer"])] + [list(h) for h in farm["hands"]]
    out = {}
    for t in range(step, (step // 24 + 1) * 24):
        act = action if t == step else _ch_tape(seat, t)
        units = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        for i in range(len(positions)):
            cmd = units[i] if i < len(units) and units[i] else ["PASS"]
            if cmd[0] in _CH_MOVES:
                dx, dy = _CH_MOVES[cmd[0]]
                nx, ny = positions[i][0] + dx, positions[i][1] + dy
                if 0 <= nx < board and 0 <= ny < board:
                    positions[i] = [nx, ny]
            elif t > step:
                out.setdefault(tuple(positions[i]), []).append((t, cmd[0]))
        for _ in range(sum(1 for o in (act.get("market") or []) if o and o[0] == "HIRE")):
            occ = {a: 0 for a in access}
            for p in positions:
                if tuple(p) in occ:
                    occ[tuple(p)] += 1
            positions.append(list(min(access, key=lambda a: (occ[a], access.index(a)))))
    return out


_CH_PARENT = agent
del agent


def agent(observation, configuration=None):
    action = _CH_PARENT(observation, configuration)
    try:
        step = int(observation["step"])
        seat = int(observation["player"])
        st = _CH_STATE.get(seat)
        if step == 0 or st is None or step <= st["step"]:
            st = _CH_STATE[seat] = {"step": -1, "credit": {}}
            if step == 0:
                for k in _CH_REPORT:
                    _CH_REPORT[k] = 0
        st["step"] = step
        if not isinstance(action, dict) or step > 717:
            return action
        day = step // 24
        farm = observation["farms"][seat]
        priv = observation["private"]
        prices = observation["market"]["prices"]
        positions = [tuple(farm["farmer"])] + [tuple(h) for h in farm["hands"]]
        units = [list(action.get("farmer") or ["PASS"])] + [list(c) for c in (action.get("hands") or [])]
        market = [list(o) for o in (action.get("market") or [])]
        changed = False
        visits = None
        for i, pos in enumerate(positions[:len(units)]):
            cmd = units[i]
            if not cmd or cmd[0] not in ("CARE", "COLLECT_FERTILIZER"):
                continue
            tile = farm["tiles"][pos[1]][pos[0]]
            if not (isinstance(tile, dict) and tile.get("animal") in _CH_ANIMALS):
                continue
            product, cap, first, interval = _CH_ANIMALS[tile["animal"]]
            since = day + 1 - int(tile.get("placed_day", 99)) - first
            if since < 0 or since % interval != 0:
                continue
            y = int(tile.get("yield_units", 0))
            if visits is None:
                visits = _ch_visits_today(observation, action)
            later = visits.get(pos, [])
            if any(op == "HARVEST" for t, op in later):
                continue
            fed = bool(tile.get("fed_today")) or any(op == "FEED" for t, op in later)
            prod = 1 + (int(tile.get("pending_care_bonus", 0)) if fed else 0)
            overflow = y + prod - cap
            if overflow <= 0 or y <= 0:
                continue
            quote = int(prices.get(product, 0))
            if cmd[0] == "COLLECT_FERTILIZER":
                if overflow * quote <= int(prices.get("FERTILIZER", 0)):
                    continue
            else:
                if any(op == "COLLECT_FERTILIZER" for t, op in later) or overflow <= 1:
                    continue
            carried = sum(int(v) for inv in priv["inventories"] for v in inv.values())
            if sum(int(v) for v in priv["shed"].values()) + carried + y >= _CH_SHED:
                _CH_REPORT["ch_shed_block"] += 1
                continue
            units[i] = ["HARVEST"]
            _CH_REPORT["ch_collect_swaps" if cmd[0] == "COLLECT_FERTILIZER" else "ch_care_swaps"] += 1
            saved = overflow if cmd[0] == "COLLECT_FERTILIZER" else overflow - 1
            _CH_REPORT["ch_saved"] += saved
            st["credit"][product] = st["credit"].get(product, 0) + saved
            changed = True
        if _CH_SELL and any(v > 0 for v in st["credit"].values()):
            view_action = {"farmer": units[0], "hands": units[1:], "market": market}
            stock = dict(projected_shed(view_action, FarmView(observation)))
            for product, credit in list(st["credit"].items()):
                if credit <= 0 or len(market) >= 10 or int(prices.get(product, 0)) < 2:
                    continue
                selling = sum(int(o[2]) for o in market if len(o) >= 3 and o[:2] == ["SELL", product])
                q = min(credit, int(stock.get(product, 0)) - selling)
                if q > 0:
                    for o in market:
                        if len(o) >= 3 and o[:2] == ["SELL", product]:
                            o[2] = int(o[2]) + q
                            break
                    else:
                        market.insert(0, ["SELL", product, q])
                    st["credit"][product] = credit - q
                    _CH_REPORT["ch_sold"] += q
                    changed = True
        if changed:
            action = dict(action)
            action["farmer"] = units[0]
            action["hands"] = units[1:]
            action["market"] = market[:10]
    except Exception:
        _CH_REPORT["ch_errors"] += 1
    return action


agent.telemetry = _CH_REPORT
agent = globals().pop('agent')


# ---------------------------------------------------------------------------
# SHEDROOM layer: sell shed goods before the night drop overflows. Own implementation.
# Built by tools/claude_build_shedroom.py (derivation there).
# ---------------------------------------------------------------------------
_SR_MARGIN = 8
_SR_HOURS = (21, 22, 23)
_SR_PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
_SR_REPORT = {"sr_turns": 0, "sr_units": 0, "sr_errors": 0}


def _sr_tape(seat, t):
    native = _IMPL.chassis.players.get(seat)
    if not native or t > 719:
        return {}
    tape = _IMPL.chassis.routes[2 if t >= 648 else native["route"]]
    return tape[t] if t < len(tape) and isinstance(tape[t], dict) else {}


_SR_PARENT = agent
del agent


def agent(observation, configuration=None):
    action = _SR_PARENT(observation, configuration)
    try:
        step = int(observation["step"])
        if step == 0:
            for k in _SR_REPORT:
                _SR_REPORT[k] = 0
        if step % 24 not in _SR_HOURS or step >= 717 or not isinstance(action, dict):
            return action
        seat = int(observation["player"])
        farm = observation["farms"][seat]
        priv = observation["private"]
        view = FarmView(observation)
        proj = dict(projected_shed(action, view))
        market = [list(o) for o in (action.get("market") or [])]
        left = dict(proj)
        night_shed = sum(max(0, int(v)) for v in proj.values())
        for o in market:
            if len(o) >= 3 and o[0] == "SELL":
                got = min(max(0, int(o[2])), max(0, int(left.get(o[1], 0))))
                left[o[1]] = left.get(o[1], 0) - got
                night_shed -= got
            elif len(o) >= 3 and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL"):
                night_shed += max(0, int(o[2]))
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = 0
        for i, pos in enumerate(view.positions):
            inv = priv["inventories"][i] if i < len(priv["inventories"]) else {}
            held = sum(max(0, int(v)) for v in inv.values())
            cmd = units[i] if i < len(units) and units[i] else ["PASS"]
            tile = farm["tiles"][pos[1]][pos[0]] if isinstance(pos, (list, tuple)) else None
            op = cmd[0]
            if op == "DROP" and _shed_adjacent(pos, view.board):
                held = 0
            elif op == "HARVEST" and isinstance(tile, dict):
                held += max(0, int(tile.get("yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and tile.get("fertilizer_available"):
                held += 1
            elif op in ("FEED", "FERTILIZE") and held > 0:
                held -= 1
            elif op == "PICKUP" and len(cmd) >= 2 and _shed_adjacent(pos, view.board):
                held += max(1, int(cmd[2]) if len(cmd) >= 3 else 1)
            carried += held
        cap = int((configuration or {}).get("shedCapacity", 100)) if isinstance(configuration, dict) else 100
        overflow = night_shed + carried - cap + _SR_MARGIN
        if overflow <= 0:
            return action
        need = {"WHEAT": 0, "FERTILIZER": 0}
        for t in range(step + 1, min(719, step + 25)):
            act = _sr_tape(seat, t)
            for c in [act.get("farmer") or ["PASS"]] + list(act.get("hands") or []):
                if not c:
                    continue
                if c[0] == "FEED":
                    need["WHEAT"] += 1
                elif c[0] == "FERTILIZE":
                    need["FERTILIZER"] += 1
        prices = observation["market"]["prices"]
        cands = []
        for item in _SR_PRODUCTS:
            spare = int(left.get(item, 0)) - need.get(item, 0)
            if spare > 0 and int(prices.get(item, 0)) >= 2:
                cands.append((int(prices.get(item, 0)), item, spare))
        cands.sort()
        sold_now = 0
        for price, item, spare in cands:
            if overflow <= 0:
                break
            q = min(spare, overflow)
            for o in market:
                if len(o) >= 3 and o[:2] == ["SELL", item]:
                    o[2] = int(o[2]) + q
                    break
            else:
                if len(market) >= 10:
                    continue
                market.append(["SELL", item, q])
            overflow -= q
            sold_now += q
        if sold_now:
            _SR_REPORT["sr_turns"] += 1
            _SR_REPORT["sr_units"] += sold_now
            action = dict(action)
            action["market"] = market
    except Exception:
        _SR_REPORT["sr_errors"] += 1
    return action


agent.telemetry = _SR_REPORT
agent = globals().pop('agent')


# ---------------------------------------------------------------------------
# HERD2 layer: goose / cow / sheep choice at the tape's goose purchase.
# Own implementation. Built by tools/claude_build_herd2.py (derivation there).
# ---------------------------------------------------------------------------
_HD2_FROM = 192
_HD2_TO = 360
_HD2_RATIO = 1.3
_HD2_MIN_GAIN = 600.0
_HD2_LOOKBACK = 3
_HD2_OPTIONS = ('COW', 'SHEEP')
_HD2_CARE = 0.8
_HD2_FUTURE = 0.0

_HD2_SPEC = {
    "GOOSE": {"cost": 300, "first": 4, "interval": 1, "per": 2, "product": "EGG", "structure": "COOP"},
    "COW": {"cost": 400, "first": 8, "interval": 2, "per": 3, "product": "MILK", "structure": "PASTURE"},
    "SHEEP": {"cost": 500, "first": 6, "interval": 3, "per": 4, "product": "WOOL", "structure": "PASTURE"},
}
_HD2_SHOP_TYPES = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"), "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_HD2_STATE = {}
_HD2_REPORT = {"hd2_decision": "", "hd2_ev": "", "hd2_rewrites": 0, "hd2_credit_units": 0,
               "hd2_sold_units": 0, "hd2_errors": 0}


def _hd2_daily_shop_demand(item, shops):
    total = 0.0
    for name in shops:
        products = _HD2_SHOP_TYPES.get(name, ())
        if item in products:
            total += 6.0 * (2 if len(products) == 1 else 1)
    return total


def _hd2_future_demand_per_day(item):
    """Expected extra daily demand of one more uniformly drawn shop instance."""
    return sum(6.0 * (2 if len(p) == 1 else 1) for p in _HD2_SHOP_TYPES.values() if item in p) / len(_HD2_SHOP_TYPES)


def _hd2_schedule(animal, placed_day, day_from):
    """Units an animal of this type produces on each day >= day_from (daily care assumed,
    scaled by _HD2_CARE)."""
    spec = _HD2_SPEC[animal]
    out = {}
    for d in range(max(day_from, placed_day + spec["first"]), 30):
        if (d - placed_day - spec["first"]) % spec["interval"] == 0:
            out[d] = out.get(d, 0.0) + 1.0 + (spec["per"] - 1) * _HD2_CARE
    return out


def _hd2_ev(option, k, obs, st):
    """Margin value of k new animals of `option`: their own revenue, plus the price change
    their supply causes on (our existing future units - rival existing future units)."""
    spec = _HD2_SPEC[option]
    item = spec["product"]
    animal_of = {"EGG": "GOOSE", "MILK": "COW", "WOOL": "SHEEP"}[item]
    day = int(obs["step"]) // 24
    seat = int(obs["player"])
    market = obs["market"]
    params = {key: dict(v) for key, v in _R37_MARKET_PARAMS.items()}
    for key, patch in (market.get("params") or {}).items():
        if key in params and isinstance(patch, dict):
            params[key].update(patch)
    # existing supply, per farm, per day
    existing = [dict(), dict()]
    for farm_index, farm in enumerate(obs["farms"]):
        for row in farm["tiles"]:
            for tile in row:
                if isinstance(tile, dict) and tile.get("animal") == animal_of:
                    for d, u in _hd2_schedule(animal_of, int(tile.get("placed_day", day)), day + 1).items():
                        existing[farm_index][d] = existing[farm_index].get(d, 0.0) + u
    shed = (obs.get("private") or {}).get("shed") or {}
    carried = sum(int(inv.get(animal_of, 0)) for inv in (obs.get("private") or {}).get("inventories") or [])
    for _ in range(int(shed.get(animal_of, 0)) + carried):
        for d, u in _hd2_schedule(animal_of, day + 1, day + 1).items():
            existing[seat][d] = existing[seat].get(d, 0.0) + u
    # Purchases the tape already plans after this turn; a family-similar rival runs the same tape.
    native = _IMPL.chassis.players.get(seat)
    if native:
        similar = _r37_similarity(obs) >= 0.9
        for t in range(int(obs["step"]) + 1, 696):
            tape = _IMPL.chassis.routes[2 if t >= 648 else native["route"]]
            if t >= len(tape) or not isinstance(tape[t], dict):
                continue
            for order in tape[t].get("market", []) or []:
                if len(order) >= 3 and order[0] == "BUY_ANIMAL" and order[1] == animal_of:
                    for _ in range(max(0, int(order[2]))):
                        for d, u in _hd2_schedule(animal_of, t // 24 + 1, day + 1).items():
                            existing[seat][d] = existing[seat].get(d, 0.0) + u
                            if similar:
                                existing[1 - seat][d] = existing[1 - seat].get(d, 0.0) + u
    ours_existing, rival_existing = existing[seat], existing[1 - seat]
    new = {}
    for d, u in _hd2_schedule(option, day + 1, day + 1).items():
        new[d] = u * k
    shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
    unlocks_left = max(0, 8 - len(shops))
    base_demand = _hd2_daily_shop_demand(item, shops) + 1.0
    extra_demand = _hd2_future_demand_per_day(item) * _HD2_FUTURE

    def path(with_new):
        inv = float(market["inventory"][item])
        prices, revenue = {}, 0.0
        for d in range(day + 1, 30):
            opened = min(unlocks_left, max(0, (d // 3) - (day // 3)))
            inv -= base_demand + extra_demand * opened
            inv += ours_existing.get(d, 0.0) + rival_existing.get(d, 0.0)
            prices[d] = _r37_market_price(item, int(round(inv)), params)
            if with_new:
                units = int(round(new.get(d, 0.0)))
                for _ in range(units):
                    price = _r37_market_price(item, int(round(inv)), params)
                    revenue += price
                    if price > 1:
                        inv += 1
        return prices, revenue

    base_prices, _ = path(False)
    new_prices, revenue = path(True)
    swing = sum((new_prices[d] - base_prices[d]) * (ours_existing.get(d, 0.0) - rival_existing.get(d, 0.0))
                for d in base_prices)
    return revenue + swing - spec["cost"] * k, revenue


def _hd2_decide(obs, action, st):
    market = action.get("market") or []
    buys = [o for o in market if len(o) >= 3 and o[0] == "BUY_ANIMAL" and o[1] == "GOOSE"]
    if not buys:
        return
    st["decided"] = True
    step = int(obs["step"])
    if not (_HD2_FROM <= step < _HD2_TO):
        return
    farm = obs["farms"][int(obs["player"])]
    if any(isinstance(t, dict) and t.get("kind") == "COOP" for row in farm["tiles"] for t in row):
        _HD2_REPORT["hd2_decision"] = "skip:coop_exists"
        return
    k = sum(max(0, int(o[2])) for o in buys)
    k_plan = max(k, 3)
    evs = {opt: _hd2_ev(opt, k_plan, obs, st)[0] for opt in ("GOOSE",) + tuple(_HD2_OPTIONS)}
    _HD2_REPORT["hd2_ev"] = ",".join("%s:%d" % (o, v) for o, v in sorted(evs.items()))
    best = max(_HD2_OPTIONS, key=lambda o: evs[o]) if _HD2_OPTIONS else None
    goose = evs["GOOSE"]
    if best is None:
        return
    gain = evs[best] - goose
    ok_ratio = evs[best] >= _HD2_RATIO * max(goose, 1.0)
    extra_cost = (_HD2_SPEC[best]["cost"] - 300) * k
    cash = float(farm.get("money", 0))
    if gain >= _HD2_MIN_GAIN and ok_ratio and cash >= 300 * k + extra_cost + 50:
        st["mode"] = best
        _HD2_REPORT["hd2_decision"] = "%s@%d" % (best, step)
    else:
        _HD2_REPORT["hd2_decision"] = "keep@%d" % step


def _hd2_rewrite(obs, action, st):
    mode = st["mode"]
    spec = _HD2_SPEC[mode]
    item = spec["product"]
    seat = int(obs["player"])
    farm = obs["farms"][seat]
    private = obs["private"]
    positions = [farm["farmer"]] + list(farm["hands"])
    market = action.get("market") or []
    cash = float(farm.get("money", 0))
    seed_cost = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
    for order in market:
        if len(order) >= 3 and order[0] == "BUY_ANIMAL" and order[1] == "GOOSE":
            n = max(0, int(order[2]))
            affordable = int(max(0.0, cash) // spec["cost"])
            order[1] = mode
            order[2] = min(n, affordable)
            cash -= order[2] * spec["cost"]
            _HD2_REPORT["hd2_rewrites"] += 1
        elif len(order) >= 3 and order[0] in ("BUY_ANIMAL", "BUY_SEED", "BUY_PRODUCT"):
            # money spent by earlier orders of the same list is not available to the swap (DS-5 #6)
            q = max(0, int(order[2]))
            if order[0] == "BUY_ANIMAL":
                cash -= q * {"GOOSE": 300, "COW": 400, "SHEEP": 500}.get(order[1], 0)
            elif order[0] == "BUY_SEED":
                cash -= q * seed_cost.get(order[1], 0)
            else:
                cash -= q * int((obs["market"]["prices"] or {}).get(order[1], 0))
        elif order and order[0] == "BUY_LAND":
            cash -= 4000
    workers = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
    for actor, work in enumerate(workers[:len(positions)]):
        if not work:
            continue
        x, y = positions[actor]
        tile = farm["tiles"][y][x]
        if work[0] == "BUILD_COOP":
            workers[actor] = ["BUILD_PASTURE"]
            _HD2_REPORT["hd2_rewrites"] += 1
        elif len(work) >= 2 and work[0] in ("PICKUP", "PLACE") and work[1] == "GOOSE":
            workers[actor] = [work[0], mode] + list(work[2:])
            _HD2_REPORT["hd2_rewrites"] += 1
            if work[0] == "PLACE":
                st["pending"].append((x, y, int(obs["step"]) // 24))
        elif len(work) >= 2 and work[0] == "PLACE" and work[1] == "EGG":
            workers[actor] = ["PLACE", item] + list(work[2:])
            _HD2_REPORT["hd2_rewrites"] += 1
        elif work == ["HARVEST"] and (x, y) in st["sites"] and isinstance(tile, dict) \
                and tile.get("animal") == mode:
            units = max(0, int(tile.get("yield_units", 0)))
            st["credit"] += units
            _HD2_REPORT["hd2_credit_units"] += units
    action["farmer"] = workers[0]
    action["hands"] = workers[1:]
    if st["credit"] > 0:
        try:
            stock = projected_shed(action, FarmView(obs))
        except Exception:
            stock = dict(private.get("shed") or {})
        planned = sum(max(0, int(o[2])) for o in market if len(o) >= 3 and o[:2] == ["SELL", item])
        extra = min(st["credit"], max(0, int(stock.get(item, 0)) - planned))
        if extra > 0:
            for order in market:
                if len(order) >= 3 and order[:2] == ["SELL", item]:
                    order[2] = int(order[2]) + extra
                    break
            else:
                if len(market) < 10:
                    market.insert(0, ["SELL", item, extra])
                else:
                    extra = 0
            st["credit"] -= extra
            _HD2_REPORT["hd2_sold_units"] += extra
    action["market"] = market


def _hd2_confirm(obs, st):
    farm = obs["farms"][int(obs["player"])]
    keep = []
    for x, y, day in st["pending"]:
        tile = farm["tiles"][y][x]
        if isinstance(tile, dict) and tile.get("animal") == st["mode"] and tile.get("placed_day") == day:
            st["sites"][(x, y)] = day
        elif int(obs["step"]) // 24 <= day + 1:
            keep.append((x, y, day))
    st["pending"] = keep


_HD2_PARENT = agent
del agent


def agent(observation, configuration=None):
    action = _HD2_PARENT(observation, configuration)
    try:
        seat = int(observation["player"])
        step = int(observation["step"])
        st = _HD2_STATE.get(seat)
        if st is None or step <= st["step"]:
            st = _HD2_STATE[seat] = {"step": -1, "inv": {}, "decided": False, "mode": None,
                                     "pending": [], "sites": {}, "credit": 0}
            if step == 0:
                _HD2_REPORT.update(hd2_decision="", hd2_ev="", hd2_rewrites=0, hd2_credit_units=0,
                                   hd2_sold_units=0, hd2_errors=0)
        st["step"] = step
        day = step // 24
        if day not in st["inv"]:
            st["inv"][day] = dict(observation["market"]["inventory"])
        if not isinstance(action, dict):
            return action
        if st["mode"]:
            _hd2_confirm(observation, st)
        elif not st["decided"]:
            _hd2_decide(observation, action, st)
        if st["mode"]:
            action = copy.deepcopy(action)
            _hd2_rewrite(observation, action, st)
    except Exception:
        _HD2_REPORT["hd2_errors"] += 1
    return action


agent.telemetry = _HD2_REPORT
agent = globals().pop('agent')


# ---------------------------------------------------------------------------
# COWSWAP layer: cow / goose / sheep at the tape's first cow purchase. Own implementation.
# Built by tools/claude_build_cowswap.py (derivation there). Requires HERD2 above.
# ---------------------------------------------------------------------------
_CS_FROM = 144
_CS_TO = 192
_CS_RATIO = 1.3
_CS_MIN_GAIN = 600.0
_CS_OPTIONS = ('GOOSE',)
_CS_SHOP_RULE = 'nomilk'
_CS_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
_CS_STATE = {}
_CS_REPORT = {"cs_decision": "", "cs_ev": "", "cs_rewrites": 0, "cs_broken": 0, "cs_credit": 0,
              "cs_sold": 0, "cs_errors": 0}


def _cs_tape(seat, t):
    native = _IMPL.chassis.players.get(seat)
    if not native or t > 719:
        return {}
    tape = _IMPL.chassis.routes[2 if t >= 648 else native["route"]]
    return tape[t] if t < len(tape) and isinstance(tape[t], dict) else {}


def _cs_spawn(positions, board):
    half = board // 2
    access = [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]
    occ = {a: 0 for a in access}
    for p in positions:
        if tuple(p) in occ:
            occ[tuple(p)] += 1
    return list(min(access, key=lambda a: (occ[a], access.index(a))))


def _cs_plan(obs, action, k, mode):
    seat = int(obs["player"])
    step = int(obs["step"])
    farm = obs["farms"][seat]
    board = len(farm["tiles"])
    positions = [list(farm["farmer"])] + [list(h) for h in farm["hands"]]
    end = (step // 24 + 1) * 24 - 1
    builds, pickups, places = [], [], []
    for t in range(step, end + 1):
        act = action if t == step else _cs_tape(seat, t)
        units = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        for i in range(len(positions)):
            cmd = units[i] if i < len(units) and units[i] else ["PASS"]
            pos = tuple(positions[i])
            if cmd[0] in _CS_MOVES:
                dx, dy = _CS_MOVES[cmd[0]]
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < board and 0 <= ny < board:
                    positions[i] = [nx, ny]
            elif cmd[0] == "BUILD_PASTURE":
                builds.append((t, i, pos))
            elif len(cmd) >= 2 and cmd[0] == "PICKUP" and cmd[1] == "COW":
                pickups.append((t, i, max(1, int(cmd[2]) if len(cmd) > 2 else 1)))
            elif len(cmd) >= 2 and cmd[0] == "PLACE" and cmd[1] == "COW":
                places.append((t, i, pos))
        hires = sum(1 for o in (act.get("market") or []) if o and o[0] == "HIRE")
        for _ in range(hires):
            positions.append(_cs_spawn(positions, board))
    chosen, tiles = [], set()
    for t, i, pos in places:
        if pos not in tiles:
            chosen.append((t, i, pos))
            tiles.add(pos)
        if len(chosen) == k:
            break
    if len(chosen) < k:
        return None
    plan = {"builds": {}, "pickups": {}, "places": {}}
    buying_land = any(o and o[0] == "BUY_LAND" for o in (action.get("market") or []))
    unlocked = list(farm.get("unlocked_quadrants") or ["NW"])
    next_quadrant = [q for q in ("NE", "SW", "SE") if q not in unlocked][:1]
    half = board // 2
    for t, i, pos in chosen:
        x, y = pos
        tile = farm["tiles"][y][x]
        if mode == "GOOSE":
            quadrant = ("N" if y < half else "S") + ("W" if x < half else "E")
            locked_but_bought = tile == "LOCKED" and buying_land and quadrant in next_quadrant
            if tile is not None and not locked_but_bought:
                return None  # already built (or occupied): cannot become a coop without extra turns
            prior = [(tb, ib) for tb, ib, pb in builds if pb == pos and tb < t]
            if not prior:
                return None
            tb, ib = prior[-1]
            plan["builds"][(tb, ib)] = pos
        carrier = [(tp, ip, q) for tp, ip, q in pickups if ip == i and tp < t]
        if not carrier:
            return None
        tp, ip, q = carrier[-1]
        plan["pickups"][(tp, ip)] = plan["pickups"].get((tp, ip), 0) + 1
        plan["places"][(t, i)] = pos
    for key, n in plan["pickups"].items():
        q = next(q for tp, ip, q in pickups if (tp, ip) == key)
        if q != n:
            return None  # a pickup that also carries unswapped cows cannot be split
    return plan


_CS_PARENT = agent
del agent


def agent(observation, configuration=None):
    action = _CS_PARENT(observation, configuration)
    try:
        seat = int(observation["player"])
        step = int(observation["step"])
        st = _CS_STATE.get(seat)
        if st is None or step <= st["step"]:
            st = _CS_STATE[seat] = {"step": -1, "decided": False, "mode": None, "plan": None,
                                    "broken": False, "sites": {}, "pending": [], "credit": 0}
            if step == 0:
                _CS_REPORT.update(cs_decision="", cs_ev="", cs_rewrites=0, cs_broken=0, cs_credit=0,
                                  cs_sold=0, cs_errors=0)
        st["step"] = step
        if not isinstance(action, dict):
            return action
        farm = observation["farms"][seat]
        positions = [farm["farmer"]] + list(farm["hands"])
        market = [list(o) for o in (action.get("market") or [])]
        # confirm placements
        if st["pending"]:
            keep = []
            for x, y, day in st["pending"]:
                tile = farm["tiles"][y][x]
                if isinstance(tile, dict) and tile.get("animal") == st["mode"] and tile.get("placed_day") == day:
                    st["sites"][(x, y)] = day
                elif step // 24 <= day:
                    keep.append((x, y, day))
            st["pending"] = keep
        if not st["decided"] and _CS_FROM <= step < _CS_TO:
            buys = [o for o in market if len(o) >= 3 and o[0] == "BUY_ANIMAL" and o[1] == "COW" and int(o[2]) > 0]
            shops_now = list((observation.get("town") or {}).get("unlocked_shops") or [])
            shop_ok = True
            if _CS_SHOP_RULE:
                # research/claude_20260913/RESULTS.md: over 48 seeds the swap only paid with an egg shop
                # open and no milk shop open (+1,254 mean over 9 seeds); with a milk shop it lost.
                no_milk = not any(s in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP") for s in shops_now)
                if _CS_SHOP_RULE == "nomilk":
                    # 14 seeds without a milk shop and without a yarn store: +1,203 mean
                    shop_ok = no_milk and "YARN_STORE" not in shops_now
                else:
                    shop_ok = no_milk and any(s in ("BAKERY", "BRUNCH_SPOT") for s in shops_now)
            if buys and not shop_ok:
                st["decided"] = True
                _CS_REPORT["cs_decision"] = "shoprule@%d" % step
            elif buys:
                st["decided"] = True
                k = sum(int(o[2]) for o in buys)
                evs = {opt: _hd2_ev(opt, k, observation, st)[0] for opt in ("COW",) + tuple(_CS_OPTIONS)}
                _CS_REPORT["cs_ev"] = ",".join("%s:%d" % (o, v) for o, v in sorted(evs.items()))
                best = max(_CS_OPTIONS, key=lambda o: evs[o])
                cow = evs["COW"]
                if evs[best] - cow >= _CS_MIN_GAIN and evs[best] >= _CS_RATIO * max(cow, 1.0):
                    plan = _cs_plan(observation, action, k, best)
                    if plan is not None:
                        st["mode"], st["plan"] = best, plan
                        _CS_REPORT["cs_decision"] = "%s@%d" % (best, step)
                        for o in market:
                            if len(o) >= 3 and o[0] == "BUY_ANIMAL" and o[1] == "COW":
                                o[1] = best
                                _CS_REPORT["cs_rewrites"] += 1
                    else:
                        _CS_REPORT["cs_decision"] = "noplan@%d" % step
                else:
                    _CS_REPORT["cs_decision"] = "keep@%d" % step
        if st["mode"] and st["plan"] and not st["broken"]:
            plan = st["plan"]
            units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
            for i in range(min(len(units), len(positions))):
                cmd = units[i] or ["PASS"]
                pos = (int(positions[i][0]), int(positions[i][1]))
                key = (step, i)
                if key in plan["builds"]:
                    if cmd == ["BUILD_PASTURE"] and pos == plan["builds"][key]:
                        units[i] = ["BUILD_COOP"]
                        _CS_REPORT["cs_rewrites"] += 1
                    else:
                        st["broken"] = True
                if key in plan["pickups"]:
                    if len(cmd) >= 2 and cmd[0] == "PICKUP" and cmd[1] == "COW":
                        units[i] = ["PICKUP", st["mode"]] + list(cmd[2:])
                        _CS_REPORT["cs_rewrites"] += 1
                    else:
                        st["broken"] = True
                if key in plan["places"]:
                    if len(cmd) >= 2 and cmd[0] == "PLACE" and cmd[1] == "COW" and pos == plan["places"][key]:
                        units[i] = ["PLACE", st["mode"]] + list(cmd[2:])
                        st["pending"].append((pos[0], pos[1], step // 24))
                        _CS_REPORT["cs_rewrites"] += 1
                    else:
                        st["broken"] = True
            if st["broken"]:
                _CS_REPORT["cs_broken"] += 1
            action = dict(action)
            action["farmer"] = units[0]
            action["hands"] = units[1:]
        # credit harvests on swapped tiles and sell them as they reach the shed
        if st["sites"]:
            product = _HD2_SPEC[st["mode"]]["product"]
            units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
            for i in range(min(len(units), len(positions))):
                x, y = int(positions[i][0]), int(positions[i][1])
                tile = farm["tiles"][y][x]
                if units[i] == ["HARVEST"] and (x, y) in st["sites"] and isinstance(tile, dict) \
                        and tile.get("animal") == st["mode"]:
                    n = max(0, int(tile.get("yield_units", 0)))
                    st["credit"] += n
                    _CS_REPORT["cs_credit"] += n
            if st["credit"] > 0:
                stock = projected_shed(action, FarmView(observation))
                planned = sum(max(0, int(o[2])) for o in market if len(o) >= 3 and o[:2] == ["SELL", product])
                extra = min(st["credit"], max(0, int(stock.get(product, 0)) - planned))
                if extra > 0:
                    for o in market:
                        if len(o) >= 3 and o[:2] == ["SELL", product]:
                            o[2] = int(o[2]) + extra
                            break
                    else:
                        if len(market) < 10:
                            market.insert(0, ["SELL", product, extra])
                        else:
                            extra = 0
                    st["credit"] -= extra
                    _CS_REPORT["cs_sold"] += extra
        action = dict(action)
        action["market"] = market
    except Exception:
        _CS_REPORT["cs_errors"] += 1
    return action


agent.telemetry = _CS_REPORT
agent = globals().pop('agent')




# EXP283 adaptive arm: clone-gated sale pre-emption with drop-time race escalation.
# Original mechanism by Ahmed Berat Ozer's project. Live top-band replays (research155) show
# rivals executing the same public route tape and quoting the same product batches at the
# same drop turns. While the rival is observed executing our tape, V43's R36 native-tape
# reservation runs with horizon 8; if the rival is then observed selling a race product at the
# very turn the same product was dropped into our shed while we did not sell it (public market
# inventory change beyond town consumption; no own realized sale; own shed stock rose), the rival
# quotes at the drop and the horizon escalates to 24 for the rest of the game.
_RACE_PARENT=agent
_RACE_HORIZON_CLONE=8
_RACE_HORIZON_ESCALATED=24
_RACE_HORIZON_MIRROR=24
_RACE_ITEMS=('CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL')
_RACE_SHOPS={'BAKERY':('EGG','WHEAT'),'PIZZA_SHOP':('MILK','TOMATO','WHEAT'),'BRUNCH_SPOT':('EGG','WHEAT','STRAWBERRY'),'YARN_STORE':('WOOL',),
             'ICE_CREAM_SHOP':('STRAWBERRY','MILK','WHEAT'),'PET_CAFE':('CARROT',),'SMOOTHIE_SHOP':('STRAWBERRY','MILK'),'FARMERS_MARKET':('WHEAT','CARROT','TOMATO','STRAWBERRY')}
_RACE_STATE={}
_RACE_REPORT=dict(race_clone_turns=0,race_horizon_turns=0,race_lost_races=0,race_escalations=0,race_errors=0)
_RACE_ORIG_RESERVE=_r36_reserve

def _race_positions_equal(farms,player):
    own,rival=farms[player],farms[1-player]
    return len(own['hands'])>0 and own['hands']==rival['hands'] and own['farmer']==rival['farmer']

def _race_clone(observation,state):
    farms=observation['farms'];player=int(observation['player'])
    if len(farms[player]['hands'])>0:
        state['hist'].append(_race_positions_equal(farms,player))
        if len(state['hist'])>6:state['hist'].pop(0)
    return len(state['hist'])>=4 and sum(state['hist'])>=4 and _r37_similarity(observation)>=.95

def _race_town(step,shops):
    out={}
    if step%4==0:
        for shop in shops:
            items=_RACE_SHOPS.get(shop,())
            for item in items:out[item]=out.get(item,0)+(2 if len(items)==1 else 1)
    if step%24==0:
        for item in _RACE_ITEMS:out[item]=out.get(item,0)+1
    return out

def _race_lost(observation,state):
    """EXP293: True when the rival sold a race product at the previous turn while we held it unsold, the common tape
    has no sale of it within the lineage's own lead/reservation window (5 turns) and sells it within the following
    24 turns: the rival pre-empts the plan's own sale ahead of us."""
    prev=state.get('prev');prev_action=state.get('prev_action')
    if prev is None or prev_action is None:return False
    step=int(observation['step']);player=int(observation['player'])
    if step!=prev['step']+1 or step%24==0:return False
    inv=observation['market']['inventory'];pinv=prev['inventory'];prices=prev['prices']
    town=_race_town(step-1,prev['shops'])
    sold={}
    for order in prev_action.get('market',[]):
        if len(order)>=3 and order[0]=='SELL' and order[1] in _RACE_ITEMS:sold[order[1]]=1
    native=_IMPL.chassis.players[player]
    for item in _RACE_ITEMS:
        before=int(prev['view'].shed.get(item,0))
        if before<=0 or item in sold or prices.get(item,0)<=1:continue
        rival=int(inv[item])-int(pinv[item])+town.get(item,0)
        if rival<=0:continue
        def planned(t):
            future=_IMPL.chassis.routes[2 if t>=648 else native['route']][t]
            return any(len(o)>=3 and o[0]=='SELL' and o[1]==item for o in future.get('market',[]))
        # every member of this lineage sells at the scheduled turn, one turn early (sale lead) or up to four turns early
        # (the base reservation): only a sale further ahead of the plan is a race
        if any(planned(t) for t in range(step-1,min(719,step+5))):continue
        if any(planned(t) for t in range(step+5,min(719,step+24))):return True
    return False

def _race_snapshot(observation):
    market=observation['market']
    return dict(step=int(observation['step']),inventory=dict(market['inventory']),prices=dict(market['prices']),shops=list(observation['town'].get('unlocked_shops',[])),view=FarmView(observation))

def _r36_reserve(obs,action):
    player=int(obs['player']);h=_RACE_STATE.get(player,{}).get('horizon',0)
    if h>_R37_HORIZONS.get(player,2):
        saved=_R37_HORIZONS.get(player);_R37_HORIZONS[player]=h
        try:return _RACE_ORIG_RESERVE(obs,action)
        finally:
            if saved is None:_R37_HORIZONS.pop(player,None)
            else:_R37_HORIZONS[player]=saved
    return _RACE_ORIG_RESERVE(obs,action)

def agent(observation,configuration=None):
    state=None
    try:
        player=int(observation['player']);step=int(observation['step'])
        state=_RACE_STATE.get(player)
        if state is None or step<=state['step']:
            state=_RACE_STATE[player]={'step':-1,'hist':[],'horizon':0,'level':_RACE_HORIZON_CLONE,'prev':None,'prev_action':None}
        if step==0:_RACE_REPORT.update(race_clone_turns=0,race_horizon_turns=0,race_lost_races=0,race_escalations=0,race_errors=0)
        state['step']=step;state['horizon']=0
        # EXP288 mirror gate: a rival whose cash after the first turn equals ours executed the same first-turn
        # round trip (a copy of this agent); against a copy the sale race is won only by pre-empting the whole day.
        if step==1:
            try:
                farms=observation['farms'];rival=farms[1-player]['money'];own=farms[player]['money']
                state['level']=_RACE_HORIZON_MIRROR if (abs(float(rival)-float(own))<0.5 and _RACE_HORIZON_MIRROR>state['level']) else state['level']
                _RACE_REPORT['race_mirror']=int(abs(float(rival)-float(own))<0.5)
            except Exception:_RACE_REPORT['race_errors']+=1
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
        if standard and 216<=step<696 and _race_clone(observation,state):
            _RACE_REPORT['race_clone_turns']+=1
            if state['level']<_RACE_HORIZON_ESCALATED and _race_lost(observation,state):
                _RACE_REPORT['race_lost_races']+=1;state['level']=_RACE_HORIZON_ESCALATED;_RACE_REPORT['race_escalations']+=1
            state['horizon']=state['level'];_RACE_REPORT['race_horizon_turns']+=1
    except Exception:_RACE_REPORT['race_errors']+=1
    snapshot=None
    try:
        if state is not None and 215<=int(observation['step'])<696:snapshot=_race_snapshot(observation)
    except Exception:_RACE_REPORT['race_errors']+=1
    action=_RACE_PARENT(observation,configuration)
    try:
        if state is not None:state['prev']=snapshot;state['prev_action']=action if snapshot is not None else None
    except Exception:_RACE_REPORT['race_errors']+=1
    _RACE_REPORT.update(getattr(_RACE_PARENT,'telemetry',{}))
    return action
agent.telemetry=_RACE_REPORT
agent=globals().pop('agent')


"""Fund urgent grain at the first quote slot; avoid unwatered last-hour plants.
Original safety contracts by Ahmed Berat Ozer, EXP258.
"""
_R127_PARENT=agent
_R127_STATES={}
_R127_REPORT={}

def _r127_fields(obs,action):
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={p for p,n in demand.items() if n>private['seeds'].get(p,0)}
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:continue
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,int(obs['step'])//24,24,100)
    return farm,private

def _r127_last_hour(obs,action):
    if int(obs['step'])%24!=23:return action
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    if not any(c and c[0]=='PLANT' for c in commands):return action
    result=copy.deepcopy(action);changed=False
    # Removing rejected requests can unblock the engine's atomic crop batch.
    # Recompute until every retained request ends the turn with a watered crop.
    for _ in range(len(commands)+1):
        farm,_=_r127_fields(obs,result);original=obs['farms'][obs['player']]
        positions=[original['farmer'],*original['hands']];drop=[]
        for actor,c in enumerate(commands):
            if not c or c[0]!='PLANT':continue
            tile=None
            if actor<len(positions):
                x,y=positions[actor];tile=farm['tiles'][y][x]
            if not (isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('crop')==c[1] and tile.get('planted_day')==int(obs['step'])//24 and tile.get('watered_today')):drop.append(actor)
        if not drop:break
        for actor in drop:commands[actor]=['PASS']
        result['farmer']=commands[0];result['hands']=commands[1:];changed=True
        _R127_REPORT['last_hour_plants_dropped']+=len(drop)
    return result if changed else action

def _r127_prefix_bound(obs,quantity):
    inventory=int(obs['market']['inventory']['WHEAT'])
    # Both players quote one unit before either commits. Before own unit j,
    # at most j-1 own and j-1 opponent wheat purchases have depleted inventory.
    return sum(_r37_market_price('WHEAT',inventory-(2*j-1)) for j in range(1,quantity+1))

def _r127_priority(obs,action,state):
    step=int(obs['step']);player=int(obs['player'])
    if not 144<=step<695:return action
    orders=action.get('market') or []
    if len(orders)>9 or any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in orders):return action
    native=_IMPL.chassis.players[player]
    future=_IMPL.chassis.routes[2 if step+1>=648 else native['route']][step+1]
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    if not any(c[:2]==['PICKUP','WHEAT'] for c in commands):return action
    if not _r97_budget(obs,orders):return action
    farm,private=_r127_fields(obs,action);night=step%24==23
    access=((4,4),(5,4),(4,5),(5,5));positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
    if night:positions=[(4,4)]
    else:
        for o in orders:
            if o and o[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    need=sum(max(0,int(c[2]) if len(c)>2 else 1) for pos,c in zip(positions,commands) if pos in access and c[:2]==['PICKUP','WHEAT'])
    stock,buys,_=_r97_market_stock(private['shed'],orders);before,loss=_r97_delivery(stock,private,night)
    shortage=max(0,need-before.get('WHEAT',0))
    if not shortage or shortage>100-sum(private['shed'].values()):return action
    cost=_r127_prefix_bound(obs,shortage)
    budget=dict(obs,farms=[dict(f) for f in obs['farms']]);budget['farms'][player]['money']-=cost
    if not _r97_budget(budget,orders):return action
    proposed=[['BUY_PRODUCT','WHEAT',shortage],*copy.deepcopy(orders)]
    stock,after_buys,_=_r97_market_stock(private['shed'],proposed);after,after_loss=_r97_delivery(stock,private,night)
    if after.get('WHEAT',0)<need or any(after_buys.get(i+1,0)<q for i,q in buys.items()) or any(q>loss.get(p,0) for p,q in after_loss.items()):return action
    state['pending_grain']=(step+1,after.get('WHEAT',0),shortage)
    _R127_REPORT['priority_grain_orders']+=1;_R127_REPORT['priority_grain_units']+=shortage
    return dict(action,market=proposed)

def agent(observation,configuration=None):
    result=_R127_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step']);state=_R127_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R127_STATES[player]={'step':-1}
            _R127_REPORT.update(last_hour_plants_dropped=0,priority_grain_orders=0,priority_grain_units=0,priority_grain_confirmed=0,priority_grain_shortfalls=0,priority_contract_errors=0)
        pending=state.pop('pending_grain',None)
        if pending and step==pending[0]:
            if observation['private']['shed'].get('WHEAT',0)>=pending[1]:_R127_REPORT['priority_grain_confirmed']+=pending[2]
            else:_R127_REPORT['priority_grain_shortfalls']+=1
        state['step']=step
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard:result=_r127_priority(observation,_r127_last_hour(observation,result),state)
    except Exception:_R127_REPORT['priority_contract_errors']=_R127_REPORT.get('priority_contract_errors',0)+1
    _R127_REPORT.update(getattr(_R127_PARENT,'telemetry',{}))
    return result
agent.telemetry=_R127_REPORT
agent=globals().pop('agent')


# ---- v44y pre-guard: quote at hour 21,22 what the hour-23 day-end storage guard (EXP-154) would dump ----
# The guard sells shed stock by price desc once shed+carried exceeds 99 at hour 23. Selling those lots
# a step earlier stays in the same town-consumption price window and quotes before a same-tape rival.
_PG_HOST=[v for v in list(globals().values()) if callable(v)][-1]
_Y_HOURS=(21, 22)
_Y_ITEMS=('MILK', 'STRAWBERRY', 'MELON', 'WOOL', 'TOMATO')
_Y_MIN_DAY=1
_Y_MARGIN=-6
_PG_REPORT={'preguard_turns':0,'preguard_units':0,'preguard_errors':0}

def _y_preguard(obs,action):
    step=int(obs['step'])
    if step%24 not in _Y_HOURS or step//24<_Y_MIN_DAY or step>=696:return action
    orders=[list(o) for o in (action.get('market') or [])]
    if len(orders)>=10:return action
    farm,private=_r127_fields(obs,action)
    stock,_,_=_r97_market_stock(private['shed'],orders)
    carried=sum(max(0,int(n)) for bag in private['inventories'] for n in bag.values())
    needed=sum(max(0,int(v)) for v in stock.values())+carried-99-_Y_MARGIN
    if needed<=0:return action
    prices=obs['market']['prices'];extra=[]
    for item in sorted(PRODUCTS,key=lambda it:-int(prices.get(it,0))):
        avail=max(0,int(stock.get(item,0)));qty=min(needed,avail)
        if qty<=0:continue
        if item in _Y_ITEMS and int(prices.get(item,0))>=2:extra.append(['SELL',item,qty])
        needed-=qty
        if needed<=0:break
    if not extra or len(orders)+len(extra)>10:return action
    _PG_REPORT['preguard_turns']+=1;_PG_REPORT['preguard_units']+=sum(o[2] for o in extra)
    return dict(action,market=orders+extra)

def agent_v44y_preguard(observation,configuration=None):
    action=_PG_HOST(observation,configuration)
    try:
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
        if standard:action=_y_preguard(observation,action)
    except Exception:_PG_REPORT['preguard_errors']+=1
    return action
agent_v44y_preguard.telemetry=_PG_REPORT


# ---- v44y: clone-mode race horizon override ----
_RACE_HORIZON_CLONE = 9

# ---- v44y: exact lockstep best-response SELL ordering against a detected clone ----
_V44Y_HOST = [v for v in list(globals().values()) if callable(v)][-1]
_V44Y_REORDER_GATE = False
_V44Y_MODE = 'as_is'  # 'as_is', 'gate_true', 'disabled'
_V44Y_REPORT = dict(v44y_reorder_turns=0, v44y_reorder_gain=0.0, v44y_gate_blocks=0, v44y_errors=0)
import itertools as _v44y_it

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

def _v44y_reorder(obs, action):
    market = action.get('market') or []
    if len(market) < 2: return action
    orders = [list(o) if isinstance(o, (list, tuple)) else o for o in market]
    blocks = []; i = 0
    while i < len(orders):
        o = orders[i]
        if o and o[0] == 'SELL':
            j = i
            while j < len(orders) and orders[j] and orders[j][0] == 'SELL': j += 1
            if 2 <= j - i <= 6: blocks.append((i, j))
            i = j
        else: i += 1
    if not blocks: return action
    view = FarmView(obs)
    stock = projected_shed(action, view)
    stock = {k: max(0, int(v)) for k, v in stock.items()}
    params = _v44y_params(obs)
    inv0 = {k: int(v) for k, v in obs['market']['inventory'].items()}
    opp = [list(o) for o in orders]
    margin = _v44y_factor_margin(opp, inv0, stock, params)
    base = margin(orders); best = base; best_orders = None
    for (i, j) in blocks:
        blk = orders[i:j]; n = j - i
        seen = set()
        for perm in _v44y_it.permutations(range(n)):
            key = tuple((blk[p][1], int(blk[p][2])) for p in perm)
            if key in seen: continue
            seen.add(key)
            cand = orders[:i] + [blk[p] for p in perm] + orders[j:]
            v = margin(cand)
            if v > best + 0.5: best = v; best_orders = cand
        if best_orders is not None:
            orders = best_orders; best_orders = None
    if best <= base + 0.5: return action
    _V44Y_REPORT['v44y_reorder_turns'] += 1; _V44Y_REPORT['v44y_reorder_gain'] += best - base
    out = dict(action); out['market'] = orders
    return out

def _v44y_clone_gate(obs):
    player = int(obs['player']); step = int(obs['step'])
    st = _RACE_STATE.get(player) or {}
    if st.get('horizon', 0) > 0: return True
    if step >= 696 and len(st.get('hist', [])) >= 4 and sum(st['hist']) >= 4:
        return _r37_similarity(obs) >= .95
    return False

def v44y_lockstep_agent(observation, configuration=None):
    action = _V44Y_HOST(observation, configuration)
    try:
        if _V44Y_MODE == 'disabled':
            return action
        step = int(observation.get('step', 0))
        if step >= 216:
            gate_ok = (not _V44Y_REORDER_GATE) or _v44y_clone_gate(observation)
            if gate_ok:
                action = _v44y_reorder(observation, action)
            else:
                _V44Y_REPORT['v44y_gate_blocks'] += 1
    except Exception:
        _V44Y_REPORT['v44y_errors'] += 1
    return action
v44y_lockstep_agent.telemetry = _V44Y_REPORT

# ==== v44y shop-aware herd wrapper (appended after the public V44 file; host entry captured first) ====
_Y_HOST=[v for v in list(globals().values()) if callable(v)][-1]
_Y_CFG={'yarnsheep': True, 'yarngeese': True, 'days': (8, 11)}
import copy as _y_copy
_Y_PRODUCT={'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}
_Y_STRUCT={'COW':'PASTURE','SHEEP':'PASTURE','GOOSE':'COOP'}
_Y_COST={'COW':400,'SHEEP':500,'GOOSE':300}
_Y_SEED={'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}
_Y_STATES={}
_Y_REPORT={'swaps':0,'pick':0,'place':0,'harvest':0,'boost':0,'errors':0,'coop':0,'declined':0}

def _y_new_state():
    return {'last':-1,'pending':[],'credit':{},'sites':{},'sale':{},'coop_swap':0}

def _y_target(kind,shops,cfg):
    yarn='YARN_STORE' in shops
    egg=('BAKERY' in shops) or ('BRUNCH_SPOT' in shops)
    milk=sum(s in ('PIZZA_SHOP','ICE_CREAM_SHOP','SMOOTHIE_SHOP') for s in shops)
    if kind=='SHEEP' and cfg.get('nosheep') and not yarn and milk>=cfg.get('min_milk',0):return 'COW'
    if kind=='COW' and cfg.get('yarnsheep') and yarn:return 'SHEEP'
    if kind=='GOOSE' and cfg.get('nogeese') and not egg:return 'SHEEP' if yarn else 'COW'
    if kind=='GOOSE' and cfg.get('yarngeese') and yarn:return 'SHEEP'
    return None

def _y_fib(n):
    a,b=1,1
    for _ in range(n):a,b=b,a+b
    return a

def _y_cash(obs,action,market):
    farm=obs['farms'][int(obs['player'])];prices=obs['market']['prices'];shed=obs['private']['shed']
    try:shed=projected_shed({'farmer':action.get('farmer') or ['PASS'],'hands':action.get('hands') or [],'market':[]},FarmView(obs))
    except Exception:pass
    cash=float(farm['money']);cost=0.0;hires=int(farm.get('hires_today',0) or 0)
    quads=len(farm.get('unlocked_quadrants',[]) or [])
    rem_shed={k:max(0,int(v)) for k,v in shed.items()}
    for o in market:
        if not o:continue
        op=o[0]
        if op=='SELL' and len(o)>=3:
            prod=o[1];qty=max(0,int(o[2]))
            avail=rem_shed.get(prod,0)
            sold=min(qty,avail)
            cash+=0.8*sold*float(prices.get(prod,0))
            rem_shed[prod]=avail-sold
        elif op=='BUY_ANIMAL' and len(o)>=3:cost+=int(o[2])*_Y_COST.get(o[1],500)
        elif op=='BUY_PRODUCT' and len(o)>=3:cost+=int(o[2])*(float(prices.get(o[1],0))+10)
        elif op=='BUY_SEED' and len(o)>=3:cost+=int(o[2])*_Y_SEED.get(o[1],100)
        elif op=='BUY_LAND':cost+=(1000,2000,4000)[min(2,max(0,quads-1))]
        elif op=='HIRE':cost+=_y_fib(hires);hires+=1
    return cash-cost

def _y_controller(obs,action,state,cfg):
    step=int(obs['step']);day=step//24;seat=int(obs['player'])
    farm=obs['farms'][seat];private=obs['private'];shed=private['shed'];inventories=private.get('inventories',[])
    shops=list((obs.get('town') or {}).get('unlocked_shops',[]) or [])
    tiles=farm['tiles'];n=len(tiles);center=n//2
    # 1. confirm last step's swapped purchases (physical shed gain)
    gained={}
    for p in state['pending']:
        to=p['to']
        if to not in gained:gained[to]=max(0,int(shed.get(to,0))-p['before'])
        got=min(p['qty'],gained[to]);gained[to]-=got
        if got>0:
            key=(p['from'],to);state['credit'][key]=state['credit'].get(key,0)+got
            if _Y_STRUCT[p['from']]!=_Y_STRUCT[to]:state['coop_swap']+=got
    state['pending']=[]
    result=_y_copy.deepcopy(action)
    market=result.get('market') or []
    result['market']=market
    # 2. purchase-point substitution by unlocked shops (cash-checked)
    if cfg['days'][0]<=day<=cfg['days'][1]:
        for o in market:
            if len(o)>=3 and o[0]=='BUY_ANIMAL' and o[1] in _Y_COST and 1<=int(o[2])<=cfg.get('maxq',2):
                to=_y_target(o[1],shops,cfg)
                if to is None or to==o[1]:continue
                trial=[list(x) if isinstance(x,list) else x for x in market]
                for t in trial:
                    if isinstance(t,list) and t==o:t[1]=to
                if _y_cash(obs,result,trial)<cfg.get('margin',100):
                    _Y_REPORT['declined']+=1;continue
                state['pending'].append({'from':o[1],'to':to,'qty':int(o[2]),'before':int(shed.get(to,0))})
                _Y_REPORT['swaps']+=int(o[2]);o[1]=to
    # 3. worker command rewrites (PICKUP / PLACE / BUILD_COOP) and harvest credit
    workers=[result.get('farmer') or ['PASS'],*(result.get('hands') or [])]
    positions=[farm['farmer'],*farm['hands']]
    avail={k:int(shed.get(k,0)) for k in _Y_COST}
    seen=set();occupied=set()
    for actor,work in enumerate(workers[:len(positions)]):
        if not work or not isinstance(work,list):continue
        inv=inventories[actor] if actor<len(inventories) else {}
        x,y=positions[actor];tile=tiles[y][x];site=(x,y);op=work[0]
        if op=='PICKUP' and len(work)>=2 and work[1] in _Y_COST:
            kind=work[1];qty=max(1,int(work[2])) if len(work)>2 else 1
            if avail.get(kind,0)>=qty:avail[kind]-=qty;continue
            if not (x in (center-1,center) and y in (center-1,center)):continue
            if any(inv.get(a,0) for a in _Y_COST):continue
            for (frm,to),c in list(state['credit'].items()):
                if frm==kind and c>=qty and avail.get(to,0)>=qty:
                    work[1]=to;state['credit'][(frm,to)]=c-qty;avail[to]-=qty;_Y_REPORT['pick']+=qty;break
        elif op=='PLACE' and len(work)>=2 and work[1] in _Y_COST:
            kind=work[1]
            if inv.get(kind,0)>0:continue
            for to in ('COW','SHEEP','GOOSE'):
                if (to!=kind and inv.get(to,0)>0 and isinstance(tile,dict) and tile.get('kind')==_Y_STRUCT[to]
                        and not tile.get('animal') and site not in occupied):
                    work[1]=to;state['sites'][site]=to;occupied.add(site);_Y_REPORT['place']+=1;break
        elif op=='BUILD_COOP' and state['coop_swap']>0:
            work[0]='BUILD_PASTURE';_Y_REPORT['coop']+=1
        elif op=='HARVEST' and site in state['sites'] and site not in seen:
            if isinstance(tile,dict) and tile.get('animal')==state['sites'][site]:
                units=max(0,int(tile.get('yield_units',0) or 0))
                if units:
                    prod=_Y_PRODUCT[tile['animal']];state['sale'][prod]=state['sale'].get(prod,0)+units;_Y_REPORT['harvest']+=units
            seen.add(site)
    result['farmer'],result['hands']=workers[0],workers[1:]
    # 4. sell the extra production at the tape's own existing sale slots (never add new orders)
    if cfg.get('boost',True):
        for prod,credit in list(state['sale'].items()):
            credit=min(credit,int(shed.get(prod,0)))
            state['sale'][prod]=credit
            if credit<=0:continue
            planned=sum(max(0,int(o[2])) for o in market if len(o)>=3 and o[0]=='SELL' and o[1]==prod)
            if planned<=0:continue
            extra=min(credit,int(shed.get(prod,0))-planned)
            if extra<=0:continue
            for o in market:
                if len(o)>=3 and o[0]=='SELL' and o[1]==prod and int(o[2])>0:
                    o[2]=int(o[2])+extra;state['sale'][prod]=credit-extra;_Y_REPORT['boost']+=extra;break
    return result

def _y_agent_shopherd(observation,configuration=None):
    action=_Y_HOST(observation,configuration)
    try:
        seat=int(observation['player']);step=int(observation['step'])
        state=_Y_STATES.get(seat)
        if state is None or step<=state['last']:state=_Y_STATES[seat]=_y_new_state()
        state['last']=step
        return _y_controller(observation,action,state,_Y_CFG)
    except Exception:
        _Y_REPORT['errors']+=1
        return action

# V47 attribution and modification notice (17 September 2026):
# Seyit Kaan Gunes, kaggle.com/code/seyitkaangunes/kaggriculture-2820-score:
# pre-overflow sale guard, clone-market lockstep ordering/horizon, and shop-aware herd layers.
# Ahmed Berat Ozer: transfer onto V46 EXP293, exact per-product score caching,
# exact physical-prefix/resource reuse, terminal no-op/movement fast paths,
# private reacting-opponent confirmation and packaging.
# Original source notices and license text above are retained.

# EXP334: remove useless cash-product sale slots without moving purchases.
_E334_ITEMS={'CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL'}
_E334_REPORT=dict(changed=0,removed=0,errors=0,singleton_fix=0)
_E334_BASE=_y_agent_shopherd

def _e334_compact_mixed(obs,action):
    market=action.get('market') or []
    if int(obs['step'])<144 or len(market)<2:return action
    segments=[];i=0
    while i<len(market):
        if len(market[i])>=3 and market[i][0]=='SELL' and market[i][1] in _E334_ITEMS:
            j=i+1
            while j<len(market) and len(market[j])>=3 and market[j][0]=='SELL' and market[j][1] in _E334_ITEMS:j+=1
            if j-i>=2:segments.append((i,j))
            i=j
        else:i+=1
    if not segments:return action
    _,private=_r127_fields(obs,action);remaining=dict(private['shed']);new=[list(o) for o in market];removed=0;consumed_singleton=False;allow_compact=True
    i=0
    while i<len(market):
        o=market[i]
        if allow_compact and len(o)>=3 and o[0]=='SELL' and o[1] in _E334_ITEMS:
            j=i+1
            while j<len(market) and len(market[j])>=3 and market[j][0]=='SELL' and market[j][1] in _E334_ITEMS:j+=1
            if j-i>=2:
                quantities={};order=[]
                for so in market[i:j]:
                    p=so[1]
                    if p not in quantities:order.append(p);quantities[p]=0
                    quantities[p]+=max(0,int(so[2]))
                kept=[]
                for p in order:
                    q=min(quantities[p],max(0,int(remaining.get(p,0))))
                    if q:kept.append(['SELL',p,q]);remaining[p]-=q
                # Empty order slots are explicitly skipped by the pinned engine parser.
                # Keep external order indices unchanged; do not pull BUY/HIRE forward.
                replacement=kept+[[] for _ in range(j-i-len(kept))]
                if replacement!=market[i:j]:removed+=j-i-len(kept);new[i:j]=replacement
                i=j
                continue
            p=o[1];take=min(max(0,int(o[2])),max(0,int(remaining.get(p,0))))
            if take:remaining[p]=int(remaining.get(p,0))-take;consumed_singleton=True
            i+=1
            continue
        if allow_compact and len(o)>=2 and o[0]=='BUY_PRODUCT' and o[1] in _E334_ITEMS:
            allow_compact=False
        i+=1
    if new==market:return action
    _E334_REPORT['changed']+=1;_E334_REPORT['removed']+=removed
    if consumed_singleton:_E334_REPORT['singleton_fix']+=1
    return dict(action,market=new)

def _e334_agent(observation,configuration=None):
    if int(observation.get('step',0))==0:
        for k in _E334_REPORT:_E334_REPORT[k]=0
    action=_E334_BASE(observation,configuration)
    try:return _e334_compact(observation,action)
    except Exception:
        _E334_REPORT['errors']+=1;return action

# EXP335: empty buyable-product sales are holes too, when no purchases exist.
_E335_ORIGINAL_COMPACT=_e334_compact_mixed

def _e334_compact(obs,action):
    market=action.get('market') or []
    if int(obs['step'])<144 or len(market)<2:return action
    if not all(len(o)>=3 and o[0]=='SELL' for o in market):return _E335_ORIGINAL_COMPACT(obs,action)
    _,private=_r127_fields(obs,action);remaining=dict(private['shed']);effective=[]
    for o in market:
        item=o[1];q=min(max(0,int(o[2])),max(0,int(remaining.get(item,0))))
        remaining[item]=max(0,int(remaining.get(item,0))-q)
        effective.append(['SELL',item,q] if q else [])
    new=[list(o) for o in effective];i=0;removed=0
    while i<len(effective):
        if effective[i] and effective[i][1] not in _E334_ITEMS:i+=1;continue
        j=i+1
        while j<len(effective) and (not effective[j] or effective[j][1] in _E334_ITEMS):j+=1
        order=[];qty={}
        for o in effective[i:j]:
            if not o:continue
            if o[1] not in qty:order.append(o[1]);qty[o[1]]=0
            qty[o[1]]+=o[2]
        kept=[['SELL',item,qty[item]] for item in order]
        new[i:j]=kept+[[] for _ in range(j-i-len(kept))];removed+=j-i-len(kept);i=j
    if new==market:return action
    _E334_REPORT['changed']+=1;_E334_REPORT['removed']+=removed
    return dict(action,market=new)

def _e335_agent(observation,configuration=None):
    return _e334_agent(observation,configuration)




# ---------------------------------------------------------------------------
# v11 entry normalisation: Kaggle's loader takes the last callable in the module
# namespace.  Rebind it to a fresh `agent` so the packaged name matches the rest
# of the v9 releases (and so validate.py's name check passes).
# ---------------------------------------------------------------------------
_V11_ENTRY = [v for v in list(globals().values()) if callable(v)][-1]


def agent(observation, configuration=None):
    return _V11_ENTRY(observation, configuration)


agent.telemetry = getattr(_V11_ENTRY, 'telemetry', {})
agent = globals().pop('agent')


# ---------------------------------------------------------------------------
# v13 V219SKIP (review suggestion #1): V219 hires a tomato crew every day from
# day 19, but tomatoes planted on day 18 only produce at the refreshes ending
# days 25-28.  Before that, watering only keeps them alive, and a plant
# survives one dry day (it dies after two consecutive dry refreshes).  On the
# chosen skip days, when every committed tomato was watered yesterday
# (consecutive_unwatered == 0), no crew is hired and nobody waters them today;
# the next day's crew waters them again.
# ---------------------------------------------------------------------------
V13V_SKIP_DAYS = (19, 21, 23)
_V13V_REPORT = dict(v_skipped=0, v_blocked=0, v_errors=0)
_V13V_ORIG_REQUEST = _v219_request


def _v219_request(obs, action, state, native):
    try:
        day = int(obs["step"]) // 24
        if day in V13V_SKIP_DAYS and state.get("committed") and state.get("requested_day") != day:
            farm = obs["farms"][int(obs["player"])]
            tomatoes = 0
            safe = True
            for x, y in state.get("targets", []):
                tile = farm["tiles"][y][x]
                if isinstance(tile, dict) and tile.get("crop") == "TOMATO":
                    tomatoes += 1
                    if int(tile.get("consecutive_unwatered", 1)) != 0:
                        safe = False
            if tomatoes and safe:
                state["requested_day"] = day
                _V13V_REPORT["v_skipped"] += 1
                return action
            if tomatoes:
                _V13V_REPORT["v_blocked"] += 1
    except Exception:
        _V13V_REPORT["v_errors"] += 1
    return _V13V_ORIG_REQUEST(obs, action, state, native)


_V13V_PARENT = agent


def agent(observation, configuration=None):
    if int(observation["step"]) == 0:
        for k in _V13V_REPORT:
            _V13V_REPORT[k] = 0
    return _V13V_PARENT(observation, configuration)


agent.telemetry = _V13V_REPORT
agent = globals().pop("agent")


# Bounded alternative productive openings. Dmitrii Gluzdov, 2026, Apache-2.0.
# The upstream The 2945 Farm source and its notices are preserved above.
_ALT_MODE = 'HybridOpening'
_ALT_RAW = copy.deepcopy(_IMPL.chassis.routes[0][:96])
_ALT_CT = dict(CT_TABLE)
_ALT_STATE = {}
_ALT_REPORT = {}

def _alt_install(mode):
    global CT_TABLE
    tape=_IMPL.chassis.routes[0]
    tape[:96]=copy.deepcopy(_ALT_RAW)
    CT_TABLE=dict(_ALT_CT)
    if mode=='Original': return
    if mode=='HybridOpening':
        tape[0]['market']=list(tape[0]['market'])+[['BUY_SEED','WHEAT',1]]
    else:
        CT_TABLE={}
        tape[0]['market']=[['BUY_PRODUCT','WHEAT',5],['BUY_SEED','WHEAT',1]]
        tape[1]['market']=[o for o in tape[1]['market'] if not (len(o)>=3 and o[0] in ('BUY_PRODUCT','SELL') and o[1]=='WHEAT')]
    # Day-zero idle hand 1 walks from (5,4) to the future (2,4) pasture.
    for step,command in {2:['WEST'],3:['WEST'],4:['WEST'],5:['PLANT','WHEAT'],6:['WATER']}.items():
        assert tape[step]['hands'][1]==['PASS']
        tape[step]['hands'][1]=command
    # On day one, water instead of building the not-yet-needed pasture.
    assert tape[29]['hands'][2]==['BUILD_PASTURE']
    tape[29]['hands'][2]=['WATER']
    # Day-two idle hand 0: water, harvest, restore pasture, deliver.
    commands=[['WEST'],['WEST'],['WEST'],['WATER'],['HARVEST'],['BUILD_PASTURE'],['EAST'],['EAST'],['DROP']]
    for step,command in zip(range(49,58),commands):
        assert tape[step]['hands'][0]==['PASS']
        tape[step]['hands'][0]=command
    if mode=='TomatoInsteadOfCow':
        tape[0]['market'].append(['BUY_SEED','TOMATO',1])
        cow=next(o for o in tape[1]['market'] if o[:2]==['BUY_ANIMAL','COW'])
        assert cow[2]==2; cow[2]=1
        # The first carrier still owns the bought cow; the other cow's site
        # becomes one tomato plant, with its worker route left in place.
        assert tape[2]['hands'][4][:2]==['PICKUP','COW']
        assert tape[3]['hands'][4]==['BUILD_PASTURE']
        assert tape[4]['hands'][4][:2]==['PLACE','COW']
        tape[2]['hands'][4]=['PASS']
        tape[3]['hands'][4]=['PASS']
        tape[4]['hands'][4]=['PLANT','TOMATO']
        tape[5]['hands'][4]=['WATER']
    assert max(len(a.get('market',[])) for a in tape[:96])<=10

def _alt_sell_extra(action,item,n):
    if n<=0:return action
    orders=[list(o) for o in action.get('market',[])]
    sell=next((o for o in orders if len(o)>=3 and o[:2]==['SELL',item]),None)
    if sell is not None:sell[2]+=n
    elif len(orders)<10:orders.append(['SELL',item,n])
    else:return action
    return dict(action,market=orders)

_ALT_PARENT=agent
def agent(observation,configuration=None):
    seat,step=int(observation['player']),int(observation['step'])
    state=_ALT_STATE.get(seat)
    if state is None or step<=state['step']:
        mode=_ALT_MODE
        if mode=='Mixed':
            # Private RNG: no mutation of the engine or opponent's random state.
            # Seed is used only for reproducible opening selection, never prediction.
            import random as _opening_random
            seed=(configuration or {}).get('seed',0)
            bit=_opening_random.Random('productive-opening:'+str(seed)+':'+str(seat)).getrandbits(1)
            mode='EarlyCycle' if bit else 'Original'
        _alt_install(mode)
        state=_ALT_STATE[seat]={'step':-1,'mode':mode}
        _ALT_REPORT.clear()
        _ALT_REPORT.update(selected_opening=mode,temporary_crop_seen=0,temporary_crop_harvested=0,
                           restored_pasture_seen=0,delivered_extra_wheat=0,tomato_seen=0,
                           tomato_water_requests=0,tomato_harvest_requests=0,tomato_units_harvest_requested=0,
                           extension_errors=0)
    action=_ALT_PARENT(observation,configuration)
    try:
        mode=state['mode']
        if mode!='Original':
            farm=observation['farms'][seat];private=observation['private']
            site=farm['tiles'][4][2]
            if step==6:_ALT_REPORT['temporary_crop_seen']=int(isinstance(site,dict) and site.get('crop')=='WHEAT')
            if step==54:
                _ALT_REPORT['temporary_crop_harvested']=int(private['inventories'][1].get('WHEAT',0))
            if step==55:_ALT_REPORT['restored_pasture_seen']=int(isinstance(site,dict) and site.get('kind')=='PASTURE')
            if step==57 and len(farm['hands'])>=1:
                if tuple(farm['hands'][0])==(4,4) and action.get('hands',[[]])[0]==['DROP']:
                    n=int(private['inventories'][1].get('WHEAT',0))
                    action=_alt_sell_extra(action,'WHEAT',n)
                    _ALT_REPORT['delivered_extra_wheat']=n
            if mode=='TomatoInsteadOfCow':
                tomato=farm['tiles'][4][4]
                if isinstance(tomato,dict) and tomato.get('crop')=='TOMATO' and tomato.get('planted_day')==0:
                    _ALT_REPORT['tomato_seen']=1
                    units=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands',[])]
                    positions=[tuple(farm['farmer'])]+[tuple(p) for p in farm['hands']]
                    watered=bool(tomato.get('watered_today'));yield_left=int(tomato.get('yield_units',0))
                    for actor,pos in enumerate(positions):
                        if pos!=(4,4) or actor>=len(units):continue
                        if units[actor][0] not in ('FEED','CARE','COLLECT_FERTILIZER','HARVEST','WATER','PASS'):continue
                        if not watered:
                            units[actor]=['WATER'];watered=True
                            _ALT_REPORT['tomato_water_requests']+=1
                        elif yield_left>0:
                            units[actor]=['HARVEST']
                            _ALT_REPORT['tomato_harvest_requests']+=1
                            _ALT_REPORT['tomato_units_harvest_requested']+=yield_left
                            yield_left=0
                        else:units[actor]=['PASS']
                    action=dict(action,farmer=units[0],hands=units[1:])
                # Tomatoes are cash produce, never a feed or route input. Sell
                # only observed shed stock beyond any parent's existing sale.
                stock=int(private['shed'].get('TOMATO',0))
                scheduled=sum(int(o[2]) for o in action.get('market',[]) if len(o)>=3 and o[:2]==['SELL','TOMATO'])
                action=_alt_sell_extra(action,'TOMATO',max(0,stock-scheduled))
    except Exception:
        _ALT_REPORT['extension_errors']+=1
    state['step']=step
    return action
agent.telemetry=_ALT_REPORT
agent=globals().pop('agent')

kaggle_submission_agent = agent


# Apache-2.0. Dmitrii Gluzdov: mature the temporary wheat one extra day.
_CL_INSTALL = _alt_install
_CL_REPORT = dict(cl_harvested=0, cl_pasture=0, cl_delivered=0, cl_errors=0)

def _alt_install(mode):
    _CL_INSTALL(mode)
    if mode not in ('EarlyCycle','HybridOpening'):
        return
    tape = _IMPL.chassis.routes[0]
    # Day-two watering remains at52; wait one more day before harvesting.
    for step in range(53,58):
        tape[step]['hands'][0] = ['PASS']
    # Hand0 finishes its original day-three work at(0,4), then idles.
    commands = [['EAST'],['EAST'],['WATER'],['HARVEST'],['BUILD_PASTURE'],['EAST'],['EAST'],['DROP']]
    for step, command in zip(range(84,92), commands):
        assert tape[step]['hands'][0] == ['PASS']
        tape[step]['hands'][0] = command

_CL_PARENT = agent
def agent(observation, configuration=None):
    step = int(observation['step'])
    if step == 0:
        for key in _CL_REPORT: _CL_REPORT[key] = 0
    action = _CL_PARENT(observation, configuration)
    try:
        seat = int(observation['player'])
        farm, private = observation['farms'][seat], observation['private']
        if step == 88:
            _CL_REPORT['cl_harvested'] = int(private['inventories'][1].get('WHEAT',0))
        if step == 89:
            tile = farm['tiles'][4][2]
            _CL_REPORT['cl_pasture'] = int(isinstance(tile,dict) and tile.get('kind')=='PASTURE')
        if step == 91 and farm['hands'] and tuple(farm['hands'][0]) == (4,4) and action['hands'][0] == ['DROP']:
            amount = int(private['inventories'][1].get('WHEAT',0))
            action = _alt_sell_extra(action,'WHEAT',amount)
            _CL_REPORT['cl_delivered'] = amount
    except Exception:
        _CL_REPORT['cl_errors'] += 1
    return action
agent.telemetry = _CL_REPORT
agent = globals().pop('agent')
kaggle_submission_agent = agent



# Conservative completion layer for the delayed opening crop and market queue.
_OW_CASH = frozenset((
    "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL",
))
_OW_STATE = {}
_OW_REPORT = {
    "opening_repairs": 0,
    "delayed_cycle_commits": 0,
    "delayed_cycle_skips": 0,
    "queue_changed_turns": 0,
    "zeroed_orders": 0,
    "pulled_orders": 0,
    "pulled_slots": 0,
    "errors": 0,
}


def _ow_standard(configuration):
    if configuration is None or not hasattr(configuration, "get"):
        return True
    return all(configuration.get(key, expected) == expected for key, expected in (
        ("boardSize", 10),
        ("turnsPerDay", 24),
        ("shedCapacity", 100),
        ("maxMarketOrdersPerTurn", 10),
    ))


def _ow_hand(action, index, command):
    hands = [list(value) for value in (action.get("hands") or [])]
    if index >= len(hands):
        return action
    hands[index] = list(command)
    return dict(action, hands=hands)


def _ow_guard_opening(observation, action):
    """Restore the original pasture when the temporary wheat never appeared."""
    if int(observation.get("step", -1)) != 29 or not isinstance(action, dict):
        return action
    seat = int(observation["player"])
    state = _ALT_STATE.get(seat)
    if not state or state.get("mode") not in ("EarlyCycle", "HybridOpening"):
        return action
    farm = observation["farms"][seat]
    site = farm["tiles"][4][2]
    valid = (
        isinstance(site, dict) and site.get("kind") == "PLANT" and
        site.get("crop") == "WHEAT" and int(site.get("planted_day", -1)) == 0
    )
    hands = action.get("hands") or []
    if valid or len(hands) <= 2 or hands[2] != ["WATER"]:
        return action
    _OW_REPORT["opening_repairs"] += 1
    return _ow_hand(action, 2, ["BUILD_PASTURE"])


def _ow_gate_delayed_cycle(observation, action):
    """Skip the delayed detour only when the pasture is already restored."""
    step = int(observation.get("step", -1))
    seat = int(observation["player"])
    state = _OW_STATE.setdefault(seat, {"step": -1, "late_cycle": None})
    if step <= state.get("step", -1):
        state.clear()
        state.update(step=-1, late_cycle=None)
    state["step"] = step
    opening = _ALT_STATE.get(seat)
    if not opening or opening.get("mode") not in ("EarlyCycle", "HybridOpening"):
        return action

    if step == 84:
        farm = observation["farms"][seat]
        site = farm["tiles"][4][2]
        hands = action.get("hands") or []
        ready = (
            len(farm.get("hands") or []) >= 1 and tuple(farm["hands"][0]) == (0, 4) and
            isinstance(site, dict) and site.get("kind") == "PLANT" and
            site.get("crop") == "WHEAT" and int(site.get("planted_day", -1)) == 0 and
            int(site.get("yield_units", 0)) >= 2 and
            len(hands) >= 1 and hands[0] == ["EAST"]
        )
        restored = isinstance(site, dict) and site.get("kind") == "PASTURE"
        if ready:
            state["late_cycle"] = True
            _OW_REPORT["delayed_cycle_commits"] += 1
        elif restored:
            state["late_cycle"] = False
            _OW_REPORT["delayed_cycle_skips"] += 1
        else:
            # Uncertain states remain under the parent safety controller.
            state["late_cycle"] = None

    if 84 <= step <= 91 and state.get("late_cycle") is False:
        return _ow_hand(action, 0, ["PASS"])
    return action


def _ow_close_queue(observation, action):
    """Remove zero-execution cash sales and stably pull later cash sales left."""
    if not isinstance(action, dict):
        return action
    market = action.get("market") or []
    if len(market) < 2:
        return action
    projected = dict(projected_shed(action, FarmView(observation)))
    remaining = {item: max(0, int(projected.get(item, 0))) for item in _OW_CASH}
    revised = []
    zeroed = 0
    for raw in market:
        order = list(raw) if isinstance(raw, (list, tuple)) else raw
        if (isinstance(order, list) and len(order) >= 3 and
                order[0] == "SELL" and order[1] in _OW_CASH):
            requested = max(0, int(order[2]))
            executed = min(requested, remaining[order[1]])
            remaining[order[1]] -= executed
            if executed <= 0:
                revised.append([])
                zeroed += 1
            else:
                revised.append(order)
        else:
            revised.append(order)

    holes = []
    pulled = 0
    distance = 0
    for index, order in enumerate(revised):
        if not order:
            holes.append(index)
            continue
        movable = (
            isinstance(order, list) and len(order) >= 3 and
            order[0] == "SELL" and order[1] in _OW_CASH and int(order[2]) > 0
        )
        if not movable or not holes:
            continue
        target = holes.pop(0)
        revised[target] = order
        revised[index] = []
        holes.append(index)
        pulled += 1
        distance += index - target

    if revised == market:
        return action
    _OW_REPORT["queue_changed_turns"] += 1
    _OW_REPORT["zeroed_orders"] += zeroed
    _OW_REPORT["pulled_orders"] += pulled
    _OW_REPORT["pulled_slots"] += distance
    return dict(action, market=revised)


_OW_PARENT = agent
del agent


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    if step == 0:
        for key in _OW_REPORT:
            _OW_REPORT[key] = 0
    action = _OW_PARENT(observation, configuration)
    try:
        if _ow_standard(configuration):
            action = _ow_guard_opening(observation, action)
            action = _ow_gate_delayed_cycle(observation, action)
            action = _ow_close_queue(observation, action)
    except Exception:
        _OW_REPORT["errors"] += 1
    return action


agent.telemetry = _OW_REPORT
agent = globals().pop("agent")


# Endgame dynamic seed-purchase commitment guard.
# Upgraded in JFJH-v1-seed-commitment to dynamically match remaining planting
# obligations in Route 2 and CARROT2 swap capacity starting from step 648 (day 27).
# Crops bought after need is satisfied can never create harvest value before step 720.
# Replaces unneeded BUY_SEED slots with [] to preserve market slot layout.
_ES_REPORT = {"orders_blocked": 0, "coins_saved_nominal": 0, "errors": 0}
_ES_PARENT = agent
del agent
_ES_SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
_SEED_COMMIT_MODE = "dynamic_commit"  # options: "as_is" (v1 static table), "dynamic_commit" (CARROT2-aware dynamic commitment), "disabled"
_R2_FUTURE_PLANTS = {
    648: (8, 2), 649: (8, 2), 650: (8, 2), 651: (8, 2), 652: (8, 2),
    653: (8, 2), 654: (8, 2), 655: (8, 2), 656: (7, 2), 657: (4, 2),
    658: (3, 2), 659: (3, 2), 660: (3, 2), 661: (3, 2), 662: (1, 1),
    663: (1, 1), 664: (1, 1), 665: (1, 1), 666: (1, 1), 667: (1, 1),
    668: (1, 1), 669: (1, 1)
}


def _es_cut_dead_seed_buys(observation, configuration, action):
    if _SEED_COMMIT_MODE == "disabled":
        return action
    if not isinstance(action, dict) or not _ow_standard(configuration):
        return action
    step = int(observation.get("step", 0))
    if step < 27 * 24:
        return action
    market = action.get("market") or []
    if not any(isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "BUY_SEED" for o in market):
        return action

    priv = observation.get("private") or {}
    seeds = priv.get("seeds") or {}
    farmer = action.get("farmer") or []
    hands = action.get("hands") or []
    units = [farmer] + hands

    p_w = sum(1 for u in units if isinstance(u, (list, tuple)) and len(u) >= 2 and u[0] == "PLANT" and u[1] == "WHEAT")
    p_c = sum(1 for u in units if isinstance(u, (list, tuple)) and len(u) >= 2 and u[0] == "PLANT" and u[1] == "CARROT")

    avail_w = max(0, int(seeds.get("WHEAT", 0)) - p_w)
    avail_c = max(0, int(seeds.get("CARROT", 0)) - p_c)

    fw, fc = _R2_FUTURE_PLANTS.get(step, (0, 0))
    if _SEED_COMMIT_MODE == "dynamic_commit":
        p_c_mkt = int(observation.get("market", {}).get("prices", {}).get("CARROT", 0))
        p_w_mkt = int(observation.get("market", {}).get("prices", {}).get("WHEAT", 0))
        ca_pays = (3 * p_c_mkt - 20) > (4 * p_w_mkt - 10 - 5.0)
        max_w = 0 if ca_pays else fw
        max_c = (fc + fw) if ca_pays else fc
    else:
        max_w = fw
        max_c = fc + fw

    revised = []
    changed = False
    for raw in market:
        order = list(raw) if isinstance(raw, (list, tuple)) else raw
        if isinstance(order, list) and len(order) >= 3 and order[0] == "BUY_SEED":
            crop = order[1]
            try:
                qty = max(0, int(order[2]))
            except (TypeError, ValueError):
                qty = 0
            if qty <= 0:
                revised.append([])
                changed = True
                continue

            if crop == "WHEAT":
                allowed = max(0, max_w - avail_w)
                buy_qty = min(qty, allowed)
                cut = qty - buy_qty
                if cut > 0:
                    _ES_REPORT["orders_blocked"] += 1
                    _ES_REPORT["coins_saved_nominal"] += cut * 10
                    changed = True
                    if buy_qty > 0:
                        order[2] = buy_qty
                        avail_w += buy_qty
                        revised.append(order)
                    else:
                        revised.append([])
                else:
                    avail_w += qty
                    revised.append(order)
            elif crop == "CARROT":
                allowed = max(0, max_c - avail_c)
                buy_qty = min(qty, allowed)
                cut = qty - buy_qty
                if cut > 0:
                    _ES_REPORT["orders_blocked"] += 1
                    _ES_REPORT["coins_saved_nominal"] += cut * 20
                    changed = True
                    if buy_qty > 0:
                        order[2] = buy_qty
                        avail_c += buy_qty
                        revised.append(order)
                    else:
                        revised.append([])
                else:
                    avail_c += qty
                    revised.append(order)
            else:
                _ES_REPORT["orders_blocked"] += 1
                _ES_REPORT["coins_saved_nominal"] += qty * _ES_SEED_COST.get(crop, 50)
                changed = True
                revised.append([])
        else:
            revised.append(order)
    return dict(action, market=revised) if changed else action


def agent(observation, configuration=None):
    if int(observation.get("step", 0)) == 0:
        for key in _ES_REPORT:
            _ES_REPORT[key] = 0
    action = _ES_PARENT(observation, configuration)
    try:
        action = _es_cut_dead_seed_buys(observation, configuration, action)
    except Exception:
        _ES_REPORT["errors"] += 1
    return action


agent.telemetry = _ES_REPORT
agent = globals().pop("agent")





# ==============================================================================
# JFJH-v10: Day 27-28 Marginal Economic Feed Protection & Wheat Liquidity Liberation
# ==============================================================================
_V10_FEED_MODE = "combined"  # 'as_is', 'combined', 'conservative'
_V9_WHEAT_MODE = "combined"
_V10_REPORT = {
    "econ_feed_cuts_day27": 0,
    "econ_feed_cuts_day28": 0,
    "pickup_trims": 0,
    "pickup_trimmed_units": 0,
    "v10_errors": 0,
}

_V9_ANIMAL_PRODUCTS = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}

def _v10_should_feed_animal(tile, day, prices):
    an = tile.get("animal")
    if an not in _FEED_ANIMAL_DAYS:
        return True
    first, interval = _FEED_ANIMAL_DAYS[an]
    first += int(tile.get("placed_day", 0))
    prod_day29 = (29 >= first and (29 - first) % interval == 0)
    unfed = int(tile.get("consecutive_unfed", 0))
    bonus = int(tile.get("pending_care_bonus", 0)) if prod_day29 else 0
    if day == 28:
        if unfed == 0:
            marginal_units = bonus
        else:
            marginal_units = (1 + bonus) if prod_day29 else 0
        item = _V9_ANIMAL_PRODUCTS.get(an)
        rev = marginal_units * float(prices.get(item, 0))
        cost = float(prices.get("WHEAT", 0))
        return rev >= cost
    if day == 27:
        if _V10_FEED_MODE == "as_is":
            return True
        item = _V9_ANIMAL_PRODUCTS.get(an)
        p_prod = float(prices.get(item, 0))
        p_wheat = float(prices.get("WHEAT", 0))
        if _V10_FEED_MODE == "conservative":
            if an == "SHEEP" and p_prod <= 5.0 and p_wheat >= 20.0:
                return False
            return True
        if 3.0 * p_prod < p_wheat:
            return False
        return True
    return True

_V10_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}

def _v9_count_surviving_feeds(obs, actor, start_step):
    player = int(obs["player"])
    native = _IMPL.chassis.players[player]
    route_id = 2 if start_step >= 648 else native["route"]
    route = _IMPL.chassis.routes[route_id]
    farm = obs["farms"][player]
    day = start_step // 24
    end_step = day * 24 + 23
    pos = list(farm["farmer"] if actor == 0 else farm["hands"][actor - 1])
    p = obs["market"]["prices"]
    valid_feeds = 0
    for t in range(start_step, end_step + 1):
        a_t = route[t]
        cmds = [a_t.get("farmer") or ["PASS"]] + list(a_t.get("hands") or [])
        if actor >= len(cmds):
            break
        c = cmds[actor]
        if not c:
            continue
        op = c[0]
        if op in _V10_MOVES:
            dx, dy = _V10_MOVES[op]
            pos[0] += dx
            pos[1] += dy
        elif op == "FEED":
            if 0 <= pos[1] < len(farm["tiles"]) and 0 <= pos[0] < len(farm["tiles"][0]):
                tile = farm["tiles"][pos[1]][pos[0]]
                if isinstance(tile, dict) and "animal" in tile:
                    if _v10_should_feed_animal(tile, day, p):
                        valid_feeds += 1
    return valid_feeds

def _v10_process_action(obs, action):
    if _V10_FEED_MODE == "as_is" and _V9_WHEAT_MODE == "as_is":
        return action
    step = int(obs.get("step", 0))
    day = step // 24
    if day not in (27, 28):
        return action
    farm = obs["farms"][int(obs["player"])]
    positions = [farm["farmer"]] + list(farm["hands"])
    prices = obs["market"]["prices"]
    cmds = [list(action.get("farmer") or ["PASS"])] + [list(c) for c in (action.get("hands") or [])]
    changed = False

    # 1. Dynamic wheat pickup trimming (day 28 only)
    if day == 28 and _V9_WHEAT_MODE in ("combined", "trim_only"):
        for a, c in enumerate(cmds):
            if c and len(c) >= 2 and c[0] == "PICKUP" and c[1] == "WHEAT":
                req_qty = int(c[2]) if len(c) > 2 else 1
                surviving = _v9_count_surviving_feeds(obs, a, step)
                needed = min(req_qty, surviving)
                if needed <= 0:
                    cmds[a] = ["PASS"]
                    changed = True
                    _V10_REPORT["pickup_trims"] += 1
                    _V10_REPORT["pickup_trimmed_units"] += req_qty
                elif needed < req_qty:
                    cmds[a] = ["PICKUP", "WHEAT", needed]
                    changed = True
                    _V10_REPORT["pickup_trims"] += 1
                    _V10_REPORT["pickup_trimmed_units"] += (req_qty - needed)

    # 2. Marginal economic feed gate (both day 27 and day 28)
    for a, cmd in enumerate(cmds):
        if cmd == ["FEED"] and a < len(positions):
            pos = positions[a]
            if 0 <= pos[1] < len(farm["tiles"]) and 0 <= pos[0] < len(farm["tiles"][0]):
                t = farm["tiles"][pos[1]][pos[0]]
                if isinstance(t, dict) and "animal" in t:
                    if not _v10_should_feed_animal(t, day, prices):
                        cmds[a] = ["PASS"]
                        changed = True
                        if day == 27:
                            _V10_REPORT["econ_feed_cuts_day27"] += 1
                        else:
                            _V10_REPORT["econ_feed_cuts_day28"] += 1

    if changed:
        return dict(action, farmer=cmds[0], hands=cmds[1:])
    return action

_V10_PARENT = agent
def agent(observation, configuration=None):
    if int(observation.get("step", 0)) == 0:
        for k in _V10_REPORT:
            _V10_REPORT[k] = 0
    action = _V10_PARENT(observation, configuration)
    try:
        action = _v10_process_action(observation, action)
    except Exception:
        _V10_REPORT["v10_errors"] += 1
    return action
agent.telemetry = _V10_REPORT
agent = globals().pop("agent")


# Final Action Execution Ledger & Output Harmonizer
_LEDGER_REPORT = {
    "own_sales_pollutions_corrected": 0,
    "pollution_diff_units": 0,
    "step91_slot_preservations": 0,
    "ledger_errors": 0
}

_PG_T_PARENT = agent
_PG_T_THRESHOLD = 31

def _ledger_reconcile_exit(observation, action):
    """Ensure _V9_RACE's observation memory uses the TRUE emitted orders instead of inner estimates."""
    player = int(observation.get("player", 0))
    step = int(observation.get("step", 0))
    st = _V9_RACE.get(player)
    if st and st.get("prev") and st["prev"].get("step") == step:
        try:
            stock = projected_shed(action, FarmView(observation))
            actual_own = {}
            for o in action.get("market") or []:
                if o and len(o) >= 3 and o[0] == "SELL" and o[1] in V9_RACE_ITEMS:
                    n = min(max(0, int(o[2])), max(0, stock.get(o[1], 0) - actual_own.get(o[1], 0)))
                    actual_own[o[1]] = actual_own.get(o[1], 0) + n
            old_own = st["prev"].get("own") or {}
            for item in V9_RACE_ITEMS:
                diff = actual_own.get(item, 0) - old_own.get(item, 0)
                if diff != 0:
                    _LEDGER_REPORT["own_sales_pollutions_corrected"] += 1
                    _LEDGER_REPORT["pollution_diff_units"] += abs(diff)
            st["prev"]["own"] = actual_own
            st["prev"]["left"] = {item: stock.get(item, 0) - actual_own.get(item, 0) for item in V9_RACE_ITEMS}
        except Exception:
            _LEDGER_REPORT["ledger_errors"] += 1

# Embedded into the frozen V10 final-action interface; no second policy call.
_CR_STATE={}
_CR_TRACE={}
_CR_REPORT={'hire_shortfalls':0,'jobs_started':0,'jobs_completed':0,'feeds_confirmed':0,
    'cares_confirmed':0,'fert_collected':0,'fert_sold':0,'wheat_borrowed':0,'wheat_repaid':0,
    'structures_restored':0,'receipt_errors':0,'deadline_jobs':0,'changed_field_commands':0,'changed_market_turns':0,'errors':0}

def _cr_preview(obs,action):
    f=copy.deepcopy(obs['farms'][int(obs['player'])]);p=copy.deepcopy(obs['private'])
    commands=[action.get('farmer',['PASS']),*action.get('hands',[])]
    need={}
    for cmd in commands:
        if len(cmd)>1 and cmd[0]=='PLANT':need[cmd[1]]=need.get(cmd[1],0)+1
    blocked={item for item,n in need.items() if n>p['seeds'].get(item,0)}
    for actor,cmd in enumerate(commands[:len(p['inventories'])]):
        effective=['PASS'] if len(cmd)>1 and cmd[0]=='PLANT' and cmd[1] in blocked else cmd
        _UNIT_NS['_apply_unit_action'](f,p,actor,effective,10,int(obs['step'])//24,24,100)
    return f,p

def _cr_observe(obs,ctx):
    pending=ctx.pop('pending',None)
    if not pending:return
    step=int(obs['step']);seat=int(obs['player']);farm=obs['farms'][seat];private=obs['private']
    if step!=pending['step']+1:_CR_REPORT['receipt_errors']+=1;return
    same_day=step//24==pending['step']//24
    if same_day and pending['hires']:
        actual=max(0,len(farm['hands'])-pending['hands'])
        missing=max(0,pending['hires']-actual);ctx['shortfall']+=missing;_CR_REPORT['hire_shortfalls']+=missing
    deposited=0
    for actor,entry in pending['jobs'].items():
        if not same_day and entry['task'] and entry['command'][0] in ('BUILD_PASTURE','BUILD_COOP'):
            pos=entry['task_position'];tile=farm['tiles'][pos[1]][pos[0]]
            expected='PASTURE' if entry['command'][0]=='BUILD_PASTURE' else 'COOP'
            if isinstance(tile,dict) and tile.get('kind')==expected:
                job=ctx['jobs'][actor];job['cursor']+=1;_CR_REPORT['structures_restored']+=1
                if job['cursor']==len(job['tasks']):_CR_REPORT['jobs_completed']+=1
            else:_CR_REPORT['receipt_errors']+=1
            continue
        if not same_day or actor>=len(private['inventories']):_CR_REPORT['receipt_errors']+=1;continue
        actual_pos=[farm['farmer'],*farm['hands']][actor]
        if list(actual_pos)!=entry['expected_pos'] or private['inventories'][actor]!=entry['expected_inventory']:
            _CR_REPORT['receipt_errors']+=1;continue
        if not entry['task']:continue
        job=ctx['jobs'][actor];cmd=entry['command'];op=cmd[0];pos=entry['task_position'];tile=farm['tiles'][pos[1]][pos[0]]
        ok=True
        if op=='FEED':
            used=entry['before_inventory'].get('WHEAT',0)-private['inventories'][actor].get('WHEAT',0)
            ok=isinstance(tile,dict) and tile.get('fed_today',False)
            if ok:ctx['loan']+=max(0,used);_CR_REPORT['wheat_borrowed']+=max(0,used);_CR_REPORT['feeds_confirmed']+=int(used>0)
        elif op=='CARE':
            ok=isinstance(tile,dict) and tile.get('cared_today',False)
            if ok:_CR_REPORT['cares_confirmed']+=1
        elif op=='COLLECT_FERTILIZER':
            gained=private['inventories'][actor].get('FERTILIZER',0)-entry['before_inventory'].get('FERTILIZER',0)
            ok=gained==1
            if ok:job['fert']+=1;_CR_REPORT['fert_collected']+=1
        elif op=='PLACE':
            moved=entry['before_inventory'].get('FERTILIZER',0)-private['inventories'][actor].get('FERTILIZER',0)
            ok=moved==cmd[2] and job['fert']>=moved
            if ok:deposited+=moved;job['fert']-=moved
        elif op=='PICKUP':
            ok=private['inventories'][actor].get('WHEAT',0)-entry['before_inventory'].get('WHEAT',0)>=cmd[2]
        elif op in ('BUILD_PASTURE','BUILD_COOP'):
            ok=isinstance(tile,dict) and tile.get('kind')==('PASTURE' if op=='BUILD_PASTURE' else 'COOP')
            if ok:_CR_REPORT['structures_restored']+=1
        if ok:
            job['cursor']+=1
            if job['cursor']==len(job['tasks']):_CR_REPORT['jobs_completed']+=1
        else:_CR_REPORT['receipt_errors']+=1
    if same_day:
        budget=pending['credit']+deposited
        sold=max(0,pending['field_fert']-private['shed'].get('FERTILIZER',0))
        parent_filled=min(pending['parent_fert_sell'],sold)
        parent_owned=max(0,parent_filled-max(0,pending['field_fert']-budget))
        own_filled=min(pending['own_fert_sell'],max(0,sold-parent_filled),max(0,budget-parent_owned))
        ctx['credit']=max(0,budget-parent_owned-own_filled);_CR_REPORT['fert_sold']+=parent_owned+own_filled
        if pending['wheat_buy']:
            expected=max(0,pending['field_wheat']-pending['parent_wheat_sell'])
            actual=min(pending['wheat_buy'],max(0,private['shed'].get('WHEAT',0)-expected))
            ctx['loan']=max(0,ctx['loan']-actual);_CR_REPORT['wheat_repaid']+=actual
            if actual!=pending['wheat_buy']:_CR_REPORT['receipt_errors']+=1
    elif pending['own_fert_sell'] or pending['wheat_buy'] or deposited:
        _CR_REPORT['receipt_errors']+=1

def _cr_walk(position,target):
    if position[0]<target[0]:return ['EAST']
    if position[0]>target[0]:return ['WEST']
    if position[1]<target[1]:return ['SOUTH']
    if position[1]>target[1]:return ['NORTH']
    return None

def _cr_safe_window(obs,action):
    step=int(obs['step']);seat=int(obs['player']);count=1+len(obs['farms'][seat]['hands'])
    native=_IMPL.chassis.players.get(seat,{})
    if any(native.get('pending',{}).get(a) for a in range(count)):return False
    for t in range(step,(step//24+1)*24):
        raw=action if t==step else _ca_tape(seat,t)
        units=[raw.get('farmer',['PASS']),*raw.get('hands',[])]
        if any(a<len(units) and units[a]!=['PASS'] for a in range(count)):return False
        for order in raw.get('market',[]):
            if order and (order[0]!='SELL' or len(order)>1 and order[1]=='WHEAT'):return False
    return True

def _cr_due_work(obs):
    # Read planned obligations from our own program, not future replay actions.
    # Virtual hired positions identify the intended missing work; execution
    # still uses only the actually hired actor and observed empty target.
    positions=[[4,4]];seat=int(obs['player']);step=int(obs['step']);builds={};cares={};feeds={}
    for t in range(step//24*24,step+1):
        raw=_ca_tape(seat,t);commands=[raw.get('farmer',['PASS']),*raw.get('hands',[])]
        for a,at in enumerate(positions):
            cmd=commands[a] if a<len(commands) else ['PASS']
            if cmd[0] in ('BUILD_PASTURE','BUILD_COOP'):builds[tuple(at)]=(cmd[0],t)
            if cmd[0]=='CARE':cares[tuple(at)]=t
            if cmd[0]=='FEED':feeds[tuple(at)]=t
            if cmd[0] in _CA_MOVES:
                dx,dy=_CA_MOVES[cmd[0]];positions[a]=[max(0,min(9,at[0]+dx)),max(0,min(9,at[1]+dy))]
        for order in raw.get('market',[]):
            if order==['HIRE']:positions.append(_ca_spawn(positions,10))
    return builds,cares,feeds

def _cr_proposals(obs,ctx,actor):
    farm=obs['farms'][int(obs['player'])];pos=[farm['farmer'],*farm['hands']][actor]
    inv=obs['private']['inventories'][actor];access=((4,4),(5,4),(4,5),(5,5));hour=int(obs['step'])%24
    params=_v44y_params(obs)
    wheat_ceiling=_v44y_price('WHEAT',obs['market']['inventory']['WHEAT']-101,params)
    reserved=sum(sum(task['command'][2] for task in j['tasks'][j['cursor']:] if task['command'][:2]==['PICKUP','WHEAT']) for j in ctx['jobs'].values())
    reserved_feed=sum(sum(task['command'][0]=='FEED' for task in j['tasks'][j['cursor']:]) for j in ctx['jobs'].values())
    available=max(0,obs['private']['shed'].get('WHEAT',0)-reserved)
    proposals=[]
    builds,cares,feeds=_cr_due_work(obs)
    for y,row in enumerate(farm['tiles']):
        for x,tile in enumerate(row):
            target=(x,y)
            if target in ctx['claimed'] or not isinstance(tile,dict) or 'animal' not in tile or not tile.get('fertilizer_available'):continue
            urgent=tile.get('consecutive_unfed',0)>0 and not tile.get('fed_today')
            tasks=[]
            needs_feed=not tile.get('fed_today') and (urgent or target in feeds)
            if needs_feed:
                if farm['money']<wheat_ceiling*(ctx['loan']+reserved_feed+1) or available+inv.get('WHEAT',0)<1:continue
                if not inv.get('WHEAT',0):
                    home=min(access,key=lambda p:abs(p[0]-pos[0])+abs(p[1]-pos[1])+abs(p[0]-x)+abs(p[1]-y))
                    tasks.append(dict(position=list(home),command=['PICKUP','WHEAT',1]))
                tasks.append(dict(position=[x,y],command=['FEED']))
                if not tile.get('cared_today'):tasks.append(dict(position=[x,y],command=['CARE']))
            if not needs_feed and target in cares and not tile.get('cared_today'):
                tasks.append(dict(position=[x,y],command=['CARE'],source_step=cares[target]))
            tasks.append(dict(position=[x,y],command=['COLLECT_FERTILIZER']))
            home=min(access,key=lambda p:abs(p[0]-x)+abs(p[1]-y))
            tasks.append(dict(position=list(home),command=['PLACE','FERTILIZER',1]))
            cost=0;at=pos
            for job in tasks:
                q=job['position'];cost+=abs(at[0]-q[0])+abs(at[1]-q[1])+1;at=q
            # Deposit and sale may finish by hour22: next hour23 receipt still
            # precedes dawn. All feed loans reserve actual repayment cash.
            if hour+cost-1>22:continue
            proposals.append((not urgent,cost,target,tasks))
    for target,(op,source_step) in builds.items():
        x,y=target;tile=farm['tiles'][y][x]
        if target in ctx['claimed'] or not(tile is None or isinstance(tile,dict) and tile.get('kind')=='WEED'):continue
        tasks=[]
        if tile is not None:tasks.append(dict(position=[x,y],command=['DIG']))
        tasks.append(dict(position=[x,y],command=[op],source_step=source_step))
        cost=abs(pos[0]-x)+abs(pos[1]-y)+len(tasks)
        if hour+cost-1<=23:proposals.append((2,cost,target,tasks))
    return sorted(proposals,key=lambda p:p[:3])

def _cr_recover(observation,configuration,action):
    obs=observation;step=int(obs['step']);seat=int(obs['player']);day=step//24
    _CR_TRACE.clear()
    if step==0:
        for key in _CR_REPORT:_CR_REPORT[key]=0
        _CR_STATE[seat]=dict(day=0,shortfall=0,jobs={},claimed=set(),loan=0,credit=0,pending=None)
    ctx=_CR_STATE.setdefault(seat,dict(day=day,shortfall=0,jobs={},claimed=set(),loan=0,credit=0,pending=None))
    _cr_observe(obs,ctx)
    if ctx['day']!=day:
        _CR_REPORT['deadline_jobs']+=sum(j['cursor']<len(j['tasks']) for j in ctx['jobs'].values())+int(ctx['loan']>0 or ctx['credit']>0)
        ctx.update(day=day,shortfall=0,jobs={},claimed=set())
    cfg=configuration or {}
    allowed=_ow_standard(configuration) and not cfg.get('marketParams',{}) and cfg.get('startingMoney',3000)==3000
    farm=obs['farms'][seat];positions=[farm['farmer'],*farm['hands']]
    original=copy.deepcopy(action);units=copy.deepcopy([action.get('farmer',['PASS']),*action.get('hands',[])])
    if allowed and day in (1,2) and ctx['shortfall'] and _cr_safe_window(obs,action):
        for actor in range(len(positions)):
            if actor in ctx['jobs'] and ctx['jobs'][actor]['cursor']<len(ctx['jobs'][actor]['tasks']):continue
            options=_cr_proposals(obs,ctx,actor)
            if options:
                _,_,target,tasks=options[0];ctx['jobs'][actor]=dict(tasks=tasks,cursor=0,fert=0)
                ctx['claimed'].add(target);_CR_REPORT['jobs_started']+=1
                _CR_TRACE.setdefault('approved_recovery_jobs',[]).append(dict(actor=actor,target=list(target),tasks=copy.deepcopy(tasks),deadline=(day+1)*24,actual_hire_shortfall=ctx['shortfall']))
    issued={}
    for actor,job in ctx['jobs'].items():
        if actor>=len(units):_CR_REPORT['receipt_errors']+=1;continue
        if job['cursor']>=len(job['tasks']):units[actor]=['PASS'];continue
        task=job['tasks'][job['cursor']];move=_cr_walk(positions[actor],task['position'])
        units[actor]=move or list(task['command'])
        issued[actor]=dict(command=units[actor],task=move is None,task_position=task['position'],before_inventory=dict(obs['private']['inventories'][actor]))
    result=dict(action,farmer=units[0],hands=units[1:]);field,private=_cr_preview(obs,result)
    predicted_deposit=0
    for actor,entry in issued.items():
        entry['expected_pos']=list([field['farmer'],*field['hands']][actor]);entry['expected_inventory']=dict(private['inventories'][actor])
        if entry['task'] and entry['command'][:2]==['PLACE','FERTILIZER']:
            predicted_deposit+=max(0,entry['before_inventory'].get('FERTILIZER',0)-entry['expected_inventory'].get('FERTILIZER',0))
    orders=copy.deepcopy(action.get('market',[]));parent_fert=sum(o[2] for o in orders if len(o)>=3 and o[:2]==['SELL','FERTILIZER'])
    parent_wheat=sum(o[2] for o in orders if len(o)>=3 and o[:2]==['SELL','WHEAT'])
    credit=ctx['credit']+predicted_deposit;stock=private['shed'].get('FERTILIZER',0)
    parent_owned=max(0,min(parent_fert,stock)-max(0,stock-credit))
    sale=min(max(0,credit-parent_owned),max(0,stock-parent_fert))
    if sale and len(orders)<10 and step%24<23:orders.append(['SELL','FERTILIZER',sale])
    else:sale=0
    buy=0
    if ctx['loan'] and step%24<23 and len(orders)<10 and all(not o or o[0]=='SELL' for o in orders):
        quote=_v44y_price('WHEAT',obs['market']['inventory']['WHEAT']-100-ctx['loan'],_v44y_params(obs))
        if farm['money']>=quote*ctx['loan']:
            buy=ctx['loan'];orders.append(['BUY_PRODUCT','WHEAT',buy])
    result['market']=orders
    _CR_REPORT['changed_field_commands']+=sum(a!=b for a,b in zip(units,[original.get('farmer',['PASS']),*original.get('hands',[])]))
    _CR_REPORT['changed_market_turns']+=int(orders!=original.get('market',[]))
    ctx['pending']=dict(step=step,hands=len(farm['hands']),hires=sum(o==['HIRE'] for o in orders),jobs=issued,
        credit=ctx['credit'],field_fert=stock,field_wheat=private['shed'].get('WHEAT',0),parent_fert_sell=parent_fert,
        parent_wheat_sell=parent_wheat,own_fert_sell=sale,wheat_buy=buy)
    return result



# SPDX-License-Identifier: Apache-2.0
# JFJH-V18: Flexon94 (cha22) sale-timing layers at the V10 parent boundary.
# Ported from the public notebook flexonafft/kaggriculture-multi-route-farming-agent
# (version 94, Apache-2.0; https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent),
# main.py SHA256 127ed3e62988c0474d386db6527ae8ca9de9bb1fe7004128557ddef67126c652.
# Ported decision rules, parameters unchanged: ADV ready-stock advancing, T62A
# terminal liquidation, EV/DP/MP evening/dawn/midday chunked lead-sells over the
# quote history, MPX rival-cadence lead-sell, MG same-item merge, IG queue hole
# closure; applied in Flexon's chain order. Not ported: PIPE16, WB3, BD, SM, CXD,
# E410, E402 (opening, buy, funding, ordering-search and input guards).
# Deviations: (1) T62A sizes each sale from the projected shed after this turn's
# unit actions (Flexon reads the pre-action shed, so same-turn deposits at step 718
# were never sold); (2) every ledger that infers rival sales from our own orders
# sees the emitted orders: V9_RACE by the existing V10 exit reconcile, OR2 by the
# executed-unit delta of these layers, RACE prev_action replaced as ADV does.
_V18_FX_ITEMS = ("CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL")
_V18_QUOTE_WIN = 12
_V18_MIN_STEP = 96
_V18_ADV_LOOK = 5
_V18_ADV_FROM = 216
_V18_ADV_TO = 718
_V18_ADV_ITEMS = ('STRAWBERRY', 'WOOL', 'EGG', 'MILK', 'MELON', 'CARROT', 'TOMATO')
_V18_WINDOWS = (('dp', (0, 1, 2), 10), ('mp', (10, 11, 12, 13), 10), ('ev', (15, 16, 17, 18, 19, 20), 10))
_V18_MPX_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
_V18_MPX_HOURS = tuple(range(12, 23))
_V18_STATE = {}
_V18_REPORT = dict(adv_turns=0, adv_units=0, term_sells=0, term_units=0,
                   ev_fires=0, ev_units=0, dp_fires=0, dp_units=0, mp_fires=0, mp_units=0,
                   mpx_fires=0, mpx_units=0, mg_turns=0, mg_merged=0,
                   ig_turns=0, ig_zeroed=0, ig_pulled=0, changed_turns=0,
                   or2_ledger_updates=0, race_ledger_updates=0, errors=0, last_error='')


def _v18_standard(configuration):
    return configuration is None or all(configuration.get(k, v) == v for k, v in
        [('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100), ('maxMarketOrdersPerTurn', 10)])


def _v18_tape(player):
    native = _IMPL.chassis.players.get(player)
    if not native or native.get('route') not in _IMPL.chassis.routes:
        return None
    return _IMPL.chassis.routes[native['route']]


def _v18_adv(obs, action, st):
    # Flexon _adv_apply with _ADV_PROTECT=True, _ADV_BOOK=False, _ADV_SUBTRACT_DEBTS=True.
    step = int(obs['step']); player = int(obs['player'])
    if step % 24 == 23 or not _V18_ADV_FROM <= step < _V18_ADV_TO: return action
    native = _IMPL.chassis.players.get(player)
    if not native: return action
    debts = native.setdefault('sell_state', {}).setdefault('r36_debts', {})
    plan = []; first = None
    for off in range(1, _V18_ADV_LOOK + 1):
        t = step + off
        if t > 718: break
        route = 2 if t >= 648 else native.get('route', 0)
        for o in _IMPL.chassis.routes[route][t].get('market', []) or []:
            if not o or len(o) < 3: continue
            if first is None: first = o
            if o[0] == 'SELL' and o[1] in _V18_ADV_ITEMS:
                try: q = max(0, int(o[2]))
                except Exception: q = 0
                q -= debts.get(t, {}).get(o[1], 0)
                if q > 0: plan.append((t, o[1], q))
    protected = first[1] if first is not None and first[0] == 'SELL' else None
    plan = [(t, item, q) for t, item, q in plan if item != protected]
    if not plan: return action
    market = [list(o) for o in (action.get('market') or [])]
    if any(len(o) > 1 and o[0] == 'BUY_PRODUCT' for o in market): return action
    stock = projected_shed(action, FarmView(obs))
    selling = {}
    for o in market:
        if len(o) >= 3 and o[0] == 'SELL':
            try: selling[o[1]] = selling.get(o[1], 0) + max(0, int(o[2]))
            except Exception: return action
    commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    picked = {c[1] for c in commands if len(c) > 1 and c[0] == 'PICKUP'}
    prices = obs['market']['prices']; added = 0; extra = []
    for item in sorted({it for _, it, _ in plan}, key=lambda it: -int(prices.get(it, 0))):
        if item in picked or int(prices.get(item, 0)) < 2: continue
        avail = int(stock.get(item, 0)) - selling.get(item, 0)
        if avail < 1: continue
        hit = next((o for o in market if len(o) >= 3 and o[0] == 'SELL' and o[1] == item), None)
        if hit is None and len(market) + len(extra) >= 10: continue
        n = 0
        for t, it, q in plan:
            if it != item or avail <= 0: continue
            take = min(q, avail); n += take; avail -= take
        if n < 1: continue
        if hit is not None: hit[2] = int(hit[2]) + n
        else: extra.append(['SELL', item, n])
        added += n
    if not added: return action
    _V18_REPORT['adv_turns'] += 1; _V18_REPORT['adv_units'] += added
    return dict(action, market=extra + market)


def _v18_t62a(obs, action, st):
    # Flexon T62A: from step 712 the market is replaced by full sales, dearest first.
    step = int(obs['step'])
    if step < 712: return action
    prices = obs['market']['prices']
    stock = projected_shed(action, FarmView(obs))
    items = [it for it, q in stock.items() if int(q) > 0 and int(prices.get(it, 0)) >= 1]
    if not items: return action
    items.sort(key=lambda it: -int(prices.get(it, 0)))
    market = [['SELL', it, int(stock[it])] for it in items[:10]]
    _V18_REPORT['term_sells'] += 1
    _V18_REPORT['term_units'] += sum(o[2] for o in market)
    return dict(action, market=market)


def _v18_window(obs, action, st, name, hours, horizon):
    # Flexon _ev_apply / _dp_apply / _mp_apply (identical bodies, disjoint hours).
    step = int(obs['step'])
    if step < _V18_MIN_STEP or step >= 700 or (step % 24) not in hours: return action
    market = [list(o) for o in (action.get('market') or [])]
    if len(market) >= MAX_ORDERS: return action
    already = {o[1] for o in market if len(o) > 1 and o[0] in ('SELL', 'BUY_PRODUCT')}
    prices = obs['market']['prices']
    stock = projected_shed(action, FarmView(obs))
    tape = _v18_tape(int(obs['player']))
    if tape is None: return action
    hist = st['quotes']
    recent = [t for t in hist if step - _V18_QUOTE_WIN <= t < step]
    added = False
    for item in _V18_FX_ITEMS:
        if item in already or len(market) >= MAX_ORDERS: continue
        q = int(prices.get(item, 0))
        if q <= 3: continue
        vals = [hist[t].get(item, 0) for t in recent if hist[t].get(item, 0) > 0]
        if vals and q < sum(vals) / len(vals): continue
        planned = 0
        for t in range(step + 1, min(len(tape), step + horizon + 1)):
            for o in (tape[t] or {}).get('market') or []:
                if len(o) >= 3 and o[0] == 'SELL' and o[1] == item:
                    planned += max(0, int(o[2]))
        if planned <= 0: continue
        qty = min(int(stock.get(item, 0)), max(1, (3 * planned + 3) // 4))
        if qty <= 0: continue
        market.insert(0, ['SELL', item, qty])
        _V18_REPORT[name + '_fires'] += 1; _V18_REPORT[name + '_units'] += qty
        added = True
    if not added: return action
    return dict(action, market=market[:MAX_ORDERS])


def _v18_mpx_draw(step):
    draw = 0
    if step % 4 == 0: draw += 1
    if step % 24 == 0: draw += 1
    return draw


def _v18_mpx(obs, action, st):
    # Flexon _mpx_apply: rival cadence from public inventory deltas, one-step price model.
    step = int(obs['step'])
    if step < 144 or step >= 696 or (step % 24) not in _V18_MPX_HOURS: return action
    player = int(obs['player'])
    inv_all = obs['market'].get('inventory') or {}
    prices = obs['market'].get('prices') or {}
    hist = st['mpx']
    prev = hist.get('prev')
    inv_now = {i: int(inv_all.get(i, 0)) for i in _V18_MPX_ITEMS}
    if prev and prev['step'] == step - 1:
        for i in _V18_MPX_ITEMS:
            d = inv_now[i] - prev['inv'][i] + _v18_mpx_draw(step - 1) - prev['own'].get(i, 0)
            hist.setdefault(i, []).append(max(0, d))
            if len(hist[i]) > 12: del hist[i][:6]
    hist['prev'] = {'step': step, 'inv': inv_now, 'own': {}}
    market_orders = [list(o) for o in (action.get('market') or [])]
    for o in market_orders:
        if len(o) >= 3 and o[0] == 'SELL' and o[1] in _V18_MPX_ITEMS:
            hist['prev']['own'][o[1]] = hist['prev']['own'].get(o[1], 0) + int(o[2])
    already = {o[1] for o in market_orders if len(o) > 1 and o[0] == 'SELL'}
    if _v18_tape(player) is None: return action
    stock = projected_shed(action, FarmView(obs))
    added = False
    for item in _V18_MPX_ITEMS:
        if item in already or len(market_orders) >= 10: continue
        avail = int(stock.get(item, 0))
        if avail <= 0: continue
        if int(prices.get(item, 0)) <= 1: continue
        rival = hist.get(item) or []
        rival_avg = (sum(rival[-4:]) / len(rival[-4:])) if rival else 0.0
        planned = 6
        try:
            inv = int(inv_all.get(item, 0))
            p_cur = float(_r37_market_price(item, inv))
            inv_next = inv + rival_avg + planned - _v18_mpx_draw(step)
            p_next = float(_r37_market_price(item, max(0, int(inv_next))))
        except Exception:
            continue
        if p_next < p_cur - 0.5:
            take = min(avail, max(1, planned // 2))
            market_orders.insert(0, ['SELL', item, take])
            _V18_REPORT['mpx_fires'] += 1; _V18_REPORT['mpx_units'] += take
            hist['prev']['own'][item] = hist['prev']['own'].get(item, 0) + take
            added = True
    if not added: return action
    return dict(action, market=market_orders[:10])


def _v18_mg(obs, action, st):
    # Flexon MERGE (E334): same (order, item) SELL/BUY_PRODUCT/BUY_SEED compaction.
    market = [list(o) for o in (action.get('market') or [])]
    if len(market) < 2: return action
    seen = {}; out = []; changed = False
    for o in market:
        if o and len(o) >= 3 and o[0] in ('SELL', 'BUY_PRODUCT', 'BUY_SEED'):
            key = (o[0], o[1])
            if key in seen:
                out[seen[key]][2] = int(out[seen[key]][2]) + int(o[2]); changed = True
                continue
            seen[key] = len(out)
        out.append(o)
    if not changed: return action
    _V18_REPORT['mg_turns'] += 1; _V18_REPORT['mg_merged'] += len(market) - len(out)
    return dict(action, market=out)


def _v18_ig(obs, action, st):
    # Flexon IG queue hole-closure (same rule as the V10 OW close queue, applied last).
    market = action.get('market') or []
    if len(market) < 2: return action
    projected = dict(projected_shed(action, FarmView(obs)))
    remaining = {item: max(0, int(projected.get(item, 0))) for item in _V18_FX_ITEMS}
    revised = []; zeroed = 0
    for raw in market:
        order = list(raw) if isinstance(raw, (list, tuple)) else raw
        if isinstance(order, list) and len(order) >= 3 and order[0] == 'SELL' and order[1] in remaining:
            executed = min(max(0, int(order[2])), remaining[order[1]])
            remaining[order[1]] -= executed
            if executed <= 0:
                revised.append([]); zeroed += 1
            else:
                revised.append(order)
        else:
            revised.append(order)
    holes = []; pulled = 0
    for index, order in enumerate(revised):
        if not order:
            holes.append(index); continue
        movable = (isinstance(order, list) and len(order) >= 3 and order[0] == 'SELL'
                   and order[1] in remaining and int(order[2]) > 0)
        if not movable or not holes: continue
        target = holes.pop(0)
        revised[target] = order; revised[index] = []
        holes.append(index); pulled += 1
    if revised == market: return action
    _V18_REPORT['ig_turns'] += 1; _V18_REPORT['ig_zeroed'] += zeroed; _V18_REPORT['ig_pulled'] += pulled
    return dict(action, market=revised)


def _v18_executed(obs, action, items):
    stock = projected_shed(action, FarmView(obs)); own = {}
    for o in action.get('market') or []:
        if o and len(o) >= 3 and o[0] == 'SELL' and o[1] in items:
            n = min(max(0, int(o[2])), max(0, int(stock.get(o[1], 0)) - own.get(o[1], 0)))
            own[o[1]] = own.get(o[1], 0) + n
    return own


def _v18_sync_ledgers(obs, before, after):
    seat, step = int(obs['player']), int(obs['step'])
    st = _OR2_STATE.get(seat)
    prev = st.get('prev') if st else None
    if prev and prev.get('step') == step:
        old = _v18_executed(obs, before, _OR2_ITEMS); new = _v18_executed(obs, after, _OR2_ITEMS)
        own = prev.setdefault('own', {})
        for item in _OR2_ITEMS:
            diff = new.get(item, 0) - old.get(item, 0)
            if diff:
                own[item] = max(0, own.get(item, 0) + diff)
        _V18_REPORT['or2_ledger_updates'] += 1
    race = _RACE_STATE.get(seat)
    if race is not None and race.get('prev_action') is not None and race.get('step') == step:
        race['prev_action'] = after
        _V18_REPORT['race_ledger_updates'] += 1


_V18_LAYERS = (('adv', _v18_adv), ('t62a', _v18_t62a),
               ('ev', lambda o, a, s: _v18_window(o, a, s, *_V18_WINDOWS[2])),
               ('dp', lambda o, a, s: _v18_window(o, a, s, *_V18_WINDOWS[0])),
               ('mp', lambda o, a, s: _v18_window(o, a, s, *_V18_WINDOWS[1])),
               ('mpx', _v18_mpx), ('mg', _v18_mg), ('ig', _v18_ig))


def _v18_sales(observation, configuration, action):
    step = int(observation.get('step', 0)); player = int(observation.get('player', 0))
    if step == 0:
        for key in _V18_REPORT:
            _V18_REPORT[key] = '' if key == 'last_error' else 0
    if not isinstance(action, dict) or not _v18_standard(configuration):
        return action
    st = _V18_STATE.get(player)
    if st is None or step <= st['step']:
        st = _V18_STATE[player] = {'step': -1, 'quotes': {}, 'mpx': {}}
    st['step'] = step
    try:
        prices = observation['market']['prices']
        st['quotes'][step] = {i: int(prices.get(i, 0)) for i in _V18_FX_ITEMS}
        if len(st['quotes']) > 96:
            for k in sorted(st['quotes'])[:48]:
                st['quotes'].pop(k, None)
    except Exception as exc:
        _V18_REPORT['errors'] += 1; _V18_REPORT['last_error'] = 'quotes:' + repr(exc)[:160]
        return action
    out = action
    for name, layer in _V18_LAYERS:
        try:
            out = layer(observation, out, st)
        except Exception as exc:
            _V18_REPORT['errors'] += 1; _V18_REPORT['last_error'] = name + ':' + repr(exc)[:160]
    if out is not action and (out.get('market') or []) != (action.get('market') or []):
        _V18_REPORT['changed_turns'] += 1
        try:
            _v18_sync_ledgers(observation, action, out)
        except Exception as exc:
            _V18_REPORT['errors'] += 1; _V18_REPORT['last_error'] = 'ledger:' + repr(exc)[:160]
    return out



# SPDX-License-Identifier: Apache-2.0
# JFJH-V19: order-race layers added to the JFJH-V18 sale chain (after MPX, before MG/IG).
# (a) Wheat buy-first: from day 4, when this turn buys >= 12 WHEAT, sells no WHEAT and
#     cash covers every cost-bearing order, the BUY_PRODUCT WHEAT orders move to the front
#     of the queue. V10 keeps them behind a BUY_SEED or a preserved empty slot, while
#     same-lineage rivals often buy at index 0 and so pay less for the same units.
# (b) Safe CXD: exact lockstep best-response SELL ordering against a mirror of our own
#     queue, ported from the public notebook flexonafft/kaggriculture-multi-route-farming-agent
#     (version 94, Apache-2.0, main.py SHA256
#     127ed3e62988c0474d386db6527ae8ca9de9bb1fe7004128557ddef67126c652, layer F4 _cxd_reorder),
#     changed to run only from day 4, only when cash covers every cost-bearing order
#     plus $300 (the donor model ignores cash, so a HIRE could lose its funding sale),
#     and to let a sale take a preserved empty slot.
import itertools as _v19_it
_V19_FROM = 96
_V19_BUY_MIN = 12
_V19_BUDGET = 800
_V19_FIXED = ('HIRE', 'BUY_SEED', 'BUY_ANIMAL', 'BUY_LAND')
_V19_ANIMAL_COST = {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}
_V19_LAND_COST = (1000, 2000, 4000)
_V19_REPORT = dict(buy_first_turns=0, buy_first_units=0, cxd_turns=0, cxd_gain=0.0, cxd_evals=0,
                   cxd_budget_hits=0, cash_skips=0)


def _v19_cash_ok(obs, orders):
    farm = obs['farms'][int(obs['player'])]
    money = float(farm.get('money', 0) or 0)
    hires = int(farm.get('hires_today', 0) or 0)
    lands = len(farm.get('unlocked_quadrants') or [])
    prices = obs['market'].get('prices') or {}
    cost = 0.0
    for o in orders:
        if not isinstance(o, list) or not o:
            continue
        try:
            qty = max(0, int(o[2])) if len(o) >= 3 else 0
        except Exception:
            qty = 0
        if o[0] == 'HIRE':
            cost += _v219_fib(hires); hires += 1
        elif o[0] == 'BUY_LAND':
            cost += _V19_LAND_COST[lands - 1] if 1 <= lands <= 3 else 4000; lands += 1
        elif o[0] == 'BUY_SEED':
            cost += _ES_SEED_COST.get(o[1], 100) * qty
        elif o[0] == 'BUY_ANIMAL':
            cost += _V19_ANIMAL_COST.get(o[1], 500) * qty
        elif o[0] == 'BUY_PRODUCT':
            cost += (float(prices.get(o[1], 0) or 0) + 5.0) * 1.1 * qty
    return money >= cost + 300.0


def _v19_buy_first(obs, action, st):
    if int(obs['step']) < _V19_FROM:
        return action
    market = [list(o) if isinstance(o, (list, tuple)) else o for o in (action.get('market') or [])]
    idx = [i for i, o in enumerate(market) if isinstance(o, list) and len(o) >= 3 and o[:2] == ['BUY_PRODUCT', 'WHEAT']]
    if not idx or idx == list(range(len(idx))):
        return action
    if any(isinstance(o, list) and o[:2] == ['SELL', 'WHEAT'] for o in market):
        return action
    qty = sum(max(0, int(market[i][2])) for i in idx)
    if qty < _V19_BUY_MIN:
        return action
    if not _v19_cash_ok(obs, market):
        _V19_REPORT['cash_skips'] += 1
        return action
    moved = set(idx)
    _V19_REPORT['buy_first_turns'] += 1; _V19_REPORT['buy_first_units'] += qty
    return dict(action, market=[market[i] for i in idx] + [o for i, o in enumerate(market) if i not in moved])


def _v19_cxd(obs, action, st):
    if int(obs['step']) < _V19_FROM:
        return action
    market = action.get('market') or []
    if len(market) < 2:
        return action
    orders = [list(o) if isinstance(o, (list, tuple)) else o for o in market]
    bought = {o[1] for o in orders if isinstance(o, list) and len(o) > 1 and o[0] == 'BUY_PRODUCT'}
    slots, sells, fixed = [], [], []
    for i, o in enumerate(orders):
        if not o:
            slots.append(i); fixed.append(o)
        elif o[0] in _V19_FIXED:
            slots.append(i); fixed.append(o)
        elif o[0] == 'SELL' and len(o) > 1 and o[1] not in bought:
            slots.append(i); sells.append(o)
    if not sells or len(slots) < 2:
        return action
    if not _v19_cash_ok(obs, orders):
        _V19_REPORT['cash_skips'] += 1
        return action
    params = _v44y_params(obs)
    stock = {k: max(0, int(v)) for k, v in projected_shed(action, FarmView(obs)).items()}
    inv0 = {k: int(v) for k, v in obs['market']['inventory'].items()}
    margin = _v44y_factor_margin([o if o else [] for o in orders], inv0, stock, params)
    base = best = margin(orders)
    best_orders = None; evals = 0
    for positions in _v19_it.permutations(slots, len(sells)):
        cand = list(orders)
        rest = [i for i in slots if i not in positions]
        for i, o in zip(positions, sells):
            cand[i] = o
        for i, o in zip(rest, fixed):
            cand[i] = o
        if cand == orders:
            continue
        evals += 1
        if evals > _V19_BUDGET:
            _V19_REPORT['cxd_budget_hits'] += 1
            break
        value = margin(cand)
        if value > best + 0.5:
            best, best_orders = value, cand
    _V19_REPORT['cxd_evals'] += evals
    if best_orders is None:
        return action
    _V19_REPORT['cxd_turns'] += 1; _V19_REPORT['cxd_gain'] += best - base
    return dict(action, market=best_orders)


_V18_LAYERS = _V18_LAYERS[:6] + (('buyfirst', _v19_buy_first), ('cxd', _v19_cxd)) + _V18_LAYERS[6:]
_V19_BASE_SALES = _v18_sales


def _v18_sales(observation, configuration, action):
    if int(observation.get('step', 0)) == 0:
        for key in _V19_REPORT:
            _V19_REPORT[key] = 0.0 if key == 'cxd_gain' else 0
    return _V19_BASE_SALES(observation, configuration, action)



# SPDX-License-Identifier: Apache-2.0
# JFJH-V21h: six-sheep (V233) crew order. Adapted from JFJH-V20 (_v20_base_worker):
# setup, FEED, CARE and HARVEST first; carried wool is delivered next; fertilizer
# rounds come last. V20 lost about three fertilizer per wool day because the
# inherited end-of-day rule sent workers home with fertilizer cargo from hour
# 23-distance. Carried items are banked automatically at day end, so here only
# wool triggers the end-of-day walk home; fertilizer collection continues to the
# last hour. Day 28/29 and the compact one-worker days keep the V19 behaviour.
_V21H_REPORT = dict(wool_first=0, late_collect=0)


def _v21h_base_worker(obs, actor, targets):
    farm=obs['farms'][obs['player']];private=obs['private'];step=int(obs['step'])
    pos=tuple(farm['hands'][actor-1]);inv=private['inventories'][actor]
    access=((4,4),(5,4),(4,5),(5,5))
    home=min(access,key=lambda p:(abs(pos[0]-p[0])+abs(pos[1]-p[1]),p))
    distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    if inv.get('WOOL',0) and step%24 >= (22 if step//24==29 else 23)-distance:
        return _v219_walk(pos,home) or ['PLACE','WOOL',inv['WOOL']]
    missing=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP') for x,y in targets)
    if missing and not inv.get('SHEEP',0) and private['shed'].get('SHEEP',0):
        return _v219_walk(pos,home) or ['PICKUP','SHEEP',min(missing,private['shed']['SHEEP'])]
    hungry=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('fed_today')) for x,y in targets)
    if hungry and not inv.get('WHEAT',0) and private['shed'].get('WHEAT',0):
        return _v219_walk(pos,home) or ['PICKUP','WHEAT',min(hungry,private['shed']['WHEAT'])]
    tasks=[];later=[]
    for target in targets:
        x,y=target;tile=farm['tiles'][y][x];command=None
        if tile is None:command=['BUILD_PASTURE']
        elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif isinstance(tile,dict) and tile.get('kind')=='PASTURE' and not tile.get('animal'):
            if inv.get('SHEEP',0):command=['PLACE','SHEEP']
        elif isinstance(tile,dict) and tile.get('animal')=='SHEEP':
            if not tile['fed_today'] and inv.get('WHEAT',0):command=['FEED']
            elif not tile['cared_today']:command=['CARE']
            elif tile['yield_units']:command=['HARVEST']
            elif tile['fertilizer_available']:
                later.append((abs(pos[0]-x)+abs(pos[1]-y),targets.index(target),target,['COLLECT_FERTILIZER']))
        if command:tasks.append((abs(pos[0]-x)+abs(pos[1]-y),targets.index(target),target,command))
    if tasks:
        _,_,target,command=min(tasks);return _v219_walk(pos,target) or command
    if inv.get('WOOL',0):
        move=_v219_walk(pos,home)
        if move is None and later:_V21H_REPORT['wool_first']+=1
        return move or ['PLACE','WOOL',inv['WOOL']]
    if later:
        _,_,target,command=min(later);move=_v219_walk(pos,target)
        if move is None and step%24 >= 20:_V21H_REPORT['late_collect']+=1
        return move or command
    if inv.get('FERTILIZER',0) and step%24 < 23-distance:
        return _v219_walk(pos,home) or ['PLACE','FERTILIZER',inv['FERTILIZER']]
    return ['PASS']


_SL_WORKER = _v21h_base_worker

# SPDX-License-Identifier: Apache-2.0
# JFJH-V21m: finish the day-28 feed round. The last refresh (end of day 28)
# releases each animal's pending care bonus only if it was fed that day, so a
# productive animal with bonus b is worth b extra units (1+b if it went unfed on
# day 27) for one wheat. The inherited V10 layer trims day-28 wheat pickups to
# the FEEDs the closing tape itself schedules for that unit, which (a) turned
# every pickup of an off-tape hand (the six-sheep crew) into PASS for the whole
# day, and (b) left tape units without wheat for productive animals the tape
# only CAREs for (the tape was recorded on a different farm). The economic test
# is unchanged: V10's _v10_should_feed_animal decides what is worth feeding.
_V21M_REPORT = dict(offtape_trim_exempt=0, pickup_extra=0, care_to_feed=0, pass_to_feed=0,
                    crew_masked=0, errors=0)
_V21M_BASE_COUNT = _v9_count_surviving_feeds


def _v21m_worth(tile, day, prices):
    return (isinstance(tile, dict) and 'animal' in tile and not tile.get('fed_today')
            and _v10_should_feed_animal(tile, day, prices))


def _v9_count_surviving_feeds(obs, actor, start_step):
    player = int(obs['player'])
    native = _IMPL.chassis.players[player]
    route = _IMPL.chassis.routes[2 if start_step >= 648 else native['route']]
    a0 = route[start_step] if start_step < len(route) else {}
    if actor >= 1 + len(a0.get('hands') or []):
        # Not a tape unit at this step: its pickup came from an overlay worker.
        _V21M_REPORT['offtape_trim_exempt'] += 1
        return 10 ** 6
    base = _V21M_BASE_COUNT(obs, actor, start_step)
    farm = obs['farms'][player]
    tiles = farm['tiles']
    day = start_step // 24
    prices = obs['market']['prices']
    pos = list(farm['farmer'] if actor == 0 else farm['hands'][actor - 1])
    seen = set()
    for t in range(start_step, min(day * 24 + 23, len(route) - 1) + 1):
        a_t = route[t]
        cmds = [a_t.get('farmer') or ['PASS']] + list(a_t.get('hands') or [])
        if actor >= len(cmds):
            break
        c = cmds[actor]
        if not c:
            continue
        if c[0] in _V10_MOVES:
            dx, dy = _V10_MOVES[c[0]]
            pos[0] += dx
            pos[1] += dy
        elif c[0] in ('FEED', 'CARE') and 0 <= pos[1] < len(tiles) and 0 <= pos[0] < len(tiles[0]):
            if _v21m_worth(tiles[pos[1]][pos[0]], day, prices):
                seen.add(tuple(pos))
    if len(seen) > base:
        _V21M_REPORT['pickup_extra'] += len(seen) - base
        return len(seen)
    return base


def _v21m_post(obs, action):
    step = int(obs['step'])
    if step // 24 != 28:
        return action
    farm = obs['farms'][int(obs['player'])]
    tiles = farm['tiles']
    positions = [farm['farmer']] + list(farm['hands'])
    invs = obs['private']['inventories']
    prices = obs['market']['prices']
    cmds = [list(action.get('farmer') or ['PASS'])] + [list(c) for c in (action.get('hands') or [])]
    claimed = {tuple(positions[a]) for a, c in enumerate(cmds) if a < len(positions) and c == ['FEED']}
    changed = False
    for a, c in enumerate(cmds):
        if a >= len(positions) or a >= len(invs) or c not in (['CARE'], ['PASS']):
            continue
        pos = tuple(positions[a])
        if pos in claimed or int(invs[a].get('WHEAT', 0)) <= 0:
            continue
        if not (0 <= pos[1] < len(tiles) and 0 <= pos[0] < len(tiles[0])):
            continue
        if not _v21m_worth(tiles[pos[1]][pos[0]], 28, prices):
            continue
        _V21M_REPORT['care_to_feed' if c == ['CARE'] else 'pass_to_feed'] += 1
        cmds[a] = ['FEED']
        claimed.add(pos)
        changed = True
    if not changed:
        return action
    return dict(action, farmer=cmds[0], hands=cmds[1:])


_V21M_VT_WORKER = _v233_worker


def _v233_worker(obs, actor, targets):
    if int(obs['step']) // 24 != 28:
        return _V21M_VT_WORKER(obs, actor, targets)
    player = obs['player']
    farm = obs['farms'][player]
    prices = obs['market']['prices']
    masked = None
    for x, y in targets:
        t = farm['tiles'][y][x]
        if isinstance(t, dict) and 'animal' in t and not t.get('fed_today') and not _v21m_worth(t, 28, prices):
            if masked is None:
                masked = [list(row) for row in farm['tiles']]
            masked[y][x] = dict(t, fed_today=True)
    if masked is None:
        return _V21M_VT_WORKER(obs, actor, targets)
    _V21M_REPORT['crew_masked'] += 1
    farms = list(obs['farms'])
    farms[player] = dict(farm, tiles=masked)
    return _V21M_VT_WORKER(dict(obs, farms=farms), actor, targets)


_V21M_PG_PARENT = _PG_T_PARENT


def _v21m_pg_parent(observation, configuration=None):
    if int(observation.get('step', -1)) == 0:
        for k in _V21M_REPORT:
            _V21M_REPORT[k] = 0
    action = _V21M_PG_PARENT(observation, configuration)
    try:
        action = _v21m_post(observation, action)
    except Exception:
        _V21M_REPORT['errors'] += 1
    return action


_v21m_pg_parent.telemetry = getattr(_V21M_PG_PARENT, 'telemetry', {})
_PG_T_PARENT = _v21m_pg_parent

# SPDX-License-Identifier: Apache-2.0
# JFJH-V21q: day-28 pickups also cover every productive animal on a tape unit's
# path whose feed can become worth it later that day (pending care bonus, or a
# missed day-27 feed). Prices still decide at FEED time (V10 gate and the V21m
# CARE->FEED substitution); spare wheat returns to the shed at midnight.
_V21Q_REPORT = dict(pickup_relaxed=0)
_V21Q_M_COUNT = _v9_count_surviving_feeds


def _v21q_potential(tile):
    if not (isinstance(tile, dict) and tile.get('animal') in _FEED_ANIMAL_DAYS) or tile.get('fed_today'):
        return False
    first, interval = _FEED_ANIMAL_DAYS[tile['animal']]
    first += int(tile.get('placed_day', 0))
    if not (29 >= first and (29 - first) % interval == 0):
        return False
    return int(tile.get('pending_care_bonus', 0)) > 0 or int(tile.get('consecutive_unfed', 0)) > 0


def _v9_count_surviving_feeds(obs, actor, start_step):
    n = _V21Q_M_COUNT(obs, actor, start_step)
    if n >= 10 ** 6 or start_step // 24 != 28:
        return n
    player = int(obs['player'])
    route = _IMPL.chassis.routes[2]
    farm = obs['farms'][player]
    tiles = farm['tiles']
    pos = list(farm['farmer'] if actor == 0 else farm['hands'][actor - 1])
    seen = set()
    for t in range(start_step, min(28 * 24 + 23, len(route) - 1) + 1):
        a_t = route[t]
        cmds = [a_t.get('farmer') or ['PASS']] + list(a_t.get('hands') or [])
        if actor >= len(cmds):
            break
        c = cmds[actor]
        if not c:
            continue
        if c[0] in _V10_MOVES:
            dx, dy = _V10_MOVES[c[0]]
            pos[0] += dx
            pos[1] += dy
        elif c[0] in ('FEED', 'CARE') and 0 <= pos[1] < len(tiles) and 0 <= pos[0] < len(tiles[0]):
            if _v21q_potential(tiles[pos[1]][pos[0]]):
                seen.add(tuple(pos))
    if len(seen) > n:
        _V21Q_REPORT['pickup_relaxed'] += len(seen) - n
        return len(seen)
    return n

def _pg_t_final(observation, configuration=None):
    if int(observation.get("step", 0)) == 0:
        for k in _LEDGER_REPORT:
            _LEDGER_REPORT[k] = 0
    action = _PG_T_PARENT(observation, configuration)
    try:
        action = _cr_recover(observation, configuration, action)
        action = _v18_sales(observation, configuration, action)
        if int(observation.get("step", -1)) == 91:
            price = float(observation.get("market", {}).get("prices", {}).get("WHEAT", 0))
            if price < _PG_T_THRESHOLD:
                revised = []
                changed = False
                for order in action.get("market") or []:
                    if len(order) >= 3 and order[0] == "SELL" and order[1] == "WHEAT":
                        revised.append([])
                        changed = True
                        _LEDGER_REPORT["step91_slot_preservations"] += 1
                    else:
                        revised.append(order)
                if changed:
                    action = dict(action, market=revised)
        _ledger_reconcile_exit(observation, action)
    except Exception:
        _LEDGER_REPORT["ledger_errors"] += 1
    return action
_PG_T_REPORT = {"sale_price_threshold": _PG_T_THRESHOLD, "ledger": _LEDGER_REPORT}
_pg_t_final.telemetry = _PG_T_REPORT
kaggle_submission_agent = _pg_t_final
agent = kaggle_submission_agent

# SPDX-License-Identifier: Apache-2.0
# Redundant-input guard, own implementation informed by public EXP410 in:
# https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing
# Frozen upstream main SHA256:
# 178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a
# EXP410 compares existing short-crop harvests with/without another fertilizer.
# This version respects CP leases, excludes shed ports, and records real receipts.
# V10 still owns default production. No wage credit, new orders, or worker moves.
# Integrate after CP unit decisions, before its final projection/pending receipt.
import copy as _rg_copy

_RG_REPORT = dict(reviews=0, covered_vetoes=0, capped_vetoes=0,
                  lease_blocks=0, reactive_worker_blocks=0,
                  confirmed_saved_inputs=0, receipt_errors=0,
                  errors=0, local_visit_scans=0)
_RG_PENDING = {}
_RG_TRACE = []


def _rg_leased(pos, cp_state):
    for key, plan in (cp_state or {}).get('plans', {}).items():
        if tuple(key) == tuple(pos) and not plan.get('completed') and not plan.get('cancelled'):
            return True
    return False


def _rg_wheat_cycle(obs, action, pos, tile, actor, cp_state):
    """Conditional equality on a native, unleased wheat cycle; never a CP tape reset."""
    if tile.get('crop') != 'WHEAT':
        return None
    if _rg_leased(pos, cp_state):
        _RG_REPORT['lease_blocks'] += 1
        return None
    seat, step = int(obs['player']), int(obs['step'])
    reactive = _R51_INPUT_STATES.get(seat, {}).get('workers', {})
    if actor in reactive or str(actor) in reactive:
        _RG_REPORT['reactive_worker_blocks'] += 1
        return None
    native = _IMPL.chassis.players.get(seat)
    if not native:
        return None
    native_day = _v219_native_day(native, step // 24)
    expected = max((len(a.get('hands', [])) for a in native_day), default=0)
    if actor > expected:
        _RG_REPORT['reactive_worker_blocks'] += 1
        return None
    end = min(718, (int(tile['planted_day']) + 6) * 24)
    visits = _ca_visits(obs, action, tuple(pos), end, start=step + 1)
    _RG_REPORT['local_visit_scans'] += 1
    prefix = []
    for visit in visits:
        if visit[2] in ('PLANT', 'DIG', 'BUILD_COOP', 'BUILD_PASTURE'):
            return None
        prefix.append(visit)
        if visit[2] == 'HARVEST':
            break
    if not prefix or prefix[-1][2] != 'HARVEST':
        return None
    kwargs = dict(y0=int(tile.get('yield_units', 0)),
                  watered_day=step // 24 if tile.get('watered_today') else -1,
                  now_step=step)
    until = int(tile.get('fertilized_until_day', -1))
    old = _ca_yield_path('WHEAT', int(tile['planted_day']), prefix,
                         fert_until=until, **kwargs)[0]
    new = _ca_yield_path('WHEAT', int(tile['planted_day']), prefix,
                         fert_until=max(until, step // 24 + 2), **kwargs)[0]
    return dict(old_yield=old, new_yield=new, harvest_step=prefix[-1][0],
                visits=prefix, equal_positive=old > 0 and old == new)


def _rg_apply(obs, final_action, cp_state=None):
    """Only replace useless FERTILIZE with PASS; preserve all market slots and moves."""
    step, seat = int(obs['step']), int(obs['player'])
    if step == 0:
        _RG_PENDING.clear()
        for key in _RG_REPORT:
            _RG_REPORT[key] = 0
    _RG_TRACE.clear()
    previous = _RG_PENDING.pop(seat, [])
    for record in previous:
        invs = obs['private']['inventories']
        if step != record['step'] + 1 or step % 24 == 0:
            _RG_REPORT['receipt_errors'] += 1
        elif record['actor'] < len(invs) and invs[record['actor']].get('FERTILIZER', 0) == record['carried']:
            _RG_REPORT['confirmed_saved_inputs'] += 1
        else:
            _RG_REPORT['receipt_errors'] += 1
    # Avoid creating an actor-carried receipt across automatic midnight deposit.
    if step % 24 == 23:
        return final_action
    units = [final_action.get('farmer') or ['PASS'], *(final_action.get('hands') or [])]
    if not any(command == ['FERTILIZE'] for command in units):
        return final_action
    try:
        farm = _rg_copy.deepcopy(obs['farms'][seat])
        private = _rg_copy.deepcopy(obs['private'])
        positions = [farm['farmer'], *farm['hands']]
        result = [list(command) for command in units]
        pending = []
        for actor, command in enumerate(result[:len(positions)]):
            pos = tuple(positions[actor]);tile = farm['tiles'][pos[1]][pos[0]]
            inv = private['inventories'][actor]
            if (command == ['FERTILIZE'] and pos not in ((4,4),(5,4),(4,5),(5,5))
                    and isinstance(tile,dict) and tile.get('kind') == 'PLANT'
                    and inv.get('FERTILIZER',0) > 0):
                _RG_REPORT['reviews'] += 1
                covered = int(tile.get('fertilized_until_day',-1)) >= step // 24 + 2
                cycle = None
                if not covered:
                    current = dict(final_action,farmer=result[0],hands=result[1:])
                    cycle = _rg_wheat_cycle(obs,current,pos,tile,actor,cp_state)
                veto = covered or bool(cycle and cycle['equal_positive'])
                _RG_TRACE.append(dict(step=step,actor=actor,pos=pos,crop=tile['crop'],
                                      covered=covered,veto=veto,cycle=cycle))
                if veto:
                    command = result[actor] = ['PASS']
                    pending.append(dict(step=step,actor=actor,carried=int(inv['FERTILIZER'])))
                    _RG_REPORT['covered_vetoes' if covered else 'capped_vetoes'] += 1
            _PLANNER_NS['_apply_unit_action'](farm,private,actor,command,len(farm['tiles']),step//24,24,100)
        if not pending:
            return final_action
        _RG_PENDING[seat] = pending
        return dict(final_action,farmer=result[0],hands=result[1:])
    except Exception:
        _RG_REPORT['errors'] += 1
        return final_action

_IC_VALUE = {}
exec(compile(__import__('publication_assets').source('policies/observed_56713902_001_007.py', 'text'), '<bounded_input_value>', 'exec'), _IC_VALUE)

# SPDX-License-Identifier: Apache-2.0
# Bounded input commitment proposals over V10's native market-stock / budget /
# delivery helpers. No new task, hire, purchase, route, or automatic EV approval.
# _ic_apply is integrated after final unit decisions and before CP final receipt.
import copy as _ic_copy

_IC_REPORT = dict(reviews=0,candidates=0,holds=0,held_units=0,
                  warehouse_receipts=0,pickup_receipts=0,pickup_extra_units=0,
                  budget_declines=0,capacity_declines=0,ownership_declines=0,
                  value_declines=0,receipt_errors=0,errors=0,two_turn_budget_declines=0,
                  mixed_fertilizer_declines=0,next_material_declines=0,eligibility_declines=0)
_IC_PENDING = {}
_IC_PICK_PENDING = {}
_IC_TRACE = []
_IC_PORTS = ((4,4),(5,4),(4,5),(5,5))


def _ic_project(obs,action):
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][int(obs['player'])],obs['private'])
    units=[action.get('farmer') or ['PASS'],*action.get('hands',[])]
    demand={}
    for command in units:
        if len(command)>1 and command[0]=='PLANT':demand[command[1]]=demand.get(command[1],0)+1
    blocked={item for item,n in demand.items() if n>private['seeds'].get(item,0)}
    for actor,command in enumerate(units[:len(private['inventories'])]):
        if len(command)>1 and command[0]=='PLANT' and command[1] in blocked:command=['PASS']
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,command,10,int(obs['step'])//24,24,100)
    return farm,private


def _ic_owned_actor(seat,actor,next_step,cp_state):
    workers=_R51_INPUT_STATES.get(seat,{}).get('workers',{})
    if actor in workers or str(actor) in workers:return True
    end=(next_step//24+1)*24
    for plan in (cp_state or {}).get('plans',{}).values():
        if plan.get('completed') or plan.get('cancelled'):continue
        if any(next_step<=int(t)<end and int(edit[0])==actor for t,edit in plan.get('edits',{}).items()):return True
    return False


def _ic_two_turn_budget(obs,orders,next_orders):
    """Fund both original purchase lists from current cash alone, same day only.

    Each opposing BUY_PRODUCT order can add at most shedCapacity=100 units;
    2 turns x 10 orders gives a 2000-unit upper bound. Add all requested own
    purchases and 128 town/post-buy units to bound both rounds' buy quotes.
    """
    combined=list(orders)+list(next_orders);seat=int(obs['player'])
    requested={item:sum(max(0,int(o[2])) for o in combined if len(o)>2 and o[:2]==['BUY_PRODUCT',item])
               for item in ('WHEAT','FERTILIZER')}
    params={k:dict(v) for k,v in _R37_MARKET_PARAMS.items()}
    for item,patch in (obs['market'].get('params') or {}).items():
        if item in params and isinstance(patch,dict):params[item].update(patch)
    quotes={item:_r37_market_price(item,int(obs['market']['inventory'][item])-2000-requested[item]-128,params)
            for item in requested}
    hires=int(obs['farms'][seat].get('hires_today',0));start_hires=hires;cost=0
    for order in combined:
        if not order:continue
        op=order[0]
        if op=='HIRE':cost+=_v219_fib(hires);hires+=1
        elif op=='BUY_LAND':cost+=4000
        elif len(order)>2:
            item,q=order[1],max(0,int(order[2]))
            if op=='BUY_PRODUCT':cost+=q*quotes[item]
            elif op=='BUY_SEED':cost+=q*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[item]
            elif op=='BUY_ANIMAL':cost+=q*{'GOOSE':300,'COW':400,'SHEEP':500}[item]
    cash=float(obs['farms'][seat]['money'])
    return dict(approved=cost<=cash,cost_upper_bound=cost,cash_available=cash,
                hire_index_start=start_hires,hire_index_end=hires,buy_quote_upper_bounds=quotes,
                uses_sale_proceeds=False)


def _ic_next_pickups(obs,postfarm,postprivate,orders,stock,cp_state):
    """One-step physical prediction, with real current hires and no future buys."""
    farm=_ic_copy.deepcopy(postfarm);private=_ic_copy.deepcopy(postprivate)
    private['shed']=dict(stock)
    for order in orders:
        if not order:continue
        if order[0]=='HIRE':
            positions=[farm['farmer'],*farm['hands']]
            farm['hands'].append(_ca_spawn(positions,10));private['inventories'].append({})
            farm['hires_today']=int(farm.get('hires_today',0))+1
        elif len(order)>2 and order[0]=='BUY_SEED':
            private['seeds'][order[1]]=private['seeds'].get(order[1],0)+max(0,int(order[2]))
    _UNIT_NS['_decay_plants'](farm,int(obs['step']))
    next_step=int(obs['step'])+1
    future=_ca_tape(int(obs['player']),next_step)
    units=[list(future.get('farmer') or ['PASS']),*[list(c or ['PASS']) for c in future.get('hands',[])]]
    positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
    # A known CP edit cannot silently remain a native PICKUP in this forecast.
    for pos,plan in (cp_state or {}).get('plans',{}).items():
        if plan.get('completed') or plan.get('cancelled') or plan.get('failed') or plan.get('foreign'):continue
        edit=plan.get('edits',{}).get(next_step)
        if edit is None:continue
        actor,cmd=edit
        if actor<len(positions) and actor<len(units) and positions[actor]==tuple(pos) and units[actor][0] not in ('NORTH','SOUTH','EAST','WEST'):
            units[actor]=list(cmd)
    pickup=[]
    initial_farm=_ic_copy.deepcopy(farm);initial_private=_ic_copy.deepcopy(private)
    demand={}
    for command in units:
        if len(command)>1 and command[0]=='PLANT':demand[command[1]]=demand.get(command[1],0)+1
    blocked={item for item,n in demand.items() if n>private['seeds'].get(item,0)}
    for actor,command in enumerate(units[:len(private['inventories'])]):
        if len(command)>1 and command[0]=='PLANT' and command[1] in blocked:command=['PASS']
        before=private['inventories'][actor].get('FERTILIZER',0)
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,command,10,next_step//24,24,100)
        if command[:2]==['PICKUP','FERTILIZER'] and positions[actor] in _IC_PORTS:
            pickup.append(dict(actor=actor,step=next_step,position=positions[actor],command=list(command),
                               requested=max(0,int(command[2])) if len(command)>2 else 1,
                               before=before,filled=private['inventories'][actor].get('FERTILIZER',0)-before,
                               after=private['inventories'][actor].get('FERTILIZER',0)))
    return dict(pickups=pickup,farm=initial_farm,private=initial_private,units=units,after_private=private,after_farm=farm)


def _ic_other_material(private):
    result=_ic_copy.deepcopy(private)
    result['shed'].pop('FERTILIZER',None)
    for inv in result['inventories']:inv.pop('FERTILIZER',None)
    return result


def _ic_candidates(obs,final_action,cp_state=None):
    """Resource-feasible prefixes only. Returned candidates still need full EV approval."""
    step,seat=int(obs['step']),int(obs['player'])
    orders=final_action.get('market') or []
    # Leave both warehouse and following pickup receipts on the same day.
    if step%24>=22 or len(orders)>10:return []
    if not any(len(o)>2 and o[:2]==['SELL','FERTILIZER'] and int(o[2])>0 for o in orders):return []
    if any(o and o[0]=='BUY_LAND' for o in orders):return []
    _IC_REPORT['reviews']+=1
    if any(len(o)>2 and o[:2]==['BUY_PRODUCT','FERTILIZER'] for o in orders):
        _IC_REPORT['mixed_fertilizer_declines']+=1;return []
    if not _r97_budget(obs,orders):_IC_REPORT['budget_declines']+=1;return []
    future=_ca_tape(seat,step+1)
    funding=_ic_two_turn_budget(obs,orders,future.get('market') or [])
    if not funding['approved']:_IC_REPORT['two_turn_budget_declines']+=1;return []
    postfarm,postprivate=_ic_project(obs,final_action)
    original_stock,original_buys,original_sales=_r97_market_stock(postprivate['shed'],orders)
    original_final,original_loss=_r97_delivery(original_stock,postprivate,False)
    baseline=_ic_next_pickups(obs,postfarm,postprivate,orders,original_final,cp_state)
    if not any(p['filled']<p['requested'] for p in baseline['pickups']):return []
    base_by_actor={p['actor']:p for p in baseline['pickups']}
    proposed=_ic_copy.deepcopy(orders);out=[]
    for held in range(1,4):
        before_stock,_,sales=_r97_market_stock(postprivate['shed'],proposed)
        before=before_stock.get('FERTILIZER',0)
        index=next((i for i in range(len(proposed)-1,-1,-1)
                    if len(proposed[i])>2 and proposed[i][:2]==['SELL','FERTILIZER'] and sales.get(i,0)>0),None)
        if index is None:break
        # A request may exceed real stock. Reduce executed quantity, not request.
        proposed[index][2]=max(0,sales[index]-1)
        stock,buys,_=_r97_market_stock(postprivate['shed'],proposed)
        final,loss=_r97_delivery(stock,postprivate,False)
        safe=(final.get('FERTILIZER',0)==before+1 and sum(final.values())<=100
              and all(buys.get(i,0)>=q for i,q in original_buys.items())
              and all(q<=original_loss.get(item,0) for item,q in loss.items()))
        if not safe:_IC_REPORT['capacity_declines']+=1;break
        following=_ic_next_pickups(obs,postfarm,postprivate,proposed,final,cp_state)
        if (following['after_farm']!=baseline['after_farm']
                or _ic_other_material(following['after_private'])!=_ic_other_material(baseline['after_private'])):
            _IC_REPORT['next_material_declines']+=1;break
        allocated=[]
        for pick in following['pickups']:
            base=base_by_actor.get(pick['actor'])
            if base is None:continue
            extra=pick['filled']-base['filled']
            if extra>0:allocated.append(dict(pick,extra=extra,baseline_filled=base['filled']))
        if sum(p['extra'] for p in allocated)!=held:break
        if any(_ic_owned_actor(seat,p['actor'],step+1,cp_state) for p in allocated):
            _IC_REPORT['ownership_declines']+=1;break
        candidate=dict(step=step,held=held,action=dict(final_action,market=_ic_copy.deepcopy(proposed)),
                       expected_next_shed_fertilizer=final.get('FERTILIZER',0),allocated=allocated,
                       baseline_next=baseline,alternative_next=following,
                       baseline_market=orders,postunit_farm=postfarm,postunit_private=postprivate,
                       original_stock=original_final,alternative_stock=final,funding_certificate=funding)
        out.append(candidate);_IC_REPORT['candidates']+=1
    return out


def _ic_reconcile(obs,action):
    seat,step=int(obs['player']),int(obs['step'])
    old_pick=_IC_PICK_PENDING.pop(seat,None)
    if old_pick:
        if step!=old_pick['step']+2 or step%24==0:_IC_REPORT['receipt_errors']+=1
        else:
            invs=obs['private']['inventories']
            for p in old_pick['allocated']:
                if p['actor']<len(invs) and invs[p['actor']].get('FERTILIZER',0)==p['after']:
                    _IC_REPORT['pickup_receipts']+=1;_IC_REPORT['pickup_extra_units']+=p['extra']
                else:_IC_REPORT['receipt_errors']+=1
    old=_IC_PENDING.pop(seat,None)
    if not old:return
    if step!=old['step']+1 or obs['private']['shed'].get('FERTILIZER',0)!=old['expected_shed']:
        _IC_REPORT['receipt_errors']+=1;return
    _IC_REPORT['warehouse_receipts']+=1
    units=[action.get('farmer') or ['PASS'],*action.get('hands',[])]
    if any(p['actor']>=len(units) or units[p['actor']]!=p['command'] for p in old['allocated']):
        _IC_REPORT['receipt_errors']+=1;return
    _IC_PICK_PENDING[seat]=old


def _ic_apply(obs,final_action,cp_state=None,approve_callback=None,eligible=True):
    """Submit one approved prefix. With no economic callback this is a no-op."""
    if int(obs['step'])==0:
        _IC_PENDING.clear();_IC_PICK_PENDING.clear()
        for key in _IC_REPORT:_IC_REPORT[key]=0
    _IC_TRACE.clear()
    try:
        _ic_reconcile(obs,final_action)
        if not eligible:_IC_REPORT['eligibility_declines']+=1;return final_action
        if approve_callback is None:return final_action
        chosen=None;best=None
        for candidate in _ic_candidates(obs,final_action,cp_state):
            value=approve_callback(obs,final_action,candidate)
            _IC_TRACE.append(dict(held=candidate['held'],allocated=candidate['allocated'],value=value))
            if not isinstance(value,dict) or not value.get('approve'):
                _IC_REPORT['value_declines']+=1;continue
            score=float(value.get('score',0))
            if chosen is None or score>best:chosen,best=candidate,score
        if chosen is None:return final_action
        _IC_REPORT['holds']+=1;_IC_REPORT['held_units']+=chosen['held']
        _IC_PENDING[int(obs['player'])]=dict(step=int(obs['step']),expected_shed=chosen['expected_next_shed_fertilizer'],
                                           allocated=_ic_copy.deepcopy(chosen['allocated']))
        return chosen['action']
    except Exception:
        _IC_REPORT['errors']+=1
        return final_action

# SPDX-License-Identifier: Apache-2.0
# H10 conservative permission for retaining an existing fertilizer sale.
# Read only parent fertilizer commitments; never refund or rewrite other goods.

_IC_PARENT_CONTRACT_REPORT = dict(checks=0, eligible=0, debt_declines=0,
                                  sheep_credit_declines=0, schema_declines=0)


def _ic_parent_snapshot(obs):
    """Call immediately before and after the ONE true V10 parent invocation.

    r36 debts are compared per due step: consuming an old debt today must not
    hide a new future fertilizer debt. V233 request-counter deltas also catch
    spending credit that was replenished by a harvest during the same call.
    """
    seat, step = int(obs['player']), int(obs['step'])
    if step == 0:
        for key in _IC_PARENT_CONTRACT_REPORT:
            _IC_PARENT_CONTRACT_REPORT[key] = 0
    try:
        native = _IMPL.chassis.players.get(seat) or {}
        debts = native.get('sell_state', {}).get('r36_debts', {})
        fertilizer = {}
        for due, goods in debts.items():
            quantity = max(0, int(goods.get('FERTILIZER', 0)))
            if quantity:
                key = int(due)
                fertilizer[key] = fertilizer.get(key, 0) + quantity
        sheep = _V233_STATES.get(seat) or {}
        credit = max(0, int(sheep.get('credit', {}).get('FERTILIZER', 0)))
        requests = max(0, int(_V233_REPORT.get('sheep_extra_fert_sales', 0)))
        return dict(known=True, seat=seat, step=step, r36_fertilizer_debts=fertilizer,
                    sheep_fertilizer_credit=credit, sheep_fertilizer_sale_requests=requests)
    except (AttributeError, TypeError, ValueError, KeyError, NameError):
        return dict(known=False, seat=seat, step=step, reason='unknown_parent_fertilizer_schema')


def _ic_parent_can_hold(before, after):
    """Abstain if this parent call allocated any fertilizer sale commitment.

    No refund is inferred. Existing older debts remain untouched. The caller
    must still reconcile previously issued H10 receipts when a new hold is vetoed.
    """
    _IC_PARENT_CONTRACT_REPORT['checks'] += 1
    if (not before.get('known') or not after.get('known')
            or (before.get('seat'), before.get('step')) != (after.get('seat'), after.get('step'))):
        _IC_PARENT_CONTRACT_REPORT['schema_declines'] += 1
        return dict(eligible=False, reason='unknown_or_unaligned_parent_snapshot')
    old = before['r36_fertilizer_debts']
    additions = {due: quantity - old.get(due, 0)
                 for due, quantity in after['r36_fertilizer_debts'].items()
                 if quantity > old.get(due, 0)}
    spent_credit = max(0, before['sheep_fertilizer_credit'] - after['sheep_fertilizer_credit'])
    new_requests = max(0, after['sheep_fertilizer_sale_requests'] - before['sheep_fertilizer_sale_requests'])
    debt = bool(additions)
    sheep = spent_credit > 0 or new_requests > 0
    if debt:
        _IC_PARENT_CONTRACT_REPORT['debt_declines'] += 1
    if sheep:
        _IC_PARENT_CONTRACT_REPORT['sheep_credit_declines'] += 1
    eligible = not debt and not sheep
    if eligible:
        _IC_PARENT_CONTRACT_REPORT['eligible'] += 1
    return dict(eligible=eligible,
                reason='no_new_parent_fertilizer_sale_commitment' if eligible else 'parent_fertilizer_sale_already_committed',
                new_r36_fertilizer_debts=additions, sheep_credit_decrease=spent_credit,
                sheep_extra_sale_requests=new_requests)

# SPDX-License-Identifier: Apache-2.0
# Bounded fixed-plan input valuation. Native unit/decay rules come from V10.
# No shadow calls to parent policy or policy-memory mutation. Forecasts are
# conditional on its online native route; real warehouse/pickup receipts remain
# authoritative. Only already-planted strawberries and day21+ are enabled.
import copy as _iv_copy
import math as _iv_math
_IV_TRACE={}
_IV_MOVES={'NORTH':(0,-1),'SOUTH':(0,1),'EAST':(1,0),'WEST':(-1,0)}
_IV_ANIMALS={'GOOSE':(4,1,4,'COOP'),'COW':(8,2,6,'PASTURE'),'SHEEP':(6,3,6,'PASTURE')}
_IV_CROPS={'WHEAT':(2,4,0,6),'CARROT':(2,3,0,4),'TOMATO':(8,8,1,4),'STRAWBERRY':(10,10,2,4),'MELON':(10,12,0,6)}
_IV_CACHE={}

def _iv_quote(obs,item,inventory):
    params={k:dict(v) for k,v in _R37_MARKET_PARAMS.items()}
    for k,v in (obs['market'].get('params') or {}).items():
        if k in params:params[k].update(v)
    return _r37_market_price(item,int(round(inventory)),params)

def _iv_midnight(farm,day):
    for row in farm['tiles']:
        for x,tile in enumerate(row):
            if not isinstance(tile,dict):continue
            if tile.get('kind')=='PLANT':
                watered=tile['watered_today'];tile['consecutive_unwatered']=0 if watered else tile['consecutive_unwatered']+1;tile['watered_today']=False
                if tile['consecutive_unwatered']>=2:row[x]={'kind':'WEED'};continue
                first,maximum,interval,cap=_IV_CROPS[tile['crop']]
                if not interval:continue
                d=day+1-tile['planted_day']-first
                if d<0 or d%interval or d//interval+1>cap:continue
                tile['yield_units']=min(cap,tile['yield_units']+(2 if watered and tile.get('fertilized_until_day',-1)>=day else 1))
                if d//interval+1==cap:tile['max_lifespan_step']=(day+2)*24
            elif 'animal' in tile:
                tile['consecutive_unfed']=0 if tile['fed_today'] else tile['consecutive_unfed']+1
                first,interval,cap,structure=_IV_ANIMALS[tile['animal']]
                if tile['consecutive_unfed']>=2:row[x]={'kind':structure};continue
                d=day+1-tile['placed_day']-first
                if d>=0 and d%interval==0:
                    bonus=tile.pop('pending_care_bonus',0) if tile['fed_today'] else 0
                    tile['yield_units']=min(cap,tile['yield_units']+1+bonus);tile['pending_care_bonus']=0
                if tile['cared_today'] and tile['fed_today']:tile['pending_care_bonus']=tile.get('pending_care_bonus',0)+1
                tile['fertilizer_available']=True;tile['fed_today']=False;tile['cared_today']=False

def _iv_plan(obs,action):
    start=obs['step'];seat=obs['player'];farm=obs['farms'][seat];pos=[list(farm['farmer']),*[list(p) for p in farm['hands']]];frames=[];visits={}
    for t in range(start,719):
        a=_iv_copy.deepcopy(action if t==start else _ca_tape(seat,t));frames.append(a)
        units=[a.get('farmer') or ['PASS'],*(a.get('hands') or [])]
        for actor,p in enumerate(pos):
            cmd=units[actor] if actor<len(units) else ['PASS'];op=cmd[0]
            if op in _IV_MOVES:
                dx,dy=_IV_MOVES[op];nx,ny=p[0]+dx,p[1]+dy
                if 0<=nx<10 and 0<=ny<10:p[:]=[nx,ny]
            else:visits.setdefault(tuple(p),[]).append((t,actor,op))
        for order in (a.get('market') or [])[:10]:
            if order and order[0]=='HIRE':pos.append(_ca_spawn(pos,10))
        if t%24==23:pos=[[4,4]]
    return frames,visits

def _iv_budget(obs,frames):
    # Funding stress check for the declared fixed-plan price scenarios only.
    # The 2000-unit envelope is NOT a bound on arbitrary whole-game rival buys.
    # Actual current/next-turn funding is certified separately by input_guard.
    # No forecast sale proceeds finance these modeled future purchases.
    total={p:sum(max(0,int(o[2])) for a in frames for o in (a.get('market') or [])[:10] if len(o)>2 and o[:2]==['BUY_PRODUCT',p]) for p in ('WHEAT','FERTILIZER')}
    prices={p:_iv_quote(obs,p,obs['market']['inventory'][p]-2000-total[p]) for p in total}
    farm=obs['farms'][obs['player']];hires=farm['hires_today'];lands=len(farm['unlocked_quadrants']);cost=0
    for off,a in enumerate(frames):
        t=obs['step']+off
        if off and t%24==0:hires=0
        for o in (a.get('market') or [])[:10]:
            if not o:continue
            if o[0]=='HIRE':cost+=_v219_fib(hires);hires+=1
            elif o[0]=='BUY_LAND':cost+=(1000,2000,4000)[min(2,max(0,lands-1))];lands+=1
            elif len(o)>2:
                q=max(0,int(o[2]))
                if o[0]=='BUY_PRODUCT':cost+=q*prices[o[1]]
                elif o[0]=='BUY_ANIMAL':cost+=q*{'GOOSE':300,'COW':400,'SHEEP':500}[o[1]]
                elif o[0]=='BUY_SEED':cost+=q*_ES_SEED_COST[o[1]]
    return dict(covered=cost<=farm['money'],cost=cost,available=farm['money'],input_price_envelope=prices,scope='conditional_fixed_plan_price_stress_no_future_sales_credit')

def _iv_forward(obs,frames,visits):
    farm=_iv_copy.deepcopy(obs['farms'][obs['player']]);private=_iv_copy.deepcopy(obs['private']);sales=[];harvests=[];fert=[];buys=[];overflow={};buy_shortfalls=0;max_shed=sum(private['shed'].values())
    for off,raw in enumerate(frames):
        t=obs['step']+off;day=t//24;a=_iv_copy.deepcopy(raw);units=[a.get('farmer')or['PASS'],*(a.get('hands')or[])];positions=[farm['farmer'],*farm['hands']]
        terminal=None
        if t==718:
            terminal=_parent_liquidate(farm,private,obs['market']['prices'])
            units=[terminal['farmer'],*terminal['hands']]
        demand={}
        for cmd in units:
            if len(cmd)>1 and cmd[0]=='PLANT':demand[cmd[1]]=demand.get(cmd[1],0)+1
        blocked={p for p,q in demand.items() if q>private['seeds'].get(p,0)}
        for actor,cmd in enumerate(units[:len(positions)]):
            pos=tuple(positions[actor]);tile=farm['tiles'][pos[1]][pos[0]];before=dict(private['inventories'][actor]);cmd=list(cmd)
            if len(cmd)>1 and cmd[0]=='PLANT' and cmd[1] in blocked:cmd=['PASS']
            if off and t%24!=23 and pos not in ((4,4),(5,4),(4,5),(5,5)) and cmd==['FERTILIZE'] and isinstance(tile,dict) and tile.get('kind')=='PLANT' and before.get('FERTILIZER',0)>0:
                covered=tile.get('fertilized_until_day',-1)>=day+2
                if tile.get('crop')=='WHEAT' and not covered and actor not in _R51_INPUT_STATES.get(obs['player'],{}).get('workers',{}) and str(actor) not in _R51_INPUT_STATES.get(obs['player'],{}).get('workers',{}):
                    future=[]
                    for v in visits.get(pos,[]):
                        if v[0]<=t:continue
                        if v[2] in ('PLANT','DIG','BUILD_COOP','BUILD_PASTURE'):future=[];break
                        future.append(v)
                        if v[2]=='HARVEST':break
                    if future and future[-1][2]=='HARVEST':
                        kw=dict(y0=tile['yield_units'],watered_day=day if tile.get('watered_today') else -1,now_step=t)
                        b=_ca_yield_path('WHEAT',tile['planted_day'],future,fert_until=tile.get('fertilized_until_day',-1),**kw)[0]
                        c=_ca_yield_path('WHEAT',tile['planted_day'],future,fert_until=max(day+2,tile.get('fertilized_until_day',-1)),**kw)[0]
                        covered=b>0 and b==c
                if covered:cmd=['PASS']
            shed_before=dict(private['shed'])
            _UNIT_NS['_apply_unit_action'](farm,private,actor,cmd,10,day,24,100)
            inv=private['inventories'][actor]
            if cmd==['HARVEST']:
                for item,q in inv.items():
                    got=q-before.get(item,0)
                    if got>0:harvests.append(dict(step=t,actor=actor,pos=pos,item=item,quantity=got))
            if cmd==['FERTILIZE'] and before.get('FERTILIZER',0)>inv.get('FERTILIZER',0):
                fert.append(dict(step=t,actor=actor,pos=pos,crop=tile.get('crop') if isinstance(tile,dict) else None,quantity=1))
            if cmd==['DROP']:
                for item,q in before.items():
                    lost=q-(private['shed'].get(item,0)-shed_before.get(item,0))
                    if lost>0:overflow[item]=overflow.get(item,0)+lost
        orders=(a.get('market') or [])[:10]
        if t==718:orders=terminal['market'][:10]
        for slot,o in enumerate(orders):
            if not o:continue
            op=o[0]
            if op=='HIRE':
                pp=[farm['farmer'],*farm['hands']];farm['hands'].append(_ca_spawn(pp,10));private['inventories'].append({});farm['hires_today']+=1
            elif op=='BUY_LAND' and len(farm['unlocked_quadrants'])<4:
                q=('NE','SW','SE')[len(farm['unlocked_quadrants'])-1];farm['unlocked_quadrants'].append(q)
                for y,row in enumerate(farm['tiles']):
                    for x,v in enumerate(row):
                        if ('N' if y<5 else 'S')+('W' if x<5 else 'E')==q and v=='LOCKED':row[x]=None
            elif len(o)>2:
                item=o[1];q=max(0,int(o[2]))
                if op=='BUY_SEED':private['seeds'][item]=private['seeds'].get(item,0)+q
                elif op in ('BUY_PRODUCT','BUY_ANIMAL'):
                    actual=min(q,max(0,100-sum(private['shed'].values())));private['shed'][item]=private['shed'].get(item,0)+actual;buy_shortfalls+=q-actual
                    if actual:buys.append(dict(step=t,slot=slot,item=item,quantity=actual))
                elif op=='SELL':
                    actual=min(q,max(0,private['shed'].get(item,0)));private['shed'][item]=private['shed'].get(item,0)-actual
                    if actual:sales.append(dict(step=t,slot=slot,item=item,quantity=actual))
        _UNIT_NS['_decay_plants'](farm,t)
        if t%24==23:
            _iv_midnight(farm,day);stock,lost=_r97_delivery(private['shed'],private,True);private['shed']=stock
            for item,q in lost.items():overflow[item]=overflow.get(item,0)+q
            private['inventories']=[{}];farm['farmer']=[4,4];farm['hands']=[];farm['hires_today']=0
        max_shed=max(max_shed,sum(private['shed'].values()))
    return dict(sales=sales,harvests=harvests,fert=fert,buys=buys,overflow=overflow,buy_shortfalls=buy_shortfalls,max_shed=max_shed,final_shed=private['shed'],final_carried=private['inventories'])

def _iv_scenarios(obs):
    day=obs['step']//24;known=list(obs['town']['unlocked_shops']);paths=[]
    for future in _IC_VALUE['SHOPS']:
        shops=[dict(name=n,step=0) for n in known]
        for k in range(8-len(known)):shops.append(dict(name=future,step=((day//3)+1+k)*72))
        for level in (1,2):
            events=[];rival=obs['farms'][1-obs['player']]
            for y,row in enumerate(rival['tiles']):
                for x,tile in enumerate(row):
                    if not isinstance(tile,dict) or tile.get('crop')!='STRAWBERRY':continue
                    held=max(0,tile.get('yield_units',0));cycle=(x,y,tile['planted_day'])
                    if held:events.append(dict(source_id=('held',cycle),kind='held',step=min(718,(day+1)*24),slot=0,quantity=held))
                    for k in range(4):
                        prod=(tile['planted_day']+10+2*k)*24
                        if obs['step']<prod<=696:
                            events.append(dict(source_id=(cycle,k),cycle_id=cycle,event_index=k,production_step=prod,kind='production',step=prod+12,slot=0,quantity=level))
            # Separate hidden-warehouse hypotheses; never assume the rival has
            # our current warehouse or current planned sales.
            if level==2:events.append(dict(source_id='unknown_warehouse',kind='warehouse',step=obs['step']+1,slot=0,quantity=20))
            paths.append(_IC_VALUE['bounded_rival_scenario'](events,shops))
    return paths

def _ic_approve(obs,final_action,candidate):
    global _IV_CACHE
    _IV_TRACE.clear();step=obs['step'];day=step//24
    reject=lambda reason,**kw:dict(approve=False,score=0,reason=reason,**kw)
    if not 21<=day<=25:return reject('outside_day21_25_scope')
    if obs['farms'][obs['player']]['money']<50000:return reject('cash_below_prefunding_scope')
    for name in ('_V219_STATES','_V233_STATES','_R51_INPUT_STATES'):
        state=globals().get(name,{}).get(obs['player'],{})
        if state.get('committed') or state.get('pending') or state.get('workers'):return reject('uncompiled_reactive_obligations',module=name)
    key=(obs['player'],step)
    if _IV_CACHE.get('key')!=key:
        frames,visits=_iv_plan(obs,final_action);budget=_iv_budget(obs,frames)
        _IV_CACHE={'key':key,'frames':frames,'visits':visits,'budget':budget}
        if budget['covered']:_IV_CACHE['baseline']=_iv_forward(obs,frames,visits)
    cache=_IV_CACHE;budget=cache['budget']
    if not budget['covered']:return reject('future_orders_not_prefunded',budget=budget)
    base=cache['baseline'];frames=list(cache['frames']);frames[0]=candidate['action'];alt=_iv_forward(obs,frames,cache['visits'])
    old={(r['step'],r['actor'],tuple(r['pos'])) for r in base['fert']};new=[r for r in alt['fert'] if (r['step'],r['actor'],tuple(r['pos'])) not in old]
    actors={p['actor'] for p in candidate['allocated']}
    if len(new)!=candidate['held'] or any(r['crop']!='STRAWBERRY' or r['actor'] not in actors or r['step']//24!=day for r in new):return reject('no_complete_strawberry_funded_prefix',jobs=new)
    if any(p!='STRAWBERRY' and q>base['overflow'].get(p,0) for p,q in alt['overflow'].items()):return reject('incremental_forecast_overflow',baseline_overflow=base['overflow'],alternative_overflow=alt['overflow'])
    if alt['buy_shortfalls']>base['buy_shortfalls']:return reject('forecast_purchase_displacement')
    # Inputs/land/hires are fixed and funded; require other sellable material
    # quantities not to fall in this conditional physical continuation.
    def qty(rows,item):return sum(r['quantity'] for r in rows if r['item']==item)
    def outside(rows):return [(r['step'],r['slot'],r['item'],r['quantity']) for r in rows if r['item'] not in ('STRAWBERRY','FERTILIZER')]
    if outside(base['sales'])!=outside(alt['sales']):return reject('other_product_sale_schedule_changed')
    fert_future=lambda rows:[(r['step'],r['slot'],r['quantity']) for r in rows if r['item']=='FERTILIZER' and r['step']>step]
    if fert_future(base['sales'])!=fert_future(alt['sales']) or fert_future(base['buys'])!=fert_future(alt['buys']):return reject('future_fertilizer_quantity_or_schedule_changed')
    gain=qty(alt['sales'],'STRAWBERRY')-qty(base['sales'],'STRAWBERRY')
    if gain<=0:return reject('no_incremental_planned_sales')
    own=[[r for r in model['sales'] if r['item']=='STRAWBERRY'] for model in (base,alt)]
    # Retained unit can forgo a sale in the current unknown joint market. A
    # full 100-unit opposing warehouse buy raises this input quote envelope.
    fert_params=dict(_R37_MARKET_PARAMS['FERTILIZER']);fert_params.update((obs['market'].get('params') or {}).get('FERTILIZER',{}))
    if fert_params['below_func']!='linear' or fert_params['above_func']!='linear':return reject('unsupported_fertilizer_price_shape')
    slope=max(fert_params['below_target'],fert_params['above_target'])*fert_params['base']/fert_params['T']
    per_buy_extra=_iv_math.ceil(slope*candidate['held'])
    future_buy_qty=sum(r['quantity'] for r in base['buys'] if r['item']=='FERTILIZER' and r['step']>step)
    future_input_penalty=future_buy_qty*per_buy_extra
    cost=candidate['held']*_iv_quote(obs,'FERTILIZER',obs['market']['inventory']['FERTILIZER']-100)+future_input_penalty
    value=_IC_VALUE['pair_value']('STRAWBERRY',step,obs['market']['inventory']['STRAWBERRY'],own[0],own[1],_iv_scenarios(obs),lambda inv:_iv_quote(obs,'STRAWBERRY',inv),cost)
    approve=value['minimum_own_gain']>0
    trace=dict(approve=approve,score=value['minimum_own_gain'],reason='fixed_plan_complete_portfolio',held=candidate['held'],jobs=new,budget=budget,production_gain=qty(alt['harvests'],'STRAWBERRY')-qty(base['harvests'],'STRAWBERRY'),sale_gain=gain,baseline_strawberry_harvest=qty(base['harvests'],'STRAWBERRY'),alternative_strawberry_harvest=qty(alt['harvests'],'STRAWBERRY'),baseline_strawberry_sold=qty(base['sales'],'STRAWBERRY'),alternative_strawberry_sold=qty(alt['sales'],'STRAWBERRY'),baseline_overflow=base['overflow'],alternative_overflow=alt['overflow'],input_cost_envelope=cost,future_fertilizer_buy_qty=future_buy_qty,future_fertilizer_price_penalty=future_input_penalty,terminal_prices='observed_prices_common_ranking_forecast',mean_gain=value['mean_own_gain'],minimum_gain=value['minimum_own_gain'],scenarios=len(value['scenarios']),horizon=718)
    _IV_TRACE.update(trace);return trace

# SPDX-License-Identifier: Apache-2.0
# V10 retains all route/production decisions. Only certified redundant inputs
# and economically approved existing-input sales are changed at this boundary.
import copy as _ic_adapter_copy

_IC_PARENT = agent
_V11_TRACE = {}
_IC_ADAPTER_REPORT = dict(observer_updates=0, errors=0)


def _ic_sync_parent(obs, action):
    """Only the full-action observer tracks fertilizer or FERTILIZE changes.

    V9/OR2 commodity lists exclude fertilizer, so their same-good flow ledger
    remains unchanged. Current parent fertilizer sale commitments are checked
    separately before allowing any retention.
    """
    seat, step = int(obs['player']), int(obs['step'])
    state = _RACE_STATE.get(seat, {})
    if (state.get('prev') or {}).get('step') == step:
        state['prev_action'] = _ic_adapter_copy.deepcopy(action)
        _IC_ADAPTER_REPORT['observer_updates'] += 1


def input_commitment_submission_entry(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _IC_ADAPTER_REPORT:
            _IC_ADAPTER_REPORT[key] = 0
        _IV_CACHE.clear()
        _IV_TRACE.clear()
    before = _ic_parent_snapshot(observation)
    parent = _IC_PARENT(observation, configuration)
    permission = _ic_parent_can_hold(before, _ic_parent_snapshot(observation))
    action = _rg_apply(observation, parent)
    action = _ic_apply(observation, action, None, _ic_approve,
                       eligible=permission['eligible'])
    try:
        if action != parent:
            _ic_sync_parent(observation, action)
    except Exception:
        _IC_ADAPTER_REPORT['errors'] += 1
    _V11_TRACE.clear()
    _V11_TRACE.update(resource_guard=_ic_adapter_copy.deepcopy(_RG_TRACE),
                      input_commitments=_ic_adapter_copy.deepcopy(_IC_TRACE),
                      parent_fertilizer_contract=permission)
    return action


agent = input_commitment_submission_entry
agent.telemetry = _IC_REPORT

# Preserve R4 default behavior and aggregate the already-approved early recovery
# trace without letting R4's late trace reset discard it. No second parent call.
_RC_PARENT=agent

def capital_recovery_submission_entry(observation,configuration=None):
    action=_RC_PARENT(observation,configuration)
    _V11_TRACE['capital_recovery']=copy.deepcopy(_CR_TRACE)
    return action

agent=capital_recovery_submission_entry
agent.telemetry=_CR_REPORT
final_capital_recovery_submission_entry=agent


# SPDX-License-Identifier: Apache-2.0
# JFJH-V22S (sched): re-planned tape days with fewer hands.
# From step 648 every world plays route 2. On its closing days the tape's
# hands do the recorded farm's field work with long walks. The same field
# commands are re-assigned offline to fewer hands: every tile keeps its
# commands in the tape's order, same-day shed deliveries are made no later
# than the tape (day 28: except the hour-20/21 fertilizer and egg deliveries,
# which go in with the day-end dump; day 29: deliveries the tape made before
# hour 16 may come as late as hour 16, before the closing sales), FEED tiles
# are served by units that pick up wheat first, all
# hands are hired at hour 0 and the farmer holds (4,4) at hour 0 so the spawn
# tiles are the planned ones. Commands that cannot change the final bank are
# dropped: CARE on days 28-29 (its bonus is banked after the last refresh),
# day-29 FEED, day-28
# WATER on day-27 plantings (outside every yield window; alive means watered
# on day 27), day-28 DIG/BUILD. A day-28 CARE on a tile without a FEED is
# kept and served by a wheat carrier, so V21m can still turn it into a FEED
# when the economic test passes; the tape's FEED commands and raw wheat
# pickups stay as they were for the layers that look ahead at them. Market
# orders are unchanged except the HIRE orders. The
# routes were solved offline (OR-Tools, analysis only); only the resulting
# commands are embedded. Segments: route 2 day 28: 8 hands (tape 11); route 2 day 29: 10 hands (tape 11).
_V22S_SEGMENTS = json.loads(__import__('publication_assets').value('observed_56713902_001_008'))
for _v22s_route, _v22s_steps in _V22S_SEGMENTS.items():
    for _v22s_step, _v22s_action in _v22s_steps.items():
        _IMPL.chassis.routes[int(_v22s_route)][int(_v22s_step)] = _v22s_action
        _ROUTES[int(_v22s_route)][int(_v22s_step)] = _v22s_action
del _v22s_route, _v22s_steps, _v22s_step, _v22s_action
final_v22s_submission_entry = agent

# ---- JFJH-V22W weed shift (2026-09-26) ---------------------------------------------------------------------
# V10 weed_repair turns a tape PLANT/BUILD_* standing on a WEED into DIG and queues the command, but the queue only
# replays while the unit stays on that tile with a no-op tape command (a PLANT only if the next tape command is not a
# move).  Once the tape moves the unit on, the plant/build is lost for good: a strawberry plot stays empty all season,
# or a pasture is never built and the cow the tape buys for it sits in the shed for the rest of the game (V21q ladder
# episode 113321857).  Here the unit replays the displaced command on the next step and then runs its own tape one
# step late until its next PASS (skipped to catch up) or the end of the day.  A PLANT is only replayed when the unit's
# next tape command is WATER and the delayed WATER still lands on the same day (a seed left unwatered on its planting
# day dies that night).  One shift per unit per day; the chassis replay queue for that unit is cleared.
_V22W_SHIFT = {}
_V22W_REPORT = {'events': 0, 'plant': 0, 'build': 0, 'skipped_plant': 0, 'busy': 0, 'shifted_steps': 0,
                'caught_up': 0, 'errors': 0}
_V22W_ROUTE_ACTION = Chassis._route_action
_V22W_ACT = Chassis.act


def _v22w_unit(action, i):
    if not isinstance(action, dict):
        return ['PASS']
    if i == 0:
        return list(action.get('farmer') or ['PASS'])
    hands = action.get('hands') or []
    return list(hands[i - 1]) if i - 1 < len(hands) and hands[i - 1] else ['PASS']


def _v22w_set(action, i, command):
    if i == 0:
        action['farmer'] = list(command)
        return
    hands = action.setdefault('hands', [])
    while len(hands) < i:
        hands.append(['PASS'])
    hands[i - 1] = list(command)


def _v22w_route_action(self, route, step):
    action = _V22W_ROUTE_ACTION(self, route, step)
    ctx = getattr(self, '_v22w_ctx', None)
    if not ctx or ctx[1] != step or not isinstance(action, dict):
        return action
    try:
        player, _, view = ctx
        shifts = _V22W_SHIFT.setdefault(player, {})
        tape = self.routes[route]
        day, hour = divmod(step, 24)
        last = 22 if day == 29 else 23
        for i, sh in list(shifts.items()):
            if sh['day'] != day or step > sh['end'] or sh['route'] != route:
                shifts.pop(i)
                continue
            if step == sh['origin'] + 1:
                command = sh['command']
                pending = (self.players.get(player) or {}).get('pending') or {}
                if pending.get(i) and pending[i][0][1] == sh['command']:
                    pending.pop(i, None)
            else:
                command = _v22w_unit(tape[step - 1], i)
            _v22w_set(action, i, command)
            _V22W_REPORT['shifted_steps'] += 1
            if step == sh['end']:
                _V22W_REPORT['caught_up'] += int(sh['caught'])
                shifts.pop(i)
        units = min(len(view.positions), 1 + len(action.get('hands') or []))
        for i in range(units):
            command = _v22w_unit(action, i)
            if not command or command[0] not in ('PLANT', 'BUILD_COOP', 'BUILD_PASTURE'):
                continue
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            tile = _tile_at(view.tiles, (int(pos[0]), int(pos[1])))
            if not (isinstance(tile, dict) and _get(tile, 'kind') == 'WEED'):
                continue
            _V22W_REPORT['events'] += 1
            if i in shifts or (player, day, i) in _V22W_DONE:
                _V22W_REPORT['busy'] += 1
                continue
            if command[0] == 'PLANT':
                if hour + 2 > last or step + 1 >= len(tape) or _v22w_unit(tape[step + 1], i) != ['WATER']:
                    _V22W_REPORT['skipped_plant'] += 1
                    continue
            elif hour + 1 > last:
                continue
            end, caught = day * 24 + last, False
            for s in range(step + 2, day * 24 + last + 1):
                if s < len(tape) and _v22w_unit(tape[s], i) == ['PASS']:
                    end, caught = s, True
                    break
            shifts[i] = dict(day=day, route=route, origin=step, command=list(command), end=end, caught=caught)
            _V22W_DONE.add((player, day, i))
            _V22W_REPORT['plant' if command[0] == 'PLANT' else 'build'] += 1
    except Exception:
        _V22W_REPORT['errors'] += 1
    return action


_V22W_DONE = set()


def _v22w_act(self, observation, configuration=None):
    try:
        step = _step_of(observation)
        player = _int(_get(observation, 'player', 0))
        if step == 0:
            _V22W_SHIFT.pop(player, None)
            for key in [k for k in _V22W_DONE if k[0] == player]:
                _V22W_DONE.discard(key)
        self._v22w_ctx = (player, step, _View(observation, player, self.cfg))
    except Exception:
        self._v22w_ctx = None
        _V22W_REPORT['errors'] += 1
    return _V22W_ACT(self, observation, configuration)


Chassis._route_action = _v22w_route_action
Chassis.act = _v22w_act
final_v22w_submission_entry = agent

# ---- JFJH-V22Y second strawberry wave on the tape's wheat cells (2026-09-27) -----------------------------
# Brunch spots, ice-cream shops, smoothie shops and farmers markets draw strawberries every fourth turn.  Where at
# least three of the four shops open by day 12 draw them, the strawberry price in our pool games stays at $160-240
# through day 27 (with two or fewer it falls to $1-55 by day 24), so a plant started on days 12-14 still sells its
# late crop well.  A strawberry planted on day P produces at the ends of days P+9, P+11, P+13 and P+15, two units
# each when it is watered and fertilized that day (fertilizer lasts three days), and holds at most four units.  The
# tape keeps watering the wheat cells it plants on days 12-14, so strawberries planted there in place of wheat stay
# alive; from the first production on, a hired care hand fertilizes on P+9 and P+13, waters the production days the
# tape's remaining commands will not water, harvests before the four-unit cap and brings the berries to the shed.
# The idea of a second strawberry planting sized by the open strawberry shops comes from watching public ladder
# replays of another team; this is our own implementation on our tape.
_V22Y_SHOPS = ('BRUNCH_SPOT', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP', 'FARMERS_MARKET')
_V22Y_MIN_SHOPS = 4
_V22Y_MIN_PRICE = 190
# worlds heading for three tomato shops run the day-18 tomato project (V219); its crew and our care hands would stack
# on the steep end of the daily hire price, so the wave stays out where two tomato shops are already open on day 12
_V22Y_TOMATO_SHOPS = ('PIZZA_SHOP', 'FARMERS_MARKET')
_V22Y_MAX_TOMATO_SHOPS = 1
_V22Y_DECIDE_STEP = 288        # day 12 hour 0
_V22Y_TARGET = {3: 8, 4: 12}
_V22Y_DAY_CAP = {12: 8, 13: 6, 14: 2}
_V22Y_WEST_MAX_X = 4          # only cells in the west half (closer to the shed, shorter care walks)
_V22Y_TWO_HANDS_FROM = 8      # plants; from this size a north hand and a south hand share the care
_V22Y_SECOND_HAND_MAX = 250   # a second care hand only while its hire price stays at or below this
_V22Y_ONE_HAND_MAX = 400      # no care hand at all on a day it would cost more (the tape keeps watering)
_V22Y_RESERVE = 3000
_V22Y_PROD = (9, 11, 13, 15)
_V22Y_STATES = {}
_V22Y_REPORT = {'active': 0, 'target': 0, 'seed_orders': 0, 'seeds_bought': 0, 'converted': 0, 'confirmed_plants': 0,
                'lost_plants': 0, 'care_hires': 0, 'care_hire_shortfalls': 0, 'fertilize': 0, 'harvest': 0,
                'harvest_units': 0, 'water': 0, 'deliveries': 0, 'placed_units': 0, 'sold_credit': 0,
                'fert_reserved': 0, 'fert_bought': 0, 'budget_declines': 0, 'one_hand_days': 0, 'priced_out_days': 0,
                'errors': 0}
_V22Y_PARENT = agent


def _v22y_planned_day(player, day):
    try:
        route = _IMPL.chassis.players[player]['route']
        tape = _IMPL.chassis.routes[route]
        return tape[day * 24:min((day + 1) * 24, 719)]
    except Exception:
        return []


def _v22y_tile(obs, pos):
    x, y = pos
    return obs['farms'][int(obs['player'])]['tiles'][y][x]


def _v22y_tape_waters(obs, player, step):
    """Cells the tape's own units still WATER today, from their current cells and the route's remaining commands."""
    out = set()
    try:
        route = _IMPL.chassis.players[player]['route']
        tape = _IMPL.chassis.routes[route]
        farm = obs['farms'][player]
        size = len(farm['tiles'])
        pos = [list(farm['farmer'])] + [list(h) for h in farm['hands']]
        end = min((step // 24 + 1) * 24, 719)
        moves = {'NORTH': (0, -1), 'SOUTH': (0, 1), 'WEST': (-1, 0), 'EAST': (1, 0)}
        for t in range(step, end):
            a = tape[t] if 0 <= t < len(tape) and isinstance(tape[t], dict) else {}
            cmds = [a.get('farmer')] + list(a.get('hands') or [])
            for i, c in enumerate(cmds):
                if i >= len(pos) or not c:
                    continue
                if c[0] in moves:
                    dx, dy = moves[c[0]]
                    pos[i] = [min(size - 1, max(0, pos[i][0] + dx)), min(size - 1, max(0, pos[i][1] + dy))]
                elif c[0] == 'WATER':
                    out.add(tuple(pos[i]))
    except Exception:
        pass
    return out


def _v22y_count_shops(obs):
    return sum(1 for s in ((obs.get('town') or {}).get('unlocked_shops') or []) if s in _V22Y_SHOPS)


def _v22y_is_straw(tile):
    return isinstance(tile, dict) and tile.get('kind') == 'PLANT' and tile.get('crop') == 'STRAWBERRY'


def _v22y_region(state, pos):
    return 'S' if state.get('two_hands') and not state.get('one_hand_today') and pos[1] >= 5 else 'N'


def _v22y_live(obs, state):
    for pos, planted in state['plants'].items():
        tile = _v22y_tile(obs, pos)
        if _v22y_is_straw(tile) and int(tile.get('planted_day', -99)) == planted:
            yield pos, planted, tile


def _v22y_useful(day, k):
    # a production at the end of `day` is only worth tending if it can be harvested on day 29 at the latest
    return k in _V22Y_PROD and day <= 28


def _v22y_next_prod(k, day):
    for p in _V22Y_PROD:
        if p >= k and day + (p - k) <= 28:
            return day + (p - k)
    return None


def _v22y_fert_due(tile, k, day):
    nxt = _v22y_next_prod(k, day)
    return k >= 7 and nxt is not None and nxt - day <= 2 and int(tile.get('fertilized_until_day', -1)) < nxt


def _v22y_tasks(obs, state, day, tape_waters, region):
    out = []
    for pos, planted, tile in _v22y_live(obs, state):
        if _v22y_region(state, pos) != region:
            continue
        k = day - planted
        units = int(tile.get('yield_units', 0))
        if k < 9:
            if int(tile.get('consecutive_unwatered', 0)) >= 1 and not tile.get('watered_today') and pos not in tape_waters:
                out.append((pos, ['WATER']))
            continue
        if units >= 3 or (units > 0 and (k >= 16 or day >= 29)):
            out.append((pos, ['HARVEST']))
        if _v22y_fert_due(tile, k, day):
            out.append((pos, ['FERTILIZE']))
        dry = int(tile.get('consecutive_unwatered', 0)) >= 1
        if not tile.get('watered_today') and pos not in tape_waters and (_v22y_useful(day, k) or dry):
            out.append((pos, ['WATER']))
    return out


def _v22y_fert_need(obs, state, day, region):
    return sum(1 for pos, planted, tile in _v22y_live(obs, state)
               if _v22y_region(state, pos) == region and _v22y_fert_due(tile, day - planted, day))


def _v22y_regions_due(obs, state, day):
    due = set()
    for pos, planted, tile in _v22y_live(obs, state):
        k = day - planted
        if 7 <= k <= 16 or (k > 16 and int(tile.get('yield_units', 0)) > 0):
            due.add(_v22y_region(state, pos))
    return sorted(due)


def _v22y_worker(obs, state, role, actor, day, step, tape_waters):
    view = FarmView(obs)
    pos = tuple(view.positions[actor])
    inv = view.inventory(actor)
    fert = int(inv.get('FERTILIZER', 0))
    if not role['loaded']:
        need = _v22y_fert_need(obs, state, day, role['region'])
        if need <= fert:
            role['loaded'] = True
        else:
            home = _v219_home(pos)
            walk = _v219_walk(pos, home)
            if walk:
                return walk
            take = max(0, min(need - fert, int(view.shed.get('FERTILIZER', 0)) - state['fert_taken']))
            short = need - fert - take
            if short > 0 and role['tries'] < 3:
                role['tries'] += 1
                role['buy'] = short
            else:
                role['loaded'] = True
            if take > 0:
                state['fert_taken'] += take
                return ['PICKUP', 'FERTILIZER', take]
            if not role['loaded']:
                return ['PASS']
    tasks = [(c, cmd) for c, cmd in _v22y_tasks(obs, state, day, tape_waters, role['region']) if cmd != ['FERTILIZE'] or fert > 0]
    home = _v219_home(pos)
    distance = abs(pos[0] - home[0]) + abs(pos[1] - home[1])
    berries = int(inv.get('STRAWBERRY', 0))
    if berries and (step >= 717 - distance or (day == 29 and step % 24 >= 16 - distance) or berries >= 8):
        walk = _v219_walk(pos, home)
        if walk:
            return walk
        role['placed'] = (step, berries)
        return ['PLACE', 'STRAWBERRY', berries]
    if tasks:
        order = {'FERTILIZE': 0, 'HARVEST': 1, 'WATER': 2}
        target, command = min(tasks, key=lambda v: (abs(pos[0] - v[0][0]) + abs(pos[1] - v[0][1]), order[v[1][0]]))
        walk = _v219_walk(pos, target)
        if walk:
            return walk
        role['last'] = {'step': step, 'command': command, 'berries': berries}
        return command
    if berries:
        walk = _v219_walk(pos, home)
        if walk:
            return walk
        role['placed'] = (step, berries)
        return ['PLACE', 'STRAWBERRY', berries]
    return ['PASS']


def _v22y_new_state(step):
    return {'last_step': step, 'active': False, 'plants': {}, 'pending_plants': {}, 'quota': {},
            'planted_by_day': {}, 'seed_day': -1, 'care_day': -1, 'workers': {}, 'hire_pending': None,
            'lost': set(), 'fert_taken': 0, 'credit': 0}


def _v22y_sync(player, step, qty):
    try:
        st9 = _V9_RACE.get(player)
        prev = st9.get('prev') if st9 else None
        if prev and prev.get('step') == step:
            prev.setdefault('own', {})['STRAWBERRY'] = int(prev['own'].get('STRAWBERRY', 0)) + qty
            if 'left' in prev:
                prev['left']['STRAWBERRY'] = max(0, int(prev['left'].get('STRAWBERRY', 0)) - qty)
        sto = _OR2_STATE.get(player)
        prev = sto.get('prev') if sto else None
        if prev and prev.get('step') == step:
            prev.setdefault('own', {})['STRAWBERRY'] = int(prev['own'].get('STRAWBERRY', 0)) + qty
        st18 = _V18_STATE.get(player)
        prev = ((st18 or {}).get('mpx') or {}).get('prev')
        if prev and prev.get('step') == step:
            prev.setdefault('own', {})['STRAWBERRY'] = int(prev['own'].get('STRAWBERRY', 0)) + qty
    except Exception:
        _V22Y_REPORT['errors'] += 1


def agent(observation, configuration=None):
    action = _V22Y_PARENT(observation, configuration)
    try:
        step = int(observation['step'])
        player = int(observation['player'])
        day, hour = step // 24, step % 24
        state = _V22Y_STATES.get(player)
        if state is None or step <= state['last_step']:
            state = _V22Y_STATES[player] = _v22y_new_state(step)
            if step == 0:
                for k in _V22Y_REPORT:
                    _V22Y_REPORT[k] = 0
        state['last_step'] = step
        if not isinstance(action, dict):
            return action
        farm = observation['farms'][player]
        private = observation.get('private') or {}
        prices = observation['market']['prices']
        if step == _V22Y_DECIDE_STEP:
            shops = _v22y_count_shops(observation)
            tomato_shops = sum(1 for s in ((observation.get('town') or {}).get('unlocked_shops') or []) if s in _V22Y_TOMATO_SHOPS)
            if (shops >= _V22Y_MIN_SHOPS and tomato_shops <= _V22Y_MAX_TOMATO_SHOPS
                    and int(prices.get('STRAWBERRY', 0)) >= _V22Y_MIN_PRICE and float(farm['money']) >= 6000):
                target = _V22Y_TARGET[min(4, shops)]
                state.update(active=True, target=target, two_hands=target >= _V22Y_TWO_HANDS_FROM)
                state['quota'] = {12: min(target, _V22Y_DAY_CAP[12])}
                _V22Y_REPORT['active'] += 1
                _V22Y_REPORT['target'] += target
        if not state['active']:
            return action
        for pos, pday in list(state['pending_plants'].items()):
            tile = _v22y_tile(observation, pos)
            if _v22y_is_straw(tile) and int(tile.get('planted_day', -1)) == pday:
                state['plants'][pos] = pday
                state['planted_by_day'][pday] = state['planted_by_day'].get(pday, 0) + 1
                _V22Y_REPORT['confirmed_plants'] += 1
        state['pending_plants'] = {}
        for pos, pday in state['plants'].items():
            tile = _v22y_tile(observation, pos)
            if pos not in state['lost'] and day - pday <= 15 and not (_v22y_is_straw(tile) and int(tile.get('planted_day', -1)) == pday):
                state['lost'].add(pos)
                _V22Y_REPORT['lost_plants'] += 1
        if hour == 0 and day in (13, 14) and day not in state['quota']:
            done = sum(state['planted_by_day'].values())
            state['quota'][day] = min(max(0, state['target'] - done), _V22Y_DAY_CAP[day])
        market = [list(o) if isinstance(o, list) else o for o in (action.get('market') or [])]
        commands = [action.get('farmer') or ['PASS']] + list(action.get('hands') or [])
        changed = False
        # seeds bought one turn ahead (the market clears after the units act), then tape wheat plantings converted
        quota = state['quota'].get(day, 0) - state['planted_by_day'].get(day, 0)
        seeds = int((private.get('seeds') or {}).get('STRAWBERRY', 0))
        if quota > 0 and state['seed_day'] != day and hour <= 20:
            want = quota - seeds
            if want <= 0:
                state['seed_day'] = day
            elif len(market) < MAX_ORDERS:
                if float(farm['money']) >= want * 100 + _V22Y_RESERVE:
                    market.append(['BUY_SEED', 'STRAWBERRY', want])
                    state['seed_day'] = day
                    changed = True
                    _V22Y_REPORT['seed_orders'] += 1
                    _V22Y_REPORT['seeds_bought'] += want
                else:
                    _V22Y_REPORT['budget_declines'] += 1
        # the tape's own strawberry plantings (if any) keep their seeds: only convert beyond them
        own_plants = sum(1 for c in commands if c == ['PLANT', 'STRAWBERRY'])
        spare = seeds - own_plants
        if quota > 0 and spare > 0 and hour <= 21:
            positions = [farm['farmer']] + list(farm['hands'])
            used = 0
            for i, cmd in enumerate(commands):
                if used >= min(quota, spare) or i >= len(positions):
                    break
                cell = tuple(positions[i])
                if cell[0] > _V22Y_WEST_MAX_X:
                    continue
                if cmd == ['PLANT', 'WHEAT'] and _v22y_tile(observation, cell) is None:
                    commands[i] = ['PLANT', 'STRAWBERRY']
                    state['pending_plants'][cell] = day
                    used += 1
                    changed = True
                    _V22Y_REPORT['converted'] += 1
        # care hand hired after the tape's last planned hire of the day
        if state['care_day'] != day:
            state.update(care_day=day, workers={}, hire_pending=None, fert_taken=0, one_hand_today=False)
        pend = state.get('hire_pending')
        if pend and pend['step'] == step - 1:
            if len(farm['hands']) == pend['hands_after']:
                for j, region in enumerate(pend['regions']):
                    actor = pend['hands_after'] - len(pend['regions']) + 1 + j
                    state['workers'][actor] = {'region': region, 'loaded': False, 'tries': 0, 'buy': 0, 'last': None, 'placed': None}
                _V22Y_REPORT['care_hires'] += len(pend['regions'])
            else:
                _V22Y_REPORT['care_hire_shortfalls'] += len(pend['regions'])
            state['hire_pending'] = None
        due = _v22y_regions_due(observation, state, day)
        if due and not state['workers'] and state['hire_pending'] is None and hour <= 16 and day <= 29:
            planned = _v22y_planned_day(player, day)
            latest = max((i for i, a in enumerate(planned) if isinstance(a, dict) and any(o and o[0] == 'HIRE' for o in (a.get('market') or []))), default=-1)
            parent_hires = sum(1 for o in market if isinstance(o, list) and o and o[0] == 'HIRE')
            if hour > latest and parent_hires == 0 and len(market) + len(due) <= MAX_ORDERS:
                n = int(farm['hires_today'])
                if len(due) > 1 and _v219_fib(n + 1) > _V22Y_SECOND_HAND_MAX:
                    state['one_hand_today'] = True
                    due = _v22y_regions_due(observation, state, day)
                    _V22Y_REPORT['one_hand_days'] += 1
                if _v219_fib(n) > _V22Y_ONE_HAND_MAX:
                    _V22Y_REPORT['priced_out_days'] += 1
                    due = []
                cost = sum(_v219_fib(n + j) for j in range(len(due)))
                if due and float(farm['money']) >= cost + _V22Y_RESERVE:
                    market.extend(['HIRE'] for _ in due)
                    state['hire_pending'] = {'step': step, 'hands_after': len(farm['hands']) + len(due), 'regions': due}
                    changed = True
                elif due:
                    _V22Y_REPORT['budget_declines'] += 1
        # keep the fertilizer the care hand still has to pick up today
        if due:
            need = sum(_v22y_fert_need(observation, state, day, r) for r in due
                       if not any(w['region'] == r and w['loaded'] for w in state['workers'].values()))
            if need:
                stock = projected_shed(dict(action, farmer=commands[0], hands=commands[1:], market=market), FarmView(observation))
                room = int(stock.get('FERTILIZER', 0)) - need
                for j, o in enumerate(market):
                    if isinstance(o, list) and len(o) >= 3 and o[0] == 'SELL' and o[1] == 'FERTILIZER':
                        q = int(o[2])
                        keep = max(0, min(q, room))
                        if keep < q:
                            market[j] = ['SELL', 'FERTILIZER', keep] if keep > 0 else []
                            _V22Y_REPORT['fert_reserved'] += q - keep
                            changed = True
                        room -= keep
        if state['workers']:
            tape_waters = _v22y_tape_waters(observation, player, step)
            state['fert_taken'] = 0
            invs = private.get('inventories') or []
            for actor, role in sorted(state['workers'].items()):
                if actor > len(farm['hands']):
                    continue
                last = role.get('last')
                if last and last['step'] == step - 1 and last['command'] == ['HARVEST'] and actor < len(invs):
                    got = int((invs[actor] or {}).get('STRAWBERRY', 0)) - last['berries']
                    if got > 0:
                        _V22Y_REPORT['harvest_units'] += got
                placed = role.get('placed')
                if placed and placed[0] == step - 1 and actor < len(invs):
                    left = int((invs[actor] or {}).get('STRAWBERRY', 0))
                    moved = max(0, placed[1] - left)
                    state['credit'] += moved
                    _V22Y_REPORT['placed_units'] += moved
                    role['placed'] = None
                while len(commands) <= actor:
                    commands.append(['PASS'])
                cmd = _v22y_worker(observation, state, role, actor, day, step, tape_waters)
                commands[actor] = cmd
                changed = True
                name = {'FERTILIZE': 'fertilize', 'HARVEST': 'harvest', 'WATER': 'water', 'PLACE': 'deliveries'}.get(cmd[0])
                if name:
                    _V22Y_REPORT[name] += 1
                if role.get('buy') and len(market) < MAX_ORDERS:
                    qty = int(role['buy'])
                    price = int(prices.get('FERTILIZER', 100))
                    if float(farm['money']) >= qty * (price + 5) + _V22Y_RESERVE:
                        market.append(['BUY_PRODUCT', 'FERTILIZER', qty])
                        _V22Y_REPORT['fert_bought'] += qty
                    role['buy'] = 0
        # sell the berries our hand brought in that the parent's own orders leave in the shed
        if state['credit'] > 0 and len(market) < MAX_ORDERS and int(prices.get('STRAWBERRY', 0)) >= 2:
            stock = projected_shed(dict(action, farmer=commands[0], hands=commands[1:], market=market), FarmView(observation))
            selling = sum(int(o[2]) for o in market if isinstance(o, list) and len(o) >= 3 and o[:2] == ['SELL', 'STRAWBERRY'])
            qty = min(state['credit'], int(stock.get('STRAWBERRY', 0)) - selling)
            if qty > 0:
                market.append(['SELL', 'STRAWBERRY', qty])
                state['credit'] -= qty
                _V22Y_REPORT['sold_credit'] += qty
                _v22y_sync(player, step, qty)
                changed = True
        if not changed:
            return action
        result = dict(action)
        result['farmer'] = commands[0]
        result['hands'] = commands[1:]
        result['market'] = market
        return result
    except Exception:
        _V22Y_REPORT['errors'] += 1
        return action


final_v22y_submission_entry = agent

# ---- JFJH-V22K market knobs re-measured on the V55 lineage (2026-09-27, diagnostic) --------------------------
# renji_starfall's public notebook "Your Market List Is an Order Book" (Apache-2.0 V55 base) swept 26 constants and
# kept four market-side values; these layers exist unchanged in our chassis, so the same four values are re-set here
# (module-level globals read at call time).  Only the constants change; no new mechanism.
_V92_P_EVERY = 2
V9_RACE_DEFAULT = 44
_OR2_SLOT_MARGIN = 8.0
_CA_MARGIN = -15.0
final_v22k_submission_entry = agent


# ---- JFJH-XRL1 release ahead of an early-dumping rival, v1 (2026-09-28) ------------------------------------
# RACEGATE (v9/3) leaves an item quoted at or below base to the tape's own schedule: uncontested, the town draw between
# now and the planned sale pays for the wait.  Against a rival that sells its whole shed as soon as the quote makes a
# new day high (the day's first high usually comes at hour 1, right after the hour-0 town draw), the wait hands it the
# first units: in the S2 losses both farms hold the same 21 strawberries at day 26 hour 0, the rival sells all 21 at
# hour 1 (118 -> 78) and we sell ours from hour 12 on.  Moving one unit from our planned sale to now changes
# (our cash - rival cash) by about slope * (2 * R - D), with R the rival's sales in between and D the town's draw in
# between.  This layer estimates the rival's stock from public data only (harvests read off its tiles, sales from
# market-inventory deltas with the exact town draw; the lower bound assumes the shed emptied whenever the quote sat at
# the $1 floor, where a sale leaves no trace in the inventory).  Each day on which our own parent held most of its
# stock through hours 0-2 is an event: the share of its day-start stock the rival sold in those hours (on a day we
# sold early too, a rival on our own tape sells with us and says nothing).  The probability that the rival sells early
# today weighs the events against a prior of one event in which it held, discounting events whose day-start quote
# stood above today's (many rivals sell early only while the quote is high) and events about another product.  At
# hour 0 releasing none, a third, two thirds or all of our ready stock of an item is compared in a lockstep simulation
# of the next day: the parent sells each planned lot at the tape's turn, or as soon as the reservation may pull it
# forward while the quote stands above base; the rival dumps at hour 1 with that probability, else holds.  Hour 0 is
# often full of HIRE orders: a same-item SELL/BUY_PRODUCT pair is netted to free a slot, else the release is retried
# at hour 1 at the head of the queue.  Released units are booked as sale debts against the tape's later planned sales
# (as the reservation does) and every inner own-sale ledger is told.  Without such evidence nothing changes.
# v1: tomatoes and carrots too; acts only while the quote is at or below base (above it the reservation already pulls
# the parent's planned lots forward); a lighter prior (0.6 events) so a rival racing every low-quote day is recognised
# after its first one or two such days.
_XRL_EST = ('CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL')
_XRL_ACT = ('STRAWBERRY', 'MILK', 'WOOL', 'MELON', 'TOMATO', 'CARROT')
_XRL_ONGOING = ('TOMATO', 'STRAWBERRY')
_XRL_ANIMAL = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}
_XRL_HOURS = (0,)
_XRL_FROM = 216            # day 9
_XRL_TO = 697              # up to day 29 hour 0
_XRL_MIN_RIVAL = 3
_XRL_P_MIN = 0.3
_XRL_PSEUDO = 4.0          # units of prior evidence that the rival does not sell early
_XRL_BASE = {'STRAWBERRY': 120, 'MILK': 160, 'WOOL': 200, 'MELON': 250, 'TOMATO': 60, 'CARROT': 35}
_XRL_MAX_RATIO = 1.0       # act only where RACEGATE holds the parent back (quote at or below base)
_XRL_KERNEL = 0.15         # quote/base excess at which an event's weight falls by e
_XRL_OTHER_W = 0.5         # weight of an event about another product
_XRL_PSEUDO_E = 0.6        # prior events in which the rival held
_XRL_MIN_GAIN = 25.0
_XRL_HORIZON = 24
_XRL_SHIFT = 3             # the parent's lead layers sell a planned lot a few turns before the tape does
_XRL_STATE = {}
_XRL_REPORT = {'turns': 0, 'releases': 0, 'units': 0, 'by_item': {}, 'gain': 0.0, 'p_last': None, 'evidence': 0,
               'skip_p': 0, 'skip_gain': 0, 'skip_room': 0, 'netted': 0, 'retries': 0, 'errors': 0, 'sync_errors': 0,
               'log': []}
_XRL_PARENT = agent
from math import exp as _xrl_exp


def _xrl_draw(shops, step):
    draw = dict.fromkeys(_XRL_EST, 0)
    if step % 4 == 0:
        for shop in shops:
            items = _V9_SHOP_ITEMS.get(shop, ())
            for item in items:
                if item in draw:
                    draw[item] += 2 if len(items) == 1 else 1
    if step % 24 == 0:
        for item in draw:
            draw[item] += 1
    return draw


def _xrl_snapshot(tiles):
    out = {}
    for y, row in enumerate(tiles):
        for x, t in enumerate(row):
            if not isinstance(t, dict):
                continue
            if t.get('kind') == 'PLANT' and t.get('crop') in _XRL_EST:
                out[(x, y)] = ('P', t['crop'], int(t.get('planted_day', -1)), int(t.get('yield_units', 0) or 0))
            elif t.get('animal') in _XRL_ANIMAL:
                out[(x, y)] = ('A', _XRL_ANIMAL[t['animal']], int(t.get('placed_day', -1)),
                               int(t.get('yield_units', 0) or 0))
    return out


def _xrl_harvested(snap, tiles, boundary):
    got = {}
    for (x, y), (kind, item, born, u0) in snap.items():
        if u0 <= 0:
            continue
        t = tiles[y][x]
        if kind == 'P' and item not in _XRL_ONGOING:
            if t is None:
                got[item] = got.get(item, 0) + u0
            continue
        same = (isinstance(t, dict) and
                ((kind == 'P' and t.get('kind') == 'PLANT' and t.get('crop') == item
                  and int(t.get('planted_day', -1)) == born) or
                 (kind == 'A' and _XRL_ANIMAL.get(t.get('animal')) == item
                  and int(t.get('placed_day', -1)) == born)))
        if not same:
            continue
        u1 = int(t.get('yield_units', 0) or 0)
        if u1 == 0 or (boundary and u1 < u0):
            got[item] = got.get(item, 0) + u0
    return got


def _xrl_new_state():
    zero = dict.fromkeys(_XRL_EST, 0)
    return {'step': -1, 'hold': dict(zero), 'lo': dict(zero), 'today': dict(zero), 'snap': None, 'prev': None,
            'h0': None, 'h0_price': {}, 'early': dict(zero), 'own_early': dict(zero), 'own_h0': {}, 'released': set(),
            'retry': set(), 'ev_sold': 0.0, 'ev_base': 0.0, 'events': []}


def _xrl_update(st, obs):
    """Advance the rival stock estimate to this observation."""
    step = int(obs['step']); seat = int(obs['player'])
    tiles = obs['farms'][1 - seat]['tiles']
    prev = st['prev']
    if prev is not None and prev['step'] == step - 1 and st['snap'] is not None:
        boundary = step % 24 == 0
        got = _xrl_harvested(st['snap'], tiles, boundary)
        if boundary:
            st['today'] = dict.fromkeys(_XRL_EST, 0)
        inv = obs['market']['inventory']; prices = obs['market']['prices']
        draw = _xrl_draw(prev['shops'], prev['step'])
        sold = {}
        for item in _XRL_EST:
            d = int(inv.get(item, 0)) - int(prev['inv'].get(item, 0)) + draw[item] - int(prev['own'].get(item, 0))
            if d > 0:
                sold[item] = d
            if int(prev['prices'].get(item, 0) or 0) <= 1 or int(prices.get(item, 0) or 0) <= 1:
                st['lo'][item] = min(st['lo'][item], st['today'][item])
        for item, n in got.items():
            st['hold'][item] += n; st['lo'][item] += n
            if not boundary:
                st['today'][item] += n
        for item, n in sold.items():
            st['hold'][item] = max(0, st['hold'][item] - n)
            st['lo'][item] = max(0, st['lo'][item] - n)
            st['today'][item] = min(st['today'][item], st['lo'][item])
            if prev['step'] % 24 <= 2:
                st['early'][item] = st['early'].get(item, 0) + n
        if prev['step'] % 24 <= 2 and not boundary:
            for item, n in prev['own'].items():
                st['own_early'][item] = st['own_early'].get(item, 0) + int(n)
    elif prev is not None:
        st['hold'] = dict.fromkeys(_XRL_EST, 0); st['lo'] = dict.fromkeys(_XRL_EST, 0)
    st['snap'] = _xrl_snapshot(tiles)
    hour = step % 24
    if hour == 0:
        st['h0'] = dict(st['lo']); st['early'] = dict.fromkeys(_XRL_EST, 0); st['released'] = set(); st['retry'] = set()
        st['own_early'] = dict.fromkeys(_XRL_EST, 0)
        shed = (obs.get('private') or {}).get('shed') or {}
        st['own_h0'] = {item: int(shed.get(item, 0) or 0) for item in _XRL_ACT}
        st['h0_price'] = {item: int(obs['market']['prices'].get(item, 0) or 0) for item in _XRL_ACT}
    elif hour == 3 and st['h0'] is not None:
        # Evidence: share of the rival's day-start stock sold in hours 0-2 (days we released on are left out, since
        # our release moves the quote the rival reacts to)
        for item in _XRL_ACT:
            base = st['h0'].get(item, 0)
            mine = st.get('own_h0', {}).get(item, 0)
            # informative days only: we held most of our own day-start stock through hours 0-2 (on a day our parent
            # sold early too, a rival on our own tape sells with us and says nothing about racing ahead of us)
            if (base >= _XRL_MIN_RIVAL and item not in st['released'] and mine >= _XRL_MIN_RIVAL
                    and 2 * st['own_early'].get(item, 0) <= mine):
                sold = min(base, st['early'].get(item, 0))
                st['ev_base'] += base; st['ev_sold'] += sold
                ratio = float(st['h0_price'].get(item, 0)) / _XRL_BASE.get(item, 100)
                st['events'].append((item, ratio, sold / float(base)))
        st['h0'] = None
    st['step'] = step


def _xrl_p(st, item=None, price=None):
    """Probability that the rival sells its day-start stock in hours 0-2 while we hold: each informative day (we held
    most of our own stock through those hours) is one event, the share of its day-start stock the rival sold then;
    an event whose day-start quote/base stood above the current one is discounted by how far (many rivals sell early
    only while the quote is high; one that sold early at a lower quote will at this one), and an event about another
    product has half weight, against a prior of _XRL_PSEUDO_E events in which the rival held."""
    if item is None:
        return st['ev_sold'] / (st['ev_base'] + _XRL_PSEUDO)
    r = float(price) / _XRL_BASE.get(item, 100)
    num = den = 0.0
    for it, ratio, frac in st['events']:
        w = _xrl_exp(-max(0.0, ratio - r) / _XRL_KERNEL) * (1.0 if it == item else _XRL_OTHER_W)
        num += w * frac; den += w
    return num / (den + _XRL_PSEUDO_E)


def _xrl_sim(item, inv0, step0, release, lots, rivals, shops, gate, hz):
    """(our revenue - rival revenue) over the next day in lockstep.  `release` units go now; each parent lot (due,
    qty) goes at the tape's turn less the lead-layer shift, or earlier -- as the reservation pulls a lot due within
    `hz` turns forward while the quote stands above RACEGATE's base -- and whatever is left at the horizon goes then."""
    inv = int(inv0); mine = theirs = 0.0
    lots = [list(lot) for lot in lots]
    last = step0 + _XRL_HORIZON
    for s in range(step0, last + 1):
        a = release if s == step0 else 0
        if s > step0:
            quote = _r37_market_price(item, inv)
            for lot in lots:
                if lot[1] > 0 and (lot[0] - _XRL_SHIFT <= s or s == last or (quote > gate and lot[0] <= s + hz)):
                    a += lot[1]; lot[1] = 0
        b = int(rivals.get(s, 0))
        while a > 0 or b > 0:
            price = _r37_market_price(item, inv); n = 0
            if a > 0:
                mine += price; a -= 1; n += 1
            if b > 0:
                theirs += price; b -= 1; n += 1
            if price > 1:
                inv += n
        inv -= _xrl_draw(shops, s)[item]
    return mine - theirs


def _xrl_plan(native, item, step, stock, debts):
    """The parent's own schedule for `stock` units: the tape's planned sales (net of debts) in the next day."""
    plan = []; left = stock
    for due in range(step + 1, min(LAST_ACT_STEP, step + _XRL_HORIZON) + 1):
        route = 2 if due >= 648 else native.get('route', 0)
        tape = _IMPL.chassis.routes.get(route) if isinstance(_IMPL.chassis.routes, dict) else _IMPL.chassis.routes[route]
        if tape is None or due >= len(tape):
            break
        planned = 0
        for o in (tape[due] or {}).get('market') or []:
            if o and len(o) >= 3 and o[0] == 'SELL' and o[1] == item:
                try:
                    planned += max(0, int(o[2]))
                except Exception:
                    pass
        planned = max(0, planned - debts.get(due, {}).get(item, 0))
        take = min(left, planned)
        if take > 0:
            plan.append((due, take)); left -= take
        if left <= 0:
            break
    return plan, left


def _xrl_lots(plan, left, step, release):
    """The parent's lots left after `release` units are booked against its earliest planned sales."""
    lots = []; skip = release
    for due, q in plan:
        take = min(q, skip); skip -= take; q -= take
        if q > 0:
            lots.append((due, q))
    rest = left - skip
    if rest > 0:
        lots.append((step + _XRL_HORIZON, rest))
    return lots


def _xrl_sync(obs, action, added):
    seat, step = int(obs['player']), int(obs['step'])
    try:
        st = _V9_RACE.get(seat)
        prev = st.get('prev') if st else None
        if prev and prev.get('step') == step:
            own = prev.setdefault('own', {}); left = prev.get('left')
            for item, n in added.items():
                own[item] = int(own.get(item, 0)) + n
                if isinstance(left, dict) and item in left:
                    left[item] = max(0, int(left.get(item, 0)) - n)
        st = _OR2_STATE.get(seat)
        prev = st.get('prev') if st else None
        if prev and prev.get('step') == step:
            own = prev.setdefault('own', {})
            for item, n in added.items():
                if item in _OR2_ITEMS:
                    own[item] = int(own.get(item, 0)) + n
        st = _V18_STATE.get(seat)
        prev = ((st or {}).get('mpx') or {}).get('prev')
        if prev and prev.get('step') == step:
            own = prev.setdefault('own', {})
            for item, n in added.items():
                if item in _V18_MPX_ITEMS:
                    own[item] = int(own.get(item, 0)) + n
        race = _RACE_STATE.get(seat)
        if race is not None and race.get('prev_action') is not None and race.get('step') == step:
            race['prev_action'] = action
    except Exception:
        _XRL_REPORT['sync_errors'] += 1


def _xrl_own_exec(action, stock):
    own = {}
    for o in action.get('market') or []:
        if o and len(o) >= 3 and o[0] == 'SELL' and o[1] in _XRL_EST:
            try:
                q = max(0, int(o[2]))
            except Exception:
                continue
            n = min(q, max(0, int(stock.get(o[1], 0)) - own.get(o[1], 0)))
            own[o[1]] = own.get(o[1], 0) + n
    return own


def _xrl_net_slot(market, stock):
    """Free one slot by netting a SELL and a BUY_PRODUCT of the same item (same shed after the market phase)."""
    for i, o in enumerate(market):
        if not (isinstance(o, list) and len(o) >= 3 and o[0] == 'SELL'):
            continue
        for j, b in enumerate(market):
            if not (isinstance(b, list) and len(b) >= 3 and b[0] == 'BUY_PRODUCT' and b[1] == o[1]) or j == i:
                continue
            try:
                sell, buy = max(0, int(o[2])), max(0, int(b[2]))
            except Exception:
                continue
            if sell > int(stock.get(o[1], 0)) or sell == buy:
                continue
            if sell > buy:
                market[i] = ['SELL', o[1], sell - buy]
            else:
                market[i] = ['BUY_PRODUCT', o[1], buy - sell]
            del market[j]
            _XRL_REPORT['netted'] = _XRL_REPORT.get('netted', 0) + 1
            return True
    return False


def _xrl_release(obs, action, st, stock, items, same_step):
    step = int(obs['step']); seat = int(obs['player'])
    native = _IMPL.chassis.players.get(seat)
    if not native or native.get('route') not in _IMPL.chassis.routes:
        return action, {}
    prices = obs['market']['prices']
    pool = _xrl_p(st)
    _XRL_REPORT['p_last'] = round(pool, 3); _XRL_REPORT['evidence'] = int(st['ev_base'])
    _XRL_REPORT['p_item'] = {item: round(_xrl_p(st, item, int(prices.get(item, 0) or 0)), 3) for item in _XRL_ACT}
    _XRL_REPORT['events'] = len(st['events'])
    market = [list(o) if isinstance(o, (list, tuple)) else o for o in (action.get('market') or [])]
    selling = {}
    for o in market:
        if isinstance(o, list) and len(o) >= 3 and o[0] == 'SELL':
            try:
                selling[o[1]] = selling.get(o[1], 0) + max(0, int(o[2]))
            except Exception:
                return action, {}
    inventory = obs['market']['inventory']
    shops = list((obs.get('town') or {}).get('unlocked_shops') or [])
    debts = native.setdefault('sell_state', {}).setdefault('r36_debts', {})
    added = {}; cands = []
    for item in items:
        rival = int(st['lo'].get(item, 0))
        if rival < _XRL_MIN_RIVAL or int(prices.get(item, 0) or 0) <= 1:
            continue
        if int(prices.get(item, 0) or 0) > _XRL_MAX_RATIO * _XRL_BASE.get(item, 0):
            continue
        p = _xrl_p(st, item, int(prices.get(item, 0) or 0))
        if p < _XRL_P_MIN:
            _XRL_REPORT['skip_p'] += 1
            continue
        avail = max(0, int(stock.get(item, 0)) - selling.get(item, 0))
        if avail <= 0:
            continue
        inv0 = int(inventory.get(item, 10000)) + min(selling.get(item, 0), int(stock.get(item, 0)))
        plan, left = _xrl_plan(native, item, step, avail, debts)
        dump = {step + (0 if same_step else 1): rival}; hold = {step + _XRL_HORIZON: rival}
        gate = V9_RACEGATE_BASE.get(item, 0) + V9_RACEGATE_MARGIN
        hz = min(_XRL_HORIZON, int((_V9_ITEM_HZ.get(seat) or {}).get(item, 12)))
        lots0 = _xrl_lots(plan, left, step, 0)
        base_a = _xrl_sim(item, inv0, step, 0, lots0, dump, shops, gate, hz)
        base_h = _xrl_sim(item, inv0, step, 0, lots0, hold, shops, gate, hz)
        best_q, best_g = 0, 0.0
        for q in sorted({max(1, avail // 3), max(1, (2 * avail) // 3), avail}):
            lots = _xrl_lots(plan, left, step, q)
            g = (p * (_xrl_sim(item, inv0, step, q, lots, dump, shops, gate, hz) - base_a)
                 + (1.0 - p) * (_xrl_sim(item, inv0, step, q, lots, hold, shops, gate, hz) - base_h))
            if g > best_g:
                best_q, best_g = q, g
        if best_q <= 0 or best_g < _XRL_MIN_GAIN:
            _XRL_REPORT['skip_gain'] += 1
            continue
        cands.append((best_g, item, best_q, rival, avail, plan, p))
    # the scarce order slots go to the largest expected gains first
    for best_g, item, best_q, rival, avail, plan, p in sorted(cands, key=lambda c: (-c[0], c[1])):
        hit = next((o for o in market if isinstance(o, list) and len(o) >= 3 and o[0] == 'SELL' and o[1] == item), None)
        if hit is not None:
            hit[2] = int(hit[2]) + best_q
        else:
            hole = next((i for i, o in enumerate(market) if not o), None)
            if hole is not None and not same_step:
                market[hole] = ['SELL', item, best_q]
            elif hole is not None:
                del market[hole]
                market.insert(0, ['SELL', item, best_q])
            elif len(market) < MAX_ORDERS or _xrl_net_slot(market, stock):
                market.insert(0, ['SELL', item, best_q])
            else:
                _XRL_REPORT['skip_room'] += 1
                if not same_step:
                    st['retry'].add(item)
                continue
        selling[item] = selling.get(item, 0) + best_q
        added[item] = best_q
        # book the released units against the tape's planned sales, earliest first (as the reservation does)
        need = best_q
        for due, q in plan:
            take = min(q, need)
            if take > 0:
                d = debts.setdefault(due, {}); d[item] = d.get(item, 0) + take; need -= take
            if need <= 0:
                break
        st['released'].add(item)
        _XRL_REPORT['releases'] += 1; _XRL_REPORT['units'] += best_q; _XRL_REPORT['gain'] += best_g
        _XRL_REPORT['by_item'][item] = _XRL_REPORT['by_item'].get(item, 0) + best_q
        if len(_XRL_REPORT['log']) < 60:
            _XRL_REPORT['log'].append([step, item, avail, rival, round(p, 2), best_q, round(best_g, 1), int(same_step)])
    if not added:
        return action, {}
    return dict(action, market=market), added


def _xrl_agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    st = _XRL_STATE.get(seat)
    if st is None or step <= st['step']:
        st = _XRL_STATE[seat] = _xrl_new_state()
        if step == 0:
            for k in ('turns', 'releases', 'units', 'skip_p', 'skip_gain', 'skip_room', 'errors', 'sync_errors',
                      'evidence', 'netted', 'retries', 'events'):
                _XRL_REPORT[k] = 0
            _XRL_REPORT['gain'] = 0.0; _XRL_REPORT['p_last'] = None; _XRL_REPORT['p_item'] = {}
            _XRL_REPORT['by_item'] = {}; _XRL_REPORT['log'] = []
    try:
        _xrl_update(st, observation)
    except Exception:
        _XRL_REPORT['errors'] += 1
        st['prev'] = None
    action = _XRL_PARENT(observation, configuration)
    out = action
    try:
        if isinstance(action, dict) and _v18_standard(configuration):
            stock = projected_shed(action, FarmView(observation))
            hour = step % 24
            if _XRL_FROM <= step < _XRL_TO and (hour in _XRL_HOURS or (hour == 1 and st['retry'])):
                _XRL_REPORT['turns'] += 1
                items = _XRL_ACT if hour in _XRL_HOURS else tuple(sorted(st['retry']))
                if hour == 1:
                    st['retry'] = set()
                    _XRL_REPORT['retries'] = _XRL_REPORT.get('retries', 0) + 1
                out, added = _xrl_release(observation, action, st, stock, items, hour == 1)
                if added:
                    _xrl_sync(observation, out, added)
            st['prev'] = {'step': step, 'inv': dict(observation['market']['inventory']),
                          'prices': dict(observation['market']['prices']), 'own': _xrl_own_exec(out, stock),
                          'shops': list((observation.get('town') or {}).get('unlocked_shops') or [])}
        else:
            st['prev'] = None
    except Exception:
        _XRL_REPORT['errors'] += 1
        st['prev'] = None
        out = action
    return out


final_xrl_submission_entry = _xrl_agent

# ---- JFJH-V22T (2026-09-27, diagnostic): third-party layer, Apache-2.0 ---------------------------------------
# Verbatim copy of "counter T-B" from the same public notebook (renji_starfall / shiiin9, Apache-2.0): the V219 tomato
# project's step-432 qualification counts pizza/farmers shops; this replaces the count with a projected revenue of the
# project's 80 units against the tomato inventory they will meet (town drain, rival standing tomato tiles).
# ---- host-agnostic variant (for bases whose entry point is not called `agent`) ----
# V55 ends with `final_price_guard`, and `agent` there is an inner layer: wrapping `agent`
# would silently skip V55's last layers.  So this copy captures the base's real entry point
# -- the last callable, exactly what Kaggle would run -- before defining anything, and does
# not delete any base name.  Everything else is byte-for-byte cxt_b_tomato_ev.py.
_CXTB_PARENT = [v for v in list(globals().values()) if callable(v)][-1]

# ==== counter T-B: gate the tomato investment on the price it will actually get ====
# (shiiin9, 2026-09-20)
#
# Layer T showed that v9/4's tomato investment is switched off by a shop count.  Reading the
# engine says what that count is really standing in for.  Only the pizza shop and the farmers
# market buy tomatoes, one per instance every four turns -- six a day each -- and the town
# centre takes one a day whatever the town looks like.  The investment produces ten tiles
# over days 26..29, twenty units a day.  So three such shops drain 19 a day against our 20:
# the author's threshold is the point where the town absorbs exactly what we grow.
#
# That is the right quantity to care about, but a count is a coarse way to measure it, because
# what sets the price is the market inventory, not the shops:
#
#     inventory  9,600 -> 1st unit 300, 80 units fetch 18,355
#     inventory 10,000 -> 1st unit  60, 80 units fetch  3,599
#     inventory 10,200 -> 1st unit  24, 80 units fetch  1,653
#     inventory 10,600 -> every unit 1
#
# TOMATO has T=200, the narrowest anchor of any crop, so six hundred units decide everything.
# A town with two tomato shops that nobody has sold into is worth far more than a town with
# three that the rival is already dumping in.  Both of those are visible at day 18: the market
# inventory is shared, and `farms` is public, so the rival's tomato tiles and the day each was
# planted can be read off the board.
#
# So this layer projects the inventory instead of counting shops.  From day 18 it drains the
# town's demand day by day, adds what the rival's standing tomato plants will produce (an
# ongoing crop yields on planted_day+8 and the three days after, then dies), adds our own
# twenty a day in the harvest window, and prices every unit with the engine's own curve.  The
# investment is taken when that revenue clears what it costs: 4,000 for the third extra
# quadrant, 500 for ten seeds, and the hires, which the parent budgets for itself.
#
# The two constants below are not guessed.  The probe recorded the real tomato inventory on
# every day of 96 replayed games, so the projection was checked against it:
#   * with no rival tomatoes the projection lands 19 units low over eight days, so the town
#     takes about 2.4 a day less than the shop table implies -- _CXTB_DRAIN_SLACK.
#   * the games where the rival grew tomatoes miss by exactly their crop: 22 tiles missed by
#     153 units and 25 tiles by 163, which is 0.75 per tile per day once the slack is taken
#     out.  A tomato plant dies after four yields, but an opponent who commits to tomatoes
#     replants, and both of those did -- so the rate is carried to the end of the season
#     rather than stopped after four days.
# The remaining error is under 25 units over eight days, against a scale (T=200) where 600
# units is the whole price range.
_CXTB_MIN_REVENUE = 7000    # coins the 80 units must be worth before committing
_CXTB_THEIR_UNITS = 0.75    # units a day per rival tomato tile (measured)
_CXTB_DRAIN_SLACK = 2.4     # units a day the town does not take after all (measured)
_CXTB_OUR_UNITS = 20        # ten tiles, days 26..29 (measured: 60..80 units in total)
_CXTB_HARVEST_DAYS = (26, 27, 28, 29)
_CXTB_REPORT = {'cxtb_calls': 0, 'cxtb_opened': 0, 'cxtb_blocked': 0, 'cxtb_errors': 0,
                'cxtb_features': []}

_CXTB_BASE_QUALIFIES = _v219_qualifies


def _cxtb_their_supply(obs, upto):
    """What the rival's tomato tiles will put into the market, day by day.

    TOMATO is an ongoing crop and yields from planted_day + 8.  `planted_day` is on the
    public tile, so the start of each plant is read rather than guessed; the rate is the
    measured one and runs to the end of the season, because an opponent who is growing
    tomatoes at day 18 replants as the plants die.
    """
    supply = {}
    them = obs['farms'][1 - obs['player']]
    for row in them['tiles']:
        for t in row:
            if isinstance(t, dict) and t.get('crop') == 'TOMATO':
                for d in range(int(t.get('planted_day', 0)) + 8, upto + 1):
                    supply[d] = supply.get(d, 0.0) + _CXTB_THEIR_UNITS
    return supply


def _cxtb_expected_revenue(obs):
    """Price our 80 units against the inventory they will meet."""
    inventory = float(obs['market']['inventory']['TOMATO'])
    day = int(obs['step']) // 24
    shops = float(sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET')
                      for s in obs['town']['unlocked_shops']))
    # The unlock schedule is deterministic -- seven shops by day 22, eight by day 24 -- and
    # each draw is uniform over the eight types, so each remaining slot demands tomatoes with
    # probability 2/8.  Carrying the expectation is enough: the draw lands before the harvest.
    pending = {22: 0.25, 24: 0.25}
    last = max(_CXTB_HARVEST_DAYS)
    theirs = _cxtb_their_supply(obs, last)
    revenue = 0.0
    for d in range(day, last + 1):
        shops += pending.get(d, 0.0)
        inventory -= 1.0 + 6.0 * shops - _CXTB_DRAIN_SLACK
        inventory += theirs.get(d, 0.0)
        if d in _CXTB_HARVEST_DAYS:
            for _ in range(_CXTB_OUR_UNITS):
                revenue += _r37_market_price('TOMATO', int(round(inventory)))
                inventory += 1
    return revenue


def _cxtb_qualifies(obs, native):
    """The author's qualification with the shop count and price floor replaced by the value."""
    farm = obs['farms'][obs['player']]
    if len(farm['tiles']) != 10 or set(farm['unlocked_quadrants']) != {'NW', 'NE', 'SW'}:
        return False
    if farm['money'] < 12000:
        return False
    if _cxtb_expected_revenue(obs) < _CXTB_MIN_REVENUE:
        return False
    if any(farm['tiles'][y][x] != 'LOCKED' for y in (5, 6) for x in range(5, 10)):
        return False
    if obs['private']['seeds'].get('TOMATO', 0) or obs['private']['shed'].get('TOMATO', 0):
        return False
    if any(isinstance(t, dict) and t.get('crop') == 'TOMATO' for row in farm['tiles'] for t in row):
        return False
    for tape in _IMPL.chassis.routes.values():
        for a in tape[432:719]:
            if any(o and o[0] == 'BUY_LAND' for o in a.get('market', [])):
                return False
            if any(c == ['PLANT', 'TOMATO'] for c in [a.get('farmer')] + a.get('hands', [])):
                return False
    return True


def _v219_qualifies(obs, native):
    """The name the agent looks up at step 432."""
    _CXTB_REPORT['cxtb_calls'] += 1
    try:
        revenue = _cxtb_expected_revenue(obs)
        ok = _cxtb_qualifies(obs, native)
        them = obs['farms'][1 - obs['player']]
        _CXTB_REPORT['cxtb_features'].append({
            'opened': bool(ok), 'base': bool(_CXTB_BASE_QUALIFIES(obs, native)),
            'revenue': round(revenue),
            'shops': sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET')
                         for s in obs['town']['unlocked_shops']),
            'price': obs['market']['prices']['TOMATO'],
            'inventory': obs['market']['inventory']['TOMATO'],
            'their_tomatoes': sum(1 for row in them['tiles'] for t in row
                                  if isinstance(t, dict) and t.get('crop') == 'TOMATO'),
        })
        _CXTB_REPORT['cxtb_opened' if ok else 'cxtb_blocked'] += 1
        return ok
    except Exception:
        _CXTB_REPORT['cxtb_errors'] += 1
        return _CXTB_BASE_QUALIFIES(obs, native)




def _cxtb_agent(observation, configuration=None):
    return _CXTB_PARENT(observation, configuration)


_cxtb_agent.telemetry = _CXTB_REPORT

final_v22t_submission_entry = _cxtb_agent


# ---- JFJH-WCT wheat carry on the town draw (2026-09-28) ------------------------------------------------------
# The town draws wheat every fourth turn after the market (one unit per open shop that uses it, plus one a day from the
# centre), which lifts the quote.  Buying N units in the market phase of a draw turn and selling them in the next turn
# earns sum_j [p(I-N-D+j) - p(I-1-j)] (buy quotes are after-buy, sell quotes before-sell, D = the draw), about N*D*slope:
# $5-50 a round trip, several round trips a day.  Several ladder rivals run such a carry (lots of 70-94 wheat bought
# at hours 4, 8, ... and sold the next turn); within our own free shed space an offline estimate on 116 ladder games
# of x4swykd gives about $800 a game.  Guards: the lot never takes the shed room the units may deposit next turn (a DROP
# into a full shed destroys the overflow), it only uses cash beyond this turn's own costs plus a reserve, it never runs
# on the last day's closing turns, and the parent never sees the carried units (its observation's shed wheat is
# reduced by them), so its feed purchases, pickups and sales are the ones it would make without the carry.  The lot
# actually bought is measured next turn against the parent's own expected wheat and sold (netted against a parent
# wheat purchase there), and OR2's own-sale ledger is told.  Both legs go at the end of the queue (moving them
# to the head, or standing down against rivals that carry too, both lost more than they saved on the ladder tapes).
_WCT_FROM = 72             # day 3
_WCT_LAST = 708            # last buy turn (sold at 709, before the closing liquidation)
_WCT_MAX = 90
_WCT_MIN = 10
_WCT_ROOM = 8              # shed room kept free on top of everything the units carry
_WCT_RESERVE = 0.0
_WCT_MIN_GAIN = 3.0
_WCT_STATE = {}
_WCT_REPORT = {'buys': 0, 'bought': 0, 'sold': 0, 'netted': 0, 'gain_est': 0.0, 'short': 0, 'skip_room': 0,
               'skip_cash': 0, 'skip_slots': 0, 'errors': 0}
_WCT_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_WCT_FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]
_WCT_SEED = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
import copy as _wct_copy


def _wct_draw(shops, step):
    d = 0
    if step % 4 == 0:
        for shop in shops:
            if 'WHEAT' in _V9_SHOP_ITEMS.get(shop, ()):
                d += 1
    if step % 24 == 0:
        d += 1
    return d


def _wct_costs(obs, market):
    """Cash the parent's own market orders may take this turn (priced conservatively)."""
    farm = obs['farms'][int(obs['player'])]
    prices = obs['market']['prices']
    hires = int(farm.get('hires_today', 0) or 0)
    lands = len(farm.get('unlocked_quadrants') or [])
    cost = 0.0
    for o in market:
        if not isinstance(o, list) or not o:
            continue
        if o[0] == 'HIRE':
            cost += _WCT_FIB[min(hires, len(_WCT_FIB) - 1)]; hires += 1
        elif o[0] == 'BUY_LAND':
            cost += (1000, 2000, 4000)[min(max(lands - 1, 0), 2)]; lands += 1
        elif len(o) >= 3:
            try:
                q = max(0, int(o[2]))
            except Exception:
                continue
            if o[0] == 'BUY_SEED':
                cost += q * _WCT_SEED.get(o[1], 100)
            elif o[0] == 'BUY_ANIMAL':
                cost += q * 500
            elif o[0] == 'BUY_PRODUCT':
                cost += q * (int(prices.get(o[1], 0) or 0) + 30)
    return cost


def _wct_gain(inv, draw, n):
    cost = sum(_r37_market_price('WHEAT', inv - k) for k in range(1, n + 1))
    rev = sum(_r37_market_price('WHEAT', inv - n - draw + k) for k in range(0, n))
    return rev - cost


def _wct_agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    st = _WCT_STATE.get(seat)
    if st is None or step <= st.get('step', -1):
        st = _WCT_STATE[seat] = {'step': -1, 'pending': None, 'carry': 0}
        if step == 0:
            for k in _WCT_REPORT:
                _WCT_REPORT[k] = 0.0 if k == 'gain_est' else 0
    st['step'] = step
    obs_parent = observation
    carry = 0
    try:
        pend = st.get('pending')
        if pend is not None and pend['step'] == step - 1:
            real = int(((observation.get('private') or {}).get('shed') or {}).get('WHEAT', 0))
            carry = max(0, min(pend['n'], real - pend['parent_wheat']))
            if carry < pend['n']:
                _WCT_REPORT['short'] += 1
        elif st.get('carry', 0) > 0 and pend is None:
            real = int(((observation.get('private') or {}).get('shed') or {}).get('WHEAT', 0))
            carry = min(st['carry'], real)
        st['pending'] = None
        if carry > 0:
            private = _wct_copy.copy(observation['private']); shed = _wct_copy.copy(private['shed'])
            shed['WHEAT'] = max(0, int(shed.get('WHEAT', 0)) - carry)
            private['shed'] = shed
            obs_parent = _wct_copy.copy(observation); obs_parent['private'] = private
    except Exception:
        _WCT_REPORT['errors'] += 1
        obs_parent = observation; carry = 0
    action = _WCT_PARENT(obs_parent, configuration)
    try:
        if not isinstance(action, dict) or not _v18_standard(configuration):
            st['carry'] = 0
            return action
        market = [list(o) if isinstance(o, (list, tuple)) else o for o in (action.get('market') or [])]
        changed = False
        if carry > 0:
            # net against a parent wheat purchase this turn, sell the rest at the end of the queue
            for o in market:
                if isinstance(o, list) and len(o) >= 3 and o[0] == 'BUY_PRODUCT' and o[1] == 'WHEAT' and carry > 0:
                    k = min(carry, max(0, int(o[2])))
                    if k > 0:
                        o[2] = int(o[2]) - k; carry -= k; _WCT_REPORT['netted'] += k; changed = True
            market = [o for o in market if not (isinstance(o, list) and len(o) >= 3 and o[0] == 'BUY_PRODUCT'
                                               and o[1] == 'WHEAT' and int(o[2]) <= 0)]
            if carry > 0:
                hit = next((o for o in market if isinstance(o, list) and len(o) >= 3 and o[0] == 'SELL'
                            and o[1] == 'WHEAT'), None)
                if hit is not None:
                    hit[2] = int(hit[2]) + carry
                elif len(market) < MAX_ORDERS:
                    market.append(['SELL', 'WHEAT', carry])
                else:
                    hole = next((i for i, o in enumerate(market) if not o), None)
                    if hole is None:
                        st['carry'] = carry      # no slot: keep carrying, hidden again next turn
                        _WCT_REPORT['skip_slots'] += 1
                        carry = -1
                    else:
                        market[hole] = ['SELL', 'WHEAT', carry]
                if carry > 0:
                    _WCT_REPORT['sold'] += carry; changed = True
                    try:
                        so = _OR2_STATE.get(seat); prev = so.get('prev') if so else None
                        if prev and prev.get('step') == step:
                            own = prev.setdefault('own', {}); own['WHEAT'] = int(own.get('WHEAT', 0)) + carry
                    except Exception:
                        _WCT_REPORT['errors'] += 1
            if carry >= 0:
                st['carry'] = 0
        # open a new lot on a draw turn
        shops = list((observation.get('town') or {}).get('unlocked_shops') or [])
        if _WCT_FROM <= step <= _WCT_LAST and step % 4 == 0 and st.get('carry', 0) == 0:
            draw = _wct_draw(shops, step)
            view = FarmView(observation)
            stock = projected_shed(dict(action, market=market), view)
            sold_w = bought_w = 0
            for o in market:
                if isinstance(o, list) and len(o) >= 3 and o[1] == 'WHEAT':
                    if o[0] == 'SELL':
                        sold_w += max(0, int(o[2]))
                    elif o[0] == 'BUY_PRODUCT':
                        bought_w += max(0, int(o[2]))
            sold_w = min(sold_w, int(stock.get('WHEAT', 0)))
            parent_wheat = int(stock.get('WHEAT', 0)) - sold_w + bought_w
            after_market = sum(max(0, int(v)) for v in stock.values())
            for o in market:
                if isinstance(o, list) and len(o) >= 3 and o[0] == 'SELL':
                    after_market -= min(max(0, int(o[2])), int(stock.get(o[1], 0)))
                elif isinstance(o, list) and len(o) >= 3 and o[0] in ('BUY_PRODUCT', 'BUY_ANIMAL'):
                    after_market += max(0, int(o[2]))
            carried = sum(max(0, int(v)) for inv in ((observation.get('private') or {}).get('inventories') or [])
                          for v in (inv or {}).values())
            room = 100 - after_market - carried - _WCT_ROOM
            money = float(observation['farms'][seat].get('money', 0) or 0)
            cash = money - _wct_costs(observation, market) - _WCT_RESERVE
            inv = int(observation['market']['inventory'].get('WHEAT', 10000)) - bought_w + sold_w
            price = max(1, int(observation['market']['prices'].get('WHEAT', 25) or 25))
            n = min(_WCT_MAX, room, int(cash // (price + 8)))
            if draw <= 0 or len(market) >= MAX_ORDERS:
                if len(market) >= MAX_ORDERS:
                    _WCT_REPORT['skip_slots'] += 1
            elif n < _WCT_MIN:
                _WCT_REPORT['skip_room' if room < _WCT_MIN else 'skip_cash'] += 1
            else:
                g = _wct_gain(inv, draw, n)
                if g >= _WCT_MIN_GAIN:
                    market.append(['BUY_PRODUCT', 'WHEAT', n])
                    st['pending'] = {'step': step, 'n': n, 'parent_wheat': parent_wheat}
                    _WCT_REPORT['buys'] += 1; _WCT_REPORT['bought'] += n; _WCT_REPORT['gain_est'] += g
                    changed = True
        if changed:
            return dict(action, market=market[:MAX_ORDERS])
        return action
    except Exception:
        _WCT_REPORT['errors'] += 1
        st['pending'] = None
        return action


final_wct_submission_entry = _wct_agent
# ---- JFJH-EOD day-end shed guard (2026-09-28, own code) -------------------------------------------------------
# At the end of every day the engine pours every unit's cargo into the shed and destroys what does not fit.  On the
# ladder x4kdrtw lost 6.6 units a game this way (75 real games; mostly day 23: the units still carry ~90 units at
# hour 23 while the hour-23 market buys next morning's wheat and fertilizer into the nearly empty shed, so the
# pour then overflows by ~18 and destroys wool, strawberries, eggs, tomatoes...).  The chassis' own room guard is
# switched off in this build, and selling cannot help at hour 23 because the cargo is not in the shed yet.  This
# layer trims hour-23 BUY_PRODUCT orders (fertilizer first, then wheat) by the projected overflow of the pour and
# re-buys the trimmed units at hours 0-3 of the next day once there is room (sells first, the deferred buy at the
# end of the queue); whatever is still missing after hour 3 is dropped and counted.
_EOD_CAP = 100
_EOD_TRIM_ORDER = ('FERTILIZER', 'WHEAT')
_EOD_RETRY_HOURS = 3
_EOD_STATE = {}
_EOD_REPORT = {'trim_turns': 0, 'trimmed': 0, 'rebought': 0, 'dropped': 0, 'errors': 0}
_EOD_PARENT = [v for v in list(globals().values()) if callable(v)][-1]


def _eod_total_after(obs, action):
    """Shed total after this turn's unit actions, market and (at hour 23) the cargo pour."""
    seat = int(obs['player']); farm = obs['farms'][seat]; private = obs['private']
    pos = [farm['farmer']] + list(farm['hands'])
    units = [action.get('farmer') or ['PASS']] + list(action.get('hands') or [])
    shed = {k: max(0, int(v)) for k, v in private['shed'].items()}
    carried = sum(max(0, int(n)) for inv in private['inventories'] for n in (inv or {}).values())
    produced = consumed = 0
    for i in range(min(len(units), len(pos))):
        a = units[i]
        if not a:
            continue
        x, y = pos[i]; tile = farm['tiles'][y][x]
        if a[0] == 'HARVEST' and isinstance(tile, dict):
            produced += max(0, int(tile.get('yield_units', 0) or 0))
        elif a[0] == 'COLLECT_FERTILIZER' and isinstance(tile, dict) and tile.get('fertilizer_available'):
            produced += 1
        elif a[0] in ('FEED', 'FERTILIZE'):
            consumed += 1
        elif a[0] == 'PLACE' and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
            consumed += 1
    projected = projected_shed(action, FarmView(obs))
    sells = buys = 0
    for o in action.get('market') or []:
        if not o or len(o) < 3:
            continue
        if o[0] == 'SELL':
            q = min(max(0, int(o[2])), max(0, int(projected.get(o[1], 0))))
            projected[o[1]] = projected.get(o[1], 0) - q
            sells += q
        elif o[0] in ('BUY_PRODUCT', 'BUY_ANIMAL'):
            buys += max(0, int(o[2]))
    return sum(shed.values()) + carried + produced - consumed + buys - sells


def _eod_agent(observation, configuration=None):
    action = _EOD_PARENT(observation, configuration)
    try:
        step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
        st = _EOD_STATE.get(seat)
        if st is None or step <= st.get('step', -1):
            st = _EOD_STATE[seat] = {'step': -1, 'deferred': {}, 'day': -1}
            if step == 0:
                for k in _EOD_REPORT:
                    _EOD_REPORT[k] = 0
        st['step'] = step
        if not isinstance(action, dict) or not _v18_standard(configuration):
            return action
        day, hour = divmod(step, 24)
        market = [list(o) if isinstance(o, (list, tuple)) else o for o in (action.get('market') or [])]
        changed = False
        # re-buy what was trimmed last night, at the end of the queue, within the room left this turn
        if st['deferred'] and day == st['day'] + 1:
            if hour <= _EOD_RETRY_HOURS:
                shed = observation['private']['shed']
                total_now = sum(max(0, int(v)) for v in shed.values())
                projected = projected_shed(dict(action, market=market), FarmView(observation))
                room = _EOD_CAP - sum(max(0, int(v)) for v in projected.values())
                for o in market:
                    if isinstance(o, list) and len(o) >= 3:
                        if o[0] == 'SELL':
                            room += min(max(0, int(o[2])), max(0, int(projected.get(o[1], 0))))
                        elif o[0] in ('BUY_PRODUCT', 'BUY_ANIMAL'):
                            room -= max(0, int(o[2]))
                for item in list(st['deferred']):
                    q = min(st['deferred'][item], max(0, room))
                    if q <= 0:
                        continue
                    hit = next((o for o in market if isinstance(o, list) and len(o) >= 3 and o[0] == 'BUY_PRODUCT' and o[1] == item), None)
                    if hit is not None:
                        hit[2] = int(hit[2]) + q
                    elif len(market) < MAX_ORDERS:
                        market.append(['BUY_PRODUCT', item, q])
                    else:
                        continue
                    st['deferred'][item] -= q; room -= q; changed = True
                    _EOD_REPORT['rebought'] += q
                    if st['deferred'][item] <= 0:
                        del st['deferred'][item]
            else:
                _EOD_REPORT['dropped'] += sum(st['deferred'].values())
                st['deferred'] = {}
        # trim tonight's buys to what the pour leaves room for
        if hour == 23 and day <= 28:
            over = _eod_total_after(observation, dict(action, market=market)) - _EOD_CAP
            if over > 0:
                for item in _EOD_TRIM_ORDER:
                    for o in market:
                        if over <= 0:
                            break
                        if isinstance(o, list) and len(o) >= 3 and o[0] == 'BUY_PRODUCT' and o[1] == item and int(o[2]) > 0:
                            k = min(int(o[2]), over)
                            o[2] = int(o[2]) - k; over -= k
                            st['deferred'][item] = st['deferred'].get(item, 0) + k
                            _EOD_REPORT['trimmed'] += k; changed = True
                if changed:
                    st['day'] = day
                    _EOD_REPORT['trim_turns'] += 1
        if changed:
            return dict(action, market=market[:MAX_ORDERS])
        return action
    except Exception:
        _EOD_REPORT['errors'] += 1
        return action


final_eod_submission_entry = _eod_agent

# ---- JFJH-V22D (2026-09-27, diagnostic): third-party layer, Apache-2.0 ---------------------------------------
# Verbatim copy of "counter D" from the public Kaggle notebook "Your Market List Is an Order Book" (renji_starfall /
# shiiin9 lineage, V55 base, Apache-2.0; agent sha256 a16e0e9b...).  It reorders the final market list: SELLs may take
# any slot held by a SELL or a fixed-price order, scored with the V44y per-unit lockstep evaluator against the list the
# stack produced before this layer (exact against a copy of the same list).  Uses the chassis' own _v44y_* helpers.
# ==== counter D: exact best-response ordering against a copy of ourselves (shiiin9, 2026-09-18) ====
# Supersedes layer A's fixed rule.  Against a V48 clone the rival's market list is exactly the
# list this stack produces before D touches it (same tape, same production, same market layers),
# so `_v44y_factor_margin` - V48's own per-unit lockstep evaluator - scores any ordering of our
# own list exactly.  V48 already uses it, but only permutes contiguous runs of 2-6 SELLs; it never
# moves a SELL past a HIRE/BUY_SEED/BUY_ANIMAL/BUY_LAND, which is where layer A found its wins.
#
# Search space: the slots held by SELLs and fixed-price orders.  SELLs may take any of them (any
# order); the fixed-price orders keep their relative order in the slots that are left.  Held fixed:
# BUY_PRODUCT (the turn-0/1 openings depend on its index), wash SELLs of an item the list also
# buys, and V48's deliberate empty slots.  Selling earlier only adds cash before a purchase, so a
# fixed-price order never moves earlier than it already is.
# Budgeted: at most _CXD_BUDGET scored orderings per turn, and the original ordering scores 0, so
# a change needs a strictly positive gain.
import itertools as _cxd_it
_CXD_HOST = [v for v in list(globals().values()) if callable(v)][-1]
_CXD_FIXED = ('HIRE', 'BUY_SEED', 'BUY_ANIMAL', 'BUY_LAND')
_CXD_BUDGET = 800
_CXD_FROM = 0
_CXD_REPORT = {'cxd_turns': 0, 'cxd_gain': 0.0, 'cxd_evals': 0, 'cxd_budget_hits': 0, 'cxd_errors': 0}
# Rival order lists to be robust against, refreshed each turn by the identification layer
# below this one. Empty means "assume the rival plays our own list", which is exact against
# a V48 copy; with several entries an ordering is scored by its worst case among them.
_CXD_MODELS = []
# The list this stack produced before D touched it. Against a V48 copy that IS the rival's
# list, so layers above D (which see an already reordered list) must model the rival with
# this, not with our reordered one.
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


def _cxd_agent(observation, configuration=None):
    action = _CXD_HOST(observation, configuration)
    try:
        if int(observation.get('step', 0)) == 0:
            _CXD_REPORT.update(cxd_turns=0, cxd_gain=0.0, cxd_evals=0, cxd_budget_hits=0, cxd_errors=0)
        if int(observation.get('step', 0)) >= _CXD_FROM:
            return _cxd_reorder(observation, action)
    except Exception:
        _CXD_REPORT['cxd_errors'] += 1
    return action

final_v22d_submission_entry = _cxd_agent

_SC29_MODE='population'
"""Factorized exact assignment and iterated responses over executable market slots."""
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
final_sep29_submission_entry=_cxd_agent


_SC29_OPEN_PARENT=final_v22d_submission_entry
def _sc29_open(obs,configuration=None):
 a=_SC29_OPEN_PARENT(obs,configuration)
 if int(obs['step'])==0:return dict(a,market=[['BUY_PRODUCT','WHEAT',9],['SELL','WHEAT',9],['BUY_PRODUCT','WHEAT',4],['BUY_SEED','WHEAT',1]])
 if int(obs['step'])==2 and int(obs['private']['shed'].get('WHEAT',0))<5:
  m=[list(o)for o in a.get('market')or[]];m.append(['BUY_PRODUCT','WHEAT',5-int(obs['private']['shed'].get('WHEAT',0))]);return dict(a,market=m)
 return a
final_sep29_open=_sc29_open
"""Restore affordable planned labour when an opening treasury hits zero."""
_SC29_LIQ_PARENT=[v for v in list(globals().values()) if callable(v)][-1]
_SC29_LIQ_REPORT=dict(turns=0, units=0, errors=0)
def _sc29_liquidity(obs,configuration=None):
    action=_SC29_LIQ_PARENT(obs,configuration)
    try:
        t=int(obs['step'])
        if t==0:_SC29_LIQ_REPORT.update(turns=0,units=0,errors=0)
        if t>=144 or t%24!=0:return action
        market=[list(o)if o else [] for o in action.get('market')or[]]
        hires=sum(bool(o)and o[0]=='HIRE' for o in market)
        if not hires:return action
        farm=obs['farms'][int(obs['player'])];n=int(farm['hires_today']);cost=sum(_WCT_FIB[min(n+j,len(_WCT_FIB)-1)]for j in range(hires));cash=float(farm['money'])
        if cash>=cost or cash>=1:return action
        stock={k:max(0,int(v))for k,v in projected_shed(action,FarmView(obs)).items()};prices=obs['market']['prices']
        # Existing sells can already finance the hires; leave those actions alone.
        if any(len(o)>2 and o[0]=='SELL' and min(stock.get(o[1],0),int(o[2]))>0 for o in market):return action
        slots=[i for i,o in enumerate(market)if not o]
        if len(market)>=MAX_ORDERS and not slots:return action
        need=cost-cash+1
        for item in ('FERTILIZER','MILK','WOOL','EGG','CARROT','STRAWBERRY','MELON','TOMATO','WHEAT'):
            available=stock.get(item,0)
            if available<=0:continue
            # Keep at least one wheat after this turn's actual pickups.
            if item=='WHEAT':available=max(0,available-1)
            price=int(prices.get(item,0))
            if available<=0 or price<=1:continue
            q=min(available,max(1,int((need+max(1,price-2)-1)//max(1,price-2))))
            if q*max(1,price-2)<need:continue
            if len(market)>=MAX_ORDERS:del market[slots[-1]]
            market.insert(0,['SELL',item,q]);out=dict(action,market=market)
            _xrl_sync(obs,out,{item:q});_v18_sync_ledgers(obs,action,out)
            _SC29_LIQ_REPORT['turns']+=1;_SC29_LIQ_REPORT['units']+=q
            return out
    except Exception:_SC29_LIQ_REPORT['errors']+=1
    return action
final_sep29_liquidity_entry=_sc29_liquidity
