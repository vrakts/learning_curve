# stephanis_games.py

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
import requests, os, sys, re, xlwt

headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTM	L, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
page_list = []
e = 1

# set files
try :
 write_path = (r'C:\Users\manager\Desktop')
 os.chdir(write_path)
except :
 write_path = (r'Z:\Users\Vrakts\Desktop')
 os.chdir(write_path)
write_file = ('stephanis.xls')
wb_write = xlwt.Workbook()
ws_write = wb_write.add_sheet("stephanis", cell_overwrite_ok = True)
ws_write.write(0, 0, "Category")
ws_write.write(0, 1, "Title")
ws_write.write(0, 2, "Code")
ws_write.write(0, 3, "Normal Price")
ws_write.write(0, 4, "Offer Price")
ws_write.write(0, 5, "URL")


page_url = input("Page? ")
# page_url = 'https://www.stephanis.com.cy/el/products/information-technology/tablets-and-ereaders/tablets?Quantity=min&PriceMin=&PriceMax=&SF_1=3061#&page=1'

if page_url.find('page=') >= 0 :
 page_url = page_url[:page_url.rfind('&page=')]

result = requests.get(page_url, headers = headers)
webpage = result.content
page_soup = soup(webpage, "html5lib")

try :
 count_soup = page_soup.find('div', {'class': 'pagination-current-page'}).text.strip()
 # page_count = int(count_soup[len(count_soup)-1:])
 page_count = int(count_soup[count_soup.find('από')+4:])
except :
 page_count = 1

print("Page count: " + str(page_count) + "\n")

if page_count > 1 :
 for i in range (1, page_count + 1) :
  if page_url.find('page=') >= 0 :
   page_url = page_url[:page_url.rfind('&page=')]
  page_url += '&page=' + str(i)
  page_list.append(page_url)
  # print("Page url: " + page_url)

for page_url in page_list :
 # print(page_url)
 result = requests.get(page_url, headers = headers)
 webpage = result.content
 page_soup = soup(webpage, "html5lib")
 
 regex = re.compile('.*property-spotlight-slide-2.*')
 containers = page_soup.findAll("div", {"class" : regex}) 
 
 for container in containers :
  price_containers = container.findAll('div', {'class': 'listing-details-heading'})
  full_title = container.find('li', {'class': 'spotlight-list-text tile-product-name'}).text
  cat = "-"
  if full_title.find('Παιχνίδι PC ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι PC ')
  elif full_title.find('Παιχνίδια PC ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδια PC ')
  elif full_title.find('Παιχνίδι Nintendo Switch ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Nintendo Switch ')
  elif full_title.find('Παιχνίδι Nintendo 3DS ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Nintendo 3DS ')
  elif full_title.find('Παιχνίδι Nintendo DS ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Nintendo DS ')
  elif full_title.find('Παιχνίδι Nintendo ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Nintendo ')
  elif full_title.find('Παιχνίδι Switch ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Switch ')
  elif full_title.find('Παιχνίδι Wii U ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Wii U ')
  elif full_title.find('Παιχνίδια Xbox One ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδια Xbox One ')
  elif full_title.find('Παιχνίδι XBOX One ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι XBOX One ')
  elif full_title.find('Παιχνίδι Xbox One ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Xbox One ')
  elif full_title.find('Παιχνίδι Xbox 360 ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Xbox 360 ')
  elif full_title.find('Παιχνίδι Xbox 360 ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Xbox 360 ')
  elif full_title.find('Παιχνίδι Xbox ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Xbox ')
  elif full_title.find('Παιχνίδι PS4 ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι PS4 ')
  elif full_title.find('Παχνίδι PS4 ') >=0 :
   useless, cat, title = full_title.partition('Παχνίδι PS4 ')
  elif full_title.find('Παιχνίδι PS Vita ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι PS Vita ')
  elif full_title.find('Παιχνίδι Ps Vita ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι Ps Vita ')
  elif full_title.find('Παιχνίδι PSP ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι PSP ')
  elif full_title.find('Παιχνίδι PS3 ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι PS3 ')
  elif full_title.find('Παιχνίδι PS2 ') >=0 :
   useless, cat, title = full_title.partition('Παιχνίδι PS2 ')
  else :
   title = full_title
  code = container.find('div', {'class': 'product-code'}).text.strip()
  if price_containers[0].find('div', {'class': 'listing-details large-was-price'}) :
   normal_price = price_containers[0].find('div', {'class': 'listing-details-heading large-now-price with-sale'}).text.strip().replace('€', '').replace('.', ',')
  else :
   normal_price = price_containers[0].text.strip().replace('€', '').replace('.', ',')
  try:
   offer_price = price_containers[2].text.strip().replace('€', '').replace('.', ',')
  except:
   offer_price = normal_price
  cat = cat.strip()
  title = title.strip()
  full_url = 'https://www.stephanis.com.cy' + container.a['href']
  print(full_url)
  if offer_price == normal_price :
   print("Title: " + title + ", Category: " + cat + ", Code: " + code + ", Price: " + normal_price + '\n')
   ws_write.write(e, 0, cat)
   ws_write.write(e, 1, title)
   ws_write.write(e, 2, code)
   ws_write.write(e, 3, normal_price)
   ws_write.write(e, 5, full_url)
  else:
   print("Title: " + title + ", Category: " + cat + ", Code: " + code + ", Price: " + normal_price + ", Discount: " + offer_price +'\n')
   ws_write.write(e, 0, cat)
   ws_write.write(e, 1, title)
   ws_write.write(e, 2, code)
   ws_write.write(e, 3, normal_price)
   ws_write.write(e, 4, offer_price)
   ws_write.write(e, 5, full_url)
  e += 1

wb_write.save(write_file)