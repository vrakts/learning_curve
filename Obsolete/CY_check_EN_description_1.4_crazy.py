# Current version 1.4 beta
#####################
# Changelog v1.4
# - Αλλαγή φακέλου αποθήκευσης.
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
# - strfmtime για καλύτερη διαχείριση ώρας και μέρας.

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
from time import time, sleep  # for the ability to measure time
import requests, xlwt, os, sys

answer = "YES"
cookies = {'language': 'en'}
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

def get_start_time() :
 global start_time, start_date
 start_time = time()  # set starting time
 today = date.today()  # set starting date
 start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
 print("")
 print("Στον επόμενο τόνο, η μέρα θα είναι: " + start_date)

def get_elapsed_time(e) :
 elapsed_time = time() - start_time
 minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
 mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
 seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
 seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
 formatted_time = str(mins) + "." + str(seconds)
 # print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
 if mins == 0 and seconds == 0 :
  print("Όσο πάει χειροτερεύει. Τελείωσε σε χρόνο 0")
 else :
  print("Όσο πάει χειροτερεύει. Τελείωσε σε " + str(mins) + " λεπτά και " + str(seconds) + " δευτερόλεπτα (" + str(round(elapsed_time, 2)) + " δευτερόλεπτα).")
 print("") 
 if e > 1 :
  input("Βρήκα " + str(e) + " να κοιμούνται. Παίξε λίγο με το πράμα σου για να κλείσω.")
 elif e == 1 :
  input("Βρήκα " + str(e) + " να κοιμάται. Παίξε λίγο με το πράμα σου για να κλείσω.")
 elif e == 0 :
  input("Είσαι 'νταξ'. Δεν κοιμάται κανένας τους. Παίξε λίγο με το πράμα σου για να κλείσω.")
 sys.exit(0)

def set_files() :
 global write_path, write_file, alt_write_file, wb_write, ws_write, wb_crazy_write, ws_crazy_write
 if os.path.exists(r"C:\Users\manager\Desktop") == True :
  write_path = (r'C:\Users\manager\Desktop')
 else :
  write_path = (r'K:\SALES\Stock\translated')
 write_file = ('en_exist.xls')
 alt_write_file = ('en_exist_alt.xls')
 crazy_file = ('en_crazy.xls')
 alt_crazy_file = ('en_crazy_alt.xls')
 os.chdir(write_path)
 wb_write = xlwt.Workbook()
 ws_write = wb_write.add_sheet("en_exist", cell_overwrite_ok = True)
 wb_crazy_write = xlwt.Workbook()
 ws_crazy_write = wb_crazy_write.add_sheet("en_exist_crazy", cell_overwrite_ok = True)
 ws_write.write(0, 0, "ΚΩΔΙΚΟΣ")
 ws_write.write(0, 1, "CRAZY")
 # ws_write.write(0, 1, "ΤΙΤΛΟΣ")
 # ws_write.write(0, 2, "CRAZY")

def list_pages() :
 global pages_list
 pages_list = []
 page_url = input("Δώσε πράμα: ")
 while page_url.find("http") >= 0 :
  pages_list.append(page_url)
  page_url = input("Έ έτσι ξεροσφύρι θα τη βγάλουμε; Δώσε κι άλλο πράμα: ")
 else :
  print("Τα μαζεύω και φεύγω.")

def get_cy_mainpage(page_url) :
 global start_page_soup, next_pages_category, total_next_pages, cat_page, query_mark, categories, cat_offset_url, crazy_page_soup
 print("Φανταστική σελίδούλα με όνομα:")
 print(page)
 result = requests.get(page_url, cookies = cookies, headers = headers)
 webpage = result.content
 start_page_soup = soup(webpage, "html5lib")
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
  result = requests.get(last_cat, cookies = cookies, headers = headers)
  webpage = result.content
  last_page_soup = soup(webpage, "html5lib")
  last_prod = last_page_soup.findAll('table', {'class': 'web-product-container'})
  total_prod = len(last_prod) + last_offset
 else :
  result = requests.get(page, cookies = cookies, headers = headers)
  webpage = result.content
  crazy_page_soup = soup(webpage, "html5lib")
  last_prod = crazy_page_soup.findAll('table', {'class': 'crazy-container'})
  total_prod = len(last_prod)
 tp = total_prod
 print("Βρήκα " + str(total_prod) + " προϊόντα. Τα κεφάλια μέσα.")
 print("")

def single_pages(cat_offset_url) :
 global containers
 # global single_page_soup
 result = requests.get(cat_offset_url, cookies = cookies, headers = headers)
 webpage = result.content
 single_page_soup = soup(webpage, "html5lib")
 if crazy_mark == False :
  containers = single_page_soup.findAll('table', {'class': 'web-product-container'})
 else :
  containers = single_page_soup.findAll('table', {'class': 'crazy-container'})

def get_cy_details(container, e) :
 global cy_code, cy_title, cy_desc_text, translated
 if crazy_mark == True :
  cy_code = container.find('tr', {'class' : 'crazy-title-row'}).span.text.strip()
 else :
  cy_code = container.font.text.replace("(", "").replace(")", "")
 a_page = "https://www.e-shop.cy/product?id=" + cy_code
 result = requests.get(a_page, cookies = cookies, headers = headers)  # with cookies plz
 webpage = result.content
 prod_page_soup = soup(webpage, "html5lib")
 cy_title = prod_page_soup.h1.text.strip()
 cy_desc_text = ""
 cy_d_soup = prod_page_soup.find('div', {'id': 'mobile_desc'})
 cy_product_table_title = prod_page_soup.find('td', {'class': 'product_table_title'})
 if cy_d_soup == None or cy_d_soup.text.find('Σύνολο ψήφων') > 0 or cy_product_table_title.text.strip() != "Description" :
  cy_desc_text = ""
  print("Το " + cy_code + " νιώθει άδειο εσωτερικά. Δεν βρήκα περιγραφή.")
 else :
  cy_desc_text = cy_d_soup.decode_contents().strip()
  if cy_desc_text.find('Product description is temporary unavailable in English') >= 0 :
   translated = False
   print("Το " + cy_code + " κοιμάται όρθιο. Θέλει μετάφραση.")
   e += 1
   write_results(e)
   # print("e = " + str(e))
  else :
   translated = True
   print("Το " + cy_code + " δεν κοιμάται. Δεν θέλει μετάφραση.")
 print("")
 return(e)

def write_results(e) :
 # print("e = " + str(e))
 ws_write.write(e, 0, cy_code)
 # ws_write.write(e, 1, cy_title)
 # if page.find("crazysundays") >= 0 :
  # ws_write.write(e, 2, "CRAZY")
 if page.find("crazysundays") >= 0 :
  ws_write.write(e, 1, "CRAZY")

def write_it_down() :
 try :
  wb_write.save(write_file)
  print(write_file + ", το έχω γραμμένο στο " + write_path)
 except :
  wb_write.save(alt_write_file)
  print("Πιθανώς κάποιος παίζει με το αρχείο. Προχωράω στο παρασύνθημα.")
  print(alt_write_file + ", το έχω γραμμένο στο " + write_path)

set_files()
try :
 crazy_mark = False
 offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
 e = 0  # represents the row inside the excel file.
 attempt = 0  # how many attempts to re-read the url in case of failure
 list_pages()
 get_start_time()
 print("")
 for page in pages_list :
  offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
  if page.find("crazysundays") >= 0 :
   crazy_mark = True
  else :
   crazy_mark = False
  get_cy_mainpage(page)
  print("")
  get_total_products()
  for q in range(0, int(total_next_pages)) :
   if crazy_mark == False :
    single_pages(cat_offset_url)
   else :
    single_pages(page)
   for container in containers :
    attempt = 0
    tp = tp - 1
    if total_prod - (total_prod - tp) > 0 :
     print("Τα πίνω με το: " + str(total_prod - tp) + "/" + str(total_prod) + ". Έχω ακόμα: " + str(total_prod - (total_prod - tp)))
    else :
     print("Τα πίνω με το: " + str(total_prod - tp) + "/" + str(total_prod) + ".")
    while attempt < 3 :
     try :
      # if crazy_mark == False :
       # e = get_cy_details(container, e)
      # else :
       # e = get_cy_details(container, e)
      e = get_cy_details(container, e)
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
  
 write_it_down()
 get_elapsed_time(e)
except KeyboardInterrupt as exc :
 # os.system('cls')
 print("")
 print("Ρε μην τον παίζεις έχουμε δουλειά!")
 input("Τι να σε κάνω; Πάτα οποιοδήποτε κουμπί για να τελειώσεις... !")
 sys.exit(0)
except Exception as exc:
 input("Κάτι δεν πάει καλά. Δες πάλι τι μου έδωσες και ξανατρέξε.")
 print(str(exc))
 sys.exit(0)
