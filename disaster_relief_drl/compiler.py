import re
RES={'WATER','FOOD','MEDICAL_KIT','SHELTER','BLANKET','RESCUE_BOAT','MEDICINE'}
def compile_drl(source):
 lines=[s.strip() for s in source.splitlines() if s.strip() and not s.strip().startswith('#')]
 tokens=[]; syn=[]; sem=[]; disaster=None; inventory={}; alloc=[]
 for no,line in enumerate(lines,1):
  for v in re.findall(r'"[^"]*"|[A-Za-z_][A-Za-z_0-9]*|\\d+|;',line):
   typ='LOCATION' if v.startswith('"') else 'NUMBER' if v.isdigit() else 'TERMINATOR' if v==';' else 'KEYWORD' if v.upper() in {'DISASTER','AT','PRIORITY','RESOURCE','ALLOCATE','TO','HIGH','MEDIUM','LOW'} else 'IDENTIFIER'
   tokens.append({'line':no,'value':v.strip('"'),'type':typ})
  m=re.fullmatch(r'DISASTER\\s+([A-Z_]+)\\s+AT\\s+"([^"]+)"\\s+PRIORITY\\s+(HIGH|MEDIUM|LOW)\\s*;',line,re.I)
  if m:
   disaster={'type':m[1].upper(),'location':m[2],'priority':m[3].upper()}; continue
  m=re.fullmatch(r'RESOURCE\\s+([A-Z_]+)\\s+(\\d+)\\s*;',line,re.I)
  if m:
   r,q=m[1].upper(),int(m[2])
   if r not in RES:sem.append(f'Line {no}: unknown resource {r}.')
   elif q<=0:sem.append(f'Line {no}: quantity must be positive.')
   elif r in inventory:sem.append(f'Line {no}: duplicate resource {r}.')
   else:inventory[r]=q
   continue
  m=re.fullmatch(r'ALLOCATE\\s+([A-Z_]+)\\s+(\\d+)\\s+TO\\s+"([^"]+)"\\s*;',line,re.I)
  if m:alloc.append({'resource':m[1].upper(),'quantity':int(m[2]),'location':m[3],'line':no});continue
  syn.append(f'Line {no}: invalid command syntax; check format and semicolon.')
 if not disaster:sem.append('Missing DISASTER declaration.')
 totals={}
 for a in alloc:
  totals[a['resource']]=totals.get(a['resource'],0)+a['quantity']
  if a['resource'] not in inventory:sem.append(f"Line {a['line']}: {a['resource']} is not declared.")
  if a['quantity']<=0:sem.append(f"Line {a['line']}: allocation must be positive.")
  if disaster and a['location'].lower()!=disaster['location'].lower():sem.append(f"Line {a['line']}: destination must match {disaster['location']}.")
 for r,q in totals.items():
  if r in inventory and q>inventory[r]:sem.append(f'Insufficient {r}: requested {q}, available {inventory[r]}.')
 ok=not syn and not sem; merged={}
 if ok:
  for a in alloc:
   k=(a['resource'],a['location']);merged[k]=merged.get(k,0)+a['quantity']
 optimized=[{'resource':k[0],'location':k[1],'quantity':q} for k,q in merged.items()]
 drir=[f'LOAD {r} {q}' for r,q in inventory.items()]+[f"DISPATCH {a['resource']} {a['quantity']} TO {a['location']}" for a in optimized]
 target=[f"Dispatch {a['quantity']} units of {a['resource'].replace('_',' ').title()} to {a['location']}." for a in optimized]
 phases=[
 {'name':'1. Lexical Analysis','status':'Passed' if tokens else 'Empty','description':'Converts source into tokens: keywords, identifiers, locations, numbers and terminators.','data':tokens},
 {'name':'2. Syntax Analysis','status':'Passed' if not syn else 'Failed','description':'Checks statements against DRL grammar.','data':syn or ['All statements follow the expected structure.']},
 {'name':'3. Semantic Analysis','status':'Passed' if ok else 'Failed','description':'Validates resource types, quantities and destination constraints.','data':syn+sem or ['Resource and destination rules are valid.']},
 {'name':'4. Intermediate Code Generation','status':'Generated' if ok else 'Blocked','description':'Creates Disaster Relief Intermediate Representation (DRIR).','data':drir if ok else ['Fix errors to generate DRIR.']},
 {'name':'5. Code Optimization','status':'Optimized' if ok else 'Blocked','description':'Merges matching allocations for the destination.','data':[f"{a['resource']} → {a['quantity']} → {a['location']}" for a in optimized] or ['Waiting for valid input.']},
 {'name':'6. Target Code Generation','status':'Generated' if ok else 'Blocked','description':'Produces readable dispatch instructions.','data':target or ['Waiting for valid input.']}]
 return {'success':ok,'phases':phases,'errors':syn+sem,'inventory':inventory,'allocations':optimized,'target_code':target,'drir':drir if ok else [],'summary':{'resources_declared':len(inventory),'allocation_lines':len(alloc),'dispatch_items':len(optimized)}}
