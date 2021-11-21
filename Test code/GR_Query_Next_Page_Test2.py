from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq

page_url = "https://www.e-shop.gr/search?q=spigen"  # this is the base query url
page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added

offset_url = page_url + page_offset + str(offset)  # this is the complete query url with offset. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0

uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

prod_info = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
prod_price = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

next_pages = page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons

next_pages_a = next_pages[0].findAll('a')  # keep all <a> only as they keep the next page numbers
total_next_pages = int(next_pages_a[len(next_pages_a)-2].text)  # this holds the exact next pages that need to be offset

for q in range(0, total_next_pages):
 print("Current page is: " + offset_url)
 print("Start of for Offset is: " + str(offset))
 if offset == 0 :
  print("Current page index is: " + str(q+1))
  for (i, p) in zip(prod_info, prod_price):
   print(str(i))
   prod_link = i.a['href']
   prod_title = i.a.text
   prod_per = i.span.text.replace("(", "").replace(")", "")
   price_text = p.text  # save text of the price result in price_text
   if price_text.count(' ') > 1:  # if price " " is more than 1 then it has a discount ... 
    price_text = price_text[price_text.find(' ')+1:].replace(" €", "")  # ... so print the second price without the euro sign
   else:
    price_text = price_text.replace(" €","")  # ... otherwise print the whole (single) price without the euro sign.
    print(prod_title + " - " + prod_per + " - " + price_text)
    offset = offset + 50
  # offset = offset + 50
  # offset_url = page_url + page_offset + str(offset)
  # uClient = uReq(page_url)
  # page_soup = soup(uClient.read(), "html.parser")
  # uClient.close()
 else :
  offset = offset + 50
  print("End of for Offset is: " + str(offset))
  offset_url = page_url + page_offset + str(offset)
  uClient = uReq(page_url)
  page_soup = soup(uClient.read(), "html.parser")
  uClient.close()


