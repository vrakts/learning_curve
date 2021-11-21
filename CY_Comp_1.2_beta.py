# Nicosia_Comp
### Ελέγχει το αρχείο αλλαγών τιμών του ανταγωνισμού
### και συγκρίνει αν οι τιμές ισχύουν στα site:
### GR, CY και του ανταγωνιστή
### Οι αλλαγές αποθηκεύονται σε άλλο αρχείο
##########################
### Τρέχουσα έκδοση 1.2 beta
##########################
# Changelog 1.2 beta
# - Try except για όλο το script.
# - Διορθώσεις στο Try except εγγραφής
##########################
# Changelog 1 beta
# - Διαβάζει σωστά το αρχείο excel
# - Ο χρήστης επιλέγει φύλλο, στήλη και γραμμή
# - Υπολογίζει μόνο Singular και CustomPC για ανταγωνισμό
# - Βγάζει τα αποτελέσματα στην οθόνη
# - Αποθηκεύει τα πάντα στο Excel
# - Βελτίωση διαδικασίας Singular
##########################
# To Do:
# - Να αποθηκεύει τις διαφορές μόνο
# - Χρονόμετρο
# - Μέσος όρος και υπολειπόμενος χρόνος
# - Ενσωμάτωση του γρήγορου τσεκ
# - Διαδικασία CustomPC

import requests, os, sys, re, xlwt, ezodf
from bs4 import BeautifulSoup as soup
from datetime import datetime
from time import sleep as nani

def get_cy_price(page_soup) :
 global cy_price, cy_title
 cy_title = page_soup.h1.text
 cy_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(cy_price) == 0 :
  cy_price = "Εξαντλημένο"
  cy_price_dif = "-"
 else : 
  cy_price_dif = cy_price[0].text.replace("\xa0€", "")
  cy_price = cy_price_dif.replace(".", ",")

def get_gr_price(page_soup) :
 global gr_price
 gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(gr_price) == 0 :
  gr_price = "Εξαντλημένο"
  gr_price_dif = "-"
 else : 
  gr_price_dif = gr_price[0].text.replace("\xa0€", "")
  gr_price = gr_price_dif.replace(".", ",")

def get_si_price(search_term) :
 global si_price, si_pcode, si_psku, si_plink, si_pavail
 si_search_url = "https://www.singular.com.cy/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&search_id=&q=" + search_term + "&dispatch=products.search"
 try :
  result = requests.get(si_search_url, headers = headers)
  webpage = result.content
  page_soup = soup(webpage, "html5lib")
  # print("Singular read OK.")
  # print("")
  si_price_container = page_soup.findAll("span", {"id" : re.compile('sec_product_price*')})
  if len(si_price_container) == 0 :
   si_price_text = "-"
   si_pcode = "-"
   si_psku = "-"
   si_plink = "-"
   si_pavail = "-"
  else :
   si_price_text = si_price_container[0].text.replace("\xa0€","").replace(".", ",")
   if si_price_text.count(',') > 1 :  # since price value on singular site has comma as a digit group seperator replace it with dot
    si_price = si_price_text.replace(',', '', 1)
   else :
    si_price = si_price_text
    # si_price = si_price_text
   si_em = page_soup.findAll('em')  # contains all EM tags that have the product ID SKU and other info
   for em in si_em :
    if em.text.find('Product Code') > 0 :
     si_pcode = em.text.strip().replace('Product Code', '')
     break
   si_psku = page_soup.find('span', {'class': 'ty-control-group__item'}).text.strip()
   si_plink = page_soup.find("input", {"name": re.compile('list_image_update*')})['value']
   si_pavail = page_soup.find("span", {"class" : "delivery-time"})
   if si_pavail == None :
    si_avail_text = "Out of stock"
   else :
    si_avail_text = si_pavail.text.strip()
   si_pavail = si_avail_text
 except Exception as exc :
  print("Άλα της, μόλις πέσαμε πάνω στο exception:")
  print(str(exc))
  print("")
 
def get_custom_price(search_term) :
 global cp_price, cp_pcode, cp_avail, cp_plink
 cp_search_url = "https://www.custompc.com.cy/search/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&scode_from_q=Y&cid=0&q=" + search_term
 try :
  result = requests.get(cp_search_url, headers = headers)
  webpage = result.content
  page_soup = soup(webpage, "html5lib")
  # print("Custom PC read OK.")
  # print("")
  custom_price = page_soup.findAll("span", {"id" : re.compile('sec_discounted_price*')})
  if len(custom_price) == 0 :
   custom_price_text = ""
   cp_pcode = ""
   cp_avail = ""
  else :
   custom_price = page_soup.findAll('span', {'class' : 'ty-price-num'})
   custom_price_text = custom_price[1].text.replace('.', ',')
   cp_prod_url = page_soup.findAll('a', {'class' : 'product-title'})
   if len(cp_prod_url) == 0 :
    cp_plink = "-"
   else :
    cp_plink = cp_prod_url[0]['href']
    # print("cp_prod_url: " + cp_prod_url)
    attempt = 0
    while attempt < 3 :
     try :
      result = requests.get(cp_plink, headers = headers)
      webpage = result.content
      cp_prod_soup = soup(webpage, "html5lib")
      break
     except http.client.IncompleteRead :
      attempt += 1
     # else :
      # pass
    cp_pcode = cp_prod_soup.find('div', {'class' : 'ty-control-group ty-sku-item cm-hidden-wrapper'}).text  # extract the product code container from the product page
    cp_pcode = cp_pcode[cp_pcode.find(':') + 1:].strip() # extract only the product code from the product page
    # print("cp_pcode: " + cp_pcode)
    try :
     cp_avail = cp_prod_soup.find('span', {'class' : 'ty-qty-in-stock ty-control-group__item'}).text.strip()  # if in stock extract availability from the product page
    except :
     cp_avail = cp_prod_soup.findAll('div', {'class' : 'ty-control-group product-list-field'})  # if not then try the no stock container
     cp_avail = cp_avail[1].text.strip()[cp_avail[1].text.strip().find(':')+2:]  # remove unecessary text
  
  cp_price = custom_price_text
 except Exception as exc :
  print("Άλα της, μόλις πέσαμε πάνω στο exception:")
  print(str(exc))
  print("")

def margin_check(page_soup) :
 global margin
 margin_exist = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
 stock_exist = page_soup.findAll("font", {"style" : "color:#ff0000;font-weight:bold;font-size:9px;font-family:arial black;"})
 if len(stock_exist) != 0 :  # if stock_exist not empty then stock sign exists
  margin = "STOCK"
 elif len(margin_exist) != 0 :  # if margin_exist not empty then stock doesn't exist and margin sign exists
  margin = "MARGIN"
 else :  # if both stock sign doesn't exist and high margin exist then no changes
  margin = "-"
  # continue

def write_it_down(write_file, alt_write_file) :
 success = False
 try :
  wb_write.save(write_file)
  success = True
 except :
  write_file = alt_write_file
  wb_write.save(write_file)
  success = True
 finally :
  if success == False :
   sys.exit("Και τα 2 αρχεία είναι μάλλον ανοιχτά. Sorry αλλά πρέπει να το ξανατρέξεις.")
  else :
   sys.exit(write_file + " σώθηκε στο " + write_path)

attempt = 0
e = 1
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

##########################
# Setting correct paths. #
##########################

if os.path.exists(r'C:\Users\Manager\Desktop\Product') == True :
 write_path = (r'C:\Users\Manager\Desktop\Product')
 print("Χρησιμοποιώ το " + write_path + " για ανάγνωση αρχείων.")
 print("")
elif os.path.exists(r"Z:\OneDrive\eShop Stuff\PRODUCT\Product") == True :
 write_path = (r"Z:\OneDrive\eShop Stuff\PRODUCT\Product")
 print("Χρησιμοποιώ το home path 1 για ανάγνωση αρχείων.")
 print("")
elif os.path.exists(r"Y:\OneDrive\eShop Stuff\PRODUCT\Product") == True :
 write_path = (r"Y:\OneDrive\eShop Stuff\PRODUCT\Product")
 print("Χρησιμοποιώ το home path 2 για ανάγνωση αρχείων.")
 print("")
else :
 print("Δεν βρίσκω το φάκελο ούτε το αρχείο. Που δι@0Lo είμαι;")
 print("")
 sys.exit()

##########################
# End of  paths setting. #
##########################

# For reading
os.chdir(write_path)
try :
 read_file = ('Αλλαγή τιμών.ods')
 print("Προσπάθεια να ανοίξω το αρχείο: " + read_file + "...")
 ezodf.config.set_table_expand_strategy('all')
 spreadsheet = ezodf.opendoc(read_file)
 ezodf.config.reset_table_expand_strategy()
 print('Τα καταφέραμε.')
 print("")
except :
 print("Δεν βρίσκω το αρχείο " + write_path + "\\" + read_file + " ή δεν ανοίγει.")
 print("")
 sys.exit()

#################
# Διάλεξε φύλλο #
#################

try :
 sheets = spreadsheet.sheets
 for i in range(0, len(sheets)) :
  print('Φύλλο ' + str(i) + ': ' + sheets[i].name)
 print("")

 answer = 'Διάλεξε φύλλο: '
 sheet_index = input(answer)
 if sheet_index == "" :
  sheet = sheets[0]
 else :
  sheet = sheets[int(sheet_index)]
 print("")

 rowcount = sheet.nrows()
 colcount = sheet.ncols()
 ac_row = 1
 for i in range(0, colcount) :
  print('Στήλη ' + str(i) + ': ' + str(sheet[0, i].value))
 print("")

#################
# Διάλεξε στήλη #
#################

 answer = 'Διάλεξε στήλη: '
 col_index = input(answer)
 if col_index == "" :
  col_index = 0
 else :
  col_index = int(col_index)
 print("")

 for i in range(1, rowcount):
  if str(sheet[i, col_index].value) != "None" :
   ac_row += 1
  else:
   print('Σύνολο γραμμών: ' + str(ac_row))
   break
 print("")

##################
# Διάλεξε γραμμή #
##################

 answer = 'Αρχική γραμμή: '
 row_index = input(answer)
 if row_index == "" :
  row_index = 1
 else :
  row_index = int(row_index)
 print("")

 write_file = ("allagi_timon.xls")
 alt_write_file = ("allagi_timon_alt.xls")

 try: 
  print("Προσπάθεια για δημιουργία: " + write_file)
  wb_write = xlwt.Workbook()
  ws_write = wb_write.add_sheet("results", cell_overwrite_ok = True)
  print("Γιούπι, τα καταφέραμε.")
  print("")
 except Exception as exc :
  print("Δεν κατάφερα να γράψω το αρχείο. Έχουμε δικαιώματα;")
  print(str(exc))
  print("")

 ws_write.write(0, 0, "ΚΩΔΙΚΟΣ")
 ws_write.write(0, 1, "ESHOP CY")
 ws_write.write(0, 2, "ESHOP GR")
 ws_write.write(0, 3, "ΑΝΤΑΓΩΝΙΣΤΗΣ")
 ws_write.write(0, 4, "ΤΙΜΗ")
 ws_write.write(0, 5, "ΚΩΔΙΚΟΣ")
 ws_write.write(0, 6, "LINK")
 ws_write.write(0, 7, "ΔΙΑΦΟΡΑ")
 ws_write.write(0, 8, "ΠΟΣΟΣΤΟ")
 ws_write.write(0, 9, "MARGIN")
 
 for i in range(row_index, ac_row) :
  attempt = 0 
  e_code = str(sheet[i, col_index].value.strip())
  gr_file_price = str(sheet[i, 2].value)
  cy_file_price = str(sheet[i, 3].value)
  comp_file_price = str(sheet[i, 7].value)
  print(str(i) + "/" + str(ac_row) + ". Απομένουν " + str(ac_row - i))
  if e_code == "None" :
   print("Άδειο κελί. Τέλος.")
   print("")
   break
  else :
   cy_page = 'https://www.e-shop.cy/product?id=' + e_code
   gr_page = 'https://www.e-shop.gr/s/' + e_code
   while attempt < 3 :
    try :
     result = requests.get(cy_page, headers = headers)
     webpage = result.content
     page_soup = soup(webpage, "html5lib")
     get_cy_price(page_soup)
     result = requests.get(gr_page, headers = headers)
     webpage = result.content
     page_soup = soup(webpage, "html5lib")
     get_gr_price(page_soup)
     firstf = cy_title.find(" ") + 1
     secondf = firstf + cy_title[firstf:].find(" ") + 1
     title_cut = cy_title[secondf:]
     search_term = title_cut[:title_cut.find(" ")]
     comp_name = str(sheet[i, 6].value).strip()
     if comp_name == 'SINGULAR' :
      get_si_price(search_term)
      comp_price = si_price
      comp_code = si_psku
      comp_link = si_plink
     elif comp_name == 'CUSTOMPC' :
      get_custom_price(search_term)
      comp_price = cp_price
      comp_code = cp_pcode
      comp_link = cp_plink
     else :
      si_price = ""
      cp_price = ""
      comp_price = ""
      comp_code = ""
      comp_link = ""

     margin_check(page_soup)
     break
    except Exception as exc :
     print("Άλα της, μόλις πέσαμε πάνω στο exception:")
     print(str(exc))
     print("Προσπαθώ πάλι σε 5 δευτερόλεπτα.")
     print("")
     attempt += 1
     nani(5)
   if attempt >= 3 :
    print("")
    print("Προσπάθησα 3 φορές. Προχωράω στον επόμενο κωδικό.")
    print("")
    continue
  # print(cy_price)
  # print(gr_price)
  # print(comp_name)
  # print(comp_price)
  try :
   flt1 = float(cy_file_price)
   flt2 = float(comp_price.replace(",", "."))
   if comp_name == "SINGULAR" or comp_name == "CUSTOMPC" :
    diff = flt1 - flt2
    diff = float(gr_file_price) - float(cy_price.replace(",", "."))  # only for CY price corrections
  except :
   diff = "-"
  try :
   flt1 = float(cy_file_price)
   flt2 = float(comp_price.replace(",", "."))
   percent_diff = flt2 - flt1
   percent = percent_diff / flt1 * 100
   percent = round(percent, 2)
  except :
   percent = "-"
  print(e_code + ", CY Price: " + cy_price + ", GR Price: " + gr_price + ", COMP: " + comp_name + " - " + comp_price)  
  ws_write.write(e, 0, e_code)
  ws_write.write(e, 1, cy_price)
  ws_write.write(e, 2, gr_price)
  ws_write.write(e, 3, comp_name)
  ws_write.write(e, 4, comp_price)
  ws_write.write(e, 5, comp_code)
  ws_write.write(e, 6, comp_link)
  ws_write.write(e, 7, diff)
  ws_write.write(e, 8, percent)
  ws_write.write(e, 9, margin)
  e += 1
except KeyboardInterrupt :
 print("")
 print("OK κατάλαβα. Διαλλειματάκι... ")
 print("")
except Exception as Exc :
 print("Άλα της, μόλις πέσαμε πάνω στο exception:")
 print(str(exc))
 print("")

try :
 timeit()
except :
 print("Δεν έχει ολοκληρωθεί το χρονόμετρο μας...")
 print("")
try :
 write_it_down(write_file, alt_write_file)
except NameError :
 print("Δεν μπορώ να γράψω τίποτα. Δεν έχει καθοριστεί σωστά το αρχείο.")
except Exception as exc:
 print("Δεν μπορώ να γράψω τίποτα.")
 print(str(exc))
 sys.exit(0)