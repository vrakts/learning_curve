from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
from urllib.request import Request
import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
from time import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

# cookies = {'language': 'en'}
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

answer = "YES"

while answer == "YES" :
 cy_code = input("Enter PER code: ")
 page_url = "https://www.e-shop.cy/product?id=" + cy_code.strip()
 req = Request(page_url, headers = headers)
 uClient = uReq(req)
 page_soup = soup(uClient.read(), "html5lib")
 uClient.close()

 cy_desc_text = ""
 cy_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 cy_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if cy_d_soup == None or cy_d_soup.text.find('Σύνολο ψήφων') > 0 or cy_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  cy_desc_text = ""
 else :
  cy_desc_text = cy_d_soup.decode_contents().strip()  # decode description content replace wrong html values and any .gr mentions
  # print(gr_desc_text)
 print("GR description: " + cy_desc_text)
 print("")
 
 page_url = "https://www.e-shop.cy/product?id=" + cy_code.strip()
 req = Request(page_url, headers = headers)
 uClient = uReq(req)
 page_soup = soup(uClient.read(), "html5lib")
 uClient.close()

 cy_desc_text = ""
 cy_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 cy_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if cy_d_soup == None or cy_d_soup.text.find('Σύνολο ψήφων') > 0 or cy_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  cy_desc_text = ""
 else :
  cy_desc_text = cy_d_soup.decode_contents().strip()  # decode description content replace wrong html values and any .gr mentions
  # print(gr_desc_text)
 print("EN description: " + cy_desc_text)
 print("")
