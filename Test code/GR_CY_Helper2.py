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
e = 1  # represents the row inside the excel file.
attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
# oneprod = 0  # is it a single item (1) or multiple items (0)

grpage = 'https://www.e-shop.gr/ypologistes-laptops-16gb-list?table=PER&category=%D6%CF%D1%C7%D4%CF%C9+%D5%D0%CF%CB%CF%C3%C9%D3%D4%C5%D3&filter-6644=1'
page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
gr_offset_url = grpage + page_offset + str(offset)  # this is the complete query url with offset. eg. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0

# Setting starting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy

################################
# Setting correct write paths. #
################################

print("")

req = urllib.request.Request(grpage, headers = headers)
attempt = 0
while attempt < 3 :
 try :
  # print("On try :" + str(attempt))
  gr_uClient = uReq(req)
  gr_page_soup = soup(gr_uClient.read(), "html.parser")
  gr_uClient.close()
  break
 except http.client.IncompleteRead :
  # print("On except :" + str(attempt))
  attempt += 1

# gr last page preparations
next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
next_pages_single = gr_page_soup.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})  # find all next page buttons assuming this is a category based query page

if gr_page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories
 print("Treating this as a category query page.")
 print("")
 if gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'}) :  # if the page has next buttons 
  next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
  total_next_pages = next_pages_category[len(next_pages_category)-1].text  # total next pages is in the last total_next_pages (-1 for indexing)
  print("Total query pages: " + str(total_next_pages))
  gr_cat_page, delim, categories = str(grpage).partition("?")
  gr_cat_offset_url = gr_cat_page + delim + "offset=" + str(offset) + "&" + categories
  last_offset = (int(total_next_pages) - 1) * 10
  gr_last_cat = gr_cat_page + delim + "offset=" + str(last_offset) + "&" + categories
  req = urllib.request.Request(gr_last_cat, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    gr_last_uClient = uReq(req)
    gr_last_page_soup = soup(gr_last_uClient.read(), "html.parser")
    gr_last_uClient.close()
    break
   except http.client.IncompleteRead :
    # print("On except :" + str(attempt))
    attempt += 1
  last_prod = gr_last_page_soup.findAll('table', {'class': 'web-product-container'})
  total_prod = len(last_prod) + last_offset
  tp = total_prod
  print("Found " + str(total_prod) + " products. Starting process now.")
  print("")
  for q in range(0, int(total_next_pages)) :
   req = urllib.request.Request(gr_cat_offset_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     gr_uClient = uReq(req)
     gr_page_soup = soup(gr_uClient.read(), "html.parser")
     gr_uClient.close()
     break
    except http.client.IncompleteRead :
     # print("On except :" + str(attempt))
     attempt += 1
   containers = gr_page_soup.findAll('table', {'class': 'web-product-container'})
   for container in containers :
    tp = tp - 1
    print("Processing item: " + str(total_prod - tp) + "/" + str(total_prod) + ". Remaining: " + str(total_prod - (total_prod - tp)))
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
    gr_categories = container.find('td', {'class' : 'web-product-info'}).text
    if gr_categories.find('Κατηγορία:') >= 0 :
     if gr_categories.find('Υποκατηγορία:') >= 0 :
      gr_cat = gr_categories[gr_categories.find("Κατηγορία:\xa0 ")+12:gr_categories.find("Υποκατηγορία:\xa0 ")-4]
      gr_subcat = gr_categories[gr_categories.find("Υποκατηγορία:\xa0 ")+15:gr_categories.find("Κατασκευαστής")-4]
      gr_brand = gr_categories[gr_categories.find("Κατασκευαστής:")+16:]
     else :
      gr_cat = gr_categories[gr_categories.find("Κατηγορία:\xa0 ")+12:gr_categories.find("Κατασκευαστής")-4]
      gr_subcat = ""
      gr_brand = gr_categories[gr_categories.find("Κατασκευαστής:")+16:]
    else :
     print("No categories found. Will leave the fields empty but will error out when uploading product.")
     gr_cat = ""
     gr_subcat = ""
     gr_brand = ""
    cy_page = "http://www.eshopcy.com.cy/product?id=" + gr_prod_per
    req = urllib.request.Request(cy_page, headers = headers)
    attempt = 0
    while attempt < 3 :
     try :
      # print("On try :" + str(attempt))
      cy_uClient = uReq(req)
      cy_page_soup = soup(cy_uClient.read(), "html.parser")
      cy_uClient.close()
      break
     except http.client.IncompleteRead :
      # print("On except :" + str(attempt))
      attempt += 1
    cy_prod_title = cy_page_soup.h1.text
    cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
    if len(cy_prod_title) == 0 :
     cy_price_text = "Θέλει άνοιγμα"
    else :
     if len(cy_price) == 0 :
      cy_price_text = "Εξαντλημένο"
     else :
      cy_price_text = cy_price[0].text.replace("\xa0€", "").replace(".", ",")
    cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
    cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
    cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
    if len(cy_categories) > 2 :
     cy_subcat = cy_categories[3].text.strip()
    else :
     cy_subcat = ""
    print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
    print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
    print("")
   offset += 10
   gr_cat_offset_url = gr_cat_page + delim + "offset=" + str(offset) + "&" + categories


