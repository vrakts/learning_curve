# Current Version 0.1 beta #
############################
# Given a specific Category URL from Singular
# it starts analyzing all products per category page
# and compare it to the 1st find from CY site
# ToDo: Add color maybe
# ToDo: Give all CY Site results in case more than 1 are found
# ToDo: add the Singular URL in the excel
# ToDo: Ask for the Singular URL
# ToDo: Read the results file and skip the product
#		if the code is already found.
# ToDo: Check on GR if CY results come empty.
# ToDo: First check with the SKU and then with product name
# ToDo: Better search
#		Filter title until 1st "/"
#		Compare Brands if possible

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
from urllib.request import Request
import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import re  # for regex
import sys  # for exit purposes in case of error

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)
print("")

def set_paths() :
 global work_path
 if os.path.exists(r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY') == True :  # does work folder exist?
  work_path = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY')
  print("Using " + work_path + " for files.")
  print("")
 elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
  work_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
  print("Using home path 1 for files.")
  print("")
 elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 2 exist?
  work_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
  print("Using home path 2 for files.")
  print("")
 else :
  sys.exit("No folders or files found. Where am I?")
 os.chdir(work_path)

def create_file(start_date) :
 global write_file, alt_write_file, wb_write, ws_write
 # for writing
 write_file = 'com_Auto_Singular.xls'  # path to xslx write file
 alt_write_file = 'com_Auto_Singular_alt.xls'   # alternate name of xls write file
 wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
 ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok = True)  # add 1st sheet in virtual workbook
 ws_write.write(0, 0, "SI_TITLE")				# write CY CODE on A1 cell
 ws_write.write(0, 1, "SI_SKU")				# write RESULT on B1 cell
 ws_write.write(0, 2, "SI_PCODE")			# write CY TITLE on C1 cell
 ws_write.write(0, 3, "SI_EAN")				# write RESULT on D1 cell
 ws_write.write(0, 4, "SI_BRAND")			# write CY PRICE on E1 cell
 ws_write.write(0, 5, "SI_PRICE")	 			# write RESULT on F1 cell
 ws_write.write(0, 6, "SI_AVAIL")				# write CY CAT on G1 cell
 ws_write.write(0, 7, "CY_CODE")				# write RESULT on H1 cell
 ws_write.write(0, 8, "CY_URL")			# write CY SUBCAT on I1 cell
 ws_write.write(0, 9, "CY_TITLE")			# write CY SUBCAT on I1 cell
 ws_write.write(0, 10, "CY_PRICE")				# write RESULT on J1 cell
 ws_write.write(0, 11, "CY_AVAIL")			# write CY BRAND on K1 cell

def get_cy_details(cy_page_soup) :
 global cy_code, cy_title, cy_price_dif, cy_price_text, cy_cat, cy_subcat, cy_brand, cy_avail_text, price_dif, pd
 gr_price_dif = '0'
 # pd = 0
 # print("Just initialized pd.")
 # if cy_page_soup.text == 0 or cy_page_soup.find('Δεν βρέθηκαν προϊόντα σχετικά με ') >= 0 :
 if cy_page_soup.find('p', {'style' : 'text-align:center;font-family:tahoma;font-size:14px;color:#808080;'}) != None :
  cy_code = cy_title = cy_price_text = cy_avail_text = "-"
 else :
  cy_code = cy_page_soup.find('td', {'style' : 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text.strip()
  cy_title = cy_page_soup.h1.text.strip()
  cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
  if len(cy_price) == 0 :
   cy_price_text = "Εξαντλημένο"
   cy_price_dif = "-"
  else :
   cy_price_dif = cy_price[0].text.replace("\xa0€", "")
   # print(cy_price_dif)
   cy_price_text = cy_price_dif.replace(".", ",")
  if len(cy_title) == 0 :
   cy_price_text = "Θέλει άνοιγμα"
   cy_cat = ""
   cy_subcat = ""
   cy_brand = ""
  else :
   cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
   if cy_categories[1].text.find(' •') > 0 :
    cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
    cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
    if len(cy_categories) > 2 :
     cy_subcat = cy_categories[3].text.strip()
    else :
     cy_subcat = ""
   else :
    cy_cat = cy_categories[1].text.strip() 
    if len(cy_categories) > 2 :
     cy_subcat = cy_categories[3].text.strip()
    else :
     cy_subcat = ""
    cy_brand = "-"
  if cy_page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:normal;"}) == None :
   cy_avail_text = "Εξαντλημένο"
  else :
   cy_a = cy_page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:normal;"})
   if cy_a.text.find('Κατόπιν') <= 16 :
    cy_avail_text = cy_a.text[cy_a.text.find(":") + 1:]
   else :
    # cy_avail_text = cy_a.text[cy_a.text.find(":") + 1:cy_a.text.find("Κατάστημα")].strip()
    # cy_avail_text = cy_a.text[cy_a.text.find("Διανομή"):cy_a.text.find("Κατάστημα")].strip()
    cy_avail_text = "Άμεσα διαθέσιμο"
  try :
   price_dif = round(float(cy_price_text.replace(',', '.')) - float(si_price.replace(',', '.')),2)
   # print("Price Difference: " + str(price_dif) + ".")
   # print("Changing pd to 1.")
   # pd = 1
  except :
   print("No price detected on either SI or CY")
   price_dif = "-"

def write_results(e) :
 # print("e in: " + str(e))
 ws_write.write(e, 0, si_title)
 ws_write.write(e, 1, si_sku)
 ws_write.write(e, 2, si_pcode)
 ws_write.write(e, 3, si_ean)
 ws_write.write(e, 4, si_brand)
 ws_write.write(e, 5, si_price)
 ws_write.write(e, 6, si_avail)
 ws_write.write(e, 7, cy_code)
 ws_write.write(e, 8, cy_page_url)
 ws_write.write(e, 9, cy_title)
 ws_write.write(e, 10, cy_price_text)
 ws_write.write(e, 11, cy_avail_text)

def write_it_down() :
 try :
  wb_write.save(write_file)
  print("")
  print(write_file + " created on " + work_path)
 except :
  print("")
  wb_write.save(alt_write_file)
  print(alt_write_file + " created on " + work_path)

# Setting paths
set_paths()

# create the virtual file
create_file(start_date)

# set the variables
e = 1
attempt = 0  # how many attempts to re-read the url in case of failure
sorry = 0  # will add up in case of exceptions
go_on = "OK"
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

si_url = 'https://www.singular.com.cy/monitors/pc-monitors/'
# si_url = 'https://www.singular.com.cy/monitors/pc-monitors/page-40/'

# Load the Singular pafe
req = Request(si_url, headers = headers)
attempt = 0
while attempt < 3 :
 try :
  # print("On try: " + str(attempt))
  uClient = uReq(req)
  page_soup = soup(uClient.read(), "html5lib")
  uClient.close()
  # get_gr_details(page_soup)
  # get_gr_description(page_soup, sheet[i, read_column].value.strip(), gr_cat)
  break
 except Exception as exc :
  # print("On exception: " + str(attempt))
  print("Oops, just bumped into the following exception while trying to load the initial Singular page:")
  print(str(exc))
  print("Retrying in 5 seconds.")
  print("")
  attempt += 1
  sorry += 1
  time.sleep(5)
 if attempt == 3 :
  # print("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
  sys.exit("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
  break
if page_soup.find('a', {'class': 'ty-pagination__item ty-pagination__btn ty-pagination__next cm-history cm-ajax ty-pagination__right-arrow'}) != None :
 next_page = page_soup.find('a', {'class': 'ty-pagination__item ty-pagination__btn ty-pagination__next cm-history cm-ajax ty-pagination__right-arrow'})['href']
else :
 next_page = "This is the last one"
# while page_soup.find('a', {'class': 'ty-pagination__item ty-pagination__btn ty-pagination__next cm-history cm-ajax ty-pagination__right-arrow'})['href'].find('page-') >= 0 :
 # next_page = page_soup.find('a', {'class': 'ty-pagination__item ty-pagination__btn ty-pagination__next cm-history cm-ajax ty-pagination__right-arrow'})['href']
while go_on == "OK" :
 containers = page_soup.findAll('div', {'class' : 'ut2-pl__content'})
 for container in containers :
  # print("Title: " + container.div.div.a['title'].strip())
  # if product_info[5].text.strip().find('EAN') >= 0 :
   # step = 3
   # si_ean = product_info[7].text.strip()
  # else :
   # step = 0
   # si_ean = '-'
  # si_title = container.div.div.a.text.strip()
  # si_sku = product_info[1].text.strip()
  # si_pcode = product_info[4].text.strip()
  # # si_ean = product_info[7].text.strip()
  # si_brand = product_info[7 + step].text.strip()
  # si_price = product_info[21 + step].text.strip()
  # si_avail = product_info[24 + step].text.strip()
  product_info = container.findAll('span')
  si_title = container.div.div.a.text.strip()
  si_sku =  product_info[1].text.strip()
  si_ean = "-"
  for i in range (0, len(product_info)) :
   product_info[i].text.strip().replace('\xa0€', '')
   if product_info[i].text.strip().find('Product Code') >=0  :
    si_pcode = product_info[i + 1].text.strip()
   if product_info[i].text.strip().find('EAN') >=0  :
    si_ean = product_info[i + 1].text.strip()
   if product_info[i].text.strip().find('Manufacturer') >=0  :
    si_brand = product_info[i + 1].text.strip()
   if product_info[i].text.strip().find('Vat') >=0  :
    si_price = product_info[i + 1].text.strip()
   if product_info[i].text.strip().find('Out of stock') >=0  :
    si_avail = product_info[i].text.strip()
   elif product_info[i].text.strip().find('Available') >=0 :
    si_avail = product_info[i - 1].text.strip()
  split_title = si_title.split()
  cy_search_term = " ".join(split_title[:3])
  cy_search_term = cy_search_term.replace('/', '').strip().replace(' ', '+')
  cy_page_url = "https://www.eshopcy.com.cy/search?q=" + cy_search_term
  print("Title:        " + si_title)
  print("SKU:          " + si_sku)
  print("Product Code: " + si_pcode)
  print("EAN Code:     " + si_ean)
  print("Brand:        " + si_brand)
  print("Price:        " + si_price)
  print("Availability: " + si_avail)
  # print("Next Page:    " + next_page)
  print("CY Search:    " + cy_search_term)
  print("CY Page:      " + cy_page_url)
  req = Request(cy_page_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    cy_uClient = uReq(req)
    cy_page_soup = soup(cy_uClient.read(), "html5lib")
    cy_uClient.close()
    break
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("")
    print("Oops, just bumped into the following exception while loading the CY page:")
    print(str(exc))
    print("Retrying in 5 seconds.")
    attempt += 1
    sorry += 1
    time.sleep(5)
  if attempt == 3 :
   # print("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
   cy_code = "ERROR"
   cy_title = "ERROR"
   cy_price_text = "ERROR"
   cy_avail_text = "ERROR"
   write_results(e)
   write_it_down()
   print("")
   sys.exit("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
  # print("Current CY soup is: " + cy_page_soup)
  multi_results = cy_page_soup.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})  # find all next page buttons assuming this is a category based single query page
  if len(multi_results) != 0 :
   cy_page_url = multi_results[1].a['href']
   req = Request(cy_page_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     cy_uClient = uReq(req)
     cy_page_soup = soup(cy_uClient.read(), "html5lib")
     cy_uClient.close()
     break
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("")
     print("Oops, just bumped into the following exception while trying to load the CY page:")
     print(str(exc))
     print("Retrying in 5 seconds.")
     attempt += 1
     sorry += 1
     time.sleep(5)
   if attempt == 3 :
    print("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
    cy_code = "ERROR"
    cy_title = "ERROR"
    cy_price_text = "ERROR"
    cy_avail_text = "ERROR"
    write_results(e)
    write_it_down()
    print("")
    sys.exit("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
  get_cy_details(cy_page_soup)
  # cy_url = cy_page_url
  print("CY Code:      " + cy_code)
  print("CY Title:     " + cy_title)
  print("CY Price:     " + cy_price_text)
  print("CY Avail:     " + cy_avail_text)
  print("")
  write_results(e)
  e += 1
 # if page_soup.findAll('a', {'data-ca-scroll': '.cm-pagination-container'})[2]['href'].find('page-') >= 0 :
  # si_url = page_soup.findAll('a', {'data-ca-scroll': '.cm-pagination-container'})[2]['href']
 # else :
  # si_url = page_soup.findAll('a', {'data-ca-scroll': '.cm-pagination-container'})[1]['href']
 if page_soup.find('a', {'class': 'ty-pagination__item ty-pagination__btn ty-pagination__next cm-history cm-ajax ty-pagination__right-arrow'}) != None :
  next_page = page_soup.find('a', {'class': 'ty-pagination__item ty-pagination__btn ty-pagination__next cm-history cm-ajax ty-pagination__right-arrow'})['href']
  si_url = next_page
  req = Request(si_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    uClient = uReq(req)
    page_soup = soup(uClient.read(), "html5lib")
    uClient.close()
    # get_gr_details(page_soup)
    # get_gr_description(page_soup, sheet[i, read_column].value.strip(), gr_cat)
    break
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("Oops, just bumped into the following exception while loading Singular's next page:")
    print(str(exc))
    print("Retrying in 5 seconds.")
    print("")
    attempt += 1
    sorry += 1
    time.sleep(5)
   if attempt == 3 :
    # print("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
    write_it_down()
    sys.exit("Sorry to inform you but we encountered an error 3 times on this run. " + str(sorry) + " exceptions caught in total. Probably the site is down or having network problems. Try again later.")
 else :
  go_on = "Last One"

write_it_down()