# stephanis_games.py

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
import requests, os, sys, re, xlwt

headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
page_list = []
e = 1
cut = 1

def write_it_down(write_file, alt_write_file) :
 # print(write_file + "saved on " + write_path)
 try :
  wb_write.save(write_file)
 except :
  wb_write.save(alt_write_file)
 sys.exit(write_file + " saved on " + write_path)

page_url = input("Page? ")
# page_url = 'https://www.stephanis.com.cy/el/products/information-technology/tablets-and-ereaders/tablets?Quantity=min&PriceMin=&PriceMax=&SF_1=3061#&page=1'

if page_url.find('page=') >= 0 :
 page_url = page_url[:page_url.rfind('&page=')]

result = requests.get(page_url, headers = headers)
webpage = result.content
page_soup = soup(webpage, "html5lib")

# set files
if os.path.exists(r"C:\Users\manager\Desktop") == True :
 write_path = (r'C:\Users\manager\Desktop')
 os.chdir(write_path)
elif os.path.exists(r"Z:\Users\Vrakts\Desktop") == True :
 write_path = (r'Z:\Users\Vrakts\Desktop')
 os.chdir(write_path)
elif os.path.exists(r"Y:\OneDrive") == True :
 write_path = (r'Y:\OneDrive')
 os.chdir(write_path)
category_name = page_soup.find("div", {"class": "breadcrumb-current-page"}).text.upper().replace(" ", "_")
# write_file = ('stephanis.xls')
write_file = (category_name + '.xls')
alt_write_file = (category_name + '_2.xls')
wb_write = xlwt.Workbook()
ws_write = wb_write.add_sheet("stephanis", cell_overwrite_ok = True)
ws_write.write(0, 0, "Category")
ws_write.write(0, 1, "Title")
ws_write.write(0, 2, "Code")
ws_write.write(0, 3, "Normal Price")
ws_write.write(0, 4, "Offer Price")
ws_write.write(0, 5, "Μέγεθος οθόνης")
ws_write.write(0, 6, "Ανάλυση οθόνης")
ws_write.write(0, 7, "Τύπος οθόνης")
ws_write.write(0, 8, "Οθόνη Αφής")
ws_write.write(0, 9, "Επεξεργαστής")
ws_write.write(0, 10, "Μνήμη RAM")
ws_write.write(0, 11, "Τύπος δίσκου")
ws_write.write(0, 12, "Χωρητικότητα")
ws_write.write(0, 13, "Κάρτα γραφικών")
ws_write.write(0, 14, "G-RAM")
ws_write.write(0, 15, "OS")
ws_write.write(0, 16, "Optical Drive")
ws_write.write(0, 17, "Ήχος")
ws_write.write(0, 18, "Κάμερα")
ws_write.write(0, 19, "Συνδεσιμότητα")
ws_write.write(0, 20, "Θύρες")
ws_write.write(0, 21, "Τροφοδοτικό")
ws_write.write(0, 22, "Μπαταρία")
ws_write.write(0, 23, "Διαρκεια μπαταρίας")
ws_write.write(0, 24, "Ειδικά χαρακτηριστικά")
ws_write.write(0, 25, "Διαστάσεις")
ws_write.write(0, 26, "Βάρος")
ws_write.write(0, 27, "Χρώμα")
ws_write.write(0, 28, "Περιλαμβάνονται")
ws_write.write(0, 29, "URL")

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
   normal_price = price_containers[0].find('div', {'class': 'listing-details-heading large-now-price with-sale'}).text.strip().replace('€', '').replace(',', '').replace('.', ',')
  else :
   normal_price = price_containers[0].text.strip().replace('€', '').replace(',', '').replace('.', ',')
  try:
   offer_price = price_containers[2].text.strip().replace('€', '').replace(',', '').replace('.', ',')
  except:
   offer_price = "-"
  cat = category_name
  cat = cat.strip()
  title = title.strip()
  full_url = 'https://www.stephanis.com.cy' + container.a['href']
  print(full_url)
  
  result = requests.get(full_url, headers = headers)
  webpage = result.content
  prod_page_soup = soup(webpage, "html5lib")
  
  values = []
  labels = []
  if prod_page_soup.find('table', {'class': 'tab-spec-list specifications w-list-unstyled'}).findAll("td", {"class", "value"}) :
   values_text = prod_page_soup.find('table', {'class': 'tab-spec-list specifications w-list-unstyled'}).findAll("td", {"class", "value"})
   labels = prod_page_soup.find('table', {'class': 'tab-spec-list specifications w-list-unstyled'}).findAll("td", {"class", "label"})
   for value in values_text :
    values.append(value.text)
  else :
   values_text = prod_page_soup.find("div", {"class" : "specs-padding"}).contents
   for i in range(len(values_text)) :
    try :
     if values_text[i].find(":") >= 0 :
      values.append(values_text[i][values_text[i].find(":")+2:].strip())
     else :
      continue
    except :
     continue
  print("Χαρακτηριστικα: " + str(len(values)))
  for i in range(0, len(values)) :
   # print(values[i].strip())
   text_to_find = labels[i].text.strip()
   column_start = 5
   try:
    if text_to_find.find('Μέγεθος οθόνης:') >= 0 :
     column = column_start
    elif text_to_find.find('Ευκρίνεια οθόνης:') >= 0 :
     column = column_start + 1
    elif text_to_find.find('Τύπος οθόνης:') >= 0 :
     column = column_start + 2
    elif text_to_find.find('Οθόνη Αφής:') >= 0 :
     column = column_start + 3
    elif text_to_find.find('Επεξεργαστής:') >= 0 :
     column = column_start + 4
    elif text_to_find.find('Μνήμη RAM:') >= 0 :
     column = column_start + 5
    elif text_to_find.find('Τύπος δίσκου:') >= 0 :
     column = column_start + 6
    elif text_to_find.find('Χωρητικότητα:') >= 0 :
     column = column_start + 7
    elif text_to_find.find('Κάρτα γραφικών:') >= 0 :
     column = column_start + 8
    elif text_to_find.find('Μνήμη κάρτας γραφικών:') >= 0 :
     column = column_start + 9
    elif text_to_find.find('Οπτική Μονάδα Δίσκου:') >= 0 :
     column = column_start + 10
    elif text_to_find.find('Ήχος:') >= 0 :
     column = column_start + 11
    elif text_to_find.find('Κάμερα:') >= 0 :
     column = column_start + 12
    elif text_to_find.find('Συνδεσιμότητα:') >= 0 :
     column = column_start + 13
    elif text_to_find.find('Θύρες:') >= 0 :
     column = column_start + 14
    elif text_to_find.find('Τροφοδοτικό:'>= 0 ) :
     column = column_start + 15
    elif text_to_find.find('Μπαταρία:') >= 0 :
     column = column_start + 16
    elif text_to_find.find('Διάρκεια ζωής μπαταρίας:') >= 0 :
     column = column_start + 17
    elif text_to_find.find('Ειδικά χαρακτηριστικά:') >= 0 :
     column = column_start + 18
    elif text_to_find.find('Διαστάσεις:') >= 0 :
     column = column_start + 19
    elif text_to_find.find('Βάρος:') >= 0 :
     column = column_start + 20
    elif text_to_find.find('Χρώμα:') >= 0 :
     column = column_start + 21
    ws_write.write(e, column, values[i].strip())	
   except :
    ws_write.write(e, column, "-")

  print("Title: " + title + ", Category: " + cat + ", Code: " + code + ", Price: " + normal_price + ", Discount: " + offer_price +'\n')
  ws_write.write(e, 0, cat)
  ws_write.write(e, 1, title)
  ws_write.write(e, 2, code)
  ws_write.write(e, 3, normal_price)
  ws_write.write(e, 4, offer_price)
  ws_write.write(e, 29, full_url)
  # ws_write.write(0, 6, "Ευκρίνεια οθόνης")
  # ws_write.write(0, 7, "Τύπος οθόνης")
  # ws_write.write(0, 8, "Οθόνη Αφής")
  # ws_write.write(0, 9, "Επεξεργαστής")
  # ws_write.write(0, 11, "Μνήμη RAM")
  # ws_write.write(0, 12, "Τύπος δίσκου")
  # ws_write.write(0, 13, "Χωρητικότητα")
  # ws_write.write(0, 14, "Κάρτα γραφικών")
  # ws_write.write(0, 15, "Μνήμη κάρτας γραφικών")
  # ws_write.write(0, 16, "Λειτουργικό Σύστημα")
  # ws_write.write(0, 17, "Οπτική Μονάδα Δίσκου")
  # ws_write.write(0, 18, "Κάμερα")
  # ws_write.write(0, 19, "Συνδεσιμότητα")
  # ws_write.write(0, 20, "Θύρες")
  # ws_write.write(0, 21, "Μπαταρία")
  # ws_write.write(0, 22, "Χρώμα")
  # ws_write.write(0, 23, "URL")
  e += 1
  if e == 6 :
   write_it_down(write_file, alt_write_file)
   # wb_write.save(write_file)
   # sys.exit(0)

# print(write_file + "saved on " + write_path)
# try :
 # wb_write.save(write_file)
# except :
 # wb_write.save(alt_write_file)

write_it_down(write_file, alt_write_file)
