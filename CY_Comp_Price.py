# CY_Comp_Price
# Έλεγχος αν η τιμή είναι όντως σωστή σε σχέση με το αρχείο Αλλαγή τιμών.

import requests, os, sys, re, xlwt, ezodf
from bs4 import BeautifulSoup as soup
from datetime import datetime
from time import sleep as nani

def get_cy_price(page_soup) :
 global cy_price, cy_title
 cy_title = page_soup.h1.text
 cy_price_soup = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(cy_price_soup) == 0 :
  cy_price_text = "ΕΞΑΝΤΛΗΜΕΝΟ"
 else : 
  cy_price_text = cy_price_soup[0].text.replace("\xa0€", "")
 
 try :
  cy_price = float(cy_price_text)
 except :
  cy_price = cy_price_text
 # print(str(cy_price)) 
 # cy_price = cy_price_text.replace(".", ",")

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

try :
 if os.path.exists(r'Z:\OneDrive\eShop Stuff\PRODUCT\Product') == True :
  write_path = (r'Z:\OneDrive\eShop Stuff\PRODUCT\Product')
 elif os.path.exists(r'Y:\OneDrive\eShop Stuff\PRODUCT\Product') == True :
  write_path = (r'Y:\OneDrive\eShop Stuff\PRODUCT\Product')
 os.chdir(write_path)
 if os.path.exists('Αλλαγή τιμών_2.ods') :
  read_file = ('Αλλαγή τιμών_2.ods')  # path to ods read file
 else :
  read_file = ('Αλλαγή τιμών.ods')  # path to ods read file
 # write_path = (r'C:\Users\Manager\Desktop\Product')
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
 else :
  print('Σύνολο γραμμών: ' + str(ac_row))
  break

answer = 'Αρχική γραμμή: '
row_index = input(answer)
if row_index == "" :
 row_index = 1
else :
 row_index = int(row_index)
print("")

# for writing
os.chdir(write_path)
write_file = ("times_dif.xls")  # name of xls write file
alt_write_file = ("times_dif_alt.xls")  # alternate name of xls write file

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
ws_write.write(0, 1, "ΑΡΧΕΙΟ")
ws_write.write(0, 2, "SITE")
ws_write.write(0, 3, "DIFFERENCE")
ws_write.write(0, 4, "MARGIN")

try :
 for i in range(row_index, ac_row) :
  attempt = 0  # how many attempts to re-read the url in case of failure
  e_code = str(sheet[i, col_index].value.strip())
  file_price = sheet[i, 3].value
  if file_price == "" or file_price == None :
   print("Το " + e_code + " δεν έχει τιμή. Παρακάτω.")
   continue
  print(str(i) + "/" + str(ac_row) + ". Απομένουν " + str(ac_row - i))
  if e_code == "None" :
   print("Άδειο κελί. Τέλος.")
   print("")
   break
  else :
   # e_code = str(sheet[i, col_index].value).strip()
   cy_page = 'https://www.e-shop.cy/product?id=' + e_code
   while attempt < 3 :
    try :
     result = requests.get(cy_page, headers = headers)
     webpage = result.content
     page_soup = soup(webpage, "html5lib")
     get_cy_price(page_soup)
     margin_exist = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
     stock_exist = page_soup.findAll("font", {"style" : "color:#ff0000;font-weight:bold;font-size:9px;font-family:arial black;"})
     if len(stock_exist) != 0 :  # if stock_exist not empty then stock sign exists
      margin = "STOCK"
     elif len(margin_exist) == 0 :  # if margin_exist is empty then margin sign doesn't exist and should be corrected
      margin = "MARGIN"
     else :  # if both stock sign doesn't exist and high margin exist then no changes
      margin = "-"
      # continue
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
  print(e_code + ", FILE: " + str(file_price) + ", SITE: " + str(cy_price))
  # try :
   # # diff = float(file_price) - float(cy_price.replace(",", "."))
   # diff = float(file_price) - float(cy_price)
  # except :
   # diff = "-"
  if file_price == "" :
   diff = 'ΘΕΛΕΙ ΤΙΜΗ'
  elif cy_price == 'ΕΞΑΝΤΛΗΜΕΝΟ' :
   diff = 'ΕΞΑΝΤΛΗΜΕΝΟ'
  else :
   diff = float(file_price) - float(cy_price)
  if diff != 0 and diff != 'ΕΞΑΝΤΛΗΜΕΝΟ' :
   ws_write.write(e, 0, e_code)
   ws_write.write(e, 1, file_price)
   ws_write.write(e, 2, cy_price)
   ws_write.write(e, 3, diff)
   ws_write.write(e, 4, margin)
   e += 1
except KeyboardInterrupt :
 print("")
 print("OK κατάλαβα. Διαλλειματάκι... ")
 print("")
except Exception as exc :
 print("Άλα της, μόλις πέσαμε πάνω στο exception:")
 print(str(exc))
 print("")

write_it_down(write_file, alt_write_file)
