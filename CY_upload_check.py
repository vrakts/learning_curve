# compare auto uploaded results with the file
# comparison is made by taking each product on file
# and comparing to what the CY site has uploaded
# if changes are detected then a NO MATCH field is saved.

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
import urllib.request
import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)
print("")

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

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

answer_term = "no"
os.chdir(work_path)
while answer_term == "no" :
 read_file = input("Please enter file name (enter for default): ")
 if read_file == "" :
  read_file = 'ΠΡΟΪΟΝΤΑ ΓΙΑ ΑΝΟΙΓΜΑ NEW.ods'
  print("Keeping default file: " + read_file)
  break
 elif read_file[-4:] != ".ods" :
  read_file = read_file + ".ods"
  answer_text = "File name is: " + read_file + ". Is that correct? Press enter for yes. "
  answer_term = input(answer_text)
# read_file = 'ΠΡΟΪΟΝΤΑ ΓΙΑ ΑΝΟΙΓΜΑ NEW.ods'
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# for writing
write_file = 'ΠΡΟΪΟΝΤΑ ΓΙΑ ΑΝΟΙΓΜΑ RESULTS.xls'  # path to xslx write file
alt_write_file = 'ΠΡΟΪΟΝΤΑ ΓΙΑ ΑΝΟΙΓΜΑ RESULTS_alt.xls'   # alternate name of xls write file

wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok = True)  # add 1st sheet in virtual workbook
ws_write.write(0, 0, "CY CODE")				# write CY CODE on A1 cell
ws_write.write(0, 1, "RESULT")				# write RESULT on B1 cell
ws_write.write(0, 2, "CY TITLE")			# write CY TITLE on C1 cell
ws_write.write(0, 3, "RESULT")				# write RESULT on D1 cell
ws_write.write(0, 4, "CY PRICE")			# write CY PRICE on E1 cell
ws_write.write(0, 5, "RESULT")	 			# write RESULT on F1 cell
ws_write.write(0, 6, "CY CAT")				# write CY CAT on G1 cell
ws_write.write(0, 7, "RESULT")				# write RESULT on H1 cell
ws_write.write(0, 8, "CY SUBCAT")			# write CY SUBCAT on I1 cell
ws_write.write(0, 9, "RESULT")				# write RESULT on J1 cell
ws_write.write(0, 10, "CY BRAND")			# write CY BRAND on K1 cell
ws_write.write(0, 11, "RESULT")				# write RESULT on L1 cell
ws_write.write(0, 12, "CY SXETIKA")			# write CY SXETIKA on M1 cell
ws_write.write(0, 13, "RESULT")				# write RESULT on N1 cell
ws_write.write(0, 14, "CY DESCRIPTION")		# write CY DESCRIPTION on O1 cell
ws_write.write(0, 15, "FILE DESCRIPTION")	# write FILE DESCRIPTION on P1 cell
ws_write.write(0, 16, "RESULT")				# write RESULT on Q1 cell

answer_term = "no"
while answer_term == "no" :
 start_row = input("Start at? ")
 if start_row == "" :
  start_row = 1
  print("Starting from row: " + str(start_row))
  break
 else :
  answer_text = "Start row is: " + str(start_row) + ". Is that correct? Press enter for yes. "
  answer_term = input(answer_text)

# Counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[2]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1
# Counting rows that contain actual data (ac_row)
for i in range(1, rowcount):
 if str(sheet[i, 0].value) != "None" :
  ac_row += 1
 else :
  break

print("")
print("Reading from sheet 3 and column 1.")
print("")

for i in range(int(start_row), 110):
 if str(sheet[i, 0].value) == "None" :
  break
 else:
  print("Current row: " + str(i) + ". Rows left: " + str(ac_row-i-1) + "/" + str(ac_row-1) + ".")
  page_url = "http://www.eshopcy.com.cy/product?id=" + sheet[i, 2].value.strip()
  req = urllib.request.Request(page_url, headers = headers)
  attempt = 1
  while attempt < 4 :
   try :
    # print("Try number " + str(attempt))
    uClient = uReq(req)
    page_soup = soup(uClient.read(), "html5lib")
    uClient.close()
    break
    # print("Read url OK.")
   except Exception as exc :
    # print("3")
    print("Oops, just bumped into the following exception: " + str(exc))
    attempt += 1
    print("Retrying in 5 seconds.")
    time.sleep(5)
  cy_code = page_soup.find('td', {'style': 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text.strip()
  # print("CY_Code: " + cy_code)
  if len(cy_code) == 0 :
   cy_code = sheet[i, 2].value.strip()
   cy_title = sheet[i, 3].value.strip()
   cy_price = "ΘΕΛΕΙ ΑΝΟΙΓΜΑ"
   # cy_cat = "ΘΕΛΕΙ ΑΝΟΙΓΜΑ"
   # cy_subcat = "ΘΕΛΕΙ ΑΝΟΙΓΜΑ"
   # cy_brand = "ΘΕΛΕΙ ΑΝΟΙΓΜΑ"
   # cy_sxetika = "ΘΕΛΕΙ ΑΝΟΙΓΜΑ"
   # cy_desc = "ΘΕΛΕΙ ΑΝΟΙΓΜΑ"
   ws_write.write(i, 0, cy_code)
   ws_write.write(i, 2, cy_title)
   ws_write.write(i, 4, cy_price)
   print("Doesn't exist. Moving on.")
   continue
  cy_title = page_soup.h1.text
  # print("CY_Title: " + cy_title)
  cy_noavail = page_soup.find('td', {'style': 'text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:12px;'})
  cy_price = page_soup.find("span", {"class" : "web-price-value-new"})
  if cy_noavail != None :
   cy_price = cy_noavail.text.strip()
  else :
   cy_price = page_soup.find("span", {"class" : "web-price-value-new"}).text.replace("\xa0€", "").replace(".", ",").strip()
  # print("CY_Price: " + cy_price)
  cy_categories = page_soup.findAll('td', {'class': 'faint1'})
  if cy_categories[1].text.find(' •') > 0 :
   cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
   cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
   if len(cy_categories) > 2 :
    cy_subcat = cy_categories[3].text.strip()
   else :
    cy_subcat = ""
  else :
   cy_cat = cy_categories[1].text.strip()
   if len(cy_categories) > 2 :
    cy_subcat = cy_categories[3].text.strip()
   else :
    cy_subcat = ""
   cy_brand = "-"
  cy_cat = cy_cat.replace('\xa0', ' ')
  # print("CY_Subcat: " + cy_subcat)
  if len(page_soup.findAll('div', {'class': 'also_box'})) > 0 :
   cy_sxetika = page_soup.findAll('div', {'class': 'also_box'})
   sxetika_list = ""
   for sxetika in cy_sxetika :
    sxetika_per_link = sxetika.a['href']
    sxetika_per = sxetika_per_link[sxetika_per_link.rfind('-')+1:]
    if len(sxetika_list) == 0 :
     sxetika_list = sxetika_per
    else :
     sxetika_list = sxetika_list + "," + sxetika_per
  else :
   sxetika_list = ""
  cy_sxetika = sxetika_list
  # print("CY_Sxetika: " + cy_sxetika)
  cy_desc_soup = page_soup.find('td', {'class': 'product_table_body'})
  cy_product_table_title = page_soup.find('td', {'class': 'product_table_title'})
  if cy_desc_soup == None or cy_desc_soup.text.find('Σύνολο ψήφων') > 0 or cy_product_table_title.text != "Περιγραφή " :
   cy_desc = ""
  else :
   cy_desc = cy_desc_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
  # print("CY_Desc: " + cy_desc)
  # print(cy_code + " - " + cy_title + " - " + cy_price)
  # print(cy_cat + " - " + cy_subcat + " - " + cy_brand)
  # if len(cy_sxetika) > 0 :
   # print(cy_sxetika)
  # if len(cy_desc) > 100 :
   # print(cy_desc[:100] + " ...")
  # elif 1 < len(cy_desc) < 100 :
   # print(cy_desc)
  # print("")
  ws_write.write(i, 0, cy_code)
  ws_write.write(i, 2, cy_title)
  ws_write.write(i, 4, cy_price)
  ws_write.write(i, 6, cy_cat)
  ws_write.write(i, 8, cy_subcat)
  ws_write.write(i, 10, cy_brand)
  ws_write.write(i, 12, cy_sxetika)
  ws_write.write(i, 14, cy_desc)
  ws_write.write(i, 15, str(sheet[i, 12].value))
  
  if cy_code == str(sheet[i, 2].value) :
   check_code = "OK"
  else :
   check_code = str(sheet[i, 2].value)
  ws_write.write(i, 1, check_code)
  
  if cy_title == str(sheet[i, 3].value) :
   check_title = "OK"
  else :
   check_title = str(sheet[i, 3].value)
  ws_write.write(i, 3, check_title)

  cy_price = cy_price.replace(',', '.')
  if cy_price.find('Εξαντλημένο') >= 0 :
   check_price = "ΕΞΑΝΤΛΗΜΕΝΟ"
  else :
   if float(cy_price) == sheet[i, 6].value :
    check_price = "OK"
   else :
    check_price = sheet[i, 6].value
  ws_write.write(i, 5, check_price)
  
  if cy_cat == str(sheet[i, 8].value) :
   check_cat = "OK"
  else :
   check_cat = str(sheet[i, 8].value)
  ws_write.write(i, 7, check_cat)
  
  # if str(sheet[i, 9].value) == None or str(sheet[i, 9].value) == "" :
   # cy_subcat = ""
  if (cy_subcat == "" and str(sheet[i, 9].value) == 'None') or (cy_subcat == str(sheet[i, 9].value)) :
   check_subcat = "OK"
  else :
   check_subcat = str(sheet[i, 9].value)
  ws_write.write(i, 9, check_subcat)
  
  if cy_brand == None or cy_brand == "" :
   cy_brand = "-"
  if cy_brand == str(sheet[i, 10].value) :
   check_brand = "OK"
  else :
   check_brand = str(sheet[i, 10].value)
  ws_write.write(i, 11, check_brand)
  
  if sheet[i, 11].value != None :
   if cy_sxetika == str(sheet[i, 11].value) :
    check_sxetika = "OK"
   else :
    check_sxetika = "NO MATCH"
  else :
   if cy_sxetika == "" :
    check_sxetika = "OK"
   else :
    check_sxetika = "NO MATCH"
  ws_write.write(i, 13, check_sxetika)
  
  if str(sheet[i, 12].value) == None or str(sheet[i, 12].value) == '' or str(sheet[i, 12].value) == 'None' :
   file_desc = ""
  else :
   file_desc = str(sheet[i, 12].value)
  if cy_desc == file_desc :
   check_desc = "OK"
  else :
   if cy_desc == file_desc + "</li>" or cy_desc == file_desc + "</p>" or cy_desc == file_desc + "<li>Εγγύηση: 2 χρόνια.</li>" or cy_desc == file_desc + "</li><li>Εγγύηση: 2 χρόνια.</li>" or cy_desc == file_desc + "</p></li><li>Εγγύηση: 2 χρόνια.</li>" or cy_desc == file_desc + "</p><li>Εγγύηση: 2 χρόνια.</li>" or cy_desc == file_desc + "</li><li>Εγγύηση: 2 χρόνια.</li></u>" or cy_desc == file_desc[:-5] + '<a class="navy_link" href="https://www.eshopcy.com.cy/support#doa">DOA 7 ημερών</a> </li>' or cy_desc == file_desc + '<a class="navy_link" href="https://www.eshopcy.com.cy/support#doa">DOA 7 ημερών</a> </li>' or cy_desc == file_desc[:-5] + '<a class="navy_link" href="https://www.eshopcy.com.cy/support#doa">DOA 7 ημερών</a>  </li>' or cy_desc == file_desc + '<a class="navy_link" href="https://www.eshopcy.com.cy/support#doa">DOA 7 ημερών</a>  </li>' or cy_desc == file_desc[:-5] + ' <a class="navy_link" href="https://www.eshopcy.com.cy/support#doa">DOA 7 ημερών</a> </li>' or cy_desc == file_desc + ' <a class="navy_link" href="https://www.eshopcy.com.cy/support#doa">DOA 7 ημερών</a> </li>' or cy_desc == file_desc[:-5] + ' <a class="navy_link" href="https://www.eshopcy.com.cy/support#doa">DOA 7 ημερών</a>  </li>' or cy_desc == file_desc + ' <a class="navy_link" href="https://www.eshopcy.com.cy/support#doa">DOA 7 ημερών</a>  </li>' or cy_desc == file_desc + '</p></li>' :
    check_desc = "OK"
   else :
    check_desc = "NO MATCH"
  ws_write.write(i, 16, check_desc)
  
  print(cy_code + " - " + check_code + ", " + cy_title + " - " + check_title + ", " + str(cy_price) + " - " + str(check_price))
  print(cy_cat + "/" + str(sheet[i, 8].value) + " - " + check_cat + ", " + cy_subcat + "/" + str(sheet[i, 9].value) + " - " + check_subcat + ", " + cy_brand + " - " + check_brand)
  if len(cy_sxetika) > 0 :
   print(cy_sxetika)
  if len(cy_desc) > 100 :
   print(cy_desc[:100] + " ...")
  elif 1 < len(cy_desc) < 100 :
   print(cy_desc)
  print("")

try :
 wb_write.save(write_file)
 print("")
 print(write_file + " created on " + work_path)
except :
 print("")
 wb_write.save(alt_write_file)
 print(alt_write_file + " created on " + work_path)

