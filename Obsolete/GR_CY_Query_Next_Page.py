from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
import xlwt  # for the ability to write to excel files
from datetime import date
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder

offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # represents the row inside the excel file.

# Input search term
answer_term = "no"

while (answer_term == "no") :
 query_term = input("Please enter your query term: ")
 # print(query_term.count(' '))
 if query_term.count(' ') > 0 :  # if query_term has at least one " "...
  # print("in if loop. Has at least 1 space")
  query_term = query_term.replace(" ", "+")
  # print(query_term)
 answer_text = "Your query term is: " + query_term + ". Is that correct? Press enter for yes. "
 answer_term = input(answer_text)
 
grpage = "https://www.e-shop.gr/search?q=" + query_term  # this is the base query url for GR
page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
gr_offset_url = grpage + page_offset + str(offset)  # this is the complete query url with offset. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0

# Setting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)

# opening xls file for writing
write_path = os.getcwd()
write_file = (r'Z:\Users\Vrakts\Desktop\Html Parser - Python\Search_Results_' + query_term + '.xls')  # path to xsl write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet("SHEET1")  # add sheet in virtual workbook named after the search string ad run date
ws_write.write(0, 0, grpage[grpage.find("=")+1:] + "-" + start_date)  # write date on A1 cell

gr_uClient = uReq(gr_offset_url)
gr_page_soup = soup(gr_uClient.read(), "html.parser")
gr_uClient.close()

# total_prod = 
gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

# gr preparations
next_pages = gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons
next_pages_a = next_pages[0].findAll('a')  # keep all <a> only as they keep the next page numbers
if len(next_pages_a) == 0 :
 total_next_pages = 1
else:
 total_next_pages = int(next_pages_a[len(next_pages_a)-2].text)  # this holds the exact next pages that need to be offset

for q in range(0, total_next_pages) :
 for (i, p) in zip(gr_prod_info, gr_prod_price):
  gr_prod_link = i.a['href']
  gr_prod_title = i.a.text
  gr_prod_per = i.span.text.replace("(", "").replace(")", "")
  gr_price_text = p.text  # save text of the price result in price_text
  if gr_price_text.count(' ') > 1 :  # if price " " is more than 1 then it has a discount ...
   gr_price_text = gr_price_text[gr_price_text.find(' ')+1:].replace(" €", "").replace(".", ",")  # ... so print the second price without the euro sign
  else :
   gr_price_text = gr_price_text.replace(" €","").replace(".", ",")  #... otherwise print the whole (single) price without the euro sign.
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
    cy_price_text = cy_price[0].text.replace("\xa0€","").replace(".", ",")
  print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text)
  ws_write.write(e, 0, gr_prod_per)
  ws_write.write(e, 1, gr_prod_title)
  ws_write.write(e, 2, gr_price_text)
  ws_write.write(e, 3, cy_price_text)
  e = e + 1
 offset = offset + 50
 offset_url = grpage + page_offset + str(offset)
 gr_uClient = uReq(offset_url)
 gr_page_soup = soup(gr_uClient.read(), "html.parser")
 gr_uClient.close()
 gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

wb_write.save(write_file)

# # opening xls file for writing
# write_path = os.getcwd()
# write_file = (r"Z:\Users\Vrakts\Desktop\Html Parser - Python\CY_Search_Results.xls")  # path to xsl write file
# wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
# ws_write = wb_write.add_sheet(cypage[cypage.find("=")+1:] + "-" + start_date)  # add sheet in virtual workbook named after the search string ad run date
# ws_write.write(0, 0, start_date)  # write date on A1 cell

# # cy preparations
# next_pages = cy_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons
# next_pages_a = next_pages[0].findAll('a')  # keep all <a> only as they keep the next page numbers
# total_next_pages = int(next_pages_a[len(next_pages_a)-2].text)  # this holds the exact next pages that need to be offset
# e = 1
# offset = 0

# for q in range(0, total_next_pages) :
 # for (i, p) in zip(cy_prod_info, cy_prod_price):
  # prod_link = i.a['href']
  # prod_title = i.a.text
  # prod_per = i.span.text.replace("(", "").replace(")", "")
  # price_text = p.text  # save text of the price result in price_text
  # if price_text.count(' ') > 1 :  # if price " " is more than 1 then it has a discount ...
   # price_text = price_text[price_text.find(' ')+1:].replace(" €", "").replace(".", ",")  # ... so print the second price without the euro sign
  # else :
   # price_text = price_text.replace(" €","").replace(".", ",")  #... otherwise print the whole (single) price without the euro sign.
  # print(prod_per + " - " + prod_title + " - " + price_text)
  # # print(e)
  # ws_write.write(e, 0, prod_per)
  # ws_write.write(e, 1, prod_title)
  # ws_write.write(e, 2, price_text)
  # e = e + 1
 # offset = offset + 50
 # offset_url = cypage + page_offset + str(offset)
 # cy_uClient = uReq(offset_url)
 # cy_page_soup = soup(cy_uClient.read(), "html.parser")
 # cy_uClient.close()
 # cy_prod_info = cy_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 # cy_prod_price = cy_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

# wb_write.save(write_file)

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
