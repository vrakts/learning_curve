# Current Version 1.1
#####################
# Reads all products that need to be opened in the CY site
# listed in an ods file and returns the GR site price or out of stock status
#####################
# Changelog V1.1
# - Asks for user to input the read file.
# - Opens the file from a predefined folder.
# Changelog V1.0
# - Opens a predefine file and folder.
# - Writes to predefined file and folder.

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
import ezodf  # for the ability to write to open document format files
from datetime import date
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder

# Input search term
answer_term = "no"

while (answer_term == "no") :
 file_name = input("Please enter the file name: ")
 answer_text = "File name is: " + file_name + ". Is that correct? Press enter for yes. "
 answer_term = input(answer_text)

# Setting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)

file_path = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY')  # path to read and write file
write_path = os.chdir(file_path)  # change active directory to file_path

# opening ods file for reading
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(file_name)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config

# opening xls file for writing
write_date = file_name.find("-")
write_file = (file_name[:file_name.find("-")+1] + "Products_Upload_Prices.xls")  # path to xslx write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet("GR_PRICES")  # add 1st sheet in virtual workbook
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
  print("Rows left: " + str(ac_row-i) + "/" + str(ac_row))
  page_url = "https://www.e-shop.gr/s/" + sheet[i, 2].value.strip()
  uClient = uReq(page_url)
  page_soup = soup(uClient.read(), "html.parser")
  uClient.close()
  gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
  if len(gr_price) == 0 :
   gr_price_text = "Εξαντλημένο"
   print("CODE = " + str(sheet[i, 2].value.strip()) + ", εξαντλημένο.")
   ws_write.write(i,0, str(sheet[i, 2].value.strip()))
   ws_write.write(i,1, gr_price_text)
  else : 
   gr_price_text = gr_price[0].text.replace("\xa0€","").replace(".", ",")
   print("CODE = " + str(sheet[i, 2].value.strip()) + ", PRICE = " + gr_price_text)
   ws_write.write(i,0, str(sheet[i, 2].value.strip()))
   ws_write.write(i,1, gr_price_text)

wb_write.save(write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
