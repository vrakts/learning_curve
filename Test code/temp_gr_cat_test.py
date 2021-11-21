from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
# import urllib.request
from urllib.request import Request
import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

def get_gr_details(page_soup) :
 global gr_prod_per, gr_prod_title, gr_price_text, gr_a_text, gr_cat, gr_subcat, gr_brand, sxetika_list, gr_categories
 gr_prod_per = page_soup.find('td', {'style' : 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text.strip()
 gr_prod_title = page_soup.h1.text
 gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(gr_price) == 0 :
  gr_price_text = "Εξαντλημένο"
 else : 
  gr_price_text = gr_price[0].text.replace("\xa0€", "").replace(".", ",")
 if page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"}) == None :
  gr_a_text = "Εξαντλημένο"
 else :
  gr_a = page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
  if gr_a.text.find('Κατόπιν') <= 16 :
   gr_a_text = gr_a.text[gr_a.text.find(":") + 2:]
  else :
   gr_a_text = gr_a.text[gr_a.text.find(":") + 2:gr_a.text.find("\n")].strip()
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
  if len(gr_categories) > 2 :
   gr_subcat = gr_categories[3].text.strip()
  else :
   gr_subcat = ""
  gr_brand = "-"
 if len(page_soup.findAll('div', {'class': 'also_box'})) > 0 :
  gr_sxetika = page_soup.findAll('div', {'class': 'also_box'})
  sxetika_list = ""
  for sxetika in gr_sxetika :
   sxetika_per_link = sxetika.a['href']
   sxetika_per = sxetika_per_link[sxetika_per_link.rfind('-')+1:]
   if len(sxetika_list) == 0 :
    sxetika_list = sxetika_per
   else :
    sxetika_list = sxetika_list + "," + sxetika_per
 else :
  sxetika_list = ""

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

# To Do: Κατηγορία με μάρκα μόνο - works
# page_url = ' https://www.e-shop.gr/esperanza-ep118kg-bluetooth-speaker-piano-black-green-p-TEL.046138'
# To Do: Κατηγορία με υποκατηγορία και μάρκα - works
# page_url = ' https://www.e-shop.gr/ilektrikos-triftis-karykeymaton-esperanza-ekp003k-p-HAP.262314'
# To Do: Κατηγορία με υποκατηγορία χωρίς μάρκα - works
# page_url = 'https://www.e-shop.gr/ziggurat-p-XB1.00278'
# To Do: Κατηγορία μόνο - works
# page_url = ' https://www.e-shop.gr/antallaktikes-sakoyles-aerostegeis-pc-vk-1015eb-28x40cm-50tmx-p-HAP.130298'
# length = 2
page_url = ' https://www.e-shop.gr/sakoyles-nedis-dubg120mie10-gia-ilektrikes-skoypes-miele-p-HAP.002635'

req = Request(page_url, headers = headers)
try :
 uClient = uReq(req)
 page_soup = soup(uClient.read(), "html5lib")
 uClient.close()
except Exception as exc :
 print("")
 print("Oops, just bumped into the following exception:")
 sys.exit(str(exc))

get_gr_details(page_soup)
print("URL: " + page_url)
print("Code: " + gr_prod_per)
print("Category: " + gr_cat)
print("SubCategory: " + gr_subcat)
print("Brand: " + gr_brand)
print("Categories length: " + str(len(gr_categories)))

