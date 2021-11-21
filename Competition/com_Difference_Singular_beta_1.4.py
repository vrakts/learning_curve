# Current Version 1.4 beta
##########################
# Reads the product codes from the competition file, and compares all
# values to the ones retrieved by the CY and Singular website.
# Will only write the changes found in an xls file.
##########################
# Changelog 1.4 beta:
# - Update for the new e-shop.cy domain
# - Searches for both SKU and Product Code from Singular.
# - Trying new methods for HTTP read errors. So far not looking good.
# - As a workaround, saves the results file on each 10 queries
#	and continue from there on the next try. To do that it compares
#	the last query line from the last line in the competition ods file.
# Changelog 1.3 beta:
# - Minor bug fixing: Calculation formulas are now more accurate,
#	results are more accurate and correctly calculates which product
#	codes and or price values are different to write
#	on the output xls file.
# - Attempt to trap HTTP read errors.
# Changelog 1.2:
# - Fixed the functions that converted the int and floats to wrong values
# Changelog 1.1:
# - New folder calculation function decides which folder to read from and write on
# - Will write only the values that have difference from the ones on file
# - Accurately retrieves prices from the original file regardless to mistakes in data entry
# - Will open the product page to get availability, product code and product price 
#	instead of getting only the price from the query page
# - Will try to write to the default file and if error occurs will write to a 2nd one
# - Much slower since it has to open 3 pages, 1 for the SI query page,
#	1 for the SI product page and 1 for the CY product page
# Changelog 1.0:
# - Reads all values on a predefined file
# - Writes back to a predefined file all information: CY and SI code and prices found from the 
#	query pages
##########################
# -- To do: Retry incase of http read failure or keep the last read row and continue
#	from there in the next run, calculate average time between products.
##########################

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from urllib.request import quote, Request
# from urllib.request import Request
# import urllib.request
from xlutils.copy import copy
from xlrd import open_workbook
import xlwt  # for the ability to write to excel (XLS) files
import ezodf  # for the ability to write to open document format (ODF) files
from datetime import date  # for the ability to get dates
# import time  # for the ability to measure time
# from time import sleep, time
from time import time
import os  # for the ability to use os functions
import os.path  # for the ability to get information on folders
import re  # for regex
import sys

##########################################
# Setting starting date and time values. #
##########################################

start_time = time()  # set starting time
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
elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :  # does home folder exist?
 read_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
 print("Using home path 1 for reading files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :  # does home folder 1 exist?
 read_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
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
elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :  # does home folder exist?
 write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
 print("Using home path 1 for writing files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :  # does home folder 1 exist?
 write_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
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

#################
# Opening files #
#################

# For reading
os.chdir(read_path)
read_file = ('SINGULAR - ΣΠΥΡΟΣ.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# Counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[0]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1
# Counting rows that contain actual data (ac_row)
for i in range(1, rowcount):
 if str(sheet[i, 0].value) != "None" :
  ac_row += 1
 else:
  break

# for writing
os.chdir(write_path)
write_file = ("CY_Singular_Difference.xls")  # name of xls write file
alt_write_file = ("CY_Singular_Difference_alt.xls")  # alternate name of xls write file
# write_file = ("test_file.xls")  # name of xls write file
# alt_write_file = ("test_file_alt.xls")  # alternate name of xls write file

try: 
 print("Trying to open file: " + write_file + "...")
 wb_read = open_workbook(write_file, formatting_info=True)
 ws_read = wb_read.sheet_by_index(0)
 # ws_read_rows = ws_read.nrows
 # for writing
 wb_write = copy(wb_read) 
 ws_write = wb_write.get_sheet(0)
 print("... success. Using last known row.")
 print("")
 if ws_read.cell_value(0, 6) == "" or ws_read.cell_value(0, 6) == "0" :
  last_read = 1
  e = 0
 else :
  last_read = int(ws_read.cell_value(0, 6))
  e = ws_read.nrows - 1
 file_is_there = 1
except :
 print("File: " + write_file + " not found. Creating one now.")
 wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
 ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok=True)  # add 1st sheet in virtual workbook
 last_read = 1
 e = 0
 file_is_there = 0

ws_write.write(0, 0, "ESHOPCY")  # write title on A1 cell
ws_write.write(0, 1, "PRICE")  # write title on B1 cell
ws_write.write(0, 2, "SINGULAR_PCODE")  # write title on C1 cell
ws_write.write(0, 3, "SINGULAR_SKU")  # write title on D1 cell
ws_write.write(0, 4, "PRICE")  # write title on E1 cell
ws_write.write(0, 5, "AVAILABILITY")  # write title on F1 cell

if last_read == (ac_row - 1) :
 print("File already run. Aborting")
 sys.exit()
elif last_read != (ac_row - 1) and last_read > 0 :
 start_from = last_read
else :
 start_from = 1

print("Starting from row: " + str(start_from))

########################
# End of opening files #
########################

# e = 0  # this is the counter for the xls write file
attempt = 0  # how many attempts to re-read the url in case of failure
sorry = 0  # will add up in case of exceptions
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

#############################
# Parsing code starts here. #
#############################

for i in range(start_from, ac_row) :
# for i in range(24, 30) :
 print("Processing row: " + str(i) + " / " + str(ac_row - 1) + ". Remaining: " + str((ac_row -1) - i) + ".")
 ws_write.write(0, 6, i)  # write the current row on G1
 ws_write.write(0, 7, str(sheet[i, 0].value).strip())  # write the PER value on H1
 if (i % 5) == 0 :
  print("File saved on row: " + str(i) + ".")
  print("")
  wb_write.save(write_file)
  wb_read = open_workbook(write_file, formatting_info=True)
  wb_write = copy(wb_read) 
  ws_write = wb_write.get_sheet(0)
 else :
  pass
 if str(sheet[i, 0].value).strip() == "None" :
  print("Empty cell in read file. Aborting.")
  break
 # elif start_from == ac_row - 1 :
  # print("File is up to date. Aborting.")
  # break
 else :
  # Starting SI parsing
  # pure_code = str(sheet[i, 2].value).strip().replace('.0', '')  # clean up the product code from . and 0s
  if str(sheet[i, 3].value).strip() == "Κατεβασμένο" and str(sheet[i, 2].value).strip() == "None" :
   print("No SKU or other code found for Singular. On to the next product.")
   continue
  else :
   pure_code = str(sheet[i, 2].value).strip().replace(' ', '+')
  # elif str(sheet[i, 3].value).strip() == "Κατεβασμένο":
   # print("No SKU found for Singular. Using old code.")
   # pure_code = str(sheet[i, 2].value).strip().replace(' ', '+')
  # else :
   # pure_code = str(sheet[i, 3].value).strip().replace(' ', '+')
  # pure_code = str(sheet[i, 3].value).strip().replace(' ', '+')  # clean up the product code from start and ending spaces - replace in between spaces with +
  pure_code = quote(pure_code.encode('iso-8859-7')).replace('%2B', '+')
  # print("pure_code is: " + pure_code)
  si_search_url = "https://www.singular.com.cy/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&search_id=&q=" + pure_code + "&dispatch=products.search"
  # print("si_search_url is: " + si_search_url)
  req = Request(si_search_url, headers = headers)
  # print("req is: " + str(req))
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    si_uClient = uReq(req)
    break
   except ValueError as exc :
    # print("1")
    print("Oops, just bumped into the following ValueError exception: " + str(exc))
    attempt += 1
    sorry += 1
    print("Retrying in 5 seconds.")
    sleep(5)
   except urllib.error.URLError as exc:
    # print("2")
    print("Oops, just bumped into the following Requests exception: " + str(exc))
    attempt += 1
    sorry += 1
    print("Retrying in 5 seconds.")
    sleep(5)
   except Exception as exc :
    # print("3")
    print("Oops, just bumped into the following exception: " + str(exc))
    attempt += 1
    sorry += 1
    print("Retrying in 5 seconds.")
    sleep(5)
  if attempt == 3 :
   print("")
   print("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
   print("")
   break
  print("Singular read OK.")
  try :
   si_page_soup = soup(si_uClient.read(), "html.parser")
   print("Singular soup OK.")
  except exception as exc:
   print("Oops, just bumped into the following exception while creating the soup: " + str(exc))
   continue
  try :
   si_uClient.close()
   print("Singular connection close OK.")
  except exception as exc:
   print("Oops, just bumped into the following exception while closing the connection: " + str(exc))
   continue
   # else :
    # pass
  # if si_page_soup.find('span', {'class': 'ty-control-group__item'}) == None :
   # si_sku = "Κατεβασμένο"
  # else :
   # si_sku = si_page_soup.find('span', {'class': 'ty-control-group__item'}).text
  si_price = si_page_soup.findAll("span", {"id" : re.compile('sec_product_price*')})  # find SI price from the query page
  if len(si_price) == 0 :  # if si_price table is empty
   # print("si_price table emtpy")   
   si_price_text = ""  # then probably item is out of stock
   si_pcode = "Κατεβασμένο"
   si_sku = "Κατεβασμένο"
   si_avail = "Κατεβασμένο"
   print("Search for " + str(sheet[i, 0].value.strip()) + " came up empty on Singular. On to the next code.")
   print("")
   continue
  else :
   # si_price = si_page_soup.findAll('span', {'class' : 'ty-price-num'})  # find all price related info from the product page
   si_price_text = si_price[0].text.replace("\xa0€","").replace(".", ",")  # keep only the price value of the first find (other values are for related products)
   if si_price_text.count(',') > 1 :  # since price value on singular site has comma as a digit group seperator replace it with dot
    si_price_text = si_price_text.replace(',', '.', 1)
   si_em = si_page_soup.findAll('em')  # contains all EM tags that have the product ID SKU and other info
   for em in si_em :
    if em.text.find('Product Code') > 0 :
     si_pcode = em.text.strip().replace('Product Code', '')
     break
   si_sku = si_page_soup.find('span', {'class': 'ty-control-group__item'}).text
   # print("si_price_text: " + str(si_price_text))
   si_avail = si_page_soup.find("span", {"class" : "delivery-time"})
   if si_avail == None :
    si_avail_text = "Out of stock"
   else :
    si_avail_text = si_avail.text.strip()
  # End of SI parsing
  # Starting CY parsing
  cy_page_url = "https://www.e-shop.cy/product?id=" + sheet[i, 0].value.strip()  # add stripped product code to product url
  req = Request(cy_page_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    cy_uClient = uReq(req)
    break
   except ValueError as exc :
    # print("1")
    print("Oops, just bumped into the following ValueError exception: " + str(exc))
    attempt += 1
    sorry += 1
    print("Retrying in 5 seconds.")
    sleep(5)
   except urllib.error.URLError as exc:
    # print("2")
    print("Oops, just bumped into the following Requests exception: " + str(exc))
    attempt += 1
    sorry += 1
    print("Retrying in 5 seconds.")
    sleep(5)
   except Exception as exc :
    # print("3")
    print("Oops, just bumped into the following exception: " + str(exc))
    attempt += 1
    sorry += 1
    print("Retrying in 5 seconds.")
    sleep(5)
  if attempt == 3 :
   print("")
   print("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
   print("")
   break
  print("CY read OK.")
  try :
   cy_page_soup = soup(cy_uClient.read(), "html.parser")
   print("CY soup OK.")
  except exception as exc:
   print("Oops, just bumped into the following exception while creating the soup: " + str(exc))
   continue
  try :
   cy_uClient.close()
   print("CY connection close OK.")
  except exception as exc:
   print("Oops, just bumped into the following exception while closing the connection: " + str(exc))
   continue
  cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})  # extract price from the product url
  if len(cy_price) == 0 :  # if the prices table length is zero
   cy_price_text = ""  # then product is out of stock so no price
  else : 
   cy_price_text = cy_price[0].text.replace("\xa0€","").replace(".", ",")  # otherwise get price stripped from euro signs and .
    # set a temp price for the CY price in the excel without zeros and stripped
  if str(sheet[i, 4].value) == "None" :   # if price value on file is empty
   cy_temp_price = ""   # set temp price as ""
  else :
   cy_temp_price = str(sheet[i, 4].value).strip().replace('€', '').strip()
   # print("cy_temp_price is empty. Not changed")
   if cy_temp_price.find(',') > 0 :  # if it has a , then it is a float
    if (cy_temp_price[:-1] != 0) and len(cy_temp_price[cy_temp_price.find(',')+1:]) == 1 :  # if the last number is not a zero and there is only 1 digit after ,
     cy_temp_price = cy_temp_price + "0"  # then add a zero to the end.
    # print("cy_temp_price is a float with 1 digit at the end. Added 1 zero.")
   else :
    cy_temp_price = str(sheet[i, 4].value).strip().replace('€', '').strip() + ",00"  # if cy_temp_price is not a float, add ,00
    # print("cy_temp_price not a float. Changed temp price to ,00")
  # print("Current price on file is: " + str(sheet[i, 8].value).strip())
  si_temp_price = str(sheet[i, 8].value).strip().replace('€', '').replace('.', ',').strip()  # set a temp price for the SI price in the excel without zeros and stripped
  # print("si_temp_price: " + si_temp_price)
  if si_temp_price == "None" :  # if temp price is empty
   si_temp_price = ""  # set temp price as ""
   # print("si_temp_price is empty. Not changed")
  elif si_temp_price.find(',') > 0 :  # if it has a , then it is a float
   if (si_temp_price[:-1] != 0) and len(si_temp_price[si_temp_price.find(',')+1:]) == 1 :  # if the last number is not a zero and there is only 1 digit after ,
    si_temp_price = si_temp_price + "0"  # then add a zero to the end.
    # print("si_temp_price is a float with 1 digit at the end. Added 1 zero.")
  elif si_temp_price.find(',') < 0 :  # if it doesn't have a , then it is not a float
   si_temp_price = str(sheet[i, 5].value).strip().replace('€', '').strip() + ",00"  # if si_temp_price is not a float, add ,00
   # print("si_temp_price not a float. Changed temp price to ,00")
  if (cy_price_text != cy_temp_price) or (si_price_text != si_temp_price) :  # if price on file and on site are different then write them on the excel file otherwise start from the top.
   # print("CY - " + cy_price_text + " excel - " + cy_temp_price + " SI - " + si_price_text + " excel - " + si_temp_price)
   e += 1
   ws_write.write(e,0, str(sheet[i, 0].value.strip()))
   ws_write.write(e,1, cy_price_text)
   ws_write.write(e,2, si_pcode)
   ws_write.write(e,3, si_sku)
   ws_write.write(e,4, si_price_text)
   ws_write.write(e,5, si_avail_text)
   
 print("EshopCY Code: " + str(sheet[i, 0].value.strip()) + ", Price File/Site: " + cy_temp_price + "/" + cy_price_text)
 print("Singular Code: " + si_pcode + ", SKU: " + si_sku + ", Price File/Site: " + si_temp_price + "/" + si_price_text)
 print("Availability: " + si_avail_text)
 if sorry > 0 :
  print("Exceptions caught: " + str(c))
 print("")
 # print(str(i))
 # ws_write.write(e,0, str(sheet[i, 0].value.strip()))
 # ws_write.write(e,1, cy_price_text)
 # ws_write.write(e,2, pure_code)
 # ws_write.write(e,3, si_sku)
 # ws_write.write(e,4, si_price_text)
 # ws_write.write(e,5, si_avail_text)
 # e = e + 1

########################
# End of parsing code. #
########################

# try to write to the 1st file. If it fails try the 2nd
try :
 wb_write.save(write_file)
except :
 wb_write.save(alt_write_file)

if e == 1 :
 print("Found " + str(e) + " change.")
elif e > 1 :
 print("Found " + str(e) + " changes.")
else :
 print("Congrats. You are up to date.")

#############################
# Calculating elapsed time. #
#############################

elapsed_time = time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = (str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
print("Script executed in: " + formatted_time)

################
# End of flie. #
################

