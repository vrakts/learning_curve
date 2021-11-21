from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
import ezodf  # for the ability to write to open document format files
from datetime import date
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import re  # for regex

# Setting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)

# opening ods file for reading
read_file = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας\ELECTROLINE - ΜΙΧΑΛΗΣ.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config

# opening xls file for writing
write_path = os.getcwd()
write_file = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results\com_Electroline_Price_Check.xls")  # path to xslx write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet("Electroline")  # add 1st sheet in virtual workbook
ws_write.write(0, 0, start_date)  # write date on A1 cell

# opening/assigning sheets, counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[0]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1

for i in range(1, rowcount):
 # print(ac_row)
 if str(sheet[i, 2].value) != "None" :
  ac_row = ac_row + 1
 else:
  break

for i in range(1, ac_row):
 if str(sheet[i, 2].value) == "None" :
  break
 else:
  pure_code = str(sheet[i, 2].value).strip().replace('.0', '')
  print("Rows left: " + str(ac_row-i) + "/" + str(ac_row))
  page_url = "https://www.electroline.com.cy/?s=" + pure_code + "&post_type=product&dgwt_wcas=1"
  uClient = uReq(page_url)
  page_soup = soup(uClient.read(), "html.parser")
  uClient.close()
  el_price = page_soup.findAll("span", {"class" : "price_int"})
  if len(el_price) == 0 :
   el_price_text = "Εξαντλημένο"
   print("CODE = " + pure_code + ", εξαντλημένο.")
   ws_write.write(i,0, pure_code)
   ws_write.write(i,1, el_price_text)
  else : 
   el_price_text = el_price[0].text.strip().replace('€', '').replace('.', ',')
   print("CODE = " + pure_code + ", PRICE = " + el_price_text)
   ws_write.write(i,0, pure_code)
   ws_write.write(i,1, el_price_text)

wb_write.save(write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
