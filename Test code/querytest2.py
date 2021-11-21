from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote
import xlwt  # for the ability to write to excel files
from datetime import date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # represents the row inside the excel file.
oneprod = 0  # is it a single item (1) or multiple items (0)

grpage = 'https://www.e-shop.gr/gadgets-paixnidia-mobile-gadgets-list?table=PER&category=MOBILE+GADGETS'  # search category page with next
print(grpage)

gr_uClient = uReq(grpage)
gr_page_soup = soup(gr_uClient.read(), "html.parser")
gr_uClient.close()


if gr_page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories and next buttons
 print("Treating this as a category query page.")
 if gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'}) :  # if the page holds containers then 
  next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
  total_next_pages = next_pages_category[3].text  # it seems that [3] always keeps the last page
  print("Total query pages: " + str(total_next_pages))
  gr_cat_page, delim, categories = str(grpage).partition("?")
  gr_cat_offset_url = gr_cat_page + delim + "offset=" + str(offset) + "&" + categories
  last_offset = (int(total_next_pages) - 1) * 10
  gr_last_cat = gr_cat_page + delim + "offset=" + str(last_offset) + "&" + categories
  gr_last_uClient = uReq(gr_last_cat)
  gr_last_page_soup = soup(gr_last_uClient.read(), "html.parser")
  gr_last_uClient.close()
  last_prod = gr_last_page_soup.findAll('table', {'class': 'web-product-container'})
  prod_count = len(last_prod) + last_offset
  print("Found " + str(prod_count) + " products.")
  for q in range(0, int(total_next_pages)) :
   gr_uClient = uReq(grpage)
   gr_page_soup = soup(gr_uClient.read(), "html.parser")
   gr_uClient.close()
   containers = gr_page_soup.findAll('table', {'class': 'web-product-container'})
   for container in containers :
    gr_prod_per = container.font.text.replace("(", "").replace(")", "")
    # print(gr_prod_per)
    gr_prod_title = container.h2.text
    # print(gr_prod_title)
    if container.find('font', {'style': 'color:#FF0000'}) :
     gr_price_text = container.find('font', {'style': 'color:#FF0000'}).text.replace(".", ",")
    else :
     gr_price_text = container.find('td', {'class': 'web-product-price'}).text.strip().replace('\xa0€', '').replace('.', ',')
    # print(gr_price_text)
    gr_a_text = container.find('div', {'style': 'display:block;width:auto;padding:0 5px 7px 0;'}).text
    # print(gr_a_text)
    # ws_write.write(e, 4, cy_price_text
    cy_page = "http://www.eshopcy.com.cy/product?id=" + gr_prod_per
    cy_uClient = uReq(cy_page)
    cy_page_soup = soup(cy_uClient.read(), "html.parser")
    cy_uClient.close()
    cy_prod_title = cy_page_soup.h1.text
    cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
    if len(cy_prod_title) == 0 :
     cy_price_text = "Θέλει άνοιγμα"
    else :
     if len(cy_price) == 0 :
      cy_price_text = "Εξαντλημένο"
     else :
      cy_price_text = cy_price[0].text.replace("\xa0€", "").replace(".", ",")
    print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
