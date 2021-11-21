# Nicosia_Comp
### Ελέγχει το αρχείο αλλαγών τιμών του ανταγωνισμού
### και συγκρίνει αν οι τιμές ισχύουν στα site:
### GR, CY και του ανταγωνιστή
### Οι αλλαγές αποθηκεύονται σε άλλο αρχείο
### Τρέχουσα έκδοση 1 beta
##########################
# Changelog 1 beta
# - Διαβάζει σωστά το αρχείο excel
# - Ο χρήστης επιλέγει φύλο και στήλη
# - Υπολογίζει μόνο Singular και CustomPC για ανταγωνισμό
# - Βγάζει τα αποτελέσματα στην οθόνη
# - Αποθηκεύει τα πάντα στο Excel
##########################
# To Do:
# - Να αποθηκεύει τις διαφορές μόνο
# - Να υπολογίζει τη διαφορά και το ποσοστό.
# - Χρονόμετρο
# - Μέσος όρος καυ υπολειπόμενος χρόνος

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
 global si_price
 si_search_url = "https://www.singular.com.cy/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&search_id=&q=" + search_term + "&dispatch=products.search"
 try :
  result = requests.get(si_search_url, headers = headers)
  webpage = result.content
  page_soup = soup(webpage, "html5lib")
  # print("Singular read OK.")
  # print("")
  si_price = page_soup.findAll("span", {"id" : re.compile('sec_product_price*')})
  
  if len(si_price) == 0 :
   si_price_text = ""
  else :
   si_price_text = si_price[0].text.replace("\xa0€","").replace(".", ",")
  
  if si_price_text.count(',') > 1 :  # since price value on singular site has comma as a digit group seperator replace it with dot
   si_price_text = si_price_text.replace(',', '.', 1)
  
  si_price = si_price_text
 
 except Exception as exc :
  print("Άλα της, μόλις πέσαμε πάνω στο exception:")
  print(str(exc))
  print("")
 
def get_custom_price(search_term) :
 global custom_price
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
  else :
   custom_price = page_soup.findAll('span', {'class' : 'ty-price-num'})
   custom_price_text = custom_price[1].text.replace('.', ',')
  
  custom_price = custom_price_text
 except Exception as exc :
  print("Άλα της, μόλις πέσαμε πάνω στο exception:")
  print(str(exc))
  print("")

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

attempt = 0  # how many attempts to re-read the url in case of failure
e = 1  # will add up in case of exceptions
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

##########################
# Setting correct paths. #
##########################

if os.path.exists(r'C:\Users\Manager\Desktop\Product') == True :  # does work folder exist?
 write_path = (r'C:\Users\Manager\Desktop\Product')
 print("Χρησιμοποιώ το " + write_path + " για ανάγνωση αρχείων.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :  # does home folder exist?
 write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
 print("Χρησιμοποιώ το home path 1 για ανάγνωση αρχείων.")
 print("")
elif os.path.exists(r"Y:\OneDrive\eShop Stuff\PRODUCT\Product") == True :  # does home folder 1 exist?
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
 read_file = ('Αλλαγή τιμών.ods')  # path to ods read file
 print("Προσπάθεια να ανοίξω το αρχείο: " + read_file + "...")
 ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
 spreadsheet = ezodf.opendoc(read_file)  # open file
 ezodf.config.reset_table_expand_strategy()  # reset ezodf config
 print('Τα καταφέραμε.')
 print("")
except :
 print("Δεν βρίσκω το αρχείο " + write_path + read_file + " ή δεν ανοίγει.")
 print("")

sheets = spreadsheet.sheets
for i in range(0, len(sheets)) :
 print('Φύλλο ' + str(i) + ': ' + sheets[i].name)

answer = 'Διάλεξε φύλλο: '
sheet_index = input(answer)
sheet = sheets[int(sheet_index)]

rowcount = sheet.nrows()
colcount = sheet.ncols()
ac_row = 1
print("")
for i in range(0, colcount) :
 print('Στήλη ' + str(i) + ': ' + str(sheet[0, i].value))

print("")
answer = 'Διάλεξε στήλη: '
col_index = input(answer)
col_index = int(col_index)
print("")

for i in range(1, rowcount):
 if str(sheet[i, col_index].value) != "None" :
  ac_row += 1
 else:
  print('Σύνολο γραμμών: ' + str(ac_row))
  print("")
  break

# for writing
os.chdir(write_path)
write_file = ("allagi_timon.xls")  # name of xls write file
alt_write_file = ("allagi_timon_alt.xls")  # alternate name of xls write file

try: 
 print("Προσπάθεια για δημιουργία: " + write_file)
 wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
 ws_write = wb_write.add_sheet("results", cell_overwrite_ok = True)  # add 1st sheet in virtual workbook
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

try :
 for i in range(1, ac_row) :
  attempt = 0  # how many attempts to re-read the url in case of failure
  e_code = str(sheet[i, col_index].value.strip())
  print(str(i) + "/" + str(ac_row) + ". Απομένουν " + str(ac_row - i))
  if e_code == "None" :
   print("Άδειο κελί. Τέλος.")
   print("")
   break
  else :
   # e_code = str(sheet[i, col_index].value).strip()
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
      break
     elif comp_name == 'CUSTOMPC' :
      get_custom_price(search_term)
      comp_price = custom_price
      break
     else :
      sin_price = ""
      custom_price = ""
      comp_price = ""
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

  print(e_code + ", CY Price: " + cy_price + ", GR Price: " + gr_price + ", COMP: " + comp_name + " - " + comp_price)
  # print("")
  ws_write.write(e, 0, e_code)
  ws_write.write(e, 1, cy_price)
  ws_write.write(e, 2, gr_price)
  ws_write.write(e, 3, comp_name)
  ws_write.write(e, 4, comp_price)
  ws_write.write(e, 5, "-")
  ws_write.write(e, 6, "-")
  ws_write.write(e, 7, "-")
  ws_write.write(e, 8, "-")
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
write_it_down(write_file, alt_write_file)