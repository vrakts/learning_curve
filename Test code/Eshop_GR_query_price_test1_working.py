######################################################
# Complete code for query. Displays first 5 products.#
######################################################

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
import xlrd  # for the ability to read excel files
path = (r"Z:\Users\Vrakts\Desktop\Html Parser - Python\test.xlsx")  # path to xslx file

page_url = "https://www.e-shop.gr/search?q=spigen"
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

prod_info = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
prod_price = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

for (i, p) in zip(prod_info, prod_price):
 prod_link = i.a['href']
 prod_title = i.a.text
 prod_per = i.span.text.replace("(", "").replace(")", "")
 price_text = p.text # save text of the price result in price_text
 if price_text.count(' ') > 1:	# if price " " is more than 1 then it has a discount ... 
  price_text = price_text[price_text.find(' ')+1:].replace(" €", "")	# ... so print the second price without the euro sign
 else:
  price_text = price_text.replace(" €","")	#... otherwise print the whole (single) price without the euro sign.
 print(prod_title + " - " + prod_per + " - " + price_text)


next_page = page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next buttons
next_page_a = next_page[0].findAll('a')  # keep all <a> only as they keep the next page numbers

