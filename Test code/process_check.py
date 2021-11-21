# pcheck.py

import psutil

def pcheck(processName):
 for proc in psutil.process_iter():
  try:
   if processName.lower() in proc.name().lower():
    return True
  except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
   pass
   return False;

pname = input("Δώσε όνομα: ")
result = pcheck(pname)

print(result)

