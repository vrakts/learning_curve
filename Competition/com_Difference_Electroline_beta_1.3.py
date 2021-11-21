# Current Version 1.3 beta
##########################
# Reads the product codes from the competition file, and compares all values
# to the ones retrieved by the CY and Electroline website. Will only write the changes
# found in an xls file.
##########################
# Changelog 1.3 beta:
# - Minor bug fixing: Calculation formulas are now more accurate, results are more accurate 
#	and correctly calculates which product codes and or price values are different to write
#	on the output xls file.
# - Attempt to trap HTTP read errors.
# Changelog 1.2:
# - Fixed the functions that converted the int and floats to wrong values
# Changelog 1.1:
# - New folder calculation function decides which folder to read from and write on
# - Will write only the values that have difference from the ones on file
# - Accurately retrieves prices from the original file regardless  to mistakes in data entry
# - Will open the product page to get availability, product code and product price 
#	instead of getting only the price from the query page
# - Will try to write to the default file and if error occurs will write to a 2nd one
# - Much slower since it has to open 3 pages, 1 for the CP query page,
#	1 for the CP product page and 1 for the CY product page
# Changelog 1.0:
# - Reads all values on a predefined file
# - Writes back to a predefined file all information: CY and CP code and prices found from the 
#	query pages
##########################
# -- To do: Retry incase of http read failure or keep the last read row and continue
#	from there in the next run, calculate average time between products.
##########################

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import urllib.request
import xlrd  # for the ability to read excel (XLS) files
import xlwt  # for the ability to write to excel (XLS) files
import ezodf  # for the ability to write to open document format (ODF) files
from datetime import date  # for the ability to get dates
import time  # for the ability to measure time
import os  # for the ability to use os functions
import os.path  # for the ability to get information on folders
import re  # for regex
import sys

##########################################
# Setting starting date and time values. #
##########################################

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)
print("")

################################
# End of date and time setting #
################################

###############################
# Setting correct read paths. #
###############################

if os.path.exists(r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας') == True :  # does work folder exist?
 read_path = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας')
 print("Using " + read_path + " for reading files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\Ανταγωνισμός Λευκωσίας") == True :  # does home folder exist?
 read_path = (r"Z:\OneDrive\HTML Parser\Ανταγωνισμός Λευκωσίας")
 print("Using home path 1 for reading files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\Ανταγωνισμός Λευκωσίας") == True :  # does home folder 1 exist?
 read_path = (r"W:\OneDrive\HTML Parser\Ανταγωνισμός Λευκωσίας")
 print("Using home path 2 for reading files.")
 print("")
else :
 print("No folders or files found. Where am I?")
 sys.exit()

##############################
# End of read paths setting. #
##############################

################################
# Setting correct write paths. #
################################

if os.path.exists(r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
 print("Using " + write_path + " for writing files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\Ανταγωνισμός Λευκωσίας") == True :  # does home folder exist?
 write_path = (r"Z:\OneDrive\Ανταγωνισμός Λευκωσίας")
 print("Using home path 1 for writing files.")
 print("")
elif os.path.exists(r"W:\OneDrive\Ανταγωνισμός Λευκωσίας") == True :  # does home folder 1 exist?
 write_path = (r"W:\OneDrive\Ανταγωνισμός Λευκωσίας")
 print("Using home path 2 for writing files.")
 print("")
else :
 if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Using " + write_path + " for writing files.")
  print("")
 else :  # if not create it
  os.makedirs(r"C:\TEMPYTH")
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Creating and using " + write_path + " for writing files.")
  print("")

###############################
# End of write paths setting. #
###############################

# Opening files
# For reading
os.chdir(read_path)
read_file = ('ELECTROLINE - ΜΙΧΑΛΗΣ.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# for writing
os.chdir(write_path)
write_file = ("CY_Electroline_Difference.xls")  # name of xls write file
alt_write_file = ("CY_Electroline_Difference.xls")  # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date)  # add 1st sheet in virtual workbook
ws_write.write(0, 0, "ESHOPCY")  # write title on A1 cell
ws_write.write(0, 1, "PRICE")  # write title on B1 cell
ws_write.write(0, 2, "ELECTROLINE")  # write title on C1 cell
ws_write.write(0, 3, "PRICE")  # write title on D1 cell
ws_write.write(0, 4, "ONLINE")  # write title on E1 cell
ws_write.write(0, 5, "STORE")  # write title on F1 cell

##################################
# Sheet and row/columns setting. #
##################################

# Counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[0]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1
# Counting rows that contain actual data (ac_row)
for i in range(1, rowcount):
 if str(sheet[i, 0].value) != "None" :
  ac_row = ac_row + 1
 else:
  break

e = 1  # this is the counter for the excel write file
attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

#########################################
# End of sheet and row/columns setting. #
#########################################

#############################
# Parsing code starts here. #
#############################

for i in range(1, ac_row) :
 print("Processing row: " + str(i) + " / " + str(ac_row - 1) + ". Remaining: " + str((ac_row -1) - i) + ".")
 if str(sheet[i, 0].value).strip() == "None" :
  print("Empty cell in read file. Aborting.")
  break
 else:
  # Starting EL parsing
  pure_code = str(sheet[i, 2].value).strip().replace('.0', '')  # clean up the product code from . and 0s
  # print("pure_code is: " + pure_code)
  el_search_url = "https://www.electroline.com.cy/?s=" + pure_code + "&post_type=product&dgwt_wcas=1"
  # print("el_search_url is: " + el_search_url)
  req = urllib.request.Request(el_search_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    el_uClient = uReq(req)
    el_page_soup = soup(el_uClient.read(), "html.parser")
    el_uClient.close()
    break
   except http.client.IncompleteRead :
    # print("On except :" + str(attempt))
    attempt = attempt + 1
   # else :
    # pass
  el_price = el_page_soup.findAll("span", {"class" : "price_int"})  # find EL price from the query page
  if len(el_price) == 0 :  # if el_price table is empty
   # print("el_price table emtpy")   
   el_price_text = ""  # then probably item is out of stock
   el_pcode = "NOSTOCK"
   el_avail = "Out of stock"
   pass
  else :
   # el_price = el_page_soup.findAll('span', {'class' : 'ty-price-num'})  # find all price related info from the product page
   el_price_text = el_price[0].text.strip().replace('€', '').replace('.', ',')  # keep only the price value of the first find (other values are for related products)
   # print("el_price_text: " + str(el_price_text))
   el_online_avail = el_page_soup.find('div', {'class': 'col-xs-7 col-md-6 delivery-options'})
   el_online_avail_text = el_online_avail.text.strip()
   el_store_avail = el_page_soup.find('div', {'class': 'row productDividerLine store-availability'})
   el_store_avail_text = el_store_avail.img['title']
   if el_store_avail_text == "In Stock" :
    el_store_avail_text = "ΔΙΑΘΕΣΙΜΟΤΗΤΑ ΚΑΤΑΣΤΗΜΑΤΩΝ"
   else :
    el_store_avail_text = "ΜΗ ΔΙΑΘΕΣΙΜΟ"
  # End of EL parsing
  # Starting CY parsing
  cy_page_url = "http://www.eshopcy.com.cy/product?id=" + sheet[i, 0].value.strip()  # add stripped product code to product url
  req = urllib.request.Request(cy_page_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    cy_uClient = uReq(req)
    cy_page_soup = soup(cy_uClient.read(), "html.parser")
    cy_uClient.close()
    break
   except http.client.IncompleteRead :
    attempt += 1
   # else :
    # pass
  cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})  # extract price from the product url
  if len(cy_price) == 0 :  # if the prices table length is zero
   cy_price_text = ""  # then product is out of stock so no price
  else : 
   cy_price_text = cy_price[0].text.replace("\xa0€","").replace(".", ",")  # otherwise get price stripped from euro signs and .
  cy_temp_price = str(sheet[i, 3].value).strip().replace('€', '').strip()  # set a temp price for the CY price in the excel without zeros and stripped
  if cy_temp_price == "None" :  # if temp price is empty
   cy_temp_price = ""  # set temp price as ""
   # print("cy_temp_price is empty. Not changed")
  elif cy_temp_price.find(',') > 0 :  # if it has a , then it is a float
   if (cy_temp_price[:-1] != 0) and len(cy_temp_price[cy_temp_price.find(',')+1:]) == 1 :  # if the last number is not a zero and there is only 1 digit after ,
    cy_temp_price = cy_temp_price + "0"  # then add a zero to the end.
    # print("cy_temp_price is a float with 1 digit at the end. Added 1 zero.")
  else :
   cy_temp_price = str(sheet[i, 3].value).strip().replace('€', '').strip() + ",00"  # if cy_temp_price is not a float, add ,00
   # print("cy_temp_price not a float. Changed temp price to ,00")
  el_temp_price = str(sheet[i, 4].value).strip().replace('€', '').strip()  # set a temp price for the CP price in the excel without zeros and stripped
  if el_temp_price == "None" :  # if temp price is empty
   el_temp_price = ""  # set temp price as ""
   # print("el_temp_price is empty. Not changed")
  elif el_temp_price.find(',') > 0 :  # if it has a , then it is a float
   if (el_temp_price[:-1] != 0) and len(el_temp_price[el_temp_price.find(',')+1:]) == 1 :  # if the last number is not a zero and there is only 1 digit after ,
    el_temp_price = el_temp_price + "0"  # then add a zero to the end.
    # print("el_temp_price is a float with 1 digit at the end. Added 1 zero.")
  else :
   el_temp_price = str(sheet[i, 4].value).strip().replace('€', '').strip() + ",00"  # if el_temp_price is not a float, add ,00
   # print("el_temp_price not a float. Changed temp price to ,00")
  if (cy_price_text != cy_temp_price) or (el_price_text != el_temp_price) :  # if price on file and on site are different then write them on the excel file otherwise start from the top.
   # print("CY - " + cy_price_text + " excel - " + temp_price + " CP - " + el_price_text + " excel - " + str(sheet[i, 4].value).strip().replace('€', '').strip())
   ws_write.write(e,0, str(sheet[i, 0].value.strip()))
   ws_write.write(e,1, cy_price_text)
   ws_write.write(e,2, pure_code)
   ws_write.write(e,3, el_price_text)
   ws_write.write(e,4, el_online_avail_text)
   ws_write.write(e,5, el_store_avail_text)
   e = e + 1
 # print("CY = " + str(sheet[i, 0].value.strip()) + ", PRICE = " + cy_price_text + ", EL = " + pure_code + ", PRICE = " + el_price_text + ", AVAIL = " + el_online_avail_text + " / " + el_store_avail_text)
 print("EshopCY Code: " + str(sheet[i, 0].value.strip()) + ", Price File/Site: " + cy_temp_price + "/" + cy_price_text)
 print("Electroline Code: " + pure_code + ", Price File/Site: " + el_temp_price + "/" + el_price_text)
 print("Availability - Online/Store: " + el_online_avail_text + "/" + el_store_avail_text)
 print("")

########################
# End of parsing code. #
########################

# try to write to the 1st file. If it fails try the 2nd
try :
 wb_write.save(write_file)
except :
 wb_write.save(alt_write_file)

if e > 1 :
 print("Found " + str(e) + " changes.")
else :
 print("Congrats. You are up to date.")

#############################
# Calculating elapsed time. #
#############################

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = (str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
print("Script executed in: " + formatted_time)

################
# End of flie. #
################

