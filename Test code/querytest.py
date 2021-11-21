from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
import xlwt  # for the ability to write to excel files
from datetime import date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder

offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # represents the row inside the excel file.

query_term = "spigen"

grpage = "https://www.e-shop.gr/search?q=" + query_term  # this is the base query url for GR
page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
gr_offset_url = grpage + page_offset + str(offset)  # this is the complete query url with offset. eg. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0

now = datetime.now()
start_time = now.strftime("%H:%M:%S")
start_date = now.strftime("%m-%d-%y")
print("Script started at " + start_date + ", " + start_time)

# opening xls file for writing
loc_home = r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Search_Results_"
loc_work = r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Search_Results_"
file_ext = ".xls"
write_file = (loc_home + query_term + file_ext)  # path to xls write file for home tests
# write_file = (loc_work + query_term + file_ext)  # path to xls write file for work tests
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date)  # add sheet in virtual workbook named after the search string ad run date

ws_write.write(0, 0, "CODE")  # write date on A1 cell
ws_write.write(0, 1, "TITLE")  # write date on B1 cell
ws_write.write(0, 2, "GR-PRICE")  # write date on C1 cell
ws_write.write(0, 3, "CY-PRICE")  # write date on D1 cell

gr_uClient = uReq(gr_offset_url) 
gr_page_soup = soup(gr_uClient.read(), "html.parser")
gr_uClient.close()

gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

# gr last page preparations
next_pages = gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons
next_pages_a = next_pages[0].findAll('a')  # keep all <a> only as they keep the next page numbers
if len(next_pages_a) == 0 :
 total_next_pages = 1
else:
 total_next_pages = int(next_pages_a[len(next_pages_a)-2].text)  # this holds the exact next pages that need to be offset

# calculating total products count
# first we need to calculate the last offset page
last_offset = (total_next_pages - 1) * 50
last_offset
# then calculate the new url
last_offset_url = grpage + page_offset + str(last_offset)
last_offset_url
# now we need to reload the last offset soup with all available products
last_uClient = uReq(last_offset_url) 
last_page_soup = soup(last_uClient.read(), "html.parser")
last_uClient.close()
last_prod_info = last_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
# last step, add the gr_prod_info of the last offset page to the offset value
total_prod = last_offset + len(last_prod_info)
total_prod

tp = total_prod

print("Found " + total_prod + "products. Starting process now.")

for q in range(0, total_next_pages) :
 for (i, p) in zip(gr_prod_info, gr_prod_price) :
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
  tp = tp - 1
  print("Products left: " + str(total_prod - tp) + "/" + str(total_prod))
  ws_write.write(e, 0, gr_prod_per)
  ws_write.write(e, 1, gr_prod_title)
  ws_write.write(e, 2, gr_price_text)
  ws_write.write(e, 3, cy_price_text)
  e = e + 1
  # tp = tp - 1
 offset = offset + 50
 offset_url = grpage + page_offset + str(offset)
 gr_uClient = uReq(offset_url)
 gr_page_soup = soup(gr_uClient.read(), "html.parser")
 gr_uClient.close()
 gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

wb_write.save(write_file)
