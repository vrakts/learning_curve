# CY_vitrines.py
### Searches all vitrines, counts current products
### and if less than 8 fills up the rest
# Initial Beta version
# - Finds all vitrines and counts current PER totals
# - Writes all results in an xls file
#
# Current Version 1.0
#####################
# - Trying to auto calcuate rest of PERs
# - Write only changes on file
# To Do
# - Auto calculate the random products to add
# - Add more than 8 PERs 
# - Case: https://www.e-shop.cy/aksesouar-psifiakon-mixanon
#   Find a way to detect the extra categories buttons

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from random import randint
import requests, os, sys, re, xlwt #, unicodedata

def set_files() :
 global write_path, write_file, alt_write_file, wb_write, ws_write
 if os.path.exists(r"Z:\OneDrive") == True :
  write_path = (r'Z:\OneDrive')
 elif os.path.exists(r"Y:\OneDrive") == True :
  write_path = (r'Y:\OneDrive')
 elif os.path.exists(r"K:\SALES") == True :
  write_path = (r'K:\SALES')
 else :
  print("Where am I?")
  input()
  sys.exit(0)
 os.chdir(write_path)
 write_file = ('vitrines.xls')
 alt_write_file = ('vitrines_2.xls')
 wb_write = xlwt.Workbook()
 ws_write = wb_write.add_sheet("vitrines", cell_overwrite_ok = True)
 ws_write.write(0, 0, "URL")
 ws_write.write(0, 1, "Title")
 ws_write.write(0, 2, "Length")
 ws_write.write(0, 3, "PERs")

def write_it_down(write_file, alt_write_file) :
 # print(write_file + "saved on " + write_path)
 try :
  wb_write.save(write_file)
 except :
  wb_write.save(alt_write_file)
 sys.exit(write_file + " saved on " + write_path)

def get_all_products(prod_count, single_page, need_count) :
 global add_per
 try :
  add_per = ""
  offset = 0
  cat_pages = []
  total_next_pages = int(prod_count / 10) + 1
  print("total_next_pages: " + str(total_next_pages))
  cat_page, query_mark, categories = str(single_page).partition("?")
  while offset < prod_count :
   # print("inside while loop")
   cat_pages.append(cat_page + query_mark + "offset=" + str(offset) + "&" + categories)
   offset += 10
   # print(str(offset))
  print("cat_pages length: " + str(len(cat_pages)))
  for page in cat_pages :
   result = requests.get(page, headers = headers)
   webpage = result.content
   single_page_soup = soup(webpage, "html5lib")
   containers = single_page_soup.findAll('table', {'class': 'web-product-container'})
   # print("containers: " + str(len(containers)))
   for container in containers :
    cy_code = container.font.text.replace("(", "").replace(")", "")
    cy_title = container.h2.text.strip()
    if container.b.font :
     cy_price = float(container.b.font.text.strip())
    else :
     cy_price = float(container.b.text.strip())
    categories = container.find('td', {'class': 'web-product-info'}).text
    category = categories[categories.find('Κατηγορία:')+10:categories.find('Υποκατηγορία:')].strip()
    brand = categories[categories.find('Κατασκευαστής:')+14:].strip()
    all_products.append(cy_code.strip())
 
  for prod in all_products :
   print(prod)
  where_at = int(len(all_products) / need_count)
  print("where_at: " + str(where_at))
  # for i in range (0, len(all_products), where_at) :
   # add_per += all_products[randint(i, i + where_at)] + ","
   # # i += where_at
   # print(str(i))
  for i in range (1, need_count) :
   add_per += all_products[randint((i * where_at) - where_at, (i *where_at))] + ","
   # i += where_at
   print(str(i))

  print("add_per: " + add_per)
 except Exception as exc :
  print(str(exc))

headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTM	L, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
page_list = []
# vitrina_per = []
vitrines_links = []  ### contains links for each vitrina
vitrines_names = []  ### contains names for each vitrina
vitrines_len = [0]  ### contains the PER total for the current vitrina
all_products = []  ### list of all products per vitrina category to fill up to 8
selected_products = [] ### the selected products to fill rest of current vitrina
offset = 0
e = 1

page_url = "https://www.e-shop.cy/"

result = requests.get(page_url, headers = headers)
webpage = result.content
page_soup = soup(webpage, "html5lib")

page_list = page_soup.findAll('a', {'class': 'menu_link'})

for i in range(0, len(page_list)) :
 try :
  vitrines_links.append(page_list[i]['href'])
  vitrines_names.append(page_list[i].text.strip().replace("\xa0", " ").replace("•", "-"))
  # vitrines_names.append(unicodedata.normalize("NFKD", page_list[i].text))
 except Exception as exc:
  print("Oops. Just bumped into the following exception:")
  print(str(exc))

set_files()

for i in range(1, len(vitrines_links)) :
 os.system("title " + str(i) + "/" + str(len(vitrines_links)) + ". " + vitrines_names[i])
 prod_count = 0
 need_count = 0
 page_url = vitrines_links[i]
 result = requests.get(page_url, headers = headers)
 webpage = result.content
 page_soup = soup(webpage, "html5lib")
 vitrina1 = page_soup.findAll('td', {'style' : 'text-align:right;padding:0 0 0 15px;vertical-align:middle;'})  ### contains all per details within the soup
 vitrina_per = []  ### contains all the PER codes in the current vitrina
 for v in range (0, len(vitrina1)) :
  # print(str(v))
  vitrina_text = vitrina1[v].a['href']  ### extract the PER URL
  vitrina_per.append(vitrina_text[vitrina_text.rfind("-")+1:])  ### keep only the PER code
 vitrines_len.append(len(vitrina_per))
 pers = ""
 print("Current vitrina: " + str(i) + "/" + str(len(vitrines_links)-1) + ". " + page_url + " - " + vitrines_links[i])
 print("Current length: " + str(len(vitrina_per)))
 if len(vitrina_per) > 0 :
  for per in vitrina_per :
   pers += per + ","
  pers = pers[:-1]
  print("PERs: " + pers)
 
 if len(vitrina_per) < 8 :
  try :
   # page_soup.find('td', {'class': 'shop_table_title'}) :
   single_page = page_soup.find('td', {'class': 'shop_table_title'}).a['href']
   single_page = 'https://www.e-shop.cy/' + single_page
   result = requests.get(single_page, headers = headers)
   webpage = result.content
   single_page_soup = soup(webpage, "html5lib")
   prod_count = single_page_soup.find('div', {'class': 'web-product-num'}).text
   prod_count = int(prod_count[:prod_count.find(" ")].strip())
   print("prod_count: " + str(prod_count))
   if prod_count > len(vitrina_per) :
    if prod_count > 8 :
     print("Can add " + str(8 - len(vitrina_per)) + " more PERs")
     need_count = 8 - len(vitrina_per)
    else :
     print("Can add " + str(prod_count - len(vitrina_per)) + " more PERs")
     need_count = prod_count - len(vitrina_per)
    get_all_products(prod_count, single_page, need_count)
    # print("add_per: " + add_per)
   else :
    print("No more PERs to add")
  except :
   print("Page doesn't have a URL to find more PERs")

 ws_write.write(e, 0, page_url)
 ws_write.write(e, 1, vitrines_names[i])
 # ws_write.write(e, 2, vitrines_len[i])
 ws_write.write(e, 2, len(vitrina_per))
 ws_write.write(e, 3, pers)
 if prod_count > len(vitrina_per) :
  if prod_count > 8 :
   ws_write.write(e, 4, "Can add " + str(8 - len(vitrina_per)) + " more PERs")
  else :
   ws_write.write(e, 4, "Can add" + str(prod_count - len(vitrina_per)) + " more PERs")
 else :
  ws_write.write(e, 4, "No more PERs to add")
 e += 1
  
write_it_down(write_file, alt_write_file)
