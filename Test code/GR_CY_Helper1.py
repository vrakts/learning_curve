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

grpage = 'https://www.e-shop.gr/search?q=iphone+11+pro+book'
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

if gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'}) :  # search result page with next buttons
 print("Treating this as a search result page.")
 print("")
 # gr last page preparations
 next_pages_search = gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons assuming this is a term based query page
 next_pages_a = next_pages_search[0].findAll('a')  # keep all <a> only as they keep the next page numbers
 if len(next_pages_a) == 0 :
  total_next_pages = 1
  print("Only 1 page in the query results")
 else:
  total_next_pages = int(next_pages_a[len(next_pages_a)-2].text)  # this holds the exact next pages that need to be offset
  print("Total query pages: " + str(total_next_pages))
 gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})
 page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
 gr_offset_url = grpage + page_offset + str(offset)  # this is the complete query url with offset. eg. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0
 # calculating total products count
 # first we need to calculate the last offset page
 last_offset = (total_next_pages - 1) * 50
 # then calculate the new url
 last_offset_url = grpage + page_offset + str(last_offset)
 # now we need to reload the last offset soup with all available products
 req = urllib.request.Request(last_offset_url, headers = headers)
 attempt = 0
 while attempt < 3 :
  try :
   # print("On try :" + str(attempt))
   last_uClient = uReq(req)
   last_page_soup = soup(last_uClient.read(), "html.parser")
   last_uClient.close()
   break
  except http.client.IncompleteRead :
   # print("On except :" + str(attempt))
   attempt += 1
 last_prod_info = last_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 # last step, add the gr_prod_info of the last offset page to the offset value
 total_prod = last_offset + len(last_prod_info)
 tp = total_prod
 print("Found " + str(total_prod) + " products. Starting process now.")
 print("")
 for q in range(0, total_next_pages) :
  for (i, p) in zip(gr_prod_info, gr_prod_price) :
   tp = tp - 1
   print("Processing item: " + str(total_prod - tp) + "/" + str(total_prod) + ". Remaining: " + str(total_prod - (total_prod - tp)))
   gr_prod_link = i.a['href']
   gr_prod_title = i.a.text
   gr_prod_per = i.span.text.replace("(", "").replace(")", "")
   gr_price_text = p.text  # save text of the price result in price_text
   if gr_price_text.count(' ') > 1 :  # if price " " is more than 1 then it has a discount ...
    gr_price_text = gr_price_text[gr_price_text.find(' ')+1:].replace(" €", "").replace(".", ",")  # ... so print the second price without the euro sign
   else :
    gr_price_text = gr_price_text.replace(" €","").replace(".", ",")  #... otherwise print the whole (single) price without the euro sign.
   gr_a_page = "https://www.e-shop.gr/product?id=" + gr_prod_per
   # gr_a_page = "https://www.e-shop.gr/tv-arielli-led-32dn10t2-32-led-hd-ready-p-PER.152681"
   req = urllib.request.Request(gr_a_page, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     gr_a_uClient = uReq(req)
     gr_a_pagesoup = soup(gr_a_uClient.read(), "html.parser")
     gr_a_uClient.close()
     break
    except http.client.IncompleteRead :
     # print("On except :" + str(attempt))
     attempt += 1
   gr_a = gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
   # gr_a_text = gr_a.text[gr_a.text.find(":")+2:]
   #############################################################
   if gr_a.text.find('Κατόπιν') <= 16 :
    gr_a_text = gr_a.text
   else :
    gr_a_text = gr_a.text[gr_a.text.find(":")+2:gr_a.text.find("\r")].strip()
   #############################################################
   gr_categories = gr_a_pagesoup.findAll('td', {'class' : 'faint1'})
   gr_cat = gr_categories[1].text[:gr_categories[1].text.find(' •')]
   gr_brand = gr_categories[1].text[gr_categories[1].text.find(' •')+2:gr_categories[1].text.find('στην')].strip()
   #############################################################
   if len(gr_categories) > 2 :
    gr_subcat = gr_categories[3].text.strip()
   else :
    gr_subcat = ""
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
   #############################################################
   cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
   cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
   cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
   if len(cy_categories) > 2 :
    cy_subcat = cy_categories[3].text.strip()
   else :
    cy_subcat = ""
   #############################################################
   # if cy_price_text != ("Εξαντλημένο", "Θέλει άνοιγμα") :
    # difference = (int(cy_price_text(",", ".")) - int(gr_price_text.replace(",", ".")) / int(gr_price_text.replace(",", ".")) * 100)
    # print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + " (" + str(difference) + ").")
   # else :
   print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
   print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
   # print("Products left: " + str(total_prod - tp) + "/" + str(total_prod))
   # tp = tp - 1
  offset = offset + 50
  offset_url = grpage + page_offset + str(offset)
  req = urllib.request.Request(offset_url, headers = headers)
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
  gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
  gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})