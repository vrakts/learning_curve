# Temporary test code to bring essential elements from singular

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

read_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")

os.chdir(read_path)
read_file = ('Singular_catchup.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# Counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[0]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 0
# Counting rows that contain actual data (ac_row)
for i in range(0, rowcount):
 if str(sheet[i, 0].value) != "None" :
  ac_row += 1
 else:
  break

# for writing
os.chdir(write_path)
write_file = ("Singular_catchup.xls")  # name of xls write file
alt_write_file = ("Singular_catchup_alt.xls")  # alternate name of xls write file

wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet("pareta", cell_overwrite_ok=True)  # add 1st sheet in virtual workbook
e = 0

ws_write.write(0, 0, "E-CODE")
ws_write.write(0, 1, "E-TITLE")
ws_write.write(0, 2, "E-PRICE")
ws_write.write(0, 3, "S-CODE")
ws_write.write(0, 4, "S-SKU")
ws_write.write(0, 5, "S-PRICE")
ws_write.write(0, 6, "S-AVAILABILITY")

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

for i in range(0, ac_row) :
 if str(sheet[i, 0].value).strip() == "None" :
  print("Empty cell in read file. Aborting.")
  break
 else :
  print("Starting CY parsing for " + sheet[i, 0].value.strip() + "...")
  cy_page_url = "http://www.eshopcy.com.cy/product?id=" + sheet[i, 0].value.strip()
  req = urllib.request.Request(cy_page_url, headers = headers)
  try :
   cy_uClient = uReq(req)
   cy_page_soup = soup(cy_uClient.read(), "html.parser")
   cy_uClient.close()
   print("OK.")
  except :
   print("Parsing CY failed.")
   continue
  cy_title = cy_page_soup.find("h1", {"style" : "color:#4f4f4f;font-family:Tahoma;font-size:18px;font-weight:bold;padding:0 0 0 0;"}).text.strip()
  cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
  cy_nostock = cy_page_soup.findAll("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:12px;"})
  if len(cy_price) == 0 and len(cy_nostock) > 0 :
   cy_price_text = cy_nostock[0].text.strip()
  else : 
   cy_price_text = cy_price[0].text.replace("\xa0€","").replace(".", ",")
  print("CY run " + str(i) + " done.")
  print("")
  print("Starting SI parsing...")
  pure_code = str(sheet[i, 1].value).strip().replace(' ', '+')
  si_search_url = str(sheet[i, 2].value).strip()
  req = urllib.request.Request(si_search_url, headers = headers)
  try :
   si_uClient = uReq(req)
   si_page_soup = soup(si_uClient.read(), "html.parser")
   si_uClient.close()
   print("OK.")
  except :
   print("Parsing SI failed.")
   continue
  si_price = si_page_soup.findAll("span", {"id" : re.compile('sec_product_price*')})
  if len(si_price) > 0 :
   si_price_text = si_price[0].text.replace("\xa0€","").replace(".", ",")
   si_em = si_page_soup.findAll('em')  
   for em in si_em :
    if em.text.find('Product Code') > 0 :
     si_pcode = em.text.strip().replace('Product Code', '')
     break
   si_sku = si_page_soup.find('span', {'class': 'ty-control-group__item'}).text
   si_avail = si_page_soup.find("span", {"class" : "delivery-time"})
   try :
    si_avail_text = si_avail.text.strip()
   except :
    si_avail_text = "Out of stock"
  else :
   si_price_text = "NO PRICE"
   si_pcode = ""
   si_sku = ""
   si_avail_text = ""
  print("SI run " + str(i) + " done.")
  print("")

 ws_write.write(i,0, str(sheet[i, 0].value.strip()))
 ws_write.write(i,1, cy_title)
 ws_write.write(i,2, cy_price_text)
 ws_write.write(i,3, si_pcode)
 ws_write.write(i,4, si_sku)
 ws_write.write(i,5, si_price_text)
 ws_write.write(i,6, si_avail_text)

wb_write.save(write_file)
