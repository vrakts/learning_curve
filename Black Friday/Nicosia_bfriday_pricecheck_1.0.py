# Current Version 1.0
######################
# Changelog V 1.0
# - Compares current value with previous. If same 
#	continues to the next value to save time.
######################
# Changelog V1.1
# - Reads all values from the Showroom ods and
#	compares them to the site. If changes are
#	present writes difference to excel file.

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import urllib.request
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
import ezodf  # for the ability to write to open document format files
from datetime import date
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for system and exit functions

# Setting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)

################################
# Setting correct write paths. #
################################

if os.path.exists(r"K:\SALES\Stock\Black Friday\2019") == True :  # does work folder exist?
 write_path = (r"K:\SALES\Stock\Black Friday\2019")
 read_path = (r"K:\SALES\Stock\Black Friday\2019")
 print("Using " + write_path + " for writing files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\Stock\Black Friday\2019") == True :  # does home folder exist?
 write_path = (r"Z:\OneDrive\HTML Parser\Stock\Black Friday\2019")
 read_path = (r"Z:\OneDrive\HTML Parser\Stock\Black Friday\2019")
 print("Using home path 1 for writing files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\Stock\Black Friday\2019") == True :  # does home folder 1 exist?
 write_path = (r"W:\OneDrive\HTML Parser\Stock\Black Friday\2019")
 read_path = (r"W:\OneDrive\HTML Parser\Stock\Black Friday\2019")
 print("Using home path 2 for writing files.")
 print("")
else :
 print("Where am I?")
 sys.exit()

###############################
# End of write paths setting. #
###############################


# opening ods file for reading
os.chdir(read_path)
read_file = ('B_FRIDAY.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config

# opening xls file for writing
os.chdir(write_path)
# write_file = "Updated_B_FRIDAY_Prices.xls"  # path to xslx write file
# alt_write_file = "Updated_B_FRIDAY_Prices_ALT.xls"  # path to xslx write file
write_file = "Updated_B_FRIDAY_Prices_2.xls"  # path to xslx write file
alt_write_file = "Updated_B_FRIDAY_Prices_ALT_2.xls"  # path to xslx write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet("prices", cell_overwrite_ok=True)  # add sheet in virtual workbook
ws_write.write(0, 0, 'CODE')  # write date on A1 cell
ws_write.write(0, 1, 'TITLE')  # write date on A1 cell
ws_write.write(0, 2, 'C.PRICE')  # write date on A1 cell
ws_write.write(0, 3, 'B.PRICE')  # write date on A1 cell
ws_write.write(0, 4, 'AVAIL')  # write date on A1 cell

# opening/assigning sheets, counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[0]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
attempt = 0  # how many attempts to re-read the url in case of failure

for i in range(1, rowcount):
 # print(ac_row)
 if str(sheet[i, 0].value) != "None" :
  ac_row = ac_row + 1
 else:
  break

for i in range(1, ac_row):
 print("Rows left: " + str(ac_row-i) + "/" + str(ac_row))
 if sheet[i, 0].value != sheet[i-1, 0].value :
  page_url = "http://www.eshopcy.com.cy/product?id=" + sheet[i, 0].value
  print(page_url)
  req = urllib.request.Request(page_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    uClient = uReq(req)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    break
   except http.client.IncompleteRead :
    # print("On except :" + str(attempt))
    attempt = attempt + 1
  # price = page_soup.findAll("span", {"class" : "web-price-value-new"})
  if page_soup.h1.text == "" :
   break
  else :
   avail = page_soup.find("td", {"style" : "text-align:left;padding:5px 0 2px 5px;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
   if page_soup.find("span", {"class" : "web-price-value-old"}) == None and page_soup.find("span", {"class" : "web-price-value-new"}) == None :
    price_new_text = "0"
    price_old_text = price_new_text
    avail_text = "Εξαντλημένο"
   elif page_soup.find("span", {"class" : "web-price-value-old"}) == None :
    price_new = page_soup.find("span", {"class" : "web-price-value-new"})
    price_old = price_new
    price_new_text = float(price_new.text.replace("\xa0€", ""))
    price_old_text = price_new_text
    avail_text = avail.text
    avail_text = avail.text[avail_text.find('ΛΕΥ: ')+5:avail_text.find('ΛΑΡ: ')-1]
   else :
    price_new = page_soup.find("span", {"class" : "web-price-value-new"})
    price_old = page_soup.find("span", {"class" : "web-price-value-old"})
    price_new_text = float(price_new.text.replace("\xa0€", ""))
    price_old_text = float(price_old.text.replace("\xa0€", ""))
    avail_text = avail.text
    avail_text = avail.text[avail_text.find('ΛΕΥ: ')+5:avail_text.find('ΛΑΡ: ')-1]
   title_text = page_soup.h1.text.strip()
   # price_text = price[0].text.replace("\xa0€", "").replace(".", ",")
   # price_old_text = float(price_old.text.replace("\xa0€", ""))
   # price_new_text = float(price_new.text.replace("\xa0€", ""))
   # if avail == None :
    # avail_text = "Εξαντλημένο"
   # else :
    # avail_text = avail.text
    # avail_text = avail.text[avail_text.find('ΛΕΥ: ')+5:avail_text.find('ΛΑΡ: ')-1]
   print("CODE: " + sheet[i, 0].value + ", Price: " + str(price_old_text) + "/" + str(price_new_text) + ", Availability: " + avail_text)
   # print("CODE = " + sheet[i, 0].value + ", PRICE = " + price_text + ", available: " + avail_text)
   # ws_write.write(i, 0, sheet[i, 0].value)
   # ws_write.write(i, 1, price_text)
   # ws_write.write(i, 2, avail_text)
 else :
  print("Skipping row " + str(i) + ". Same value as the previous one")
 ws_write.write(i, 0, sheet[i, 0].value)
 ws_write.write(i, 1, title_text)
 ws_write.write(i, 2, price_old_text)
 ws_write.write(i, 3, price_new_text)
 ws_write.write(i, 4, avail_text)

wb_write.save(write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
