# Current Version 1.2 BETA
##########################
# Reads all products that need to be opened in the CY site
# listed in an ods file and returns the GR site price or out of stock status
##########################
# Changelog V1.2 BETA
# - Retrieves complete list of code, title, category, brand,
#	subcategory, price and description.
# - Uses the updated path and file read and write functions.
# Changelog V1.1
# - Asks for user to input the read file.
# - Opens the file from a predefined folder.
# Changelog V1.0
# - Opens a predefined file and folder.
# - Writes to predefined file and folder.

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import urllib.request
import ezodf  # for the ability to open and write open document format (ODF) files
import xlrd  # for the ability to read excel (XLS) files
import xlwt  # for the ability to write to excel (XLS) files
from datetime import date  # for the ability to get dates
import time  # for the ability to measure time
import os  # for the ability to use os functions
import os.path  # for the ability to get information on folders
import re  # for regex
import sys

# Input search term
answer_term = "no"

while (answer_term == "no") :
 file_name = input("Please enter the file name: ")
 answer_text = "File name is: " + file_name + ". Is that correct? Press enter for yes. "
 answer_term = input(answer_text)

##########################################
# Setting starting date and time values. #
##########################################

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)
print("")

##########################
# Setting correct paths. #
##########################

if os.path.exists(r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY') == True :  # does work folder exist?
 work_path = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY')
 print("Using " + work_path + " for reading files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
 work_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 print("Using home path 1 for reading files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 2 exist?
 work_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 print("Using home path 2 for reading files.")
 print("")
else :
 print("No folders or files found. Where am I?")
 sys.exit()

#########################
# End of paths setting. #
#########################

# Opening files
os.chdir(work_path)
# For reading
if file_name[-4:] != ".ods" :
 read_file = file_name + ".ods"
else :
 read_file = file_name
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# for writing
write_file = (file_name[:file_name.find("-")+1] + " Products_Upload_Analysis.xls")  # path to xslx write file
alt_write_file = (file_name[:file_name.find("-")+1] + " Products_Upload_Analysis_ALT.xls")   # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok=True)  # add 1st sheet in virtual workbook
ws_write.write(0, 0, "CODE")		# write date on A1 cell
ws_write.write(0, 1, "TITLE")		# write date on B1 cell
ws_write.write(0, 2, "OEM")			# write date on C1 cell
ws_write.write(0, 3, "GR-PRICE")	# write date on D1 cell
ws_write.write(0, 4, "GR-CAT")		# write date on E1 cell
ws_write.write(0, 5, "GR-SUBCAT")	# write date on F1 cell
ws_write.write(0, 6, "GR-BRAND")	# write date on G1 cell
ws_write.write(0, 7, "SXETIKA")		# write date on H1 cell
ws_write.write(0, 8, "GR-DESC")		# write date on I1 cell
ws_write.write(0, 9, "GR-AVAIL")	# write date on J1 cell
ws_write.write(0, 10, "CY-PRICE")	# write date on K1 cell
ws_write.write(0, 11, "CY-CAT")		# write date on L1 cell
ws_write.write(0, 12, "CY-SUBCAT")	# write date on M1 cell
ws_write.write(0, 13, "CY-BRAND")	# write date on N1 cell

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
  ac_row += 1
 else :
  break

#########################################
# End of sheet and row/columns setting. #
#########################################

attempt = 0  # how many attempts to re-read the url in case of failure
e = 0
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

for i in range(1, ac_row):
 if str(sheet[i, 2].value) == "None" :
  break
 else:
  print("Rows left: " + str(ac_row-i) + "/" + str(ac_row))
  page_url = "https://www.e-shop.gr/s/" + sheet[i, 2].value.strip()
  req = urllib.request.Request(page_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    uClient = uReq(req)
    page_soup = soup(uClient.read(), "html5lib")
    uClient.close()
    break
   except http.client.IncompleteRead :
    # print("On except :" + str(attempt))
    attempt = attempt + 1
  # gr_code = page_url[page_url.rfind("/")+1:]
  gr_code = page_url[page_url.rfind("/")+1:]
  gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
  gr_categories = page_soup.findAll('td', {'class': 'faint1'})
  gr_cat = gr_categories[1].text[:gr_categories[1].text.find(' •')]
  gr_brand = gr_categories[1].text[gr_categories[1].text.find(' •')+2:gr_categories[1].text.find('στην')].strip()
  if len(gr_categories) > 2 :
   gr_subcat = gr_categories[3].text.strip()
  else :
   gr_subcat = ""
  
  gr_oem = ""
  if page_soup.find('td', {'class': 'product_table_body'}) == None :
   gr_desc = ""
   gr_desc_text = ""
  else :
   gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
   if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
    gr_desc = ""
    gr_desc_text = ""
   else :
    gr_desc = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
   if gr_desc.find('Vendor OEM:') > 0 :
    string, oem, rest = gr_desc.rpartition('Vendor OEM:')
    gr_desc_text = string
    # gr_oem = rest.replace("</li>", "").strip()
    oem = rest
    gr_oem, delim, oem_rest = oem.partition('<')
   if gr_desc.find('Barcode') > 0 :
    string, barcode, rest = gr_desc.rpartition('Barcode')
    gr_desc_text = string.strip()
   if gr_desc.find('2 χρόνια!') > 0 :
    string, warranty, rest = gr_desc.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')
    gr_desc_text = string + "." + rest
   if gr_desc.find("Εφ' όρου ζωής") or gr_desc.find("Lifetime") or gr_desc.find("Εφόρου ζωής") or gr_desc.find("Εφ\x92 όρου ζωής") > 0 :
    if gr_desc.find("Εγγύηση") > 0 :
     string, warranty, rest = gr_desc.rpartition('Εγγύηση')
    elif gr_desc.find("Warranty") > 0 :
     string, warranty, rest = gr_desc.rpartition('Warranty')
    gr_desc_text = string + "Εγγύηση:</b> Εφ' όρου ζωής.</li>"
   if gr_desc_text.find('<!--CRAZY') == 0 :
    crazy, align, rest = gr_desc_text.partition('-->')
    if rest.find('<p ') >= 0 :
     gr_desc_text = crazy + align + '<p align="justify">' + rest[rest.find(">")+1:].strip()
    else :
     gr_desc_text = crazy + align + '<p align="justify">' + rest.strip()

 
   if gr_desc_text.find('!--CRAZY') < 0 :
    if gr_desc_text.find('<p ') >= 0 :
     p, align, rest = gr_desc_text.partition('>')
     gr_desc_text = '<p align="justify">' + rest.strip()
    else :
     gr_desc_text = '<p align="justify">' + gr_desc_text.strip()
 
  if len(gr_price) == 0 :
   gr_price_text = "Εξαντλημένο"
   print("CODE = " + gr_code + ", εξαντλημένο.")
  else : 
   gr_price_text = gr_price[0].text.replace("\xa0€", "").replace(".", ",")
  gr_sxetika = page_soup.findAll('div', {'class': 'also_box'})
  sxetika_list = ""
  for sxetika in gr_sxetika :
   sxetika_per_link = sxetika.a['href']
   sxetika_per = sxetika_per_link[sxetika_per_link.rfind('-')+1:]
   if len(sxetika_list) == 0 :
    sxetika_list = sxetika_per
   else :
    sxetika_list = sxetika_list + "," + sxetika_per

 print("CODE = " + str(gr_code) + ", PRICE = " + gr_price_text)
 print("Category = " + gr_cat + ", SubCat = " + gr_subcat)
 print("Description = " + gr_desc)
 print("Sxetika: " + sxetika_list)
 print("")
 ws_write.write(i, 0, gr_prod_per)
 # ws_write.write(i, 1, gr_prod_title)
 ws_write.write(i, 2, gr_oem)
 ws_write.write(i, 3, gr_price_text)
 ws_write.write(i, 4, gr_cat)
 ws_write.write(i, 5, gr_subcat)
 ws_write.write(i, 6, gr_brand)
 ws_write.write(i, 7, sxetika_list)
 ws_write.write(i, 8, gr_desc_text)
 # ws_write.write(i, 9, gr_a_text)
 # ws_write.write(i, 10, cy_price_text)
 # ws_write.write(i, 11, cy_cat)
 # ws_write.write(i, 12, cy_subcat)
 # ws_write.write(i, 13, cy_brand)
 e += 1

# try to write to the 1st file. If it fails try the 2nd
try :
 wb_write.save(write_file)
except :
 wb_write.save(alt_write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")

print("")
print("File: " + work_path + "\\" + write_file + " saved.")
finished = input("Total products processed: " + str(e) + ". Ready when you are...")


