# read the page and create the soup

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
from urllib.request import Request
import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

###################################
# Change the URL below please ... #
###################################

page_url = "https://www.e-shop.gr/skoypa-ilektriki-telco-sl160-800w-xrysafi-p-HAP.136428"
req = Request(page_url, headers = headers)
attempt = 0
while attempt < 3 :
 try :
  # print("On try :" + str(attempt))
  uClient = uReq(req)
  page_soup = soup(uClient.read(), "html5lib")
  uClient.close()
  gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
  gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
  break
 # except http.client.IncompleteRead :
 except Exception as exc :
  # print("On except :" + str(attempt))
  print("")
  print("Oops, just bumped into the following exception:")
  print(str(exc))
  print("Retrying in 5 seconds.")
  attempt += 1
  time.sleep(5)

