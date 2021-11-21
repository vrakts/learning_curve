from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
import ezodf  # for the ability to write to open document format files
from datetime import date
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder

# Setting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)

# opening ods file for reading
read_file = (r'K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Ανταγωνισμός Λευκωσίας SUM.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config

# opening xlsx file for writing
write_path = os.getcwd()
write_file = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results\High_Margin_Check.xlsx")  # path to xslx write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date)  # add sheet in virtual workbook
ws_write.write(0, 0, start_date)  # write date on A1 cell

# opening/assigning sheets, counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[0]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows.
colcount = sheet.ncols()

page_url = "http://www.eshopcy.com.cy/product?id="
q_url = page_url + sheet[1, 0].value

# sample urls with and without margin sign
# q_url1 = "http://www.eshopcy.com.cy/product?id=TEL.002161"  # no margin
# q_url2 = "http://www.eshopcy.com.cy/product?id=PER.155828"  # has margin

for i in range(1, 5):
 print("Rows left: " + str(rowcount-i) + "/" + str(rowcount))
 page_url = "http://www.eshopcy.com.cy/product?id=" + sheet[i, 2].value
 print(page_url)
 uClient = uReq(page_url)
 page_soup = soup(uClient.read(), "html.parser")
 uClient.close()
 q_margin = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
 if len(q_margin) == 0 :
  print("For " + sheet[i, 2].value + " margin doesn't exist")
  ws_write.write(i, 0, sheet[i, 0].value)
  ws_write.write(i, 1, "NO")
 else: 
  print("For " + sheet[i, 2].value + " margin exists")
  ws_write.write(i, 0, sheet[i, 2].value)
  ws_write.write(i, 1, "YES")

wb_write.save(write_file)







# margin check code follows
q_margin = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
q_margin

if len(q_margin) == 0 :
 print( "For " + q_url1 + " margin doesn't exist")
else :
 print( "For " + q_url1 + " margin exists")


 
uClient = uReq(q_url2)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()
q_margin = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
q_margin

if len(q_margin) == 0 :
 print( "For " + q_url2 + " margin doesn't exist")
else :
 print( "For " + q_url2 + " margin exists")
 
