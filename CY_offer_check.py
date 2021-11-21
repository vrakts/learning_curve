# CY_offer_check.py
# checks the front page offers for english translation.
########################
# Current version 1 beta
########################
# Save it somewhere. Show more interactive dialogs. Try and except.

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
 start = datetime.now()
 start_date = start.strftime("%d-%m-%Y")
 start_time = start.strftime("%H:%M:%S")
 print("Εκκίνηση: " + start_date)
 print("")

def load_soup(page, wait, retries) :
 # print("Μέσα στη σούπα.")
 attempt = 0
 while attempt < retries :
  try :
   result = requests.get(page, cookies = cookies, headers = headers)
   webpage = result.content
   page_soup = soup(webpage, "html5lib")
   break   
   # print("Έξω από τη σούπα.")
   # print("")
  except Exception as exc :
   print("")
   print("Στο φόρτωμα της σελίδας, πέσαμε πάνω στο:")
   print(str(exc))
   print("Ξαναπροσπαθώ σε " + str(retries)+ ".")
   nani(wait)
   attempt += 1
 if attempt == retries :
  print("Προσπάθησα " + str(attempt) + " φορές και δεν τα κατάφερα.")
  input()
  sys.exit(0)
 
 return(page_soup)

def set_files() :
 global write_file, alt_write_file, spreadsheet, ac_row, gr_url, wb_write, ws_write, sheets, sheet, write_path
 if os.path.exists(r"K:\SALES\Stock\Scripts\translated") == True :  # does work folder exist?
  write_path = (r"K:\SALES\Stock\Scripts\translated")
 elif os.path.exists(r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does work folder exist?
  write_path = (r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
  write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
  write_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"Y:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
  write_path = (r"Y:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 else :
  if your_choice == "2" :
   write_path = (r"C:\TEMPYTH")
   if os.path.exists(write_path) == True :  # does temp folder exist?
    print("Δεν βρέθηκαν oi προκαθορισμένοι φάκελοι. Χρησιμοποιώ " + write_path)
   else :  # if not create it
    print("Δεν βρέθηκαν oi προκαθορισμένοι φάκελοι. Δημιουργώ και χρησιμοποιώ " + write_path)
    os.makedirs(write_path)
  else :
   print("Δεν βρέθηκαν οι προκαθορισμένοι φάκελοι. Που είναι το αρχείο... οέο?")
   input("Προσπάθησε ξανά.")
   sys.exit(1)  

 write_file = ("Translate_Needed_" + start_date + ".xls")  # name of xls write file
 alt_write_file = ("Translate_Needed_" + start_date + ".xls")  # alternate name of xls write file
 wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
 ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok = True)  # add sheet in virtual workbook named after the search string ad run date
 ws_write.write(0, 0, "CODE")			# write CODE on A1 cell

def write_results(e, code) :
 ws_write.write(e, 0, code) 		# OK

def write_it_down(write_path, write_file) :
 print("Τρέχων φάκελος: " + os.getcwd())
 os.chdir(write_path)
 print("Χρησιμοποιώ το " + os.getcwd())
 wb_write.save(write_file)
 try :
  wb_write.save(write_file)
 except Exception as exc :
  print(str(exc))
  write_file = alt_write_file
  wb_write.save(write_file)
 print("")
 print("Το αρχείο: " + write_file + " δημιουργήθηκε στο " + os.getcwd())

try :
 cookies = {'language': 'en'}
 headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
 wait = 3
 retries = 3
 e = 1
 page_count = 1
 # start = 1
 trans_list = []
 
 get_start_time()
 set_files()
 
 pages = []
 pages.append("https://www.e-shop.cy/offers?id=1")
 pages.append("https://www.e-shop.cy/offers?id=2")
 pages.append("https://www.e-shop.cy/offers?mid=0&sid=1")
 pages.append("https://www.e-shop.cy/offers?mid=0&sid=2")

 for page_url in pages :
  print("Σελίδα: " + str(page_count) + "/" + str(len(pages)))
  page_count += 1
  start_page_soup = load_soup(page_url, wait, retries)
  containers = start_page_soup.findAll('div', {'class': 'prodauto'})
  start = 1
  print("Έλα πάμε.")
  for container in containers :
   """ optional lines to stop the count for test purposes """
   # if start == 10 :
    # break
   """ end of optional lines """ 

   if len(containers) - start == 1 :
    print_text = "Απομένει 1."
   elif len(containers) - start == 0 :
    print_text = "Τελευταίο."
   else :
    print_text = "Τρέχω το " + str(start) + "/" + str(len(containers)) + ". Απομένουν " + str(len(containers) - start)
   print(print_text)
   prod_url = container.find('td', {'style':'text-align:center;padding:10px 0 0 0;vertical-align:bottom;'}).a['href']
   prod_code = prod_url[prod_url.rfind('-')+1:]
   prod_page_soup = load_soup(prod_url, wait, retries)
   cy_desc_text = ""
   cy_d_soup = prod_page_soup.find('div', {'id': 'mobile_desc'})
   cy_product_table_title = prod_page_soup.find('td', {'class': 'product_table_title'})
   if cy_d_soup == None or cy_d_soup.text.find('Σύνολο ψήφων') > 0 or cy_product_table_title.text.strip() != "Description" :
    cy_desc_text = ""
    print("Το " + prod_code + " νιώθει άδειο εσωτερικά. Δεν βρήκα περιγραφή.")
   else :
    cy_desc_text = cy_d_soup.decode_contents().strip()
    if cy_desc_text.find('Product description is temporary unavailable in English') >= 0 :
     translated = False
     print("Το " + prod_code + " κοιμάται όρθιο. Θέλει μετάφραση.")
     trans_list.append(prod_code)
    else :
     translated = True
     print("Το " + prod_code + " δεν κοιμάται. Δεν θέλει μετάφραση.")
   start += 1
  
 if len(trans_list) > 0 :
  print("")
  print("Βρήκα τα παρακάτω " + str(len(trans_list)) + ":")
  for code in trans_list :
   print(code)
   write_results(e, code)
   e += 1
 else :
  print("All clear.")
 print("")
 write_it_down(write_path, write_file)
 
except KeyboardInterrupt :
 try :
  print("")
  input("Διαλλειματάκι;")
  print("")
 except :
  sys.exit(0)
except Exception as exc:
 print("Εξαίρεση: " + str(exc))
finally :
 # print("")
 # print("Τέλος εξαίρεσης.")
 sys.exit(0)