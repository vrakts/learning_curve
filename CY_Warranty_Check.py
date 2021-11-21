# CY_Warranty_Check.py
### Ελέγχει την περιγραφή του κάθε προϊόντος και κρατάει την εγγύηση
### γράφει όλο το κείμενο της περιγραφής σε ένα excel για έλεγχο μετά.
# Current Version 1 beta
""" Έγινε αλλαγή στο όνομα του αρχείου και στο all_links """

def errorlog(value) :
 now = datetime.now()
 formatted = now.strftime("%Y-%m-%d %H:%M:%S")
 try :
  errorlog = open("cy_warranty_errorlog.txt","a")
 except Exception as exc :
  print("Προειδοποίηση, πέσαμε σε εξαίρεση. Πιθανώς να μην γραφτούν κινήσεις στο errorlog.")
  print(str(exc))
 errorlog.write(formatted + ": " + value + "\n")
 errorlog.close()

try :
 from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
 from random import randint
 from time import sleep as nani
 from datetime import datetime
 import requests, os, sys, re, xlwt #, unicodedata
except Exception as exc :
 import sys
 from datetime import datetime
 print("Κάτι πάθαμε κατά το import.")
 print(str(exc))
 error_text = "while importing modules the following exception occured: " + str(exc)
 errorlog(error_text)
 sys.exit(0)

def files_setup() :
 global write_path, wb_write, ws_write, write_file, alt_write_file
 try :
  if os.path.exists(r"Z:\OneDrive") == True :
   write_path = (r'Z:\OneDrive')
  elif os.path.exists(r"Y:\OneDrive") == True :
   write_path = (r'Y:\OneDrive')
  elif os.path.exists(r"K:\SALES") == True :
   write_path = (r'K:\SALES')
  else :
   print("Where am I?")
   input()
   sys.exit(0)
  now = datetime.now()
  date_for_file = now.strftime("%Y-%m-%d")
  os.chdir(write_path)
  write_file = ("Warranty_Check_Convs_" + date_for_file + ".xls")  # name of xls write file
  alt_write_file = ("Warranty_Check_Convs_" + date_for_file + ".xls")  # alternate name of xls write file
  print("Προσπάθεια για δημιουργία: " + write_file)
  wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
  ws_write = wb_write.add_sheet(date_for_file, cell_overwrite_ok = True)  # add 1st sheet in virtual workbook
  print("Γιούπι, τα καταφέραμε.")
  print("")
  ws_write.write(0, 0, "ΚΑΤΗΓΟΡΙΑ")
  ws_write.write(0, 1, "ΜΑΡΚΑ")
  ws_write.write(0, 2, "ΚΩΔΙΚΟΣ")
  ws_write.write(0, 3, "ΤΙΤΛΟΣ")
  ws_write.write(0, 4, "ΕΓΓΥΗΣΗ")
  now = datetime.now()
  formatted = now.strftime("%Y-%m-%d %H:%M:%S")
  errorlog = open("cy_warranty_errorlog.txt","a")
  errorlog.write("-_-_-_-_-_-_-_-_-_-_-\n")
  errorlog.write("Started at: " + formatted + "\n")
  errorlog.close()
 except Exception as exc :
  print("Δεν κατάφερα να γράψω το αρχείο. Έχουμε δικαιώματα;")
  print(str(exc))
  error_text = "while trying to setup files the following error occured: " + str(exc)
  errorlog(error_text)
  print("")

def load_soup(page, wait, retries) :
 # print("Μέσα στη σούπα.")
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
   print("Ώπα πέσαμε πάνω στο:")
   print(str(exc))
   error_text = "while loading soup for " + page + " the following exception occured: " + str(exc)
   errorlog(error_text)
   print("Ξαναπροσπαθώ σε " + str(wait)+ ".")
   nani(wait)
   attempt += 1
 if attempt == retries :
  print("Προσπάθησα " + str(retries) + " φορές και δεν τα κατάφερα.")
  input()
  sys.exit(0)
 
 return(page_soup)

def all_links() :
 print("Μετράω links.")
 urls = []
 needed_links = []
 page_url = "https://www.e-shop.cy/"
 links_soup = load_soup(page_url, wait, retries)
 urls = links_soup.find('div', {'id': 'dropdown_25'}).findAll('a', {'class': 'menu_link'})
 for i in range(0, len(urls)) :
  try :
   needed_links.append(urls[i]['href'])
   print(needed_links[i])
  except Exception as exc:
   print("Ώπα πέσαμε πάνω στο:")
   print(str(exc))
   error_text = "while loading links the following errorion occured: " + str(exc)
   errorlog(error_text)
 # needed_links = ['https://www.e-shop.cy/search_main?table=PER&category=CONVERTERS']
 print("Τέλος τα links.")
 print("")
 return(needed_links)

def get_all_products(page_url, page_soup) :
 print("Βρίσκω όλα τα προϊόντα.")
 attempt = 0
 all_products = []
 while attempt < retries :
  try :
   offset = 0
   cat_pages = []
   trs = []
   prod_count = page_soup.find('div', {'class': 'web-product-num'}).text
   prod_count = int(prod_count[:prod_count.find(" ")].strip())
   total_next_pages = int(prod_count / 10) + 1
   print("Συνολο σελιδών: " + str(total_next_pages))
   cat_page, query_mark, categories = str(page_url).partition("?")
   while offset < prod_count :
    # print("inside while loop")
    cat_pages.append(cat_page + query_mark + "offset=" + str(offset) + "&" + categories)
    offset += 10
    # print(str(offset))
   # print("Σύνολο cat_pages: " + str(len(cat_pages)))
   p = 0
   for page in cat_pages :
    p += 1
    print_text = "Μετρώντας τα προϊόντα της σελίδας: " + str(p)
    if p != len(cat_pages) :
     print(print_text, end='\r')
    else :
     print(print_text)
     # print("")
   # print(page)
    # sys.stdout.write('\x1b[1A')
    # # sys.stdout.write('\x1b[1A')
    # # sys.stdout.write('\x1b[2K')
    single_page_soup = load_soup(page, wait, retries)
    # print(single_page_soup.title)
    containers = single_page_soup.findAll('table', {'class': 'web-product-container'})
    for container in containers :
     cy_code = container.font.text.replace("(", "").replace(")", "")
     # print(gr_code)
     all_products.append(cy_code)
   break
  except Exception as exc :
   print("")
   print("Ώπα πέσαμε πάνω στο:")
   print(str(exc))
   print("Ξαναπροσπαθώ σε " + str(wait)+ ".")
   error_text = "while loading all products for " + page + " the following exception occured: " + str(exc)
   errorlog(error_text)
   nani(wait)
   attempt += 1
 if attempt == retries :
  print("Προσπάθησα " + str(retries) + " φορές και δεν τα κατάφερα.")
  input()
  sys.exit(0)
 print("Τέλος τα προϊόντα.")
 print("")
 return(all_products)

def get_cy_details(container) :
 global cy_title, cy_brand, cy_category, cy_warranty #, cy_price, 
 print("Στις λεπτομέρειες.")
 # print("")
 prod_url = 'https://www.e-shop.cy/product?id=' + container
 print('prod_url: ' + prod_url)
 # print("")
 page_soup = load_soup(prod_url, wait, retries)
 cy_title = page_soup.h1.text
 cy_categories = page_soup.findAll('td', {'class': 'faint1'})
 # print('cy_categories: ' + cy_categories.text)
 # cy_category = cy_categories[cy_categories.find('Κατηγορία:')+10:cy_categories.find('Υποκατηγορία:')].strip()
 if len(cy_categories) == 0 :
  cy_category = "-"
  cy_brand = "-"
  cy_subcat = ""
 elif cy_categories[1].text.find(' •') > 0 :
  cy_category = cy_categories[1].text[:cy_categories[1].text.find(' •')]
  cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
  if len(cy_categories) > 2 :
   cy_subcat = cy_categories[3].text.strip()
  else :
   cy_subcat = ""
 else :
  cy_category = cy_categories[1].text.strip() 
  if len(cy_categories) > 2 :
   cy_subcat = cy_categories[3].text.strip()
  else :
   cy_subcat = ""
  cy_brand = "-"
 desc_text = ""
 d_soup = page_soup.find('td', {'class': 'product_table_body'})
 product_table_title = page_soup.find('td', {'class': 'product_table_title'})
 if d_soup == None or d_soup.text.find('Σύνολο ψήφων') > 0 or product_table_title.text.strip() != "Περιγραφή" :
  desc_text = ""
 else :
  desc_text = d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
 if desc_text.find('Εγγύηση') >= 0 :
  before, warranty, rest = desc_text.rpartition("Εγγύηση:")
  cy_warranty = warranty + rest
 else :
  before, lastli, rest = desc_text.rpartition('<li>')
  cy_warranty = lastli + rest 
 print("Τέλος οι λεπτομέρειες.")
 print("")

def write_results(e) :
 # print("e = " + str(e))
 ws_write.write(0, 5, "<li><b>Εγγύηση:</b> 2 χρόνια.")
 ws_write.write(e, 0, cy_category)
 ws_write.write(e, 1, cy_brand)
 ws_write.write(e, 2, cy_code)
 ws_write.write(e, 3, cy_title)
 ws_write.write(e, 4, cy_warranty)
 

def write_it_down(e, null) :
 # print("Γράφω: " + str(e))
 if null == 0 :
  try :
   wb_write.save(write_file)
  except :
   wb_write.save(alt_write_file)
 elif e > 1 :
  try :
   wb_write.save(write_file)
   print(write_file + ", το έχω γραμμένο στο " + write_path)
  except :
   print("Πιθανώς κάποιος παίζει με το αρχείο. Προχωράω στο παρασύνθημα.")
   wb_write.save(alt_write_file)
   print(alt_write_file + ", το έχω γραμμένο στο " + write_path)
 else :
  print("Δεν έχει γίνει καμία αλλαγή στο αρχείο.")

try :
 headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
 offset = 0
 e = 1
 attempt = 0
 retries = 10
 wait = 3
 all_products = []
 prod_count = 0
 os.system("title " + "Setting up files...")
 files_setup()
 os.system("title " + "Gathering links...")
 needed_links = all_links()
 l_id = 0
 for link in needed_links :
  # page_url = "https://www.e-shop.cy/search_main?table=HAP&&category=%CA%CB%C9%CC%C1%D4%C9%D3%D4%C9%CA%C1"
  os.system("title " + "Page: " + str(l_id) + "/"+ str(len(needed_links)))
  l_id += 1
  p_id = 0
  print("Τρέχω τη σελίδα: " + link)
  # print("")
  page_soup = load_soup(link, wait, retries)
  try :
   if page_soup.find('td', {'class': 'shop_table_title'}) :
    page_link = "https://www.e-shop.cy/" + page_soup.find('td', {'class': 'shop_table_title'}).a['href']
   else :
    page_link = link
   print("Αλήθεια τρέχω τη σελίδα: " + page_link)
   print("")
  except Exception as exc :
   error_text = "while loading soup for " + link + " the following error occured: " + str(exc)
   errorlog(error_text)
   print("Ώπα: " + str(exc))
   continue
  all_products = []
  page_soup = load_soup(page_link, wait, retries)
  all_products = get_all_products(page_link, page_soup)
  for product in all_products :
   print("all_products: " + product)
  print("")
  for cy_code in all_products :
   # print("")
   p_id += 1
   os.system("title " + "Page: " + str(l_id) + "/"+ str(len(needed_links)) + ". Item: " + str(p_id) + "/" + str(len(all_products)))
   print(cy_code)
   get_cy_details(cy_code)
   write_results(e) #, cy_code, cy_title, cy_category, cy_brand, cy_warranty)
   e += 1
  write_it_down(e, 0)
except KeyboardInterrupt :
 try :
  error_text = "aborted by user"
  errorlog(error_text)
  print("")
  input("Διαλλειματάκι;")
 except :
  sys.exit(0)
except Exception as exc:
 print("Ώπα: " + str(exc))
finally :
 print("reached finally")
 errorlog("reached finally")
 write_it_down(e, 1)
 sys.exit(0)