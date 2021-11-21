# Current Version 1.2
#####################
# Changelog V1.2
# - Can decode and encode Greek characters for correct URL binnding
#####################
# Changelog V1.1
# - Included the updated more accurate next page sequence
# - Asks for query term
# - Can now save both GR and CY results to a preconfigured xls file
# - Calculates total number of products accurately (not used currently but might be useful)
# - Returns availability for GR and CY
# - New folder calculation function decides which folder to read from and write on
# - Will try to write to the default file and if error occurs will write to a 2nd one
#####################
# Changelog V1.0
# - Returns all products from the GR and CY page from a preconfigured query term only
# - Writes 2 seperate files for GR and CY with results
# To Do : Work with categories.
# To Do : recognise if the query has only one product.

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
 url_term = quote(query_term.encode('iso-8859-7')).replace('%2B', '+')

# if url_term.find("://") > 0 :
 # grpage = url_term
# else :
 # grpage = "https://www.e-shop.gr/search?q=" + url_term  # this is the base query url for GR

grpage = "https://www.e-shop.gr/search?q=" + url_term  # this is the base query url for GR
page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
gr_offset_url = grpage + page_offset + str(offset)  # this is the complete query url with offset. eg. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0

# Setting starting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy

# start_time = datetime.now()
# start_time_frm = start_time.strftime("%H:%M:%S")
# start_date = start_time.strftime("%d-%m-%y")
# print("Script started at " + start_date + ", " + start_time_frm)

################################
# Setting correct write paths. #
################################

if os.path.exists(r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results")
 print("")
 print("Using " + write_path + " for writing files.")
elif os.path.exists(r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Home") == True :  # does home folder exist?
 write_path = (r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Home")
 print("")
 print("Using " + write_path + " for writing files.")
else :
 if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
  write_path = (r"C:\TEMPYTH")
  print("")
  print("Predefined paths don't exist. Using " + write_path + " for writing files.")
 else :  # if not create it
  os.makedirs(r"C:\TEMPYTH")
  write_path = (r"C:\TEMPYTH")
  print("")
  print("Predefined paths don't exist. Creating and using " + write_path + " for writing files.")

###############################
# End of write paths setting. #
###############################

# Opening files
# for writing
os.chdir(write_path)
write_file = ("GR_CY_Search_Results_" + query_term + ".xls")  # name of xls write file
alt_write_file = ("GR_CY_ALT_Search_Results_" + query_term + ".xls")  # alternate name of xls write file

# loc_home = r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Home\Search_Results_"
# loc_work = r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results\Search_Results_"
# file_ext = ".xls"
# write_file = (loc_home + query_term + file_ext)  # path to xls write file for home tests
# # write_file = (loc_work + query_term + file_ext)  # path to xls write file for work tests
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date)  # add sheet in virtual workbook named after the search string ad run date

ws_write.write(0, 0, "CODE")  # write date on A1 cell
ws_write.write(0, 1, "TITLE")  # write date on B1 cell
ws_write.write(0, 2, "GR-PRICE")  # write date on C1 cell
ws_write.write(0, 3, "GR-AVAIL")  # write date on D1 cell
ws_write.write(0, 4, "CY-PRICE")  # write date on E1 cell

gr_uClient = uReq(gr_offset_url) 
gr_page_soup = soup(gr_uClient.read(), "html.parser")
gr_uClient.close()

if len(gr_page_soup.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})) == 0 :
 print("Only 1 product found. Treating results as a single product page")
 print("")
 gr_prod_per = gr_page_soup.find('td', {'style' : 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text
 gr_prod_link = 'https://www.e-shop.gr/product?id=' + gr_prod_per
 gr_prod_title = gr_page_soup.h1.text
 gr_price_text = gr_page_soup.find('span', {'class' : 'web-price-value-new'}).text.replace('\xa0€', '').replace('.', ',')
 gr_a = gr_page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
 gr_a_text = gr_a.text[gr_a.text.find(":")+2:gr_a.text.find("\r")]
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
 ws_write.write(e, 0, gr_prod_per)
 ws_write.write(e, 1, gr_prod_title)
 ws_write.write(e, 2, gr_price_text)
 ws_write.write(e, 3, gr_a_text)
 ws_write.write(e, 4, cy_price_text)
 # try to write to the 1st file. If it fails try the 2nd
 try :
  wb_write.save(write_file)
 except :
  wb_write.save(alt_write_file)
 elapsed_time = time.time() - start_time
 minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
 mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
 seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
 seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
 formatted_time = str(mins) + "." + str(seconds)
 print("")
 sys.exit("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")

gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

# gr last page preparations
next_pages = gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons
if len(next_pages) == 0 :
 print("")
 sys.exit("Search result is probably empty. Try again with different terms.")
 # break
else :
 next_pages_a = next_pages[0].findAll('a')  # keep all <a> only as they keep the next page numbers
 if len(next_pages_a) == 0 :
  total_next_pages = 1
 else:
  total_next_pages = int(next_pages_a[len(next_pages_a)-2].text)  # this holds the exact next pages that need to be offset


# calculating total products count
# first we need to calculate the last offset page
last_offset = (total_next_pages - 1) * 50
# then calculate the new url
last_offset_url = grpage + page_offset + str(last_offset)
# now we need to reload the last offset soup with all available products
last_uClient = uReq(last_offset_url) 
last_page_soup = soup(last_uClient.read(), "html.parser")
last_uClient.close()
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
  gr_a_uClient = uReq(gr_a_page)
  gr_a_pagesoup = soup(gr_a_uClient.read(), "html.parser")
  gr_a_uClient.close()
  gr_a = gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
  # gr_a_text = gr_a.text[gr_a.text.find(":")+2:]
  gr_a_text = gr_a.text[gr_a.text.find(":")+2:gr_a.text.find("\r")]
  if gr_a_text.find("Κατόπιν") :
   gr_a_text = gr_a_text + "ς"
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
 gr_uClient = uReq(offset_url)
 gr_page_soup = soup(gr_uClient.read(), "html.parser")
 gr_uClient.close()
 gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

# try to write to the 1st file. If it fails try the 2nd
try :
 wb_write.save(write_file)
except :
 wb_write.save(alt_write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("")
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
