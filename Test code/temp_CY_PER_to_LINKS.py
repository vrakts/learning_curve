# PER LINKS. JUST THAT. Takes the PER from the file and resolves the actual URL.

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from urllib.request import quote
import urllib.request
from xlutils.copy import copy
from xlrd import open_workbook
import xlwt  # for the ability to write to excel (XLS) files
import ezodf  # for the ability to write to open document format (ODF) files
from datetime import date  # for the ability to get dates
import time  # for the ability to measure time
import os  # for the ability to use os functions
import os.path  # for the ability to get information on folders
import re  # for regex
import sys

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)
print("")

read_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
print("Using home path 1 for reading files.")
print("")
os.chdir(read_path)
read_file = ('SINGULAR - ΓΙΩΡΓΟΣ.ods')  # path to ods read file
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

write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
print("Using Z:\OneDrive\ for writing files.")
print("")

os.chdir(write_path)
write_file = ("PER_LINKS.xls")  # name of xls write file
alt_write_file = ("PER_LINKS_alt.xls")  # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok=True)  # add 1st sheet in virtual workbook
ws_write.write(0, 0, "PRODUCT CODE")  # write title on A1 cell
ws_write.write(0, 1, "TITLE")  # write title on B1 cell
ws_write.write(0, 2, "ESHOP LINK")  # write title on C1 cell
ws_write.write(0, 3, "PER LINK")  # write title on D1 cell

attempt = 0  # how many attempts to re-read the url in case of failure
sorry = 0  # will add up in case of exceptions
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

for i in range (1, ac_row) :
 cy_page_url = "http://www.eshopcy.com.cy/product?id=" + sheet[i, 0].value.strip()  # add stripped product code to product url
 req = urllib.request.Request(cy_page_url, headers = headers)
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
   time.sleep(5)
  except urllib.error.URLError as exc:
   # print("2")
   print("Oops, just bumped into the following Requests exception: " + str(exc))
   attempt += 1
   sorry += 1
   print("Retrying in 5 seconds.")
   time.sleep(5)
  except Exception as exc :
   # print("3")
   print("Oops, just bumped into the following exception: " + str(exc))
   attempt += 1
   sorry += 1
   print("Retrying in 5 seconds.")
   time.sleep(5)
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
 cy_per = cy_page_soup.find('td', {'style' : 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text.strip()
 cy_title = cy_page_soup.find('h1', {'style' : 'color:#4f4f4f;font-family:Tahoma;font-size:18px;font-weight:bold;padding:0 0 0 0;'}).text.strip()
 cy_link = cy_page_soup.find('link', {'rel' : 'canonical'})['href'].strip()
 cy_perlink = "http://www.eshopcy.com.cy/product?id=" + cy_per
 ws_write.write(i,0, cy_per)
 ws_write.write(i,1, cy_title)
 ws_write.write(i,2, cy_link)
 ws_write.write(i,3, cy_perlink)
 print(cy_per + " - " + cy_title)
 print(cy_link)
 print(cy_perlink)
 print("")

try :
 wb_write.save(write_file)
except :
 wb_write.save(alt_write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = (str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
print("Script executed in: " + formatted_time)

