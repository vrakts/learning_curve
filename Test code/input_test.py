import sys
import os
from datetime import date
from datetime import datetime

try :
 operations = []
 i = 0
 answer = " "
 
 while answer != "" :
  answer = input("Paste values (leave empty to terminate process): ")
  answer = answer.replace('•', '').strip()
  operations.append(answer)
 
 for t in operations :
  print(">"+ t + "<")
 
 file = open("comp.txt", "w")
 for l in operations :
  # print(l)
  code = l[:l.find('\t')].strip()
  print(code)
  file.write(code + "\n")
  # file.write(l.replace('Ø', '') + "\n")

 file.close()
except Exception as exc :
 print("Exception: " + str(exc))