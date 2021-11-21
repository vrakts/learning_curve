import os  # for the ability to use os function like clearing the screen buffer
import sys  # for the ability to use system functions like exit
from itertools import chain  # for the ability to concatenate lists

greek_codes   = chain(range(0x370, 0x3e2), range(0x3f0, 0x400))
greek_symbols = (chr(c) for c in greek_codes)
greek_letters = [c for c in greek_symbols if c.isalpha()]


answer_term = "no"
ton_exeis_mikro = "false"
try :
 while answer_term == "no" :
  if ton_exeis_mikro == "false" :
   keimeno = "Δώσε πράμα: "
  else :
   keimeno = "Δώσε μεγαλύτερο πράμα ...: "
  trans_text = input(keimeno)
  os.system('cls')
  posa_vrikes = 0
  if len(trans_text) > 2 :
   ton_exeis_mikro = "false"
   # total = len(greek_letters)
   i = 1
   for i in range(len(trans_text)) :
    for c in greek_letters :
     if trans_text[i] == c :
      posa_vrikes += 1
      if trans_text[i:].find(' ') >= 0 :
       leksi = trans_text[trans_text[:i].rfind(' ')+1:trans_text[i:].find(' ')+i]
      else :
       leksi = trans_text[trans_text[:i].rfind(' ')+1:]
      print("Βρήκα το " + c + " στη λέξη " + leksi + " θέση " + str(i + 1))
   if posa_vrikes == 0 :
    print("Είσαι 'νταξ' ...")
   print("")
  else :
   ton_exeis_mikro = "true"
   # print("Είσαι 'νταξ' ...")
except KeyboardInterrupt as e :
 os.system('cls')
 print("Ρε μην τον παίζεις έχουμε δουλειά !")
 input("Τι να σε κάνω. Πάτα οποιοδήποτε κουμπι για να τελειώσεις...!")
 sys.exit(0)

