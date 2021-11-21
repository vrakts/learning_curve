# what_to_do.py
# Πρόχειρος και γρήγορος ανταγωνισμός GR - CY

import requests, os, sys, re, xlwt, ezodf
from bs4 import BeautifulSoup as soup
from datetime import datetime
from time import sleep as nani

answer = "YES"
cookies = {'language': 'en'}
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
e = 1
today = datetime.now()
date = today.strftime("%y-%d-%m")
gr_codes = []
cy_codes = []

def set_files() :
 global write_path, write_file, alt_write_file, wb_write, ws_write
 if os.path.exists(r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :
  write_path = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας')
 else :
  input("Δεν βρέθηκε ο φακελος.")
  sys.exit(0)
 write_file = ('GR-CY_' + date + '.xls')
 alt_write_file = ('GR-CY_' + date + 'alt.xls')
 os.chdir(write_path)
 wb_write = xlwt.Workbook()
 ws_write = wb_write.add_sheet("auto_comp", cell_overwrite_ok = True)
 ws_write.write(0, 0, "ΚΩΔΙΚΟΣ")
 ws_write.write(0, 1, "ΤΙΤΛΟΣ")
 ws_write.write(0, 2, "GR")
 ws_write.write(0, 3, "CY")

def choice() :
 global choice
 choice_ok = False
 while choice_ok == False :
  print("1. Λίστα με αποτελέσματα μόνο.")
  print("2. Ανταγωνισμός.")
  answer_text = "Επιλογή: "
  choice = input(answer_text)
  try :
   val = int(choice)
   if val >= 1 and val <= 2 :
    choice_ok = True
  except ValueError:
   try:
    val = float(choice)
    if val >= 1 and val <= 2 :
     choice_ok = True
   except ValueError:
    choice_ok = False
    print("")
    print("Η επιλογή σου δεν είναι αριθμός. Δοκίμασε πάλι.")
  if choice_ok == False :
   print("")
   print("Προσπάθησε πάλι επιλέγοντας 1 ή 2.")
 choice = val

def list_pages() :
 global pages_list
 pages_list = []
 page_url = input("Δώσε πράμα: ")
 while page_url.find("http") >= 0 :
  pages_list.append(page_url)
  cy_page_url = 'https://www.e-shop.cy/' + page_url[page_url.find('gr/') + 3:]
  pages_list.append(cy_page_url)
  page_url = input("Έ έτσι ξεροσφύρι θα τη βγάλουμε; Δώσε κι άλλο πράμα: ")
 else :
  if len(pages_list) == 0 :
   pages_list.append('https://www.e-shop.cy/search_main?table=PER&&category=%CC%CD%C7%CC%C7+RAM')
  print("Τα μαζεύω και φεύγω.")

def get_cy_mainpage(page_url) :
 global start_page_soup, next_pages_category, total_next_pages, cat_page, query_mark, categories, cat_offset_url
 print("Φανταστική σελίδούλα με όνομα:")
 print(page)
 result = requests.get(page_url, cookies = cookies, headers = headers)
 webpage = result.content
 start_page_soup = soup(webpage, "html5lib")
 next_pages_category = start_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})
 try :
  total_next_pages = next_pages_category[len(next_pages_category)-1].text
 except :
  total_next_pages = "1"
 print("Σύνολο σελίδων: " + str(total_next_pages))
 cat_page, query_mark, categories = str(page_url).partition("?")
 cat_offset_url = cat_page + query_mark + "offset=" + str(offset) + "&" + categories
 # print("")
 # print("Offset page: " + cat_offset_url)

def get_gr_mainpage(page_url) :
 global start_page_soup, next_pages_category, total_next_pages, cat_page, query_mark, categories, cat_offset_url
 print("Φανταστική σελίδούλα με όνομα:")
 print(page)
 result = requests.get(page_url, cookies = cookies, headers = headers)
 webpage = result.content
 start_page_soup = soup(webpage, "html5lib")
 next_pages_category = start_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})
 try :
  total_next_pages = next_pages_category[len(next_pages_category)-1].text
 except :
  total_next_pages = "1"
 print("Σύνολο σελίδων: " + str(total_next_pages))
 cat_page, query_mark, categories = str(page_url).partition("?")
 cat_offset_url = cat_page + query_mark + "offset=" + str(offset) + "&" + categories
 # print("")
 # print("Offset page: " + cat_offset_url)

def get_total_products() :
 global total_prod, tp
 last_offset = (int(total_next_pages) - 1) * 10
 last_cat = cat_page + query_mark + "offset=" + str(last_offset) + "&" + categories
 result = requests.get(last_cat, cookies = cookies, headers = headers)
 webpage = result.content
 last_page_soup = soup(webpage, "html5lib")
 last_prod = last_page_soup.findAll('table', {'class': 'web-product-container'})
 total_prod = len(last_prod) + last_offset
 tp = total_prod
 print("Βρήκα " + str(total_prod) + " προϊόντα. Τα κεφάλια μέσα.")
 print("")

def single_pages(cat_offset_url) :
 global containers
 # global single_page_soup
 result = requests.get(cat_offset_url, cookies = cookies, headers = headers)
 webpage = result.content
 single_page_soup = soup(webpage, "html5lib")
 containers = single_page_soup.findAll('table', {'class': 'web-product-container'})

def get_cy_details(container) :
 global cy_code, cy_title, cy_price
 cy_code = container.font.text.replace("(", "").replace(")", "")
 cy_title = container.h2.text.strip()
 if container.b.font :
  cy_price = float(container.b.font.text.strip())
 else :
  cy_price = float(container.b.text.strip())

def get_gr_details(gr_code) :
 global gr_price
 gr_url = 'https://www.e-shop.gr/product?id=' + gr_code
 gr_result = requests.get(gr_url, cookies = cookies, headers = headers)
 gr_webpage = gr_result.content
 gr_page_soup = soup(gr_webpage, "html5lib")
 gr_price_list = gr_page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(gr_price_list) == 0 :
  gr_price_text = "Εξαντλημένο"
  gr_price = gr_price_text
 else : 
  gr_price_text = gr_price_list[0].text.replace("\xa0€", "")
  # print("gr_price_text: " + gr_price_text)
  gr_price = float(gr_price_text)
  # print("gr_price: " + str(gr_price))

try :
 choice()
 set_files()
 list_pages()
 print("")
 for page in pages_list :
  offset = 0  # starting offset value set to 0 and in each for loop, 10 will be added
  get_gr_mainpage(page)
  print("")
  get_total_products()
  for q in range(0, int(total_next_pages)) :
   single_pages(cat_offset_url)
   for container in containers :
    attempt = 0
    tp -= 1
    while attempt < 3 :
     try :
      # print("Μπαίνω CY")
      get_gr_details(container)
      # print("CY OK")
      gr_codes.append(gr_code)
	  