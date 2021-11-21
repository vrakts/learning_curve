# Current Version 1 beta
##########################
# Changelog V1 beta
# - Βρίσκει το Vendor OEM Code απο τα site του κατασκευαστή
##########################
# - Στεφανής να βρίσκει τον κωδικό κατηγορίας
# - Καλύτερος κώδικας για Bionic και CustomPC

try :
 from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
 from random import randint
 from time import sleep as nani
 from datetime import datetime
 from urllib.request import quote  # enables encoding greek characters in url
 from urllib.parse import unquote  # enables decoding of greek characters
 import requests, os, sys, re, ezodf, clipboard, ctypes
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
 gr_oem = ""
 # page_soup = load_soup(page_soup, wait, retries)
 gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  gr_oem = ""
 else :
  gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html values and any .gr mentions
  if gr_desc_text.find('Vendor OEM:') > 0 :
   print("Επικοινωνώ με τους Vendors...")
   if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
    string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
   else :
    string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
   gr_desc_text = string.strip()  # keep only what is before the OEM
   oem = rest.strip()  # keep only what is after the OEM
   gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
   gr_oem = gr_oem.strip()
 
 return(gr_oem)

def get_ste_details(page_url) :
 ste_oem = ""
 ste_oem = page_url[page_url.rfind("/") + 1:]
 return(ste_oem)

def get_pub_details(page_url) :
 pub_oem = ""
 pub_oem = page_url[page_url.rfind("prod") + 4:page_url.rfind("pp")]
 return(pub_oem)

def get_ele_details(page_soup) :
 ele_oem = ""
 ele_oem = page_soup.find('span', {'class': 'single-product-sku'}).text.replace("SKU #", "").strip()
 return(ele_oem)

def get_kot_details(page_soup) :
 kot_oem = ""
 kot_oem = page_soup.find('span', {'class': 'prCode'}).text.strip()
 return(kot_oem)

def get_bio_details(page_soup) :
 bio_text = ""
 bio_oem_temp = ""
 bio_oem = ""
 bio_text = str(page_soup.find('div', {'data-react-class': 'products/ProductView'}))
 bio_oem_temp = bio_text[bio_text.find("mini_url"):bio_text.find(".jpg")]
 bio_oem = bio_oem_temp[bio_oem_temp.rfind("/") + 1:]
 return(bio_oem)

def get_sin_details(page_soup) :
 sin_oem = ""
 sin_oem = page_soup.find('span', {'class': 'ty-control-group__item'}).text.strip()
 # re.compile('list_image_update*')})['
 return(sin_oem)

def get_cus_details(page_soup) :
 cus_text = ""
 cus_oem_temp = ""
 cus_oem = ""
 cus_text = str(page_soup)
 cus_oem_temp = cus_text[cus_text.find("ty-control-group__item cm-reload"):cus_text.find("<!--product_code")]
 cus_oem = cus_oem_temp[cus_oem_temp.rfind('">') + 2:]
 return(cus_oem)

def get_my_vendor(page_url) :
 if page_url.find("public-cyprus") >= 0 :
  vendor_oem = get_pub_details(page_url)
 elif page_url.find("stephanis") >= 0 :
  vendor_oem = get_ste_details(page_url)
 else:
  page_soup = load_soup(page_url, wait, retries)
  if page_url.find("e-shop.gr") >= 0 :
   vendor_oem = get_gr_details(page_soup)
  elif page_url.find("electroline") >= 0 :
   vendor_oem = get_ele_details(page_soup)
  elif page_url.find("bionic") >= 0 :
   vendor_oem = get_bio_details(page_soup)
  elif page_url.find("singular") >= 0 :
   vendor_oem = get_sin_details(page_soup)
  elif page_url.find("custompc") >= 0 :
   vendor_oem = get_cus_details(page_soup)
  elif page_url.find("kotsovolos") >= 0 :
   vendor_oem = get_kot_details(page_soup)
 return(vendor_oem) 

try :
 wait = 3
 retries = 3
 vendor_oem = ""
 headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
 s_text = clipboard.paste().strip()
 if s_text.find("http") < 0 :
  page_url = "https://www.e-shop.gr/product?id=" + s_text
 else :
  page_url = s_text
 vendor_oem = get_my_vendor(page_url)
 if vendor_oem == "" :
  print("Άδεια η πόλη, που πήγανε όλοι;")
 else :
  print(vendor_oem)
  clipboard.copy(vendor_oem)
except Exception as exc :
 print("Εξαίρεση: " + str(exc))

