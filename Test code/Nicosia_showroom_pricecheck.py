from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
import ezodf  # for the ability to write to open document format files
import time  # for the ability to measure time
from datetime import date
import os  # for the ability to use os function like change folder

read_file = (r'K:\SALES\Stock\Stock.ods')  # path to ods read file
os.chdir(r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results")
write_path = os.getcwd()
write_file = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results\Updated_Showroom_Prices.xlsx")  # path to xslx write file

ezodf.config.set_table_expand_strategy('all')
spreadsheet = ezodf.opendoc(read_file)
ezodf.config.reset_table_expand_strategy()


# wb_read = xlrd.open_workbook(read_file)  # open workbook as wb works for xlsx files
# sheet = wb_read.sheet_by_index(0)  # open 1st sheet from wb works for xlsx files
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet('PriceResults')  # add sheet in virtual workbook

start_time = time.time()  # set starting time
today = date.today()
start_date = today.strftime("%d/%m/%Y")
print("Script started at " + start_date)

for i in range(1, sheet.nrows):
 page_url = "http://www.eshopcy.com.cy/product?id=" + sheet.cell_value(i,0)
 print(page_url)
 uClient = uReq(page_url)
 page_soup = soup(uClient.read(), "html.parser")
 uClient.close()
 price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(price) == 0:
  price_text = "Εξαντλημένο"
  print("CODE = " + sheet.cell_value(i, 0) + price_text)
  ws_write.write(i, 0, sheet.cell_value(i, 0))
  ws_write.write(i, 1, price_text)
 else: 
  price_text = price[0].text.replace("\xa0€", "").replace(".", ",")
  print("CODE = " + sheet.cell_value(i, 0) + ", PRICE = " + price_text)
  ws_write.write(i, 0, sheet.cell_value(i, 0))
  ws_write.write(i, 1, price_text)
 print("Rows left: " + str(sheet.nrows-i) + "/" + str(sheet.nrows))

wb_write.save(write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
