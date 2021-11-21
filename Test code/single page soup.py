from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote
import xlwt  # for the ability to write to excel files
from datetime import date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

gr_uClient = uReq('https://www.e-shop.gr/search?q=bks+cougars&t=&c=&offset=0') 
gr_page_soup = soup(gr_uClient.read(), "html.parser")
gr_uClient.close()

gr_a = gr_page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
gr_a_text = gr_a.text[gr_a.text.find(":")+2:gr_a.text.find("\r")]
