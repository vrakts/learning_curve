# Current version 1.6 beta
#####################
# Changelog v1.6
# - Καλύτερα definitions ιδίως στο load_soup.
# - Αν υπάρχει το αρχείο διαβάζει από εκεί αλλιώς ζητάει URL
# - Σημειώνει αν έχει ελληνική ή αγλλική μετάφραση.
#####################
# Changelog v1.5.1
# - Γράφει και τον τίτλο στο excel.
#####################
# Changelog v1.4
# - Υπολογίζει και τα Crazy προϊόντα και γράφει την αντίστοιχη σήμανση στο excel.
# - Διορθώσεις στο for loop για καλύτερες επιδόσεις.
#####################
# Changelog v1.3
# - Μαζεύει μπόλικα link και τα τρέχει ένα ένα.
#####################
# Changelog v1.2
# - Τώρα το πρόγραμμα μιλάει στα Ελληνικά.
# - Теперь программа говорит по-русски, вероятно, неправильно, хотя.
#####################
# Changelog v1.1
# - Added a test write path for the Manager's PC
# - Enclosed all processes in functions for easy calling.
# - Try and Except for various errors
# - Cosmetic changes.
#####################
# Changelog v1
# - From a category URL check all product descriptions for EN translation.
# - Writes non translated to a file.
#####################
# To Do
# - Αναγνώριση των Crazy links

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
import requests
# import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
from time import time, sleep  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

def get_start_time() :
 global start_time, start_date
 start_time = time()  # set starting time
 today = date.today()  # set starting date
 start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
 print("")
 print("Στον επόμενο τόνο, η μέρα θα είναι: " + start_date)

def get_elapsed_time(e) :
 elapsed_time = time() - start_time
 # print(str(time()))
 # print(str(start_time))
 # print(str(elapsed_time))
 minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
 mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
 seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
 seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
 # formatted_time = str(mins) + "." + str(seconds)
 # print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
 mins = int(mins)
 seconds = int(seconds)
 if mins == 0 and seconds == 0 :
  print("Όσο πάει χειροτερεύει. Τελείωσε σε χρόνο 0")
 else :
  print("Όσο πάει χειροτερεύει. Τελείωσε σε " + str(mins) + " λεπτά και " + str(seconds) + " δευτερόλεπτα (" + str(round(elapsed_time, 2)) + " δευτερόλεπτα).")
 print("")

 if mins > 60:
  hours = int(mins / 60)
 else:
  hours = 0

 if hours > 0:
  rem_mins = (mins % (hours * 60))
 else:
  rem_mins = mins

 if len(str(hours)) == 1:
  hours = "0" + str(hours)
 if len(str(rem_mins)) == 1:
  rem_mins = "0" + str(rem_mins)
 
 formatted_time = str(hours) + ":" + str(rem_mins) + ":" + str(seconds) + " (H:M:S)"
 ws_write.write(0, 5, formatted_time)

def set_files() :
 global write_path, write_file, alt_write_file, wb_write, ws_write
 if os.path.exists("C:\\Users\\manager\\Desktop") == True :
  write_path = ("C:\\Users\\manager\Desktop")
 elif os.path.exists("K:\\SALES\\Stock\\Scripts\\translated") == True :
  write_path = ("K:\\SALES\\Stock\\Scripts\\translated")
 elif os.path.exists("Z:\OneDrive\eShop Stuff\PRODUCT\Product") == True :
  write_path = ("Z:\OneDrive\eShop Stuff\PRODUCT\Product")
 write_file = ('Translate_Needed_' + start_date + '.xls')
 alt_write_file = ('Translate_Needed_alt_' + start_date + '.xls')
 os.chdir(write_path)
 wb_write = xlwt.Workbook()
 ws_write = wb_write.add_sheet("en_exist", cell_overwrite_ok = True)
 ws_write.write(0, 0, "ΚΩΔΙΚΟΣ")
 ws_write.write(0, 1, "ΤΙΤΛΟΣ")
 ws_write.write(0, 2, "GR")
 ws_write.write(0, 3, "EN")
 ws_write.write(0, 4, "CRAZY")

def list_pages() :
 global pages_list
 pages_list = []
 
 if os.path.exists("K:\\SALES\\Stock\\Scripts\\urlcheck.txt") == True :
  print("Το αρχείο urlcheck.txt βρέθηκε. Φορτώνω από εκεί.")
  text_file = open("K:\\SALES\\Stock\\Scripts\\urlcheck.txt","r")
  lines = text_file.readlines()
  for line in lines :
   if line.find("http") == 0 :
    pages_list.append(line.strip())
    print("Πρόσθεσα: " + line.strip())
  text_file.close()
 else :
  print("Δεν βρέθηκε το αρχείο.")
  page_url = input("Δώσε πράμα: ")
  if page_url == "":
   print("Εκκένωσης...")
   sys.exit(1)
  while page_url.find("http") >= 0 :
   pages_list.append(page_url)
   page_url = input("Έ έτσι ξεροσφύρι θα τη βγάλουμε; Δώσε κι άλλο πράμα: ")
  else :
   print("Τα μαζεύω και φεύγω.")

def get_cy_mainpage(page_url) :
 global total_next_pages, cat_page, query_mark, categories, cat_offset_url, crazy_page_soup
 print("Φανταστική σελίδούλα με όνομα:")
 print(page_url)
 start_page_soup = load_soup(page_url, wait, retries, "EL")
 # result = requests.get(page_url, cookies = cookies, headers = headers)
 # webpage = result.content
 # start_page_soup = soup(webpage, "html5lib")
 if crazy_mark == False :
  next_pages_category = start_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})
  try :
   total_next_pages = next_pages_category[len(next_pages_category)-1].text
  except :
   total_next_pages = "1"
  print("Σύνολο σελίδων: " + str(total_next_pages))
  cat_page, query_mark, categories = str(page_url).partition("?")
  cat_offset_url = cat_page + query_mark + "offset=" + str(offset) + "&" + categories
 else :
  crazy_page_soup = start_page_soup.findAll('table', {'class': 'crazy-container'})
  total_next_pages = "1"
 # print("")
 # print("Offset page: " + cat_offset_url)

def get_total_products() :
 global total_prod, tp
 if crazy_mark == False :
  last_offset = (int(total_next_pages) - 1) * 10
  last_cat = cat_page + query_mark + "offset=" + str(last_offset) + "&" + categories
  # result = requests.get(last_cat, cookies = cookies, headers = headers)
  # webpage = result.content
  # last_page_soup = soup(webpage, "html5lib")
  last_page_soup = load_soup(last_cat, wait, retries, "EL")
  last_prod = last_page_soup.findAll('table', {'class': 'web-product-container'})
  total_prod = len(last_prod) + last_offset
 else :
  # result = requests.get(page, cookies = cookies, headers = headers)
  # webpage = result.content
  # crazy_page_soup = soup(webpage, "html5lib")
  crazy_page_soup = load_soup(page, wait, retries, "EL")
  last_prod = crazy_page_soup.findAll('table', {'class': 'crazy-container'})
  total_prod = len(last_prod)
 tp = total_prod
 print("Βρήκα " + str(total_prod) + " προϊόντα. Τα κεφάλια μέσα.")
 print("")

def load_soup(page, wait, retries, lang) :
 attempt = 0
 while attempt < retries :
  try :
   if lang == "EN":
    result = requests.get(page, cookies = cookies, headers = headers)
   else:
    result = requests.get(page, headers = headers)
   webpage = result.content
   page_soup = soup(webpage, "html5lib")
   break
  except Exception as exc :
   print("")
   print("Στο φόρτωμα της σελίδας, πέσαμε πάνω στο:")
   print(str(exc))
   print("Ξαναπροσπαθώ σε " + str(retries)+ ".")
   sleep(wait)
   attempt += 1
 if attempt == retries :
  print("Προσπάθησα " + str(attempt) + " φορές και δεν τα κατάφερα.")
  input()
  sys.exit(0)
 
 return(page_soup)

#def get_cy_details(container, e) :
def get_cy_details(container) :
 global cy_code, en_title, en_desc_text, translated, gr_desc, prod_page_soup_el
 translated = False
 gr_desc = False
 if crazy_mark == True :
  cy_code = container.find('tr', {'class' : 'crazy-title-row'}).span.text.strip()
 else :
  cy_code = container.font.text.replace("(", "").replace(")", "")
 a_page = "https://www.e-shop.cy/product?id=" + cy_code
 # result = requests.get(a_page, cookies = cookies, headers = headers)  # with cookies plz
 # webpage = result.content
 # prod_page_soup = soup(webpage, "html5lib")
 prod_page_soup_en = load_soup(a_page, wait, retries, "EN")
 en_title = prod_page_soup_en.h1.text.strip()
 en_desc_text = ""
 en_d_soup = prod_page_soup_en.find('div', {'id': 'mobile_desc'})
 en_product_table_title = prod_page_soup_en.find('td', {'class': 'product_table_title'})
 if en_d_soup == None or en_d_soup.text.find('Σύνολο ψήφων') > 0 or en_product_table_title.text.strip() != "Description" :
  en_desc_text = ""
  translated = False
  # print("Το " + cy_code + " δεν έχει ελληνική ούτε αγγλική περιγραφή.")
 else :
  en_desc_text = en_d_soup.decode_contents().strip()
  if en_desc_text.find('Product description is temporary unavailable in English') >= 0 :
   translated = False
   # print("Το " + cy_code + " έχει ελληνική και δεν έχει αγγλική περιγραφή.")
   # print("e = " + str(e))
  else :
   translated = True
   # print("Το " + cy_code + " έχει αγγλική περιγραφή.")
 
 gr_desc_text = ""
 if selection == "":
  gr_desc = True
  prod_page_soup_el = ""
 elif selection == "EL":
  prod_page_soup_el = load_soup(a_page, wait, retries, "EL")
  gr_d_soup = prod_page_soup_el.find('div', {'id': 'mobile_desc'})
  gr_product_table_title = prod_page_soup_el.find('td', {'class': 'product_table_title'})
  if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text.strip() != "Περιγραφή" :
   gr_desc_text = ""
   gr_desc = False
   # print("Το " + cy_code + " δεν έχει ελληνική περιγραφή.")
  else :
   gr_desc = True
   # print("Το " + cy_code + " έχει ελληνική περιγραφή.")

 if gr_desc == False and translated == False:
  print("Το " + cy_code + " δεν έχει ούτε ελληνική ούτε αγγλική περιγραφή.")
 elif gr_desc == True and translated == True:
  print("Το " + cy_code + " έχει ελληνική και αγγλική περιγραφή.")
 elif gr_desc == True and translated == False:
  print("Το " + cy_code + " έχει ελληνική και δεν έχει αγγλική περιγραφή.")
 elif gr_desc == False and translated == True:
  print("Το " + cy_code + " δεν έχει ελληνική και έχει αγγλική περιγραφή.")

 print("")
 # return(e)

def write_results(e) :
 print("Γράφω: " + cy_code)
 ws_write.write(e, 0, cy_code)
 print("Γράφω: " + en_title)
 ws_write.write(e, 1, en_title)
 if selection == "EL":
  if gr_desc == False:
   gr_desc_value = "NO GR"
  else:
   gr_desc_value = "OK"
 else:
  gr_desc_value = "-"
 print("Γράφω: " + gr_desc_value)
 ws_write.write(e, 2, gr_desc_value)
 if translated == False:
  translate_value = "NO EN"
 else:
  translate_value = "OK"
 print("Γράφω: " + translate_value)
 ws_write.write(e, 3, translate_value)
 if page.find("crazysundays") >= 0 :
  crazy_value = "CRAZY"
 else :
  crazy_value = "-"
 print("Γράφω: " + crazy_value)
 ws_write.write(e, 4, crazy_value)
 print("Γράφω: " + warranty_text)
 if warranty_text != "":
  ws_write.write(e, 5, warranty_text)
 else:
  ws_write.write(e, 5, "-")
 print("")

def write_it_down() :
 try :
  wb_write.save(write_file)
  print(write_file + ", το έχω γραμμένο στο " + write_path)
 except :
  wb_write.save(alt_write_file)
  print("Πιθανώς κάποιος παίζει με το αρχείο. Προχωράω στο παρασύνθημα.")
  print(alt_write_file + ", το έχω γραμμένο στο " + write_path)

def initialize():
 answer = "YES"
 cookies = {'language': 'en'}
 headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
 wait = 5
 retries = 3
 attempt = 0
 crazy_mark = False
 e = 1
 return(answer, cookies, headers, wait, retries, attempt, crazy_mark, e)

def aarrg() :
 war_selection = False
 selection = ""
 if len(sys.argv) > 1 :
  for arg in sys.argv :
   selection = ""
   if arg.find("-el") == 0 or arg.find("-EL") == 0 :
    selection = "EL"
    print("Βρήκα '" + selection + "'. Θα ψάξω και στα ελληνικά.")
   
   if arg.find("-war") == 0 or arg.find("-WAR") == 0 :
    print("Βρήκα 'WAR'. Θα γίνει πόλεμος εγγύησης αλά ελληνικά.")
    war_selection = True
    selection = "EL"
 else:
  selection = ""
  war_selection = False
 
 return(selection, war_selection)

def get_warranty(page_soup) :
 global warranty_text
 warranty_text = ""
 cy_desc_text = ""
 cy_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 cy_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if cy_d_soup == None or cy_d_soup.text.find('Σύνολο ψήφων') > 0 or cy_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  cy_desc_text = ""
 else :
  cy_desc_text = cy_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html values and any .gr mentions
  if cy_desc_text.find('Eγγύηση') >= 0:
   string, warranty, rest = cy_desc_text.rpartition('Eγγύηση:')
  elif cy_desc_text.find('Εγγύηση') >= 0:
   string, warranty, rest = cy_desc_text.rpartition('Εγγύηση:')
  warranty_text = rest.strip().replace('<a class="navy_link" href="https://www.e-shop.cy/support#doa">DOA 7 ημερών</a>', '')
 
try :
 answer, cookies, headers, wait, retries, attempt, crazy_mark, e = initialize()
 selection, war_selection = aarrg()
 # print("selection: " + selection)
 get_start_time()
 set_files()
 list_pages()
 print("")
 for page in pages_list :
  offset = 0  # starting offset value set to 0 and in each for loop, 10 will be added
  if page.find("crazysundays") >= 0 :
   crazy_mark = True
  else :
   crazy_mark = False
  get_cy_mainpage(page)
  print("")
  get_total_products()
  for q in range(0, int(total_next_pages)) :
   single_page_soup = load_soup(cat_offset_url, wait, retries, "GR")
   if crazy_mark == False :
    containers = single_page_soup.findAll('table', {'class': 'web-product-container'})
   else :
    containers = single_page_soup.findAll('table', {'class': 'crazy-container'})
   
   for container in containers :
    attempt = 0
    tp = tp - 1
    if total_prod - (total_prod - tp) > 0 :
     print("Τα πίνω με το: " + str(total_prod - tp) + "/" + str(total_prod) + ". Έχω ακόμα: " + str(total_prod - (total_prod - tp)))
    else :
     print("Τα πίνω με το: " + str(total_prod - tp) + "/" + str(total_prod) + ".")
    while attempt < 3 :
     try :
      # e = get_cy_details(container, e)
      get_cy_details(container)
      if prod_page_soup_el != "":
       get_warranty(prod_page_soup_el)
      else:
       pass
      # print("Translated: " + str(translated))
      # print("gr_desc: " + str(gr_desc))
      if war_selection == True:
       write_results(e)
       e += 1
      elif translated == False or gr_desc == False:
       write_results(e)
       e += 1
      break
     except Exception as exc :
      print("")
      print("Όχι ρε φίλε. Μόλις σκόνταψα γιατί:")
      print(str(exc))
      print("Κάτσε να σκουπιστώ και ξαναπροσπαθώ σε 3 δεύτερα.")
      attempt += 1
      sleep(5)
     if attempt >= 3 :
      print("")
      print("Ρε φίλε προσπάθησα 3 φορές. Φαίνεται δεν ταιριάζουμε. Να περάσει ο επόμενος.")
      print("")
      continue
   if crazy_mark == True :
    continue
   else :
    offset += 10
    cat_offset_url = cat_page + query_mark + "offset=" + str(offset) + "&" + categories
  
 get_elapsed_time(e)
 # print("e: " + str(e))
 if e > 1:
  write_it_down()
 else:
  pass
 found = e - 1
 if found > 1 :
  input("Βρήκα " + str(found) + " να κοιμούνται. Παίξε λίγο με το πράμα σου για να κλείσω.")
 elif found == 1 :
  input("Βρήκα " + str(found) + " να κοιμάται. Παίξε λίγο με το πράμα σου για να κλείσω.")
 elif found == 0 :
  input("Είσαι 'νταξ'. Δεν κοιμάται κανένας τους. Παίξε λίγο με το πράμα σου για να κλείσω.")
 print("")
except KeyboardInterrupt as exc :
 # os.system('cls')
 print("")
 print("Ρε μην τον παίζεις έχουμε δουλειά!")
 try:
  input("Τι να σε κάνω; Πάτα οποιοδήποτε κουμπί για να τελειώσεις... !")
  print("")
  sys.exit(0)
 except:
  print("")
  sys.exit(0)
except Exception as exc:
 input("Κάτι δεν πάει καλά. Δες πάλι τι μου έδωσες και ξανατρέξε.")
 print(str(exc))
 sys.exit(0)
