import os  # for the ability to use os function like clearing the screen buffer
import sys  # for the ability to use system functions like exit
from itertools import chain  # for the ability to concatenate lists
import clipboard  # for the ability to read and wrtie from the clipboard 

greek_codes   = chain(range(0x370, 0x3e2), range(0x3f0, 0x400))
greek_symbols = (chr(c) for c in greek_codes)
greek_letters = [c for c in greek_symbols if c.isalpha()]

answer_term = "no"
ton_exeis_mikro = "false"
try :
 while answer_term == "no" :
  if ton_exeis_mikro == "false" :
   keimeno = "Μετάφρασε πράμα: "
  else :
   keimeno = "Μετάφρασε μεγαλύτερο πράμα ...: "
  trans_text = input(keimeno)
  os.system('cls')
  posa_vrikes = 0
  if len(trans_text) > 2 :
   ton_exeis_mikro = "false"
   i = 1
   trans_auth = trans_text
   if trans_text.find('  ') >= 0 :
    print("Βρήκα: '  '")
    trans_text = trans_text.replace('  ', ' ')
    posa_vrikes += 1
   if trans_text.find('Α') >= 0 :
    print("Βρήκα: 'Α'")
    trans_text = trans_text.replace('Α', 'A')
    posa_vrikes += 1
   if trans_text.find('Β') >= 0 :
    print("Βρήκα: 'Β'")
    trans_text = trans_text.replace('Β', 'B')
    posa_vrikes += 1
   if trans_text.find('Γ') >= 0 :
    print("Βρήκα: 'Γ'")
    trans_text = trans_text.replace('Γ', 'G')
    posa_vrikes += 1
   if trans_text.find('Δ') >= 0 :
    print("Βρήκα: 'Δ'")
    trans_text = trans_text.replace('Δ', 'D')
    posa_vrikes += 1
   if trans_text.find('Ε') >= 0 :
    print("Βρήκα: 'Ε'")
    trans_text = trans_text.replace('Ε', 'E')
    posa_vrikes += 1
   if trans_text.find('Ζ') >= 0 :
    print("Βρήκα: 'Ζ'")
    trans_text = trans_text.replace('Ζ', 'Z')
    posa_vrikes += 1
   if trans_text.find('Η') >= 0 :
    print("Βρήκα: 'Η'")
    trans_text = trans_text.replace('Η', 'H')
    posa_vrikes += 1
   if trans_text.find('Ι') >= 0 :
    print("Βρήκα: 'Ι'")
    trans_text = trans_text.replace('Ι', 'I')
    posa_vrikes += 1
   if trans_text.find('Κ') >= 0 :
    print("Βρήκα: 'Κ'")
    trans_text = trans_text.replace('Κ', 'K')
    posa_vrikes += 1
   if trans_text.find('Λ') >= 0 :
    print("Βρήκα: 'Λ'")
    trans_text = trans_text.replace('Λ', 'L')
    posa_vrikes += 1
   if trans_text.find('Μ') >= 0 :
    print("Βρήκα: 'Μ'")
    trans_text = trans_text.replace('Μ', 'M')
    posa_vrikes += 1
   if trans_text.find('Ν') >= 0 :
    print("Βρήκα: 'Ν'")
    trans_text = trans_text.replace('Ν', 'N')
    posa_vrikes += 1
   if trans_text.find('Ξ') >= 0 :
    print("Βρήκα: 'Ξ'")
    trans_text = trans_text.replace('Ξ', 'X')
    posa_vrikes += 1
   if trans_text.find('Ο') >= 0 :
    print("Βρήκα: 'Ο'")
    trans_text = trans_text.replace('Ο', 'O')
    posa_vrikes += 1
   if trans_text.find('Π') >= 0 :
    print("Βρήκα: 'Π'")
    trans_text = trans_text.replace('Π', 'P')
    posa_vrikes += 1
   if trans_text.find('Ρ') >= 0 :
    print("Βρήκα: 'Ρ'")
    trans_text = trans_text.replace('Ρ', 'R')
    posa_vrikes += 1
   if trans_text.find('Σ') >= 0 :
    print("Βρήκα: 'Σ'")
    trans_text = trans_text.replace('Σ', 'S')
    posa_vrikes += 1
   if trans_text.find('Τ') >= 0 :
    print("Βρήκα: 'Τ'")
    trans_text = trans_text.replace('Τ', 'T')
    posa_vrikes += 1
   if trans_text.find('Υ') >= 0 :
    print("Βρήκα: 'Υ'")
    trans_text = trans_text.replace('Υ', 'Y')
    posa_vrikes += 1
   if trans_text.find('Φ') >= 0 :
    print("Βρήκα: 'Φ'")
    trans_text = trans_text.replace('Φ', 'F')
    posa_vrikes += 1
   if trans_text.find('Χ') >= 0 :
    print("Βρήκα: 'Χ'")
    trans_text = trans_text.replace('Χ', 'X')
    posa_vrikes += 1
   if trans_text.find('ς') >= 0 :
    print("Βρήκα: 'ς'")
    trans_text = trans_text.replace('ς', 'S')
    posa_vrikes += 1
   if posa_vrikes == 1 :
    print("Σύνολο " + str(posa_vrikes) + " χαρακτήρας.")
   else :
    print("Σύνολο " + str(posa_vrikes) + " χαρακτήρες.")
   print("Ήταν :       " + trans_auth)
   print("Το διόρθωσα: " + trans_text)
   clipboard.copy(trans_text)
   # trans_text = trans_text.replace('Θ', 'TH')
   # trans_text = trans_text.replace('Ψ', 'PS')
   # trans_text = trans_text.replace('Ω', 'O')
   if posa_vrikes == 0 :
    print("Είσαι 'νταξ' ...")
   print("")
  else :
   ton_exeis_mikro = "true"
except KeyboardInterrupt as e :
 os.system('cls')
 print("Ρε μην τον παίζεις έχουμε δουλειά !")
 input("Τι να σε κάνω. Πάτα οποιοδήποτε κουμπι για να τελειώσεις...!")
 sys.exit(0)

