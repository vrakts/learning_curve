# προσωρινό script για να τραβήξει τον τίτλο και κατηγορία για το κάθε προϊόν.

try :
 from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
 from random import randint
 from time import sleep as nani
 from datetime import datetime
 from urllib.request import quote  # enables encoding greek characters in url
 from urllib.parse import unquote  # enables decoding of greek characters
 import requests, os, sys, re, ezodf, xlwt
except KeyboardInterrupt :
 import sys
 sys.exit(0)
except Exception as exc :
 import sys
 print("Κάτι πάθαμε κατά το import.")
 print(str(exc))
 sys.exit(0)

def load_soup(page, wait, retries) :
 # print("Μέσα στη σούπα.")
 attempt = 0
 print("Φορτώνω σούπα: " + page)
 while attempt < retries :
  try :
   result = requests.get(page, headers = headers)
   webpage = result.content
   page_soup = soup(webpage, "html5lib")
   break   
   # print("Έξω από τη σούπα.")
   # print("")
  except Exception as exc :
   print("")
   print("Στο φόρτωμα της σελίδας, πέσαμε πάνω στο:")
   print(str(exc))
   print("Ξαναπροσπαθώ σε " + str(retries)+ ".")
   nani(wait)
   attempt += 1
 if attempt == retries :
  print("Προσπάθησα " + str(attempt) + " φορές και δεν τα κατάφερα.")
  input()
  sys.exit(0)
 
 return(page_soup)

def get_gr_details(page_soup) :
 global gr_prod_per, gr_prod_title, gr_price_dif, gr_price_text, gr_a_text, gr_cat, gr_subcat, gr_brand, sxetika_list
 gr_price_dif = '0'
 # pd = 0
 gr_prod_per = page_soup.find('td', {'style' : 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text.strip()
 gr_prod_title = page_soup.h1.text
 gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(gr_price) == 0 :
  gr_price_text = "Εξαντλημένο"
  gr_price_dif = "-"
 else : 
  gr_price_dif = gr_price[0].text.replace("\xa0€", "")
  # print(gr_price_dif)
  gr_price_text = gr_price_dif.replace(".", ",")
 if page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"}) == None :
  gr_a_text = "Εξαντλημένο"
 else :
  gr_a = page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
  if gr_a.text.find('Κατόπιν') <= 16 :
   gr_a_text = gr_a.text[gr_a.text.find(":") + 2:]
  else :
   gr_a_text = gr_a.text[gr_a.text.find(":") + 2:gr_a.text.find("\n")].strip()
 gr_categories = page_soup.findAll('td', {'class': 'faint1'})
 if len(gr_categories) == 0 :
  gr_cat = "-"
  gr_brand = "-"
  gr_subcat = ""
 elif gr_categories[1].text.find(' •') > 0 :
  gr_cat = gr_categories[1].text[:gr_categories[1].text.find(' •')]
  gr_brand = gr_categories[1].text[gr_categories[1].text.find(' •')+2:gr_categories[1].text.find('στην')].strip()
  if len(gr_categories) > 2 :
   gr_subcat = gr_categories[3].text.strip()
  else :
   gr_subcat = ""
 else :
  gr_cat = gr_categories[1].text.strip()
  if len(gr_categories) > 2 :
   gr_subcat = gr_categories[3].text.strip()
  else :
   gr_subcat = ""
  gr_brand = "-"
 if len(page_soup.findAll('div', {'class': 'also_box'})) > 0 :
  gr_sxetika = page_soup.findAll('div', {'class': 'also_box'})
  sxetika_list = ""
  for sxetika in gr_sxetika :
   sxetika_per_link = sxetika.a['href']
   sxetika_per = sxetika_per_link[sxetika_per_link.rfind('-')+1:]
   if len(sxetika_list) == 0 :
    sxetika_list = sxetika_per
   else :
    sxetika_list = sxetika_list + "," + sxetika_per
 else :
  sxetika_list = ""

def write_results(e) :
 # print("e in: " + str(e))
 ws_write.write(e, 0, gr_prod_per) 		# OK
 ws_write.write(e, 1, gr_prod_title)	# OK
 ws_write.write(e, 2, gr_cat)			# OK
 ws_write.write(e, 3, gr_subcat)		# OK
 ws_write.write(e, 4, gr_brand)			# OK

def write_it_down() :
 wb_write.save(write_file)
 print("")
 print("Το αρχείο: " + write_file + " δημιουργήθηκε στο " + write_path)

try :
 write_path = (r"Z:\OneDrive\HTML Parser\Python")
 os.chdir(write_path)
 ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
 spreadsheet = ezodf.opendoc("Αλλαγή τιμών.ods")  # open file
 ezodf.config.reset_table_expand_strategy()  # reset ezodf config
 sheets = spreadsheet.sheets
 for i in range(0, len(sheets)) :
  print(str(i) + ": " + sheets[i].name)
 answer = input("Διάλεξε: ")
 sheet = sheets[int(answer)]
 # sheet = sheets[4]
 print("Sheet name: " + sheet.name)
 rowcount = sheet.nrows()  
 colcount = sheet.ncols()
 ac_row = 1
 for i in range(1, rowcount):
  if str(sheet[i, 0].value) != "None" :
   ac_row += 1
  else :
   break
 
 write_file = sheet.name + "_sort.xls"
 print("")
 print("Write File: " + write_file)
 print("")
 wb_write = xlwt.Workbook()
 ws_write = wb_write.add_sheet(sheet.name, cell_overwrite_ok = True)
 ws_write.write(0, 0, "CODE")		# write CODE on A1 cell
 ws_write.write(0, 1, "TITLE")		# write TITLE on B1 cell
 ws_write.write(0, 2, "GR-CAT")		# write GR-CAT on E1 cell
 ws_write.write(0, 3, "GR-SUBCAT")	# write GR-SUBCAT on F1 cell
 ws_write.write(0, 4, "GR-BRAND")	# write GR-BRAND on G1 cell

 offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
 e = 1  # represents the row inside the excel file.
 attempt = 0
 retries = 10
 wait = 3
 headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
 
 for i in range(1, ac_row):
 # for i in range(1, 10):
  if str(sheet[i, 0].value) == "None" :
   break
  else :
   page_url = "https://www.e-shop.gr/product?id=" + sheet[i, 0].value.strip()
   page_soup = load_soup(page_url, wait, retries)
   get_gr_details(page_soup)
   print(gr_prod_per + " - " + gr_prod_title)
   print(gr_cat + " - " + gr_subcat + " - " + gr_brand)
   print("")
   write_results(e)
   e += 1
 write_it_down()
except KeyboardInterrupt :
 try :
  # print("")
  input("Διαλλειματάκι;")
  print("")
 except :
  sys.exit(0)
except Exception as exc:
 print("Εξαίρεση: " + str(exc))
finally :
 print("Τέλος εξαίρεσης.")
 sys.exit(0)