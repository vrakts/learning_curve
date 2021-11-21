from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import urllib.request
import xlrd  # for the ability to read excel (XLS) files
import xlwt  # for the ability to write to excel (XLS) files
import ezodf  # for the ability to open and write open document format (ODF) files
from datetime import date  # for the ability to get dates
import time  # for the ability to measure time
import os  # for the ability to use os functions
import os.path  # for the ability to get information on folders
import re  # for regex
import sys

attempt = 0  # how many attempts to re-read the url in case of failure
e = 0
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

work_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
os.chdir(work_path)
file_name = ('2019 OCTOBER 15 - ΠΡΟΪΟΝΤΑ ΓΙΑ ΑΝΟΙΓΜΑ.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(file_name)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# for writing
write_file = (file_name[:file_name.find("-")+1] + " Products_Upload_Analysis_test.xls")  # path to xslx write file
alt_write_file = (file_name[:file_name.find("-")+1] + "Products_Upload_Analysis_test_ALT.xls")   # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet('test')  # add 1st sheet in virtual workbook
ws_write.write(0,0, 'CODE')
ws_write.write(0,1, 'OEM')
ws_write.write(0,2, 'GR_PRICE')
ws_write.write(0,3, 'CATEGORY')
ws_write.write(0,4, 'BRAND')
ws_write.write(0,5, 'SUBCAT')
ws_write.write(0,6, 'DESCRIPTION')

# page_url = "https://www.e-shop.gr/s/TLS.031826"  # no description
# page_url = "https://www.e-shop.gr/s/TLS.051047"  # description
# page_url = "https://www.e-shop.gr/s/ANA.WNG01451"  # oem manual
page_url = "https://www.e-shop.gr/s/PER.901547"  # laptop finds tool description
# page_url = "https://www.e-shop.gr/s/TLS.031455"  # no subcategory -- finds lifetime
# page_url = "https://www.e-shop.gr/s/PER.577447"  # lifetime
# page_url = "https://www.e-shop.gr/s/TLS.011551"  # br/ br/
# page_url = "https://www.e-shop.gr/s/TLS.011588"  # br/ br/
# page_url = "https://www.e-shop.gr/s/PER.574240"  # align problem
# page_url = "https://www.e-shop.gr/s/TLS.011215"  # crazy no align
# page_url = "https://www.e-shop.gr/s/TLS.011227"  # crazy with correct align



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
# gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
# gr_d_soup = page_soup.find('div', {'class' : 'mobile_product_desc'}).contents[1]
# if page_soup.find('div', {'class' : 'mobile_product_desc'}) == None:
if page_soup.find('td', {'class': 'product_table_body'}) == None :
 gr_desc = ""
 gr_desc_text = ""
else :
 # gr_d_soup = page_soup.find('div', {'class' : 'mobile_product_desc'}).contents[1]
 # gr_d_soup = page_soup.find('div', {'class' : 'mobile_product_desc'})
 gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
 # gr_desc = gr_desc.text.replace('• ', '</li><li>')
 # gr_desc = '<p align="justify">' + gr_d_soup.text.replace('• ', '</li><li><b>').replace('</li>', '</p>', 1).replace('<li>', '<li><b>', 1).replace('</li>', '</li><b>').replace(':', ':</b>')
 # gr_desc = '<p align="justify">' + gr_d_soup.text.replace('• ', '</li><li><b>').replace('</li>', '</p>', 1).replace(':', ':</b>')
 if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
  gr_desc = ""
  gr_desc_text = ""
 else :
  gr_desc = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
  gr_desc_text = gr_desc
  if gr_desc.find('Vendor OEM:') > 0 :
   string, oem, rest = gr_desc.rpartition('Vendor OEM:')
   gr_desc_text = string.strip()
   gr_oem = rest.replace("</li>", "").strip()
  else :
   gr_desc_text = gr_desc
  if gr_desc.find('Barcode') > 0 :
   string, barcode, rest = gr_desc.rpartition('Barcode')
   # gr_desc_text = string.replace("br/", "br")
   gr_desc_text = string.strip()
  else :
   gr_desc_text = gr_desc
  if gr_desc.find('2 χρόνια!') > 0 :
   # string, warranty, rest = gr_desc.rpartition('2 χρόνια!')
   string, warranty, rest = gr_desc.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')
   gr_desc_text = string + "." + rest
  else :
   gr_desc_text = gr_desc
  if gr_desc.find("Εφ' όρου ζωής") or gr_desc.find("Lifetime") or gr_desc.find("Εφόρου ζωής") or gr_desc.find("Εφ\x92 όρου ζωής") > 0 :
   if gr_desc.find("Εγγύηση") > 0 :
    string, warranty, rest = gr_desc.rpartition('Εγγύηση')
   elif gr_desc.find("Warranty") > 0 :
    string, warranty, rest = gr_desc.rpartition('Warranty')
   gr_desc_text = string + "Εγγύηση:</b> Εφ\' όρου ζωής.</li>"
  else :
   gr_desc_text = gr_desc
  # gr_desc_text = gr_desc_text.replace("<br/>", "<br>").replace(".gr", "")
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
 print("CODE = " + str(gr_code) + ", εξαντλημένο.")
else : 
 gr_price_text = gr_price[0].text.replace("\xa0€","").replace(".", ",")

print("CODE = " + str(gr_code) + ", PRICE = " + gr_price_text)
print("Brand = " + gr_brand + ", Category = " + gr_cat + ", SubCat = " + gr_subcat)
# print("Description = " + gr_desc_text)
ws_write.write(1,0, gr_code)
ws_write.write(1,1, gr_oem)
ws_write.write(1,2, gr_price_text)
ws_write.write(1,3, gr_cat)
ws_write.write(1,4, gr_brand)
ws_write.write(1,5, gr_subcat)
ws_write.write(1,6, gr_desc_text)
e += 1

wb_write.save(write_file)

print("")
print("File: " + work_path + "\\" + write_file + " saved.")
finished = input("Total products processed: " + str(e) + ". Ready when you are...")


