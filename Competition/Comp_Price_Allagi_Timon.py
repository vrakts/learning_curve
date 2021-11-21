# Comp_Price_Allagi_Timon.py
# Έλεγχος αν η τιμή στο αρχείο Αλλαγή τιμών έχει αλλάξει σε CY, GR και ανταγωνιστές
# Ο στόχος είναι να ελέγχει αν κάποιος ανταγωνιστής έχει χαμηλότερη τιμή και να το καταγράφει.

import requests, os, sys, re, xlwt, ezodf
from bs4 import BeautifulSoup as soup
from datetime import datetime
from time import sleep as nani

def get_start_time() :
 global start_time, start_date
 start = datetime.now()
 start_date = start.strftime("%d-%m-%Y")
 start_time = start.strftime("%H:%M:%S")
 print("Εκκίνηση: " + start_date)
 print("")
 
def set_read_files() :
 global write_path, read_file, spreadsheet
 try :
  if os.path.exists(r'Z:\OneDrive\eShop Stuff\PRODUCT\Product') == True :
   write_path = (r'Z:\OneDrive\eShop Stuff\PRODUCT\Product')
  elif os.path.exists(r'Y:\OneDrive\eShop Stuff\PRODUCT\Product') == True :
   write_path = (r'Y:\OneDrive\eShop Stuff\PRODUCT\Product')
  os.chdir(write_path)
  if os.path.exists('Αλλαγή τιμών.ods') :
   read_file = ('Αλλαγή τιμών.ods')  # path to ods read file
  else :
   read_file = ('Αλλαγή τιμών_2.ods')  # path to ods read file
  # write_file = ("Comp_Price_Diffs.xls")  # name of xls write file
  # alt_write_file = ("Comp_Price_Diffs_alt.xls")  # alternate name of xls write file

  print("Προσπάθεια να ανοίξω το αρχείο: " + read_file + "...")
  ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
  spreadsheet = ezodf.opendoc(read_file)  # open file
  ezodf.config.reset_table_expand_strategy()  # reset ezodf config
  print('Τα καταφέραμε.')
  print("")
 except :
  print("Δεν βρίσκω το αρχείο " + write_path + read_file + " ή δεν ανοίγει.")
  print("")
  sys.exit()

def set_write_files(index) :
 global write_file, alt_write_file, wb_write, ws_write
 os.chdir(write_path)
 write_file = ("times_dif_" + str(index) + "-" + start_date + ".xls")  # name of xls write file
 alt_write_file = ("times_dif_alt_" + str(index) + "-" + start_date + ".xls")  # alternate name of xls write file
 wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
 ws_write = wb_write.add_sheet("results", cell_overwrite_ok = True)  # add 1st sheet in virtual workbook
 ws_write.write(0, 0, "ΚΩΔΙΚΟΣ")
 ws_write.write(0, 1, "ΤΙΤΛΟΣ")
 ws_write.write(0, 2, "ΑΡΧΕΙΟ")
 ws_write.write(0, 3, "SITE")
 ws_write.write(0, 4, "ΔΙΑΦΟΡΑ")
 ws_write.write(0, 5, "GR ΤΙΜΗ")
 ws_write.write(0, 6, "STATUS")

def set_sheets() :
 global ac_row, col_index, row_index, sheet, sheets, sheet_index
 sheet_list = []
 sheets = spreadsheet.sheets
 # for i in range(0, len(sheets)) :
  # print('Φύλλο ' + str(i + 1) + ': ' + sheets[i].name)

 print("Μαζεύω τα φύλλα... υπομονή.")
 for i in range(0, len(sheets)) :
  sheet_list.append(sheets[i].name)
 
 for i in range(0, len(sheet_list)) :
  print('Φύλλο ' + str(i + 1) + ': ' + sheet_list[i])

 answer = 'Διάλεξε φύλλο: '
 sheet_index = input(answer)
 if sheet_index == "" :
  sheet_index = 0
 else :
  sheet_index = int(sheet_index) - 1
 
 sheet = sheets[sheet_index]
 print("")
 
 rowcount = sheet.nrows()
 colcount = sheet.ncols()
 ac_row = 1
 for i in range(0, colcount) :
  print('Στήλη ' + str(i + 1) + ': ' + str(sheet[0, i].value))

 answer = 'Διάλεξε στήλη: '
 col_index = input(answer)
 if col_index == "" :
  col_index = 0
 else :
  col_index = int(col_index) - 1
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

def load_soup(page, wait, retries) :
 print("Μέσα στη σούπα του " + page + ".")
 attempt = 0
 while attempt < retries :
  try :
   result = requests.get(page, headers = headers)
   webpage = result.content
   page_soup = soup(webpage, "html5lib")
   break   
   # print("Έξω από τη σούπα.")
   # print("")
  except Exception as exc :
   print("")
   print("Στο φόρτωμα της σελίδας, πέσαμε πάνω στο:")
   print(str(exc))
   print("Ξαναπροσπαθώ σε " + str(wait)+ ".")
   nani(wait)
   attempt += 1
 if attempt == retries :
  print("Προσπάθησα " + str(attempt) + " φορές και δεν τα κατάφερα.")
  input()
  sys.exit(0)
 
 return(page_soup)

def margin_check(page_soup) :
 margin_exist = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
 stock_exist = page_soup.findAll("font", {"style" : "color:#ff0000;font-weight:bold;font-size:9px;font-family:arial black;"})
 if len(stock_exist) != 0 :  # if stock_exist not empty then stock sign exists
  margin = "STOCK"
 elif len(margin_exist) == 0 :  # if margin_exist is empty then margin sign doesn't exist and should be corrected
  margin = "MARGIN"
 else :  # if both stock sign doesn't exist and high margin exist then no changes
  margin = "-"

def get_cy_price(page_soup) :
 # global cy_price, cy_title
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
 
 return(cy_price, cy_title)

def get_gr_price(page_soup) :
 gr_title = page_soup.h1.text
 gr_price_soup = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(gr_price_soup) == 0 :
  gr_price_text = "ΕΞΑΝΤΛΗΜΕΝΟ"
 else : 
  gr_price_text = gr_price_soup[0].text.replace("\xa0€", "")
 
 try :
  gr_price = float(gr_price_text)
 except :
  gr_price = gr_price_text
 # print(str(cy_price)) 
 # cy_price = cy_price_text.replace(".", ",")
 
 return(gr_price, gr_title)

def write_it_down(write_file, alt_write_file, e) :
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
   print("Βρέθηκαν αλλαγές: " + str(e - 1))
   sys.exit(write_file + " σώθηκε στο " + write_path)

try :
 print("Αρχικοποίηση παραμέτρων...")
 test_run = 0
 attempt = 0  # how many attempts to re-read the url in case of failure
 e = 1  # will add up in case of exceptions
 retries = 10
 wait = 3
 headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
 print("Done")

 get_start_time()
 set_read_files()
 set_sheets()
 set_write_files(sheets[sheet_index].name)
 
 for i in range(row_index, ac_row) :
  e_code = str(sheet[i, col_index].value.strip())
  file_price = sheet[i, 3].value
  gr_file_price = sheet[i, 2].value
  if file_price == "" or file_price == None :
   print("Το " + e_code + " δεν έχει τιμή. Παρακάτω.")
   continue
  if ac_row - i - 1 == 0 :
   print(str(i) + "/" + str(ac_row - 1) + ".")
  else :
   print(str(i) + "/" + str(ac_row - 1) + ". Απομένουν " + str(ac_row - i - 1))
  if e_code == "None" :
   print("Άδειο κελί. Τέλος.")
   print("")
   break
  else :
   cy_page = 'https://www.e-shop.cy/product?id=' + e_code
   gr_page = 'https://www.e-shop.gr/product?id=' + e_code
   page_soup = load_soup(cy_page, wait, retries)
   cy_price, cy_title = get_cy_price(page_soup)
   gr_page_soup = load_soup(gr_page, wait, retries)
   gr_price, gr_title = get_gr_price(gr_page_soup)
  # print(e_code + ", FILE: " + str(file_price) + ", SITE: " + str(cy_price))
  # print("GR FILE: " + str(gr_file_price) + ", GR SITE: " + str(gr_price))
  # print("")
  if file_price == "" :
   cy_diff = 'ΘΕΛΕΙ ΤΙΜΗ'
  elif cy_price == 'ΕΞΑΝΤΛΗΜΕΝΟ' or gr_price == 'ΕΞΑΝΤΛΗΜΕΝΟ' :
   cy_diff = 'ΕΞΑΝΤΛΗΜΕΝΟ'
  else :
   cy_diff = float(file_price) - float(cy_price)
   gr_diff = float(gr_file_price) - float(gr_price)
   if cy_diff == 0 and gr_diff == 0 :
    price_check = "OK"
   else :
    price_check = "CHECK"
    ws_write.write(e, 0, e_code)
    ws_write.write(e, 1, cy_title)
    ws_write.write(e, 2, file_price)
    ws_write.write(e, 3, cy_price)
    ws_write.write(e, 4, cy_diff)
    ws_write.write(e, 5, gr_price)
    ws_write.write(e, 6, price_check)
    e += 1
  print(e_code + ", FILE: " + str(file_price) + ", SITE: " + str(cy_price))
  print("GR FILE: " + str(gr_file_price) + ", GR SITE: " + str(gr_price))
  if i == test_run :
   break
  try :
   print(price_check + ": " + str(e - 1))
   print("")
  except :
   print("")

except KeyboardInterrupt :
 print("")
 print("OK κατάλαβα. Διαλλειματάκι... ")
 print("")
except Exception as exc :
 print("Άλα της, μόλις πέσαμε πάνω στο exception:")
 print(str(exc))
 print("")

if e > 1 :
 write_it_down(write_file, alt_write_file, e)
else :
 print("Δεν βρέθηκαν αλλαγές δεν σώζω αρχείο.")
