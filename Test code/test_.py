from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote
import urllib.request
import xlwt  # for the ability to write to excel files
from datetime import date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

page_url = 'http://gvrakas.com/whoami/'
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

attempt = 0  # how many attempts to re-read the url in case of failure

req = urllib.request.Request(page_url, headers = headers)
attempt = 0
while attempt < 4 :
 attempt = attempt + 1
 try :
  # print("On try :" + str(attempt))
  gr_uClient = uReq(req)
  gr_page_soup = soup(gr_uClient.read(), "html.parser")
  gr_uClient.close()
  break
 except Exception as ex :
  if attempt == 3 :
   print("Tried 3 times. Quitting now.")
   sys.exit()
  else :
   print("Exception caught :" + str(ex) + ". Retrying in 5 seconds.")
   time.sleep(5)

gr_page_soup