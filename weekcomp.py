def ti_paizei() :
 # weekcomp.py
 ############################
 # Current Version 1.0.1 beta
 ############################
 # Κοιτάει συγκεκριμένες κατηγορίες στους ανταγωνιστές για το φθηνότερο προϊόν
 # Singular filters:?features_hash=
 # - 15.6'' = 7-56893
 # - 17.3'' = 7-56894
 # - i5 = 23-7990
 # - i7 = 23-7989
 # - i9 = 23-56972
 # - i5+i7+i9 = 23-7990-7989-56972
 # - 15.6''+17.3'' + i5+i7+i9 = 7-56893-56894_23-7990-7989-56972
 print("Τρέχουσα έκδοση: 1.0.1 beta.")

try :
 from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
 from time import sleep as nani
 from datetime import datetime
 import requests
 from selenium import webdriver
 from selenium.webdriver import ChromeOptions
 from selenium.webdriver.common.keys import Keys
 from selenium.webdriver.chrome.options import Options  
 import xlwt
 import ezodf
 import re
 import os
 import sys
except KeyboardInterrupt :
 import sys
 sys.exit(0)
except Exception as exc :
 import sys
 print("Κάτι πάθαμε κατά το import.")
 print(str(exc))
 sys.exit(0)

def get_start_time() :
 global start_time, start_date
 start = datetime.now()
 start_date = start.strftime("%d-%m-%Y")
 start_time = start.strftime("%H:%M:%S")
 print("Εκκίνηση: " + start_date)
 print("")

def load_soup(page) :
 # print("Μέσα στη σούπα.")
 wait = 3
 retries = 3
 headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
 attempt = 0
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

def set_files() :
 global ws_write, wb_write, write_path, write_file, alt_write_file
 if os.path.exists(r"Z:\OneDrive\eShop Stuff\PRODUCT\Product") == True :
  write_path = (r"Z:\OneDrive\eShop Stuff\PRODUCT\Product")
 elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"Y:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"Y:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 else :
  write_path = (r"C:\TEMPYTH")
 
 write_file = ("weekcomp.xls")  # name of xls write file
 alt_write_file = ("weekcomp_alt.xls")  # alternate name of xls write file
 
 wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
 ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok = True)  # add sheet in virtual workbook named after the search string ad run date
 ws_write.write(0, 0, "CATEGORY")
 ws_write.write(0, 1, "CY-PRICE")
 ws_write.write(0, 2, "CY-LINK")
 ws_write.write(0, 3, "ST-PRICE")
 ws_write.write(0, 4, "ST-LINK")
 ws_write.write(0, 5, "PUB-PRICE")
 ws_write.write(0, 6, "PUB-LINK")
 ws_write.write(0, 7, "SIN-PRICE")
 ws_write.write(0, 8, "SIN-LINK")
 ws_write.write(0, 9, "EL-PRICE")
 ws_write.write(0, 10, "EL-LINK")
 ws_write.write(0, 11, "BIO-PRICE")
 ws_write.write(0, 12, "BIO-LINK")
 ws_write.write(0, 13, "KOT-PRICE")
 ws_write.write(0, 14, "KOT-LINK")
 ws_write.write(0, 15, "CY_WINS")

def write_results(e) :
 # print("e in: " + str(e))
 """ THINK IT THROUGH """
 ws_write.write(e, 0, categories[i])
 ws_write.write(e, 1, cy_price)
 ws_write.write(e, 2, cy_url)
 ws_write.write(e, 3, st_price)
 ws_write.write(e, 4, st_url)
 ws_write.write(e, 5, pub_price)
 ws_write.write(e, 6, pub_url)
 ws_write.write(e, 7, sin_price)
 ws_write.write(e, 8, sin_url)
 ws_write.write(e, 9, el_price)
 ws_write.write(e, 10, el_url)
 ws_write.write(e, 11, bio_price)
 ws_write.write(e, 12, bio_url)
 ws_write.write(e, 13, kot_price)
 ws_write.write(e, 14, kot_url)
 ws_write.write(e, 15, winner)

def write_it_down(write_file) :
 if os.path.exists(r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"Y:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"Y:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 else :
  write_path = (r"C:\TEMPYTH")
 print("Τρέχων φάκελος: " + os.getcwd())
 os.chdir(write_path)
 print("Χρησιμοποιώ το " + os.getcwd())
 # wb_write.save(write_file)
 try :
  wb_write.save(write_file)
 except Exception as exc :
  print(str(exc))
  write_file = alt_write_file
  wb_write.save(write_file)
 print("")
 print("Το αρχείο: " + write_file + " δημιουργήθηκε στο " + os.getcwd())

def set_categories() :
 """
 ΤΗΛΕΟΡΑΣΗ 32" (HD READY)
 ΤΗΛΕΟΡΑΣΗ 32" (FULL HD)
 ΤΗΛΕΟΡΑΣΗ 40"- 43"
 ΤΗΛΕΟΡΑΣΗ 49"- 50"
 ΤΗΛΕΟΡΑΣΗ 55"
 ΤΗΛΕΟΡΑΣΗ 65"
 ΤΗΛΕΟΡΑΣΗ ULTRA HD
 LAPTOP 15,6" (LOW BUDGET) + WINDOWS
 LAPTOP 15,6" (i3 CPU) + WINDOWS
 LAPTOP 15,6" (i5 CPU) + WINDOWS
 LAPTOP 15,6" (i7 CPU) + WINDOWS
 TABLET (LOW BUDGET)
 TABLET 10"
 ΕΞΩΤΕΡΙΚΟΣ ΣΚΛΗΡΟΣ ΔΙΣΚΟΣ 2.5" 500GB
 ΕΞΩΤΕΡΙΚΟΣ ΣΚΛΗΡΟΣ ΔΙΣΚΟΣ 2.5" 1TB
 ΕΞΩΤΕΡΙΚΟΣ ΣΚΛΗΡΟΣ ΔΙΣΚΟΣ 2.5" 2TB
 ΠΟΛΥΜΗΧΑΝΗΜΑ (LOW BUDGET)
 """
 categories = []
 cy_links = []
 st_links = []
 pub_links = []
 kot_links = []
 sin_links = []
 el_links = []
 bio_links = []
 # # include lists
 cy_include = ["LED HD", "", "", ""]
 st_include = ['32"', '32"', "", "49:50"]
 pub_include = ['32"', '32"', ""]
 kot_include = ["", "", ""]
 sin_include = ["", "", ""]
 el_include = ["", "", ""]
 bio_include = ["", "", ""]
 
 categories.append('ΤΗΛΕΟΡΑΣΗ 32" (HD READY)')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D4%C7%CB%C5%CF%D1%C1%D3%C7&filter-86=1&filter-916=1')
 st_links.append('https://www.stephanis.com.cy/el/products/sound-and-vision/television-and-accessories/television?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_852=2793&SF_857=2835#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tileoraseis/tileoraseis/?N=146120889+3609381576+666718199&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Ftileoraseis%2Ftileoraseis%2F')
 kot_links.append('https://www.kotsovolos.cy/kotsovoloscyprus/sound-vision/televisions/led-lcd/filters/f/f11004/HD-Ready/f11006/32inch?orderBy=3')
 sin_links.append('')
 el_links.append('https://www.electroline.com.cy/product-category/sound-vision/tvs115/tv-s-11501/?filter1=resolution&filter1value3=hd&filter0=display-size&filter0value3=32')
 bio_links.append("https://bionic.com.cy/products/c/tvs/f/hd-ready++32--/definition+screen-size")
 
 categories.append('ΤΗΛΕΟΡΑΣΗ 32" (FULL HD)')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D4%C7%CB%C5%CF%D1%C1%D3%C7&filter-86=1&filter-917=1')
 st_links.append('https://www.stephanis.com.cy/el/products/sound-and-vision/television-and-accessories/television?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_852=2793&SF_857=2838#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tileoraseis/tileoraseis/?N=146120889+3609381576+1176384630&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Ftileoraseis%2Ftileoraseis%2F')
 kot_links.append('https://www.kotsovolos.cy/kotsovoloscyprus/sound-vision/televisions/led-lcd/filters/f/f11004/Full-HD/f11006/32inch?orderBy=3')
 sin_links.append('')
 el_links.append('https://www.electroline.com.cy/product-category/sound-vision/tvs115/tv-s-11501/?filter1=resolution&filter1value2=full-hd&filter0=display-size&filter0value3=32&filter100=brand%27')
 bio_links.append("https://bionic.com.cy/products/c/tvs/f/full-hd++32--/definition+screen-size")
 
 categories.append('ΤΗΛΕΟΡΑΣΗ 40"- 43"')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D4%C7%CB%C5%CF%D1%C1%D3%C7&filter-88=1&filter-11598=1')
 st_links.append('https://www.stephanis.com.cy/el/products/sound-and-vision/television-and-accessories/television?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_852=2794#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tileoraseis/tileoraseis/?N=146120889+1820408144&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Ftileoraseis%2Ftileoraseis%2F')
 kot_links.append('https://www.kotsovolos.cy/sound-vision/televisions/led-lcd/filters/f/f11006/40inch_or_42inch_or_43inches?orderBy=3')
 sin_links.append('')
 el_links.append('https://www.electroline.com.cy/product-category/sound-vision/tvs115/tv-s-11501/?filter0=display-size&filter0value4=39-43')
 bio_links.append("https://bionic.com.cy/products/c/tvs/f/43--/screen-size")
 
 categories.append('ΤΗΛΕΟΡΑΣΗ 49"- 50"')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D4%C7%CB%C5%CF%D1%C1%D3%C7&filter-9742=1&filter-92=1')
 st_links.append('https://www.stephanis.com.cy/el/products/sound-and-vision/television-and-accessories/television?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_852=2794&SF_852=2795#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tileoraseis/tileoraseis/?N=146120889+2537109762&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Ftileoraseis%2Ftileoraseis%2F')
 kot_links.append('https://www.kotsovolos.cy/sound-vision/televisions/led-lcd/filters/f/f11360/48_50-%CE%AF%CE%BD%CF%84%CF%83%CE%B5%CF%82?orderBy=3')
 sin_links.append('')
 el_links.append('https://www.electroline.com.cy/product-category/sound-vision/tvs115/tv-s-11501/?filter0=display-size&filter0value5=47-55')  # filter 49-50''
 bio_links.append("https://bionic.com.cy/products/c/tvs/f/50--/screen-size")
 
 categories.append('ΤΗΛΕΟΡΑΣΗ 55"')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D4%C7%CB%C5%CF%D1%C1%D3%C7&filter-94=1')
 st_links.append('https://www.stephanis.com.cy/el/products/sound-and-vision/television-and-accessories/television?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_852=2795#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tileoraseis/tileoraseis/?N=146120889+1213905562&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Ftileoraseis%2Ftileoraseis%2F')
 kot_links.append('https://www.kotsovolos.cy/sound-vision/televisions/led-lcd/filters/f/f11360/55_58-%CE%AF%CE%BD%CF%84%CF%83%CE%B5%CF%82?orderBy=3')
 sin_links.append('')
 el_links.append('https://www.electroline.com.cy/product-category/sound-vision/tvs115/tv-s-11501/?filter0=display-size&filter0value5=47-55')  # filter 55''
 bio_links.append("https://bionic.com.cy/products/c/tvs/f/55--/screen-size")
 
 categories.append('ΤΗΛΕΟΡΑΣΗ 65"')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D4%C7%CB%C5%CF%D1%C1%D3%C7&filter-9739=1')
 st_links.append('https://www.stephanis.com.cy/el/products/sound-and-vision/television-and-accessories/television?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_852=2796#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tileoraseis/tileoraseis/?N=146120889+157187437&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Ftileoraseis%2Ftileoraseis%2F')
 kot_links.append('https://www.kotsovolos.cy/sound-vision/televisions/led-lcd/filters/f/f11360/60_65-%CE%AF%CE%BD%CF%84%CF%83%CE%B5%CF%82?orderBy=3')
 sin_links.append('')
 el_links.append('https://www.electroline.com.cy/product-category/sound-vision/tvs115/tv-s-11501/?filter0=display-size&filter0value6=60-98')  # filter 60''
 bio_links.append("https://bionic.com.cy/products/c/tvs/f/65--/screen-size")
 
 categories.append('ΤΗΛΕΟΡΑΣΗ ULTRA HD')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D4%C7%CB%C5%CF%D1%C1%D3%C7&filter-9747=1')
 st_links.append('https://www.stephanis.com.cy/el/products/sound-and-vision/television-and-accessories/television?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_857=2836#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tileoraseis/tileoraseis/?N=146120889+2726789980&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Ftileoraseis%2Ftileoraseis%2F')
 kot_links.append('https://www.kotsovolos.cy/sound-vision/televisions/led-lcd/filters/f/f11360/60_65-%CE%AF%CE%BD%CF%84%CF%83%CE%B5%CF%82?orderBy=3')
 sin_links.append('')
 el_links.append('https://www.electroline.com.cy/product-category/sound-vision/tvs115/tv-s-11501/?filter1=resolution&filter1value6=ultra-hd&filter0=display-size')
 bio_links.append("https://bionic.com.cy/products/c/tvs/f/4k-ultra-hd/definition")
 
 categories.append('LAPTOP 15,6” (LOW BUDGET) + WINDOWS')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D6%CF%D1%C7%D4%CF%C9+%D5%D0%CF%CB%CF%C3%C9%D3%D4%C5%D3&filter-140=1&filter-11606=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/laptops-and-accessories/laptops?view=thumbnails&recordsPerPage=12&sortBy=price-asc')
 pub_links.append('https://www.public-cyprus.com.cy/cat/computers-and-software/laptops/?=undefined&N=3358872248+4131216112&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Fcomputers-and-software%2Flaptops%2F')
 kot_links.append('https://www.kotsovolos.cy/kotsovoloscyprus/computing/laptop-tablet-ipad/notebook-macbook-ultrabook?orderBy=3')
 sin_links.append('https://www.singular.com.cy/laptops/laptops-notebooks/?features_hash=7-56893')
 el_links.append('https://www.electroline.com.cy/product-category/computing/computers130/laptops13005/?filter4=operating-system&filter4value2=windows-10&filter0=display-size&filter0value4=15-15-6')
 bio_links.append('https://bionic.com.cy/products/c/notebooks/f/15-6--/screen-size')
 
 categories.append('LAPTOP 15,6” (i3 CPU) + WINDOWS')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D6%CF%D1%C7%D4%CF%C9+%D5%D0%CF%CB%CF%C3%C9%D3%D4%C5%D3&filter-140=1&filter-11606=1&filter-505=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/laptops-and-accessories/laptops?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_871=2960#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/computers-and-software/laptops/?=undefined&N=3358872248+4131216112+1389225763&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Fcomputers-and-software%2Flaptops%2F')
 kot_links.append('https://www.kotsovolos.cy/kotsovoloscyprus/computing/laptop-tablet-ipad/notebook-macbook-ultrabook?orderBy=3&pageSize=60')  # filter i3s
 sin_links.append('')  # no i3 filter
 el_links.append('https://www.electroline.com.cy/product-category/computing/computers130/laptops13005/?filter1=processor&filter1value14=intel-core-i3&filter4=operating-system&filter4value2=windows-10&filter0=display-size&filter0value4=15-15-6')
 bio_links.append("https://bionic.com.cy/products/c/notebooks/f/15-6--++intel-core-i3/screen-size+cpu-family")
 
 categories.append('LAPTOP 15,6” (i5 CPU) + WINDOWS')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D6%CF%D1%C7%D4%CF%C9+%D5%D0%CF%CB%CF%C3%C9%D3%D4%C5%D3&filter-140=1&filter-11606=1&filter-506=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/laptops-and-accessories/laptops?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_871=2958#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/computers-and-software/laptops/?=undefined&N=3358872248+4131216112+1331599528&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Fcomputers-and-software%2Flaptops%2F')
 kot_links.append('https://www.kotsovolos.cy/kotsovoloscyprus/computing/laptop-tablet-ipad/notebook-macbook-ultrabook?orderBy=3&pageSize=60')  # filter i5s
 sin_links.append('https://www.singular.com.cy/laptops/laptops-notebooks/?features_hash=7-56893_23-7990')
 el_links.append('https://www.electroline.com.cy/product-category/computing/computers130/laptops13005/?filter1=processor&filter1value15=intel-core-i5&filter4=operating-system&filter4value2=windows-10&filter0=display-size&filter0value4=15-15-6')
 bio_links.append("https://bionic.com.cy/products/c/notebooks/f/15-6--++intel-core-i5/screen-size+cpu-family")
 
 categories.append('LAPTOP 15,6” (i7 CPU) + WINDOWS')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%D6%CF%D1%C7%D4%CF%C9+%D5%D0%CF%CB%CF%C3%C9%D3%D4%C5%D3&filter-140=1&filter-11606=1&filter-507=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/laptops-and-accessories/laptops?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_871=2964#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/computers-and-software/laptops/?=undefined&N=3358872248+4131216112+1104529468&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Fcomputers-and-software%2Flaptops%2F')
 kot_links.append('https://www.kotsovolos.cy/kotsovoloscyprus/computing/laptop-tablet-ipad/notebook-macbook-ultrabook?orderBy=3&pageSize=60')  # filter i7s
 sin_links.append('https://www.singular.com.cy/laptops/laptops-notebooks/?features_hash=7-56893_23-7989')
 el_links.append('https://www.electroline.com.cy/product-category/computing/computers130/laptops13005/?filter1=processor&filter1value16=intel-core-i7&filter4=operating-system&filter4value2=windows-10&filter0=display-size&filter0value4=15-15-6')
 bio_links.append("https://bionic.com.cy/products/c/notebooks/f/15-6--++intel-core-i7/screen-size+cpu-family")
 
 categories.append('TABLET (LOW BUDGET)')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=TABLETS&filter-8317=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/tablets-and-ereaders/tablets?view=thumbnails&recordsPerPage=12&sortBy=price-asc')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tablets/syskeyes-tablet/?_dyncharset=UTF-8&=undefined&Ns=sku.cyprusActualPrice|0 ')
 kot_links.append('https://www.kotsovolos.cy/kotsovoloscyprus/computing/laptop-tablet-ipad/tablets-ipad?orderBy=3')
 sin_links.append('https://www.singular.com.cy/laptops/tablets-ipad/ ')  # exclude fireOS
 el_links.append('https://www.electroline.com.cy/product-category/computing/tablets130/tablets13014/')
 bio_links.append("https://bionic.com.cy/products/c/tablets")
 
 categories.append('TABLET 10"')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=TABLETS&filter-6807=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/tablets-and-ereaders/tablets?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_852=3491#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/tablets/syskeyes-tablet/?=undefined&N=2689123182+1807066425&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Ftablets%2Fsyskeyes-tablet%2F')
 kot_links.append('https://www.kotsovolos.cy/computing/laptop-tablet-ipad/tablets-ipad/filters/f/f11001/10inches_11inches?orderBy=3')
 sin_links.append('https://www.singular.com.cy/laptops/tablets-ipad/ ')  # exclude fireOS include 10 - 10.1''
 el_links.append('https://www.electroline.com.cy/product-category/computing/tablets130/tablets13014/?filter0=display-size&filter0value3=9-0-10-9')  # include only 10-10,9
 bio_links.append("https://bionic.com.cy/products/c/tablets/f/10--+10-1--+10-2--+10-3--+10-4--+10-5--/size")
 
 categories.append('ΕΞΩΤΕΡΙΚΟΣ ΣΚΛΗΡΟΣ ΔΙΣΚΟΣ 2.5" 500GB')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%C5%CE%D9%D4%C5%D1%C9%CA%CF%C9+%C4%C9%D3%CA%CF%C9&filter-7113=1&filter-7118=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/storage/external-hard-disks-hdd?view=thumbnails&recordsPerPage=12&sortBy=price-asc')  # search for 500GB
 pub_links.append('https://www.public-cyprus.com.cy/cat/perifereiaka/external-hdd/?=undefined&N=1579089047+586514322&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Fperifereiaka%2Fexternal-hdd%2F')
 kot_links.append('https://www.kotsovolos.cy/computing/storage-hard-disk-drives-and-usb-sticks/external-hdd?orderBy=3')  # filter 500GB
 sin_links.append('https://www.singular.com.cy/hard-drives/external-hard-drives/?features_hash=5-19_21-1861 ')  # exclude solid state drive or include Hard drive
 el_links.append('https://www.electroline.com.cy/product-category/computing/peripherals130/multimedia-external-disk-hdd13015/')  # include only 500gb 2.5''
 bio_links.append("https://bionic.com.cy/products/c/external-hard-disks/f/500gb/capacity")
 
 categories.append('ΕΞΩΤΕΡΙΚΟΣ ΣΚΛΗΡΟΣ ΔΙΣΚΟΣ 2.5" 1TB')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%C5%CE%D9%D4%C5%D1%C9%CA%CF%C9+%C4%C9%D3%CA%CF%C9&filter-7113=1&filter-7120=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/storage/external-hard-disks-hdd?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_866=2924#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/perifereiaka/external-hdd/?=undefined&N=1579089047+4271818516&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Fperifereiaka%2Fexternal-hdd%2F')
 kot_links.append('https://www.kotsovolos.cy/computing/storage-hard-disk-drives-and-usb-sticks/external-hdd/filters/f/f11352/1000?orderBy=3')  # filter 500GB
 sin_links.append('https://www.singular.com.cy/hard-drives/external-hard-drives/?features_hash=5-20_21-1861 ')  # exclude solid state drive or include Hard drive
 el_links.append('https://www.electroline.com.cy/product-category/computing/peripherals130/multimedia-external-disk-hdd13015/')  # include only 1tb 2.5''
 bio_links.append("https://bionic.com.cy/products/c/external-hard-disks/f/1-tb/capacity")
 
 categories.append('ΕΞΩΤΕΡΙΚΟΣ ΣΚΛΗΡΟΣ ΔΙΣΚΟΣ 2.5" 2TB')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&category=%C5%CE%D9%D4%C5%D1%C9%CA%CF%C9+%C4%C9%D3%CA%CF%C9&filter-7113=1&filter-7122=1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/storage/external-hard-disks-hdd?view=thumbnails&recordsPerPage=12&sortBy=price-asc&Quantity=min&PriceMin=&PriceMax=&SF_866=2922#')
 pub_links.append('https://www.public-cyprus.com.cy/cat/perifereiaka/external-hdd/?=undefined&N=1579089047+771515606&Ns=sku.cyprusActualPrice%7C0&_dyncharset=UTF-8&origUrl=%2Fcat%2Fperifereiaka%2Fexternal-hdd%2F')
 kot_links.append('https://www.kotsovolos.cy/computing/storage-hard-disk-drives-and-usb-sticks/external-hdd/filters/f/f11352/2000?orderBy=3')
 sin_links.append('https://www.singular.com.cy/hard-drives/external-hard-drives/?features_hash=5-1649_21-1861 ')  # exclude solid state drive or include Hard drive
 el_links.append('https://www.electroline.com.cy/product-category/computing/peripherals130/multimedia-external-disk-hdd13015/')  # include only 2tb 2.5''
 bio_links.append("https://bionic.com.cy/products/c/external-hard-disks/f/2-tb/capacity")
 
 categories.append('ΠΟΛΥΜΗΧΑΝΗΜΑ (LOW BUDGET)')
 cy_links.append('https://www.e-shop.cy/search_main?table=PER&&category=%D0%CF%CB%D5%CC%C7%D7%C1%CD%C7%CC%C1%D4%C1')
 st_links.append('https://www.stephanis.com.cy/el/products/information-technology/printers-and-consumables/printers-all-in-one?view=thumbnails&recordsPerPage=12&sortBy=price-asc')
 pub_links.append('https://www.public-cyprus.com.cy/cat/perifereiaka/printers/multifuction-inkjet/?_dyncharset=UTF-8&=undefined&Ns=sku.cyprusActualPrice|0 ')
 kot_links.append('https://www.kotsovolos.cy/kotsovoloscyprus/computing/printing-consumables/all-in-one?orderBy=3')
 sin_links.append('https://www.singular.com.cy/printers-scanners/inkjet-all-in-one/ ')
 el_links.append('https://www.electroline.com.cy/product-category/computing/printers130/mfp-inkjet13013/')  # include only 2tb 2.5''
 bio_links.append("https://bionic.com.cy/products/c/printers/f/multifunction/multifunction")
 
 return(categories, cy_links, st_links, pub_links, kot_links, sin_links, el_links, bio_links)

def smallest_price(list) :
 min_count = 0
 min = list[0]
 for a in range(0, len(list)) :
  if isinstance(list[a], float) :
   if list[a] < min :
    min = list[a]
    min_count = a
  else :
   continue
 return min_count

def cy_stuff(links, i) :  # with product/price containers fixed for empty list and urls
 page_url = links[i]
 print("Current CY link: " + page_url)
 if page_url == '' :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  link_soup = load_soup(page_url)
  products_containers = link_soup.findAll('table', {'class' : 'web-product-container'})
 
 if len(products_containers) == 0 :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  pricelist = []
 
 for product in products_containers : 
  display_price = product.find('td', {'class': 'web-product-price'}).text.replace('€', '').strip()
  price = float(display_price.replace(',', ''))
  pricelist.append(price)
 
 min_list = smallest_price(pricelist)
 right_product = False
 
 # while right_product == False:
  # product = products_containers[min_list]
  # if product.h2.text.find("FULL HD") >= 0:
   # min_list += 1
  # else:
   # right_product = True
 
 price = pricelist[min_list]
 title = product.h2.text.strip()
 code = product.font.text.strip()
 url = product.a['href']
 #  title = link_soup.find('table', {'class': 'web-product-container'}).h2.text.strip()
 #  code = link_soup.find('table', {'class': 'web-product-container'}).font.text.strip()
 #  url = link_soup.find('table', {'class': 'web-product-container'}).a['href']
 print('Category: ' + categories[i])
 # print('min list: ' + str(min_list))
 print('title:    ' + title)
 print('code:     ' + code)
 print('url:      ' + url)
 print('price:    ' + str(price))
 print(pricelist)
 return(price, title, code, url)

def st_stuff(links, i) :  # with product/price containers and fixed for empty list and urls
 page_url = links[i]
 print("Current Stephanis link: " + page_url)
 if page_url == '' :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  link_soup = load_soup(page_url)
  products_containers = link_soup.findAll('div', {'class' : 'item-wrapper'})
 
 if len(products_containers) == 0 :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  pricelist = []
 
 for product in products_containers : 
  if product.find('div', {'class': 'listing-details-column large-stephanis-card-price large-single'}) :
   display_price = product.find('div', {'class': 'listing-details-column large-stephanis-card-price large-single'}).div.text.replace('€', '').strip()
  elif product.find('div', {'class': 'listing-details-heading large-now-price with-sale'}) :
   display_price = product.find('div', {'class': 'listing-details-heading large-now-price with-sale'}).text.replace('€', '').strip()
  price = float(display_price.replace(',', ''))
  pricelist.append(price)
 
 min_list = smallest_price(pricelist)
 product = products_containers[min_list]
 price = pricelist[min_list]
 title = product.find('li', {'class': 'spotlight-list-text tile-product-name'}).text.strip()
 code = product.find('div', {'class': 'product-code'}).text.strip()
 url = product.a['href']
 if url.find('https://www.stephanis.com.cy') >= 0 :
  pass
 else :
  url = 'https://www.stephanis.com.cy' + url
 print('Category: ' + categories[i])
 # print('min list: ' + str(min_list))
 print('title:    ' + title)
 print('code:     ' + code)
 print('url:      ' + url)
 print('price:    ' + str(price))
 print(pricelist)
 return(price, title, code, url)

def pub_stuff(links, i) :  # with product/price containers and fixed for empty list and urls
 page_url = links[i]
 print("Current Public link: " + page_url)
 if page_url == '' :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  link_soup = load_soup(page_url)
  products_containers = link_soup.findAll('div', {'class' : 'col-sm-6 col-lg-4'})
 
 if len(products_containers) == 0 :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  pricelist = []
 
 for product in products_containers : 
  display_price = product.find('div', {'class': 'teaser--product-final-price large'})['data-price']
  price = float(display_price.replace('.', '').replace(',', '.'))
  pricelist.append(price)
  """price is wrong, sort out decimals."""
 min_list = smallest_price(pricelist)
 product = products_containers[min_list]
 price = pricelist[min_list]
 title = product.find('a', {'class': 'teaser--product-title product-page-link istile'}).text.strip()
 url = product.find('a', {'class': 'teaser--product-title product-page-link istile'})['href']
 if url.find('https://www.public-cyprus.com.cy') >= 0 :
  pass
 else :
  url = 'https://www.public-cyprus.com.cy' + url
 code = url[url.rfind('/prod') + 5:url.rfind('pp')]
 print('Category: ' + categories[i])
 # print('min list: ' + str(min_list))
 print('title:    ' + title)
 print('code:     ' + code)
 print('url:      ' + url)
 print('price:    ' + str(price))
 print(pricelist)
 return(price, title, code, url)

def sin_stuff(links, i) :  # with product/price containers and fixed for empty list and urls
 page_url = links[i]
 print("Current Singular link: " + page_url)
 if page_url == '' :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  link_soup = load_soup(page_url)
  products_containers = link_soup.findAll('div', {'class' : 'ty-product-list clearfix'})
 
 if len(products_containers) == 0 :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  pricelist = []
 
 for product in products_containers : 
  if product.find('div', {'class' : 'ut2-pl__price pr-row pr-color'}) :
   prices_containers = product.find('div', {'class' : 'ut2-pl__price pr-row pr-color'}).findAll('bdi')
  else :
   prices_containers = product.find('div', {'class' : 'ut2-pl__price pr-row'}).findAll('bdi')
  
  if len(prices_containers) > 3 :
   display_price = prices_containers[2].text.replace('€', '').strip()
  else :
   display_price = prices_containers[1].text.replace('€', '').strip()
  price = float(display_price.replace(',', ''))
  pricelist.append(price)
 # return(pricelist)
 
 min_list = smallest_price(pricelist)
 product = products_containers[min_list]
 price = pricelist[min_list]
 title = product.find('a', {'class' : 'product-title'}).text.strip()
 title[:title.find('|')].strip()
 code = product.find('div', {'class' : 'ty-control-group ty-sku-item cm-hidden-wrapper'}).span.text.strip()
 url = product.find('a', {'class' : 'product-title'})['href']
 print('Category: ' + categories[i])
 # print('min list: ' + str(min_list))
 print('title:    ' + title)
 print('code:     ' + code)
 print('url:      ' + url)
 print('price:    ' + str(price))
 print(pricelist)
 return(price, title, code, url)

def el_stuff(links, i) :  # with product/price containers and fixed for empty lists and urls
 page_url = links[i]
 print("Current Electroline link: " + page_url)
 if page_url == '' :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  link_soup = load_soup(page_url)
  products_containers = link_soup.findAll('li', {'class': re.compile('listing-product listing-product--rows-layout*')})
  
 if len(products_containers) == 0 :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  pricelist = []
 
 for product in products_containers : 
  if product.ins :
   display_price = product.ins.text.replace('€', '').strip()
  elif product.find('span', {'class' : 'listing-product-price listing-product-price--without-loyalty'}) :
   display_price = product.find('span', {'class' : 'listing-product-price listing-product-price--without-loyalty'}).text.replace('€', '').strip()
  else :
   display_price = product.find('div', {'class' : 'listing-product-price listing-product-price--rows-layout'}).text.replace('€', '').strip()
 
  # print('Price: ' + display_price)
  price = float(display_price.replace(',', ''))
  # print('Float: ' + str(price))
  pricelist.append(price)
 
 min_list = smallest_price(pricelist)
 product = products_containers[min_list]
 price = pricelist[min_list]
 """title = ol.li.h3.text"""
 title = product.find('div', {'class' : 'listing-product__title-group'}).h3.text.strip()
 code = product.find('div', {'class' : 'listing-product__title-group'}).span.text.strip()
 url = product.find('a', {'class' : 'listing-product__image-link'})['href']
 print('Category: ' + categories[i])
 # print('min list: ' + str(min_list))
 print('title:    ' + title)
 print('code:     ' + code)
 print('url:      ' + url)
 print('price:    ' + str(price))
 print(pricelist)
 return(price, title, code, url)

def bio_stuff(links, i) :  # with product/price containers and fixed for empty lists and urls
 page_url = links[i]
 print("Current Bionic link: " + page_url)
 if page_url == '' :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  # driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", chrome_options = chrome_options)
  driver.get(page_url)
  nani(2)
  link_soup = soup(driver.page_source, features = "lxml")
  # link_soup = load_soup(page_url)
  temp_container = link_soup.findAll('div', {'class': 'product-container'})
  products_containers = []
  for temp in range(1, len(temp_container)): 
   products_containers.append(temp_container[temp])
  
 if len(products_containers) == 0 :
  price = title = code = url = '-'
  return(price, title, code, url)
 else :
  pricelist = []
 
 # print("len(products_containers):" + str(len(products_containers)))
 # for product in products_containers :
  # try :
   # product.h3.text.strip()
  # except : 
   # product.h3
 
 for product in products_containers : 
  if product.find('div', {'class': 'price loyalty'}) :
   display_price = product.find('div', {'class': 'price loyalty'}).h3.text.replace('€', '').strip()
  elif product.find('div', {'class': 'price periodic'}) :
   display_price = product.find('div', {'class': 'price periodic'}).h3.text.replace('€', '').strip()
  elif product.find('div', {'class': 'retail-price'}) :
   display_price = product.find('div', {'class': 'retail-price'}).h3.text.replace('€', '').strip()
  else :
   display_price = product.find('div', {'class': 'price regular'}).h3.text.replace('€', '').strip()
  price = float(display_price.replace(',', ''))
  pricelist.append(price)
 
 min_list = smallest_price(pricelist)
 product = products_containers[min_list]
 price = pricelist[min_list]
 """title = ol.li.h3.text"""
 title = product.find('div', {'class' : 'product-title'}).h4.a.text.strip()
 code = product.h5.span.text.strip()
 url = product.find('div', {'class' : 'product-title'}).h4.a['href']
 if url.find("bionic.com.cy") < 0 :
  url = "https://bionic.com.cy" + url
 
 print('Category: ' + categories[i])
 # print('min list: ' + str(min_list))
 print('title:    ' + title)
 print('code:     ' + code)
 print('url:      ' + url)
 print('price:    ' + str(price))
 print(pricelist)
 return(price, title, code, url)

def kot_stuff(links, i) :  # with product/price containers
 page_url = links[i]
 print("Current Kotsovolos link: " + page_url)
 link_soup = load_soup(page_url)
 # url = kot_soup.h2.a['href']
 # url
 # title = kot_soup.h2.text.strip()
 # title
 # code = kot_soup.find('span', {'class': 'prCode'}).text.strip()
 products_containers = link_soup.findAll('div', {'class' : 'productWrap'})
 if len(products_containers) == 0:
  price = title = code = url = "-"
  return("-", "-", "-", "-")
  # return(price, title, code, url)
 pricelist = []
 for product in products_containers : 
  if product.text.find('κερδίζεις') >= 0 :
   price = product.find('div', {'class' : 'price'}).text.strip().replace('\n', '').replace('\t', '')[4:]
   # init_price = price[:price.find('€')]
   discount_price = price[price.find('€') + 1:price.find('ΤΙΜΗ')]
   price = float(discount_price.replace(',', ''))
  else :
   price = product.find('div', {'class' : 'price'}).text.strip().replace('\n', '').replace('\t', '')
   init_price = price[1:price.find('ΤΙΜΗ')]
   discount_price = "-"
   price = float(init_price.replace(',', ''))
  pricelist.append(price)
 # price = kot_soup.find('div', {'class': 'price simplePrice'}).text.strip()
 # price = float(price.replace('€', ''))
 # price
 min_list = smallest_price(pricelist)
 product = products_containers[min_list]
 price = pricelist[min_list]
 title = product.h2.text.strip()
 title = title.replace('  ',' ')
 code = product.find('span', {'class', 'prCode'}).text.strip()
 url = product.h2.a['href']
 if url.find('https://www.kotsovolos.cy') >= 0 :
  pass
 else :
  url = 'https://www.kotsovolos.cy/' + url
 print('Category: ' + categories[i])
 # print('min list: ' + str(min_list))
 print('title:    ' + title)
 print('code:     ' + code)
 print('url:      ' + url)
 print('price:    ' + str(price))
 print(pricelist)
 return(price, title, code, url)

def winner_is() :
 winners = [cy_price, st_price, pub_price, sin_price, el_price, bio_price, kot_price]
 winners = []
 
 if type(cy_price) == str:
  winners.append(1000000)
 else:
  winners.append(cy_price)
 
 if type(st_price) == str:
  winners.append(1000000)
 else:
  winners.append(st_price)

 if type(pub_price) == str:
  winners.append(1000000)
 else:
  winners.append(pub_price)

 if type(sin_price) == str:
  winners.append(1000000)
 else:
  winners.append(sin_price)

 if type(el_price) == str:
  winners.append(1000000)
 else:
  winners.append(el_price)

 if type(bio_price) == str:
  winners.append(1000000)
 else:
  winners.append(bio_price)

 if type(kot_price) == str:
  winners.append(1000000)
 else:
  winners.append(kot_price)

#  for w in winners :
#   print(str(w))
#   print(type(w))
 winner = smallest_price(winners)
 
 print("Smallest winner: " + str(winner))
 
 if winner == 0 :
  print("winner = 0")
  winner = "CY"
  cy_wins = True
 else :
  print("winner != 0")
  winner = "NOT CY"
  cy_wins = False
 print(winner)
 print("And the winner is: " + winner)

def chrome_init():
 chrome_options = ChromeOptions()
 chrome_options.add_argument("--headless")
 chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
 chrome_options.add_argument("--log-level=OFF")
 try:
  print("Ξεκινάω τον Chrome Driver για τους δύσκολους...")
  driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", options = chrome_options)
  chrome_drv = True
  print("Chrome Driver ΟΚ...")
 except Exception as exc:
  print("Φαίνεται πως δεν ξεκίνησε ο Chrome Driver. Κάποιοι ανταγωνιστές δεν θα δουλέψουν σήμερα...")
  print("Error: " + str(exc))
  chrome_drv = False
 
 print("")
 return chrome_options, driver, chrome_drv

def initialize():
 trial_run = 0
 e = 1
 winners = []
 winner = "not set"
 return(trial_run, e, winners, winner)

try :
 trial_run, e, winners, winner = initialize()
 get_start_time()
 set_files()
 chrome_options, driver, chrome_drv = chrome_init()
 categories, cy_links, st_links, pub_links, kot_links, sin_links, el_links, bio_links = set_categories()
 
 for i in range(trial_run, len(categories)) :
  print("-" * (len(categories[i]) + 2))
  print("|" + categories[i] + "|")
  print("-" * (len(categories[i]) + 2))
  print("")
  cy_price, cy_title, cy_code, cy_url = cy_stuff(cy_links, i)
  print("")
  st_price, st_title, st_code, st_url = st_stuff(st_links, i)
  print("")
  pub_price, pub_title, pub_code, pub_url = pub_stuff(pub_links, i)
  print("")
  sin_price, sin_title, sin_code, sin_url = sin_stuff(sin_links, i)
  print("")
  el_price, el_title, el_code, el_url = el_stuff(el_links, i)
  print("")
  bio_price, bio_title, bio_code, bio_url = bio_stuff(bio_links, i)
  print("")
  kot_price, kot_title, kot_code, kot_url = kot_stuff(kot_links, i)
  print("")
  winner = winner_is()
  write_results(e)
  e += 1
  write_it_down(write_file)
  print("")
 print("")
 print("Bye bye Chrome Driver...")
 driver.quit()
 print("")
except KeyboardInterrupt :
 print("")
 print("OK κατάλαβα. Διαλλειματάκι... ")
 print("")
except Exception as exc:
 exception_type, exception_object, exception_traceback = sys.exc_info()
 filename = exception_traceback.tb_frame.f_code.co_filename
 line_number = exception_traceback.tb_lineno
 print("")
 print("Ώπα πέσαμε πάνω σε εξαίρεση:")
 print("Τύπος:  ", exception_type)
 print("Αρχείο: ", filename)
 print("Γραμμή: ", line_number)
 sys.exit(0)
