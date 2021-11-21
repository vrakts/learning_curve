from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
import xlwt  # for the ability to write to excel files
from datetime import date
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder

# Setting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)

# opening xls file for writing
write_path = os.getcwd()
write_file = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results\Search_Results.xls")  # path to xslx write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet("GR_SEARCH")  # add sheet in virtual workbook
ws_write.write(0, 0, start_date)  # write date on A1 cell

page_url = "https://www.e-shop.gr/search?q=spigen"  # this is the base query url
page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # represents the row inside the excel file.

offset_url = page_url + page_offset + str(offset)  # this is the complete query url with offset. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0

uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

prod_info = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
prod_price = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

next_pages = page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons
next_pages_a = next_pages[0].findAll('a')  # keep all <a> only as they keep the next page numbers
total_next_pages = int(next_pages_a[len(next_pages_a)-2].text)  # this holds the exact next pages that need to be offset

for q in range(0, total_next_pages) :
 # print("Start for loop. Current page is: " + offset_url)
 # print("Offset is: " + str(offset))
 # print("Current page index is: " + str(q+1))
 for (i, p) in zip(prod_info, prod_price):
  prod_link = i.a['href']
  prod_title = i.a.text
  prod_per = i.span.text.replace("(", "").replace(")", "")
  price_text = p.text  # save text of the price result in price_text
  if price_text.count(' ') > 1 :  # if price " " is more than 1 then it has a discount ...
   price_text = price_text[price_text.find(' ')+1:].replace(" €", "").replace(".", ",")  # ... so print the second price without the euro sign
  else :
   price_text = price_text.replace(" €","").replace(".", ",")  #... otherwise print the whole (single) price without the euro sign.
  print(prod_per + " - " + prod_title + " - " + price_text)
  # print(e)
  ws_write.write(e, 0, prod_per)
  ws_write.write(e, 1, prod_title)
  ws_write.write(e, 2, price_text)
  e = e + 1
 offset = offset + 50
 offset_url = page_url + page_offset + str(offset)
 uClient = uReq(offset_url)
 page_soup = soup(uClient.read(), "html.parser")
 uClient.close()
 prod_info = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 prod_price = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

wb_write.save(write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
