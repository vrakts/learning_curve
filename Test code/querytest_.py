# fixed only query page
# need to lool into category and the rest. Category should work for multiple and single page.

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
# dirty = 0  # did something change? then dirty will change to 1
e = 1  # this the write excel file position.
attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

# answer_term = "no"

# while (answer_term == "no") :
 # query_term = input("Please enter your query term: ")
 # # # print(query_term.count(' '))
 # # if query_term.find('http') :  # if query_term is a url...
  # # query_url = quote(text.encode('utf-8'))
 # if query_term.count(' ') > 0 :  # if query_term has at least one " "...
  # # print("in if loop. Has at least 1 space")
  # query_term = query_term.replace(" ", "+")
  # # print(query_term)
 # answer_text = "Your query term is: " + query_term + ". Is that correct? Press enter for yes. "
 # answer_term = input(answer_text)
 # url_term = quote(query_term.encode('iso-8859-7')).replace('%2B', '+')

# if query_term.find("://") > 0 :
 # grpage = query_term
# else :
 # grpage = "https://www.e-shop.gr/search?q=" + url_term  # this is the base query url for GR


# grpage = 'https://www.e-shop.gr/search?q=spigen'  # search result page
# grpage = 'https://www.e-shop.gr/gadgets-paixnidia-mobile-gadgets-list?table=PER&category=MOBILE+GADGETS'  # search category page with next
# grpage = 'https://www.e-shop.gr/gadgets-paixnidia-mobile-gadgets-spigen-list?table=PER&category=MOBILE+GADGETS&filter-26640=1'  # search category page no next
# grpage = 'https://www.e-shop.gr/gadgets-paixnidia-mobile-gadgets-tp-link-list?table=PER&category=MOBILE+GADGETS&filter-16255=1'   # search category page one product
# grpage = 'https://www.e-shop.gr/search?q=AMIKO+SPIEL'  # single product page
# grpage = 'https://www.e-shop.gr/search?q=customize'  # empty search page
print(grpage)

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
  attempt = attempt + 1

# gr last page preparations
next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
next_pages_single = gr_page_soup.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})  # find all next page buttons assuming this is a category based query page

if gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'}) :  # search result page with next buttons
 print("Treating this a search result page.")
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
   attempt = attempt + 1
 last_prod_info = last_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 # last step, add the gr_prod_info of the last offset page to the offset value
 total_prod = last_offset + len(last_prod_info)
 tp = total_prod
 print("")
 print("Found " + str(total_prod) + " products. Starting process now.")
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
     attempt = attempt + 1
   gr_a = gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
   # gr_a_text = gr_a.text[gr_a.text.find(":")+2:]
   gr_a_text = gr_a.text[gr_a.text.find(":")+2:gr_a.text.find("\r")]
   if gr_a_text.find("Κατόπιν") :
    gr_a_text = gr_a_text + "ς"

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
     attempt = attempt + 1
   cy_prod_title = cy_page_soup.h1.text
   cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
   if len(cy_prod_title) == 0 :
    cy_price_text = "Θέλει άνοιγμα"
   else :
    if len(cy_price) == 0 :
     cy_price_text = "Εξαντλημένο"
    else :
     cy_price_text = cy_price[0].text.replace("\xa0€", "").replace(".", ",")
   # if cy_price_text != ("Εξαντλημένο", "Θέλει άνοιγμα") :
    # difference = (int(cy_price_text(",", ".")) - int(gr_price_text.replace(",", ".")) / int(gr_price_text.replace(",", ".")) * 100)
    # print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + " (" + str(difference) + ").")
   # else :
   print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
   # print("Products left: " + str(total_prod - tp) + "/" + str(total_prod))
   # ws_write.write(e, 0, gr_prod_per)
   # ws_write.write(e, 1, gr_prod_title)
   # ws_write.write(e, 2, gr_price_text)
   # ws_write.write(e, 3, gr_a_text)
   # ws_write.write(e, 4, cy_price_text)
   e = e + 1
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
    attempt = attempt + 1
  gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
  gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})
elif gr_page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories
 print("Treating this as a category query page.")
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
    attempt = attempt + 1
  last_prod = gr_last_page_soup.findAll('table', {'class': 'web-product-container'})
  prod_count = len(last_prod) + last_offset
  print("Found " + str(prod_count) + " products.")
  for q in range(0, int(total_next_pages)) :

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
     attempt = attempt + 1
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
      attempt = attempt + 1
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
 else :
  total_next_pages = 0  # single search result page with categories
  containers = gr_page_soup.findAll('table', {'class' : 'web-product-container'})
  print("Only 1 page and " + str(len(containers)) + " products found.")
  print("")
  # len(containers)
  for container in containers :
   gr_prod_per = container.font.text.replace("(", "").replace(")", "")
   # print(gr_prod_per)
   gr_prod_title = container.h2.text
   # print(gr_prod_title)
   gr_price_text = container.find('font', {'style': 'color:#FF0000'}).text.replace(".", ",")
   # print(gr_price_text)
   gr_a_text = container.find('div', {'style': 'display:block;width:auto;padding:0 5px 7px 0;'}).text
   # print(gr_a_text)
   # ws_write.write(e, 4, cy_price_text
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
     attempt = attempt + 1
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
   # ws_write.write(e, 0, gr_prod_per)
   # ws_write.write(e, 1, gr_prod_title)
   # ws_write.write(e, 2, gr_price_text)
   # ws_write.write(e, 3, gr_a_text)
   # ws_write.write(e, 4, cy_price_text)
   e = e + 1
elif gr_page_soup.findAll("h1", {"style": "color:#4f4f4f;font-family:Tahoma;font-size:18px;font-weight:bold;padding:0 0 0 0;"}) :
 print("Only 1 pr`oduct found. Treating results as a single product page.")
 print("")
 gr_prod_per = gr_page_soup.find('td', {'style' : 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text
 gr_prod_link = 'https://www.e-shop.gr/product?id=' + gr_prod_per
 gr_prod_title = gr_page_soup.h1.text
 gr_price_text = gr_page_soup.find('span', {'class' : 'web-price-value-new'}).text.replace('\xa0€', '').replace('.', ',')
 gr_a = gr_page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
 gr_a_text = gr_a.text[gr_a.text.find(":")+2:gr_a.text.find("\r")]
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
   attempt = attempt + 1
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
else :
 print("")
 print("Search result is probably empty. Try again with different terms.")

