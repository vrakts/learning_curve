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

def description(gr_desc_text) :
 global string, warranty, rest, gr_desc_result
 if gr_desc_text.find('Vendor OEM:') > 0 :
  if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
   string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
  else :
   string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
  gr_desc_text = string.strip()  # keep only what is before the OEM
  oem = rest.strip()  # keep only what is after the OEM
  gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
  gr_oem = gr_oem.strip()
 # if gr_desc_text.find('<br><br>Barcode') > 0 :  # if barcode exists in GR
 if gr_desc_text.find('Barcode:') > 0 :  # if both barcode and OEM exists
  if gr_desc_text.find('<br><br>Barcode:') > 0 :
   string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode')  # seperate the text
  else :
   string, barcode, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
  # gr_desc_text = string.strip() + rest.strip() # keep only what is before the barcode
  gr_desc_text = string.strip() # keep only what is before the barcode
  # while gr_desc_text.strip()[-4:] == "<br>" :  # if the 4 ending text characters are <br>
   # string, br, rest = gr_desc_text.rpartition('<br>')  # seperate the text
   # gr_desc_text = string.strip()  # keep ony what is before <br>
  # gr_oem = rest.replace("</li>", "").strip()
 if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
  crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
  gr_desc_text = rest.strip()  # keep only the rest of the text
 # if gr_desc_text.find('<p ') >= 0 :
  # p, align, rest = gr_desc_text.partition('>')
  # gr_desc_text = '<p align="justify">' + rest.strip()pyth
 if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
  p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
  gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
 else :
  gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
 if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
  if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
   string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
  elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
   string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
  if gr_prod_title.find('ASUS') > 0 :
   warranty_text = ' <a href="page.phtml?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b> </li>'
  else :
   warranty_text = ' .</b> </li>'
  gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
 elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
  if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
   string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
  elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
   string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
  gr_desc_text = string + "<b>Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
 elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
  string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
  gr_desc_text = string + rest.strip()  # and keep the before and after text
 elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
  string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
  gr_desc_text = string + rest.strip()  # and keep the before and after text
 else :
  print("No Warranty found.")
 if gr_desc_text == '<p align="justify">' :
  gr_desc_text = ""
 if gr_desc_text.find('1 χρόνο') > 0 or gr_desc_text.find('1 Χρόνο') > 0 or gr_desc_text.find('1 Χρόνος') > 0 or gr_desc_text.find('1 χρόνος') > 0 or gr_desc_text.find('1 Έτος') > 0 or gr_desc_text.find('1 έτος') > 0 :   # if the years are misspelled it is not autocorrected in the CY site. Not looking for "." at the end.
  gr_desc_text = gr_desc_text.replace('1 Χρόνος', '2 χρόνια')
  gr_desc_text = gr_desc_text.replace('1 χρόνος', '2 χρόνια')
  gr_desc_text = gr_desc_text.replace('1 Χρόνο', '2 χρόνια')
  gr_desc_text = gr_desc_text.replace('1 χρόνο', '2 χρόνια')
  gr_desc_text = gr_desc_text.replace('1 Έτος', '2 χρόνια')
  gr_desc_text = gr_desc_text.replace('1 έτος', '2 χρόνια')
 gr_desc_result = gr_desc_text

attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

page_url = "https://www.e-shop.gr/laptop-lenovo-yoga-530-14ikb-81ek01a6mh-14-fhd-touch-intel-core-i7-8550u-8gb-256gb-ssd-windows-10-p-PER.917050"
req = urllib.request.Request(page_url, headers = headers)
attempt = 0
while attempt < 3 :
 try :
  # print("On try :" + str(attempt))
  uClient = uReq(req)
  page_soup = soup(uClient.read(), "html5lib")
  uClient.close()
  break
 # except http.client.IncompleteRead :
 except Exception as exc :
  # print("On except :" + str(attempt))
  print("Oops, just bumped into the following exception: " + str(exc))
  print("Retrying in 5 seconds.")
  attempt += 1
  time.sleep(5)

gr_prod_per = page_url[page_url.rfind("/")+1:]
gr_prod_title = page_soup.h1.text
gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
gr_categories = page_soup.findAll('td', {'class': 'faint1'})
if gr_categories[1].text.find(' •') > 0 :
 gr_cat = gr_categories[1].text[:gr_categories[1].text.find(' •')]
 gr_brand = gr_categories[1].text[gr_categories[1].text.find(' •')+2:gr_categories[1].text.find('στην')].strip()
 if len(gr_categories) > 2 :
  gr_subcat = gr_categories[3].text.strip()
 else :
  gr_subcat = ""
else :
 gr_cat = gr_categories[1].text.strip()
 gr_subcat = gr_categories[3].text.strip()
 gr_brand = ""

gr_oem = ""
gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
 gr_desc_text = ""
else :
 gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html calues and any .gr mentions

description(gr_desc_text)

# print(string)
# print(warranty)
# print(rest)
print(gr_desc_result)
