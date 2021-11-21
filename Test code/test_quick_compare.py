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

offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # represents the row inside the excel file.
attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
answer_term = "no"

grpage = 'https://www.e-shop.gr/search_main.phtml?table=PER'

req = Request(grpage, headers = headers)
attempt = 0
while attempt < 3 :
 try :
  # print("On try :" + str(attempt))
  gr_uClient = uReq(req)
  gr_page_soup = soup(gr_uClient.read(), "html5lib")
  gr_uClient.close()
  # gr last page preparations
  next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
  next_pages_single = gr_page_soup.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})  # find all next page buttons assuming this is a category based single query page
  break
 except Exception as exc :
  # print("On except :" + str(attempt))
  print("Oops, just bumped into the following exception: " + str(exc))
  print("Retrying in 5 seconds.")
  attempt += 1
  time.sleep(5)


if gr_page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories
# https://www.e-shop.gr/ilektrikes-syskeues-ilektrikes-skoupes-1001w-eos-1200w-list?table=HAP&category=%C7%CB%C5%CA%D4%D1%C9%CA%C5%D3+%D3%CA%CF%D5%D0%C5%D3&filter-12563=1
 print("Treating this as a category query page.")
 print("")
 if gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'}) :  # if the page has next buttons 
  next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
  total_next_pages = next_pages_category[len(next_pages_category)-1].text  # total next pages is in the last total_next_pages (-1 for indexing)
  print("Total query pages: " + str(total_next_pages))
  gr_cat_page, query_mark, categories = str(grpage).partition("?")
  gr_cat_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
  last_offset = (int(total_next_pages) - 1) * 10
  gr_last_cat = gr_cat_page + query_mark + "offset=" + str(last_offset) + "&" + categories
  req = Request(gr_last_cat, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    gr_last_uClient = uReq(req)
    gr_last_page_soup = soup(gr_last_uClient.read(), "html5lib")
    gr_last_uClient.close()
    last_prod = gr_last_page_soup.findAll('table', {'class': 'web-product-container'})
    total_prod = len(last_prod) + last_offset
    tp = total_prod
    break
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("Oops, just bumped into the following exception: " + str(exc))
    print("Retrying in 5 seconds.")
    attempt += 1
    time.sleep(5)
  print("Found " + str(total_prod) + " products. Starting process now.")
  print("")
  for q in range(0, int(total_next_pages)) :
   # print("Current page: " + gr_cat_offset_url + " #" + str(q))
   req = Request(gr_cat_offset_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     gr_uClient = uReq(req)
     gr_page_soup = soup(gr_uClient.read(), "html5lib")
     gr_uClient.close()
     containers = gr_page_soup.findAll('table', {'class': 'web-product-container'})
     break
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("Oops, just bumped into the following exception: " + str(exc))
     print("Retrying in 5 seconds.")
     attempt += 1
     time.sleep(5)
   for container in containers :
    tp = tp - 1
    print("Processing item: " + str(total_prod - tp) + "/" + str(total_prod) + ". Remaining: " + str(total_prod - (total_prod - tp)))
    gr_prod_per = container.font.text.replace("(", "").replace(")", "")
    # print(gr_prod_per)
    gr_prod_title = container.h2.text
    gr_prod_price = container.find("td", {"class": "web-product-price"}).text.strip().replace("\xa0€", "")
    print("Code: " + gr_prod_per + ", Title: " + gr_prod_title + ", Price: " + gr_prod_price)
   offset += 10  # ADD 10 TO THE URL OFFSET VALUE
   gr_cat_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
  
  