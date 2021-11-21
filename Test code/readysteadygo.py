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

req = Request(page_url, headers = {"User-Agent": "Mozilla/5.0"})
uClient = uReq(req)
page_soup = soup(uClient.read(), "html.parser")
