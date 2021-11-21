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

offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # this the write excel file position.
attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

grpage = 'https://www.e-shop.gr/ypologistes-laptops-list?table=PER&category=%D6%CF%D1%C7%D4%CF%C9+%D5%D0%CF%CB%CF%C3%C9%D3%D4%C5%D3'
req = urllib.request.Request(grpage, headers = headers)
gr_uClient = uReq(req)
gr_page_soup = soup(gr_uClient.read(), "html.parser")
gr_uClient.close()
i = 0
req = urllib.request.Request(grpage, headers = headers)
containers = gr_page_soup.findAll('table', {'class': 'web-product-container'})

gr_prod_link = containers[0].find('td', {'class': 'web-product-title'}).a['href']
gr_prod_per = containers[0].find('td', {'class': 'web-product-title'}).font.text.replace('(', '').replace(')', '')
gr_prod_title = containers[0].find('td', {'class': 'web-product-title'}).a.h2.text
##
gr_prod_sort = containers[0].findAll('td', {'class': 'web-product-info'})[1]

gr_prod_specs = gr_prod_sort.text.replace("Χαρακτηριστικά:", "").replace("\xa0", "").replace(" • ", ",").strip()

gr_prod_link = containers[2].find('td', {'class': 'web-product-title'}).a['href']
gr_prod_per = containers[2].find('td', {'class': 'web-product-title'}).font.text.replace('(', '').replace(')', '')
gr_prod_title = containers[2].find('td', {'class': 'web-product-title'}).a.h2.text
##
gr_prod_sort = containers[2].findAll('td', {'class': 'web-product-info'})[1]

if gr_prod_sort.text.find("Αχαρν") > 0:
 print(gr_prod_per + " Βρέθηκε το Αχαρν.")
 gr_prod_specs = gr_prod_sort.text.replace("Χαρακτηριστικά:", "").replace("\xa0", "").replace(" • ", ",").strip()
 gr_prod_specs = gr_prod_specs[0:gr_prod_specs.find("Αχαρν")].strip()
 gr_prod_specs
else :
 print(gr_prod_per + " Δεν βρέθηκε το Αχαρν.¨")
 gr_prod_specs = gr_prod_sort.text.replace("Χαρακτηριστικά:", "").replace("\xa0", "").replace(" • ", ",").strip()
 gr_prod_specs
