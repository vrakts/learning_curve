from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
page_url = "https://www.e-shop.gr/search?q=spigen"
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()
