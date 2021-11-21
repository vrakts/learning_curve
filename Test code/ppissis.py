from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import Request
import re

e = 0

##################
# Alternative 1: #
##################

# page_url = "https://ppissis.com.cy"
# uClient = uReq(page_url, headers = {"User-Agent": "Mozilla/5.0"})
# page_soup = soup(uClient.read(), "html.parser")
# uClient.close()

##################
# Alternative 2: #
##################

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

page1_url = "https://ppissis.com.cy/el/category/mobile-phones"
page2_url = "https://ppissis.com.cy/_nuxt/e1aa0a99bb6eafb846bb.js"

req1 = Request(page1_url, headers = {"User-Agent": "Mozilla/5.0"})
uClient1 = uReq(req1)
page_soup1 = soup(uClient1.read(), "html.parser")
uClient1.close()

req2 = Request(page2_url, headers = {"User-Agent": "Mozilla/5.0"})
uClient2 = uReq(req2)
page_soup2 = soup(uClient2.read(), "html.parser")
uClient2.close()

# For loop:

for i in range(1, len(containers)) :
 e = e + 1
 if e == 10 :
  input("Press a key to continue...") 
  e = 0
 try :
  print("")
  print("i is: " + str(i))
  print(containers[i]['title'])
  print(containers[i]['href'])
 except :
  print("")
  print("Using except...")
  print(containers[i]['href'])
  print("i is: " + str(i))
  pass
