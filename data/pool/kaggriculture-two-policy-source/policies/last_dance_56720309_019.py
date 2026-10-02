"""Bounded H10 value primitives; no policy takeover, orders, hires or game engine.
Cell unit/decay callbacks are supplied from V10's verified native primitives.
Single-cell midnight rule follows kaggle-environments1.32.7 (Apache-2.0).
Caller owns feasible route, inventory-prefix and transport/capacity certificates.
"""
from copy import deepcopy

ONGOING = {'TOMATO': (8,1), 'STRAWBERRY': (10,2)}
SHOPS = {'BAKERY':('EGG','WHEAT'),'PIZZA_SHOP':('MILK','TOMATO','WHEAT'),
         'BRUNCH_SPOT':('EGG','WHEAT','STRAWBERRY'),'YARN_STORE':('WOOL',),
         'ICE_CREAM_SHOP':('STRAWBERRY','MILK','WHEAT'),'PET_CAFE':('CARROT',),
         'SMOOTHIE_SHOP':('STRAWBERRY','MILK'),
         'FARMERS_MARKET':('WHEAT','CARROT','TOMATO','STRAWBERRY')}

def funded_marginal_jobs(jobs, available, added=1):
    """Select by the actual worker's consuming prefix, never by largest EV.

    jobs must already be in execution order, same worker, and exclude/mark
    projected no-ops or r3 guards with consumes=False. Unknown cost => abstain.
    """
    before=max(0,int(available));after=before+max(0,int(added));new=[]
    for index,job in enumerate(jobs):
        if job.get('consumes') is None:return {'known':False,'reason':'unknown_prefix_consumption','jobs':[]}
        if not job['consumes']:continue
        old=before>0;alt=after>0
        before-=int(old);after-=int(alt)
        if alt and not old:new.append(dict(job,index=index))
    return {'known':True,'jobs':new,'unused_additional':max(0,after-before)}

def _refresh_cell(farm,day):
    tile=farm['tiles'][0][0]
    if not isinstance(tile,dict) or tile.get('kind')!='PLANT':return
    was_watered=tile['watered_today'];tile['consecutive_unwatered']=0 if was_watered else tile['consecutive_unwatered']+1;tile['watered_today']=False
    if tile['consecutive_unwatered']>=2:farm['tiles'][0][0]={'kind':'WEED'};return
    first,interval=ONGOING[tile['crop']];after=day+1-tile['planted_day']-first
    if after<0 or after%interval:return
    event=after//interval+1
    if event>4:return
    bonus=2 if was_watered and tile.get('fertilized_until_day',-1)>=day else 1
    tile['yield_units']=min(4,tile['yield_units']+bonus)
    if event==4:tile['max_lifespan_step']=(day+2)*24

def cell_path(tile,start,visits,apply_unit,decay,extra_fert=None,end=719):
    """Real observed tile -> all scheduled harvests until replacement/terminal.

    Every FERT visit must explicitly have funded=True/False. Other workers'
    service on this same cell belongs in visits too, sorted by step/actor.
    extra_fert=(step,actor) changes exactly one unfunded dose, no added work.
    The exact physical primitive runs on a one-cell farm; no movement is modeled.
    """
    if not isinstance(tile,dict) or tile.get('crop') not in ONGOING:return {'known':False,'reason':'unsupported_current_crop'}
    f={'farmer':[0,0],'hands':[],'tiles':[[deepcopy(tile)]]};p={'shed':{},'inventories':[{}],'seeds':{}}
    by={};harvests=[];consumed=[];states={};changed=0
    for v in sorted(visits,key=lambda v:(v['t'],v['actor'])):
        if start<=v['t']<end:by.setdefault(v['t'],[]).append(v)
    for t in range(start,min(719,end)):
        for v in by.get(t,[]):
            cmd=v['cmd'];op=cmd[0] if cmd else 'PASS'
            if op in ('PLANT','BUILD_COOP','BUILD_PASTURE'):
                return {'known':True,'harvests':harvests,'fertilizer_used':consumed,'changed_doses':changed,'stop':t,'states':states,'end_tile':deepcopy(f['tiles'][0][0])}
            if op not in ('WATER','HARVEST','FERTILIZE','DIG'):continue
            if op=='FERTILIZE' and 'funded' not in v:return {'known':False,'reason':'unfunded_future_visit_unknown','at':t}
            original=bool(v.get('funded'));override=(t,v['actor'])==extra_fert
            if override and original:return {'known':False,'reason':'extra_dose_already_funded'}
            p['inventories']=[{'FERTILIZER':int(original or override)}]
            before=p['inventories'][0].copy()
            apply_unit(f,p,0,list(cmd),1,t//24,24,100)
            if p['inventories'][0].get('FERTILIZER',0)<before.get('FERTILIZER',0):
                consumed.append((t,v['actor']));changed+=int(override)
            for item in ONGOING:
                quantity=p['inventories'][0].get(item,0)-before.get(item,0)
                if quantity>0:harvests.append({'step':t,'actor':v['actor'],'item':item,'quantity':quantity})
        decay(f,t)
        if t%24==23:_refresh_cell(f,t//24)
        states[t+1]=deepcopy(f['tiles'][0][0])
    return {'known':True,'harvests':harvests,'fertilizer_used':consumed,'changed_doses':changed,'stop':min(719,end),'states':states,'end_tile':deepcopy(f['tiles'][0][0])}

def sale_schedule(path,deliveries):
    """Require a dated planned deposit+sale and capacity for each harvest.

    deliveries[(harvest_step,actor)]={sale_step,slot,capacity,route_preserved=True}.
    Midnight auto-drop at h23 is after market: earliest sale_step is nextstep.
    These are caller-certified forecasts, never future observed state.
    """
    if not path.get('known'):return {'known':False,'reason':path.get('reason')}
    sales=[]
    for h in path['harvests']:
        d=deliveries.get((h['step'],h['actor']))
        if not d or not d.get('route_preserved') or d.get('capacity',0)<h['quantity']:
            return {'known':False,'reason':'delivery_or_capacity_uncertified','harvest':h}
        minimum=h['step']+1 if d.get('automatic_midnight') else h['step']
        if not minimum<=d.get('sale_step',-1)<=718:return {'known':False,'reason':'no_legal_sale_window','harvest':h}
        sales.append({'step':int(d['sale_step']),'slot':int(d['slot']),'quantity':h['quantity']})
    return {'known':True,'sales':sales}

def bounded_rival_scenario(events,shops):
    """Validate separate lawful supply hypotheses; do not scale event yields.

    production quantities <=2 per natural event; held-yield events <=4/cell;
    hypothetical warehouse lot <=100. Caller schedules legal harvest/delivery
    opportunities and unique source_ids. These bounds do not certify a private
    opponent's actual inventory, service, orders or future investments.
    """
    seen=set();production=set()
    for e in events:
        key=e['source_id']
        if key in seen:raise ValueError('rival source double counted')
        seen.add(key)
        if not 0<=int(e['slot'])<10:raise ValueError('invalid rival market slot')
        if e['kind']=='production':
            event=(e['cycle_id'],int(e['event_index']))
            if not 0<=event[1]<4 or event in production:raise ValueError('production event duplicated/outside finite cycle')
            production.add(event)
        limit={'production':2,'held':4,'warehouse':100}[e['kind']]
        if not 0<=e['quantity']<=limit:raise ValueError('unlawful per-event supply bound')
    if sum(e['quantity'] for e in events if e['kind']=='warehouse')>100:raise ValueError('warehouse scenarios exceed physical capacity')
    if len(shops)>8 or any(s['name'] not in SHOPS or s['step']<0 or s['step']%72 for s in shops):raise ValueError('illegal shop path')
    return {'events':list(events),'shops':list(shops)}

def pair_value(item,start,inventory,own_parent,own_alternative,scenarios,quote,input_cost):
    """Reprice ALL own same-good sales through718 in each common scenario.

    own_parent/alternative include shed+cargo+current-crop held yield+remaining
    committed production ONCE. They are complete sale schedules, not just the
    target crop's marginal units. No asset residue, wage saving or travel charge.
    quote(inventory) uses actual observed public params; actual cost of retained
    FERT (marginal forgone sale, not free input) is provided by caller.
    """
    own=[]
    for events in (own_parent,own_alternative):
        table={}
        for e in events:
            if not start<=e['step']<=718 or e['quantity']<0:raise ValueError('invalid own sale schedule')
            slot=int(e['slot'])
            if not 0<=slot<10:raise ValueError('invalid own market slot')
            key=(e['step'],slot);table[key]=table.get(key,0)+int(e['quantity'])
        own.append(table)
    results=[]
    for scenario in scenarios:
        rival={}
        for e in scenario['events']:
            if e['kind']=='production' and e.get('production_step',start+1)<=start:raise ValueError('past production must be in held yield, not future output')
            if start<=e['step']<=718:
                key=(e['step'],int(e['slot']));rival[key]=rival.get(key,0)+int(e['quantity'])
        incomes=[]
        for arm in (0,1):
            inv=float(inventory);ours=theirs=0.
            for t in range(start,719):
                for slot in range(10):
                    my=own[arm].get((t,slot),0);op=rival.get((t,slot),0)
                    # Same-slot unit quotes are simultaneous; both see the
                    # pre-round price, then successful sales increment inventory.
                    common=min(my,op)
                    for _ in range(common):
                        price=quote(inv);ours+=price;theirs+=price
                        if price>1:inv+=2
                    for is_own,q in ((True,my-common),(False,op-common)):
                        for _ in range(q):
                            price=quote(inv)
                            if is_own:ours+=price
                            else:theirs+=price
                            if price>1:inv+=1
                # Town consumption is after all market orders in the real rule.
                if t%4==0:
                    for unlock in scenario['shops']:
                        if unlock['step']<=t and item in SHOPS[unlock['name']]:inv-=2 if len(SHOPS[unlock['name']])==1 else 1
                if t%24==0:inv-=1
            incomes.append((ours,theirs))
        delta=incomes[1][0]-incomes[0][0]-float(input_cost);rival_delta=incomes[1][1]-incomes[0][1]
        results.append({'own_gain':delta,'rival_gain':rival_delta,'margin_gain':delta-rival_delta,'parent_revenue':incomes[0][0],'alternative_revenue':incomes[1][0]})
    return {'scenarios':results,'minimum_own_gain':min(r['own_gain'] for r in results),'mean_own_gain':sum(r['own_gain'] for r in results)/len(results),'horizon':718,'input_opportunity_cost':input_cost}
