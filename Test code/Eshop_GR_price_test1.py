from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
# from pyexcel_ods import get_data  # for the ability to read ods files
path = (r"C:\Users\Manager\Documents\Html Parser - Python\test.xlsx")  # path to xslx file

wb = xlrd.open_workbook(path)  # open workbook as wb
sheet = wb.sheet_by_index(0)  # open 1st sheet from wb
# sheet.cell_value(1, 2)  # show row 1 and column 2 data
	
# for i in range(1, 3):

for i in range(1, sheet.nrows):
 print(i)
 page_url = "https://www.e-shop.gr/s/" + sheet.cell_value(i,2)
 print(page_url)
 uClient = uReq(page_url)
 page_soup = soup(uClient.read(), "html.parser")
 uClient.close()
 pexist = page_soup.findAll("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:12px;"})
 pexist_value = pexist[0].text
 print("pexist_value = ", pexist_value)
if pexist_value == "Εξαντλημένο. Αποστολή ενημέρωσης με email μόλις ξαναγίνει διαθέσιμο":
	print("CODE = " + sheet.cell_value(i,2) + ", PRICE = 0")
else:
	gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
	gr_price_text = gr_price[0].text.replace("\xa0€","")
	print("CODE = " + sheet.cell_value(i,2) + ", PRICE = " + gr_price_text)
	
	


 
# below, for a given code will return the price. 
page_url = "https://www.e-shop.gr/spigen-rugged-armor-back-cover-case-for-huawei-mate-lite-20-black-p-TEL.057737"
print(page_url)
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()
gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
gr_price_text = gr_price[0].text.replace("\xa0€","")
print("CODE = " + page_url[-10:] + ", PRICE = " + gr_price_text)

# below, for a given search term will return link, code, title and price.
page_url = "https://www.e-shop.gr/search?q=spigen"	# link with discounts.
page_url = "https://www.e-shop.gr/search?q=brother"	# link with single price.
print(page_url)
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# για την αναζήτηση, φτάνει μέσα στο 
# <div id="web_body"> που έχει τους πίνακες με τα προϊόντα
# και προχωράει μέσα σε κάθε tr κτλ μέχρι που φτάνει στο 
# <table border="0" cellpadding="0" cellspacing="0" width="100%"><tr><td colspan="5" style="text-align:center;font-family:tahoma;font-size:14px;padding:0 0 10px 0;color:#808080;">Βρέθηκαν 272 προϊόντα σχετικά με <b>spigen</b>. Βλέπετε από 1 έως 50</td></tr>
page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.tr

# για την αναζήτηση, φτάνει μέσα στο 
# <div id="web_body"> που έχει τους πίνακες με τα προϊόντα
# και προχωράει μέσα σε κάθε tr κτλ μέχρι που φτάνει στο
# td valign="middle" style="padding:3px 6px 3px 3px;border-bottom:#909090 1px solid;"> που περιέχει το link
# τα αποθηκεύει στο prod_info
prod_info = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
prod_info[1].a['href']	# gives the link
prod_info[1].a.text 	# gives the product title
prod_info[1].span.text	# gives the PER with ()

# για την αναζήτηση, φτάνει στο font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;">
# και επιστρέφει τις τιμές.
prod_price = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})
prod_price[1].text # prints the product price with discount if available
prod_price[1].text[0:4] # prints the first 4 characters of prod_price

test.find(' ') # returns the position of " " given that the variable test holds the price.
prod_price[1].text.count(' ') # counts how many times character " " is encountered.

price_text = prod_price[1].text # save text of the price result in price_text
if price_text.count(' ') > 1:	# if price " " is more than 1 then it has a discount ... 
 price_text[price_text.find(' ')+1:].replace(" €","")	# ... so print the second price without the euro sign
else:
 price_text.replace(" €","")	#... otherwise print the whole (single) price without the euro sign.


#####################################################
# Complete code for query. Displays first 5 products.
#####################################################
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

page_url = "https://www.e-shop.gr/search?q=spigen"
print(page_url)
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
