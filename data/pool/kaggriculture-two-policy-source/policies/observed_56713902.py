
import base64 as _co64,zlib as _coz
_CO30_SOURCES=[__import__('publication_assets').source('policies/observed_56713902_001.py', 'b85z'), __import__('publication_assets').source('policies/observed_56713902_009.py', 'b85z')]
_CO30_AGENTS=[]
for _i,_blob in enumerate(_CO30_SOURCES):
 _ns={'__name__':'contingent_policy_'+str(_i)}
 exec(_coz.decompress(_co64.b85decode(_blob)).decode(),_ns)
 _CO30_AGENTS.append([v for v in _ns.values()if callable(v)][-1])
_CO30_MODE=2
_CO30_CHOICE=None
_SC29_CO_REPORT={'choice':None,'opponent_money':None,'opponent_hands':None,'errors':0}
_CO30_HOME=None
_CO30_SWAP=False
def contingent_two_step_roles(obs,configuration=None):
 global _CO30_CHOICE,_CO30_HOME,_CO30_SWAP
 step=int(obs['step']);p=int(obs['player'])
 if step==0:
  _CO30_SWAP=False;_CO30_CHOICE=None;_CO30_HOME=list(obs['farms'][1-p]['farmer'])
  initial=[policy(obs,configuration)for policy in _CO30_AGENTS]
  return dict(initial[0],market=[list(o)for o in initial[0].get('market',[])if o[:2]!=['BUY_SEED','WHEAT']]+[['BUY_ANIMAL','COW',1]])
 if step==1:
  for policy in _CO30_AGENTS:policy(obs,configuration)
  return {'farmer':['PICKUP','COW',1],'hands':[],'market':[['HIRE']for _ in range(5)]+[['BUY_ANIMAL','COW',1],['BUY_ANIMAL','SHEEP',2]]}
 if _CO30_CHOICE is None:
  rival=obs['farms'][1-p];cash=rival['money'];hands=len(rival['hands'])
  _CO30_CHOICE=int(hands>=5 and list(rival['farmer'])==_CO30_HOME)
  if _CO30_MODE in(0,1):_CO30_CHOICE=_CO30_MODE
  _SC29_CO_REPORT.update(choice=_CO30_CHOICE,opponent_money=cash,opponent_hands=hands,opponent_farmer=rival['farmer'])
 view=obs;roles=None
 if step<24 and len(obs['farms'][p]['hands'])==5 and (_CO30_CHOICE==0 or (step>=6 and _CO30_SWAP)):
  roles=[1,0,2,5,3,4]if _CO30_CHOICE==0 else [0,1,4,3,2,5];positions=[obs['farms'][p]['farmer']]+list(obs['farms'][p]['hands'])
  view=dict(obs);view['farms']=list(obs['farms']);view['farms'][p]=dict(obs['farms'][p],farmer=positions[roles[0]],hands=[positions[i]for i in roles[1:]])
  view['private']=dict(obs['private'],inventories=[obs['private']['inventories'][i]for i in roles])
 action=dict(_CO30_AGENTS[_CO30_CHOICE](view,configuration));hands=[list(x)for x in action.get('hands',[])]
 if step==2:
  orders=[list(o)for o in action.get('market',[])]
  if _CO30_CHOICE==0:
   action['farmer']=['WEST']
   if len(hands)>=3:hands[0]=['PASS'];hands[1]=['NORTH'];hands[2]=['WEST']
   if not any(o[:2]==['BUY_SEED','WHEAT']for o in orders):orders.append(['BUY_SEED','WHEAT',1])
  else:orders.append(['BUY_ANIMAL','SHEEP',1])
  action['market']=orders[:10]
 if _CO30_CHOICE==1 and step in(2,3,4,5)and len(hands)>3:
  hands[3]={2:['PASS'],3:['PICKUP','SHEEP',1],4:['WEST'],5:['PLACE','SHEEP',1]}[step]
  if step==5:
   positions=obs['farms'][p]['hands'];inventories=obs['private']['inventories']
   _CO30_SWAP=positions[1]==positions[3]and inventories[2]==inventories[4]and inventories[2].get('SHEEP',0)>=1
   _SC29_CO_REPORT['exchange_verified']=_CO30_SWAP
   if _CO30_SWAP:hands[1]=['BUILD_PASTURE']
   else:hands[3]=['BUILD_PASTURE'];_SC29_CO_REPORT['errors']+=1
 action['hands']=hands
 if roles is not None:
  virtual=[action.get('farmer',['PASS'])]+hands;actual=[['PASS']for _ in roles]
  for i,k in enumerate(roles):
   if i<len(virtual):actual[k]=virtual[i]
  action['farmer']=actual[0];action['hands']=actual[1:]
 return action
