### crazy_fill.py

try :
 from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
 from random import randint
 from time import sleep as nani
 import requests, os, sys, re, xlwt, ezodf
except Exception as exc :
 import sys
 print("Κάτι πάθαμε κατά το import.")
 print(str(exc))
 sys.exit(0)

def files_setup() :
 global read_file_exist, wb_write, ws_write, read_file, write_file, alt_write_file, work_path, sheets, spreadsheet
 try :
  if os.path.exists(r'Z:\OneDrive\eShop Stuff\Synced') == True :
   work_path = (r'Z:\OneDrive\eShop Stuff\Synced')
  elif os.path.exists(r"K:\SALES\Stock") == True :
   work_path = (r"K:\SALES\Stock")
  print("Using " + work_path + " for writing files.")
  print("")
  os.chdir(work_path)
  if os.path.exists('Yellow Week.ods') :
   read_file = ('Yellow Week.ods')  # path to ods read file
  print("Προσπάθεια να ανοίξω το αρχείο: " + read_file + "...")
  ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
  spreadsheet = ezodf.opendoc(read_file)  # open file
  ezodf.config.reset_table_expand_strategy()  # reset ezodf config
  sheets = spreadsheet.sheets
  print('Τα καταφέραμε.')
  print("")
 except Exception as exc :
  print("Δεν βρίσκω το αρχείο Stock.ods")
  # print(str(exc))
 try :
  write_file = ("YELLOW_20.xls")  # name of xls write file
  alt_write_file = ("YELLOW_20_alt.xls")  # alternate name of xls write file
  print("Προσπάθεια για δημιουργία εικονικού αρχείου: " + write_file)
  wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
  ws_write = wb_write.add_sheet("YELLOW_20", cell_overwrite_ok = True)  # add 1st sheet in virtual workbook
  print("Γιούπι, τα καταφέραμε.")
  print("")
  ws_write.write(0, 0, "ΚΩΔΙΚΟΣ")
  ws_write.write(0, 1, "ΤΙΤΛΟΣ")
  ws_write.write(0, 2, "ΑΡΧΙΚΗ")
  ws_write.write(0, 3, "CRAZY")
  ws_write.write(0, 4, "ΚΑΤΗΓΟΡΙΑ")
 except Exception as exc :
  print("Δεν κατάφερα να γράψω το αρχείο. Έχουμε δικαιώματα;")
  print(str(exc))
  print("")

def holy_sheets(sheets) :
 global sheet, ac_row, col_index, row_index
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

 colcount = sheet.ncols()
 for i in range(0, colcount) :
  print('Στήλη ' + str(i) + ': ' + str(sheet[0, i].value))

 answer = 'Διάλεξε στήλη: '
 col_index = input(answer)
 if col_index == "" :
  col_index = 0
 else :
  col_index = int(col_index)
 print("")

 rowcount = sheet.nrows()
 ac_row = 1
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

def load_soup(page) :
 # temp_product = page[page.rfind("=") + 1:]
 # print("Loading soup for " + temp_product)
 # print("")
 result = requests.get(page, headers = headers)
 webpage = result.content
 page_soup = soup(webpage, "html5lib")
 return(page_soup)

try :
 headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
 attempt = 0
 retries = 10
 e = 1
 os.system("title " + "Creating files")
 files_setup()
 os.system("title " + "Holy Sheet")
 holy_sheets(sheets)
 for i in range(1, ac_row) :
  pcode = sheet[i, 0].value.strip()
  print_text = pcode + ". Rows left: " + str(ac_row-i) + "/" + str(ac_row)
  os.system("title " + print_text)
  page_url = "https://www.e-shop.cy/product?id=" + pcode
  page_soup = load_soup(page_url)
  price = page_soup.findAll("span", {"class" : "web-price-value-new"})
  avail = page_soup.find("td", {"style" : "text-align:left;padding:5px 0 2px 5px;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
  if len(price) == 0 :
   price_text = "0"
   avail_text = "Εξαντλημένο"
  else : 
   price_text = price[0].text.replace("\xa0€", "").replace(".", ",").strip()
   avail_text = avail.text
   if avail_text.find('ËÅÌ:') >= 0 :
    avail_text = avail_text[avail_text.find('ËÅÕ: ')+5:avail_text.find('ËÁÑ: ')-1].strip()
   else :
    avail_text = avail_text[avail_text.find('ΛΕΥ: ')+5:avail_text.find('ΛΑΡ: ')-1].strip()
   # print("CODE: " + sheet[i, 0].value + ", Price: " + price_text + ", Availability: " + avail_text)
  if avail_text == "Εξαντλημένο" :
   continue
  print("Βρήκα: " + avail_text + " στο " + pcode)
  for x in range(0, int(avail_text)) :
   """ γράψε στο νέο αρχείο """
   ws_write.write(e, 0, pcode)
   ws_write.write(e, 1, sheet[i, 1].value)
   ws_write.write(e, 2, price_text)
   ws_write.write(e, 3, sheet[i, 3].value)
   ws_write.write(e, 4, sheet[i, 5].value)
   e += 1
  print(print_text)
  print("")

 wb_write.save(write_file)
except KeyboardInterrupt :
 try :
  # print("")
  input("Διαλλειματάκι;")
  print("")
 except :
  sys.exit(0)
except Exception as exc :
 print("Exception: ")
 print(str(exc))
finally :
 wb_write.save(write_file)