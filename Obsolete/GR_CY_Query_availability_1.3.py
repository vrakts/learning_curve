# Current Version Beta 1.3
##########################
# Changelog V1.3
# - Can determine if the result is a search result page
#	a category search page, a single item result or 
#	an empty search result.
# - Updated xls writing functions - Need to check
# - URL read error trap.
##########################
# Changelog V1.2
# - Can decode and encode Greek characters for correct URL binding
##########################
# Changelog V1.1
# - Included the updated more accurate next page sequence
# - Asks for query term
# - Can now save both GR and CY results to a preconfigured xls file
# - Calculates total number of products accurately (not used currently but might be useful)
# - Returns availability for GR and CY
# - New folder calculation function decides which folder to read from and write on
# - Will try to write to the default file and if error occurs will write to a 2nd one
##########################
# Changelog V1.0
# - Returns all products from the GR and CY page from a preconfigured query term only
# - Writes 2 seperate files for GR and CY with results
# To Do : Work with categories.
# To Do : recognise if the query has only one product.

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

# Input search term
answer_term = "no"

while (answer_term == "no") :
 query_term = input("Please enter your query term: ")
 # # print(query_term.count(' '))
 # if query_term.find('http') :  # if query_term is a url...
  # query_url = quote(text.encode('utf-8'))
 if query_term.count(' ') > 0 :  # if query_term has at least one " "...
  # print("in if loop. Has at least 1 space")
  query_term = query_term.replace(" ", "+")
  # print(query_term)
 answer_text = "Your query term is: " + query_term + ". Is that correct? Press enter for yes. "
 answer_term = input(answer_text)

############################################################################
# The below needs refining. If ** is detected it's passed on to the grpage #
# but it breaks when it starts the BSoup functions probably because the    #
# element requested cannot be found in the soup.                           #
############################################################################
# if answer_term == '**' :
 # query_term = answer_term + query_term
 # print("Searching for: " + query_term)
# else :
 # print("Searching for: " + query_term)
 
if query_term.find("://") > 0 :  # if query_term is a full URL then use this as the grpage.
 url_term = query_term  # assign query_term to url_term
 grpage = url_term  # assign the url entered to the grpage variable
 if url_term.find('search') > 0 :
  filename = url_term[url_term.rfind('=')+1:]
 else :
  filename = url_term[url_term.rfind('/')+1:url_term.rfind('?')]
else :  # if query_term is a search term then add the base url to it
 url_term = quote(query_term.encode('iso-8859-7')).replace('%2B', '+')
 grpage = "https://www.e-shop.gr/search?q=" + url_term  # this is the base query url for GR
 filename = query_term

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

if os.path.exists(r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
 print("Using " + write_path + " for writing files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results") == True :  # does home folder exist?
 write_path = (r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results")
 print("Using home path 1 for writing files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results") == True :  # does home folder 1 exist?
 write_path = (r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results")
 print("Using home path 2 for writing files.")
 print("")
else :
 if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Using " + write_path + " for writing files.")
  print("")
 else :  # if not create it
  os.makedirs(r"C:\TEMPYTH")
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Creating and using " + write_path + " for writing files.")
  print("")

###############################
# End of write paths setting. #
###############################

# Opening files
# for writing
os.chdir(write_path)
write_file = ("GRvsCY_Search_Results_" + filename + ".xls")  # name of xls write file
alt_write_file = ("GRvsCY_ALT_Search_Results_" + filename + ".xls")  # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date)  # add sheet in virtual workbook named after the search string ad run date

ws_write.write(0, 0, "CODE")  # write date on A1 cell
ws_write.write(0, 1, "TITLE")  # write date on B1 cell
ws_write.write(0, 2, "GR-PRICE")  # write date on C1 cell
ws_write.write(0, 3, "GR-AVAIL")  # write date on D1 cell
ws_write.write(0, 4, "CY-PRICE")  # write date on E1 cell

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
   attempt = attempt + 1
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
   # if gr_a_text.find("Κατόπιν") :
    # gr_a_text = gr_a_text + "ς"
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
   ws_write.write(e, 0, gr_prod_per)
   ws_write.write(e, 1, gr_prod_title)
   ws_write.write(e, 2, gr_price_text)
   ws_write.write(e, 3, gr_a_text)
   ws_write.write(e, 4, cy_price_text)
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
    attempt = attempt + 1
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
     attempt = attempt + 1
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
    ws_write.write(e, 0, gr_prod_per)
    ws_write.write(e, 1, gr_prod_title)
    ws_write.write(e, 2, gr_price_text)
    ws_write.write(e, 3, gr_a_text)
    ws_write.write(e, 4, cy_price_text)
    e = e + 1
    print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
   offset = offset + 10
   gr_cat_offset_url = gr_cat_page + delim + "offset=" + str(offset) + "&" + categories
 else :
  total_next_pages = 0  # single search result page with categories
  containers = gr_page_soup.findAll('table', {'class' : 'web-product-container'})
  total_prod = len(containers)
  tp = total_prod
  print("Only 1 page and " + str(total_prod) + " products found.")
  print("")
  # len(containers)
  for container in containers :
   tp = tp - 1
   print("Processing item: " + str(total_prod - tp) + "/" + str(total_prod) + ". Remaining: " + str(total_prod - (total_prod - tp)))
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
   ws_write.write(e, 0, gr_prod_per)
   ws_write.write(e, 1, gr_prod_title)
   ws_write.write(e, 2, gr_price_text)
   ws_write.write(e, 3, gr_a_text)
   ws_write.write(e, 4, cy_price_text)
   e = e + 1
elif gr_page_soup.findAll("h1", {"style": "color:#4f4f4f;font-family:Tahoma;font-size:18px;font-weight:bold;padding:0 0 0 0;"}) :  # single product found
 print("Only 1 product found. Treating results as a single product page.")
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
  ws_write.write(e, 0, gr_prod_per)
  ws_write.write(e, 1, gr_prod_title)
  ws_write.write(e, 2, gr_price_text)
  ws_write.write(e, 3, gr_a_text)
  ws_write.write(e, 4, cy_price_text)
  e = e + 1 
else :
 # print("")
 print("Search result is probably empty. Try again with different terms.")
 sys.exit()
 

# try to write to the 1st file. If it fails try the 2nd
try :
 wb_write.save(write_file)
 print("")
 print(write_file + " created on " + write_path)
except :
 print("")
 wb_write.save(alt_write_file)
 print(alt_write_file + " created on " + write_path)


elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("")
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
