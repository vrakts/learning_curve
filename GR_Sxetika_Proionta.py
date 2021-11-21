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

# Setting starting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy

offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # this the write excel file position.
attempt = 0  # how many attempts to re-read the url in case of failure
sxetika_list = ""  # this holds a list of also products. empty it out on each start to be safe.
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

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
 if query_term.find("://") > 0 :
  print("Entered a complete URL. No encoding will happen")
  url_term = query_term
 else :
  url_term = quote(query_term.encode('iso-8859-7')).replace('%2B', '+')

if os.path.exists(r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results")
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

# Opening files
# for writing
filename = url_term[url_term.rfind('/')+1:url_term.rfind('?')]
os.chdir(write_path)
write_file = ("GR_Sxetika_" + filename + ".xls")  # name of xls write file
alt_write_file = ("GR_ALT_Sxetika_" + filename + ".xls")  # alternate name of xls write file

wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date)  # add sheet in virtual workbook named after the search string ad run date
ws_write.write(0, 0, "CODE")  # write date on A1 cell
ws_write.write(0, 1, "TITLE")  # write date on B1 cell
ws_write.write(0, 2, "PRICE")  # write date on C1 cell
ws_write.write(0, 3, "SXETIKA")  # write date on D1 cell

# grpage = 'https://www.e-shop.gr/ypologistes-polymixanimata-list?table=PER&category=%D0%CF%CB%D5%CC%C7%D7%C1%CD%C7%CC%C1%D4%C1'

grpage = url_term
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

print("Treating this as a category query page.")
if gr_page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories
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
   # print("q value = " + str(q))
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
    #  print(container)
    gr_prod_link = container.find('td', {'class': 'web-product-title'}).a['href']
    gr_prod_per = container.find('td', {'class': 'web-product-title'}).font.text.replace('(', '').replace(')', '')
    gr_prod_title = container.find('td', {'class': 'web-product-title'}).a.h2.text
    if container.find('font', {'style': 'color:#FF0000'}) :
     gr_prod_price = container.find('font', {'style': 'color:#FF0000'}).text.replace(".", ",")
    else :
     gr_prod_price = container.find('td', {'class': 'web-product-price'}).text.strip().replace('\xa0€', '').replace('.', ',')
    req = urllib.request.Request(gr_prod_link, headers = headers)
    attempt = 0
    while attempt < 3 :
     try :
      # print("On try :" + str(attempt))
      gr_sxetika_uClient = uReq(req)
      gr_sxetika_page_soup = soup(gr_sxetika_uClient.read(), "html.parser")
      gr_sxetika_uClient.close()
      break
     except http.client.IncompleteRead :
      # print("On except :" + str(attempt))
      attempt = attempt + 1
    gr_prod_sxetika = gr_sxetika_page_soup.findAll('div', {'class': 'also_box'})
    sxetika_list = ""
    for sxetika in gr_prod_sxetika :
     sxetika_per_link = sxetika.a['href']
     sxetika_per = sxetika_per_link[sxetika_per_link.rfind('-')+1:]
     if len(sxetika_list) == 0 :
      sxetika_list = sxetika_per
     else :
      sxetika_list = sxetika_list + "," + sxetika_per
    print(gr_prod_per + " - " + gr_prod_title + " - " + gr_prod_price)
    print(gr_prod_link)
    print("Σχετικά: " + sxetika_list)
    print("")
    if sxetika_list != "" :
     ws_write.write(e, 0, gr_prod_per)
     ws_write.write(e, 1, gr_prod_title)
     ws_write.write(e, 2, gr_prod_price)
     ws_write.write(e, 3, sxetika_list)
     e = e + 1
    else :
     continue  
   offset = offset + 10
   gr_cat_offset_url = gr_cat_page + delim + "offset=" + str(offset) + "&" + categories
 else :
  total_next_pages = 0  # single search result page with categories
  print("Only 1 page found.")
  containers = gr_page_soup.findAll('table', {'class' : 'web-product-container'})
  # len(containers)
  for container in containers :
   #  print(container)
   gr_prod_link = container.find('td', {'class': 'web-product-title'}).a['href']
   gr_prod_per = container.find('td', {'class': 'web-product-title'}).font.text.replace('(', '').replace(')', '')
   gr_prod_title = container.find('td', {'class': 'web-product-title'}).a.h2.text
   if container.find('font', {'style': 'color:#FF0000'}) :
    gr_prod_price = container.find('font', {'style': 'color:#FF0000'}).text.replace(".", ",")
   else :
    gr_prod_price = container.find('td', {'class': 'web-product-price'}).text.strip().replace('\xa0€', '').replace('.', ',')
   req = urllib.request.Request(gr_prod_link, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     gr_sxetika_uClient = uReq(req)
     gr_sxetika_page_soup = soup(gr_sxetika_uClient.read(), "html.parser")
     gr_sxetika_uClient.close()
     break
    except http.client.IncompleteRead :
     # print("On except :" + str(attempt))
     attempt = attempt + 1
   gr_prod_sxetika = gr_sxetika_page_soup.findAll('div', {'class': 'also_box'})
   sxetika_list = ""
   for sxetika in gr_prod_sxetika :
    sxetika_per_link = sxetika.a['href']
    sxetika_per = sxetika_per_link[sxetika_per_link.rfind('-')+1:]
    if len(sxetika_list) == 0 :
     sxetika_list = sxetika_per
    else :
     sxetika_list = sxetika_list + "," + sxetika_per
   if sxetika_list.find('ANA.FAB0001') >= 0 :
    sxetika_list.replace('ANA.FAB0001', 'ANA.GOS00001')
   print(gr_prod_per + " - " + gr_prod_title + " - " + gr_prod_price)
   print(gr_prod_link)
   print("Σχετικά: " + sxetika_list)
   print("")
   if sxetika_list != "" :
    ws_write.write(e, 0, gr_prod_per)
    ws_write.write(e, 1, gr_prod_title)
    ws_write.write(e, 2, gr_prod_price)
    ws_write.write(e, 3, sxetika_list)
    e = e + 1
   else :
    continue  

# try to write to the 1st file. If it fails try the 2nd
try :
 wb_write.save(write_file)
 print("File " + write_file + " saved in " + write_path + ".")
except :
 wb_write.save(alt_write_file)
 print("File " + alt_write_file + " saved in " + write_path + ".")

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("")
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")

finished = input("Found " + str(e) + " products. Ready when you are...")
