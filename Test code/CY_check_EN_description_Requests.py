# from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
# from urllib.request import quote  # enables encoding greek characters in url
# from urllib.parse import unquote  # enables decoding of greek characters
# from urllib.request import Request
from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
import requests
import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
from time import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

cookies = {'language': 'en'}
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

answer = "YES"

### Sample PER codes
# translated
# https://www.e-shop.cy/natec-nmy-0897-merlin-24ghz-1600dpi-wireless-optical-mouse-p-PER.573694
# not translated
# https://www.e-shop.cy/product?id=ANA.DRS0001

while answer == "YES" :
 cy_code = input("Enter PER code: ")
 page_url = "https://www.e-shop.cy/product?id=" + cy_code.strip()
 result = requests.get(page_url, cookies = cookies, headers = headers)
 webpage = result.content
 page_soup = soup(webpage, "html5lib")
 cy_title = page_soup.h1.text
 cy_desc_text = ""
 cy_d_soup = page_soup.find('td', {'class': 'product_table_body'})
 cy_product_table_title = page_soup.find('td', {'class': 'product_table_title'})
 print(cy_title)
 if cy_d_soup == None or cy_d_soup.text.find('Σύνολο ψήφων') > 0 or cy_product_table_title.text.strip() != "Description" :
  cy_desc_text = ""
 else :
  cy_desc_text = cy_d_soup.decode_contents().strip()
  if cy_desc_text.find('Product description is temporary unavailable in English') >= 0 :
   translated = False
   print("Not translated.")
  else :
   translated = True
   print("Translated.")

 print("")
