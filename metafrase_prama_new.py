import os
import sys  # for the ability to use system functions like exit
from itertools import chain  # for the ability to concatenate lists
import clipboard  # for the ability to read and wrtie from the clipboard 

greek_codes   = chain(range(0x370, 0x3e2), range(0x3f0, 0x400))
greek_symbols = (chr(c) for c in greek_codes)
greek_list = [c for c in greek_symbols if c.isalpha()]
greek_letters = []
for i in range(20, 44) :
 greek_letters.append(greek_list[i])

eng_letters = ['A', 'B', 'G', 'D', 'E', 'Z', 'H', 'TH', 'I', 'K', 'L', 'M', 'N', 'X', 'O', 'P', 'R', 'S', 'T', 'Y', 'F', 'X', 'PS', 'O']

answer_term = "no"
ton_exeis_mikro = "false"
try :
 while answer_term == "no" :
  if ton_exeis_mikro == "false" :
   keimeno = "Μετάφρασε πράμα: "
  else :
   keimeno = "Μετάφρασε μεγαλύτερο πράμα ...: "
  trans_auth = input(keimeno)
  os.system('cls')
  posa_vrikes = 0
  if len(trans_auth) > 2 :
   ton_exeis_mikro = "false"
   # i = 1
   na_ton_valo = []
   for i in range(len(trans_auth)) :
    na_ton_valo.append(' ')
   trans_text = trans_auth
   text_list = list(trans_auth)
   for i in range(len(text_list)) :
    for c in range(len(greek_letters)) :
     if text_list[i] == greek_letters[c] :
      posa_vrikes += 1
      na_ton_valo[i] = "^"
      text_list[i] = eng_letters[c]
      if trans_text[i:].find(' ') >= 0 :
       leksi = trans_text[trans_text[:i].rfind(' ')+1:trans_text[i:].find(' ')+i]
      else :
       leksi = trans_text[trans_text[:i].rfind(' ')+1:]
      print("Βρήκα το " + greek_letters[c] + " στη λέξη " + leksi + " θέση " + str(i + 1))
   trans_text = "".join(text_list)
   if trans_text.find('ς') >= 0 :
    posa_vrikes += 1
    trans_text = trans_text.replace('ς', 'S')
   if trans_text.find('  ') >= 0 :
    print("Βρήκα: '  '")
    posa_vrikes += 1
    trans_text = trans_text.replace('  ', ' ')
   if posa_vrikes == 1 :
    print("Σύνολο " + str(posa_vrikes) + " χαρακτήρας.")
   else :
    print("Σύνολο " + str(posa_vrikes) + " χαρακτήρες.")
   print("")
   na_ton_valo = "".join(na_ton_valo)
   print("Ήταν :       " + trans_auth)
   print("Τους βρήκα:  " + na_ton_valo)
   print("Το διόρθωσα: " + trans_text)
   clipboard.copy(trans_text)
   if posa_vrikes == 0 :
    print("Είσαι 'νταξ' ...")
   print("")
  else :
   ton_exeis_mikro = "true"
except KeyboardInterrupt as e :
 os.system('cls')
 print("Ρε μην τον παίζεις έχουμε δουλειά !")
 input("Τι να σε κάνω. Πάτα οποιοδήποτε κουμπί για να τελειώσεις... !")
 sys.exit(0)
