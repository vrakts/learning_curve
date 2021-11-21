from bs4 import BeautifulSoup as soup  # import BeautifulSoup function of bs4 library
from urllib.request import urlopen as uReq  # import urlopn function from urllib library and use it as a Web client
import os  # import os for Operating System functions
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
import time  # for the ability to measure time

path = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Ανταγωνισμός Λευκωσίας SUM.ods")

q_url1 = "http://www.eshopcy.com.cy/product?id=TEL.002161" # no margin
q_url2 = "http://www.eshopcy.com.cy/product?id=PER.155828" # has margin

uClient = uReq(q_url1)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()
q_margin = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
q_margin

if len(q_margin) == 0 :
 print( "For " + q_url1 + " margin doesn't exist")
else :
 print( "For " + q_url1 + " margin exists")


 
uClient = uReq(q_url2)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()
q_margin = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
q_margin

if len(q_margin) == 0 :
 print( "For " + q_url2 + " margin doesn't exist")
else :
 print( "For " + q_url2 + " margin exists")
 
