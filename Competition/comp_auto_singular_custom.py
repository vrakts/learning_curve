# comp_auto_singular_custom
### Για τώρα δουλεύει μόνο μνήμες

import requests, os, sys, re, xlwt, ezodf
from bs4 import BeautifulSoup as soup
from datetime import datetime
from time import sleep as nani

answer = "YES"
cookies = {'language': 'en'}
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
e = 1
print_debug = True

def print_debug(print_text) :
 if print_debug == True :
  print(print_text)

def set_files() :
 global write_path, write_file, alt_write_file, wb_write, ws_write
 if os.path.exists(r"Z:\OneDrive\eShop Stuff\PRODUCT\Product\Auto Comp") == True :
  write_path = (r'Z:\OneDrive\eShop Stuff\PRODUCT\Product\Auto Comp')
 elif os.path.exists(r"Y:\OneDrive\eShop Stuff\PRODUCT\Product\Auto Comp") == True :
  write_path = (r'Y:\OneDrive\eShop Stuff\PRODUCT\Product\Auto Comp')
 write_file = ('auto_comp_ram.xls')
 alt_write_file = ('auto_comp_ram_alt.xls')
 os.chdir(write_path)
 wb_write = xlwt.Workbook()
 ws_write = wb_write.add_sheet("auto_comp", cell_overwrite_ok = True)
 ws_write.write(0, 0, "ΚΩΔΙΚΟΣ")
 ws_write.write(0, 1, "ΤΙΤΛΟΣ")
 ws_write.write(0, 2, "ΤΙΜΗ")
 ws_write.write(0, 3, "GR")
 ws_write.write(0, 4, "SINGULAR")
 ws_write.write(0, 5, "SKU")
 ws_write.write(0, 6, "LINK")
 ws_write.write(0, 7, "CUSTOMPC")
 ws_write.write(0, 8, "SKU")
 ws_write.write(0, 9, "LINK")

def choice() :
 global choice
 choice_ok = False
 while choice_ok == False :
  print("1. Λίστα με αποτελέσματα μόνο.")
  print("2. Ανταγωνισμός.")
  answer_text = "Επιλογή: "
  choice = input(answer_text)
  try :
   val = int(choice)
   if val >= 1 and val <= 2 :
    choice_ok = True
  except ValueError:
   try:
    val = float(choice)
    if val >= 1 and val <= 2 :
     choice_ok = True
   except ValueError:
    choice_ok = False
    print("")
    print("Η επιλογή σου δεν είναι αριθμός. Δοκίμασε πάλι.")
  if choice_ok == False :
   print("")
   print("Προσπάθησε πάλι επιλέγοντας 1 ή 2.")
 choice = val

def list_pages() :
 global pages_list
 pages_list = []
 page_url = input("Δώσε πράμα: ")
 while page_url.find("http") >= 0 :
  pages_list.append(page_url)
  page_url = input("Έ έτσι ξεροσφύρι θα τη βγάλουμε; Δώσε κι άλλο πράμα: ")
 else :
  if len(pages_list) == 0 :
   pages_list.append('https://www.e-shop.cy/search_main?table=PER&&category=%CC%CD%C7%CC%C7+RAM')
  print("Τα μαζεύω και φεύγω.")

def load_soup(page) :
 # temp_product = page[page.rfind("=") + 1:]
 # print("Loading soup for " + temp_product)
 # print("")
 result = requests.get(page, headers = headers)
 webpage = result.content
 page_soup = soup(webpage, "html5lib")
 return(page_soup)

def get_cy_mainpage(page_url) :
 global start_page_soup, next_pages_category, total_next_pages, cat_page, query_mark, categories, cat_offset_url
 print("Φανταστική σελίδούλα με όνομα:")
 print(page_url)
 start_page_soup = load_soup(page_url)
 next_pages_category = start_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})
 try :
  total_next_pages = next_pages_category[len(next_pages_category)-1].text
 except :
  total_next_pages = "1"
 print("Σύνολο σελίδων: " + str(total_next_pages))
 cat_page, query_mark, categories = str(page_url).partition("?")
 cat_offset_url = cat_page + query_mark + "offset=" + str(offset) + "&" + categories
 # print("")
 # print("Offset page: " + cat_offset_url)

def get_total_products() :
 global total_prod, tp
 last_offset = (int(total_next_pages) - 1) * 10
 last_cat = cat_page + query_mark + "offset=" + str(last_offset) + "&" + categories
 last_page_soup = load_soup(last_cat)
 last_prod = last_page_soup.findAll('table', {'class': 'web-product-container'})
 total_prod = len(last_prod) + last_offset
 tp = total_prod
 print("Βρήκα " + str(total_prod) + " προϊόντα. Τα κεφάλια μέσα.")
 print("")

def single_pages(cat_offset_url) :
 global containers
 # global single_page_soup
 single_page_soup = load_soup(cat_offset_url)
 containers = single_page_soup.findAll('table', {'class': 'web-product-container'})

def get_cy_details(container) :
 global cy_code, cy_title, cy_price, cy_brand, cy_category
 cy_code = container.font.text.replace("(", "").replace(")", "")
 cy_title = container.h2.text.strip()
 if container.b.font :
  cy_price = float(container.b.font.text.strip())
 else :
  cy_price = float(container.b.text.strip())
 categories = container.find('td', {'class': 'web-product-info'}).text
 category = categories[categories.find('Κατηγορία:')+10:categories.find('Υποκατηγορία:')].strip()
 brand = categories[categories.find('Κατασκευαστής:')+14:].strip()

def get_gr_details(gr_code) :
 global gr_price, gr_vendor
 gr_vendor = ""
 gr_url = 'https://www.e-shop.gr/product?id=' + gr_code
 gr_page_soup = load_soup(gr_url)
 gr_price_list = gr_page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(gr_price_list) == 0 :
  gr_price_text = "Εξαντλημένο"
  gr_price = gr_price_text
 else : 
  gr_price_text = gr_price_list[0].text.replace("\xa0€", "")
  print_text = "gr_price_text: " + gr_price_text
  print_debug(print_text)
  gr_price = float(gr_price_text)
  print_text = "gr_price: " + str(gr_price)
  print_debug(print_text)
 gr_d_soup = gr_page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 gr_product_table_title = gr_page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  gr_vendor = ""
 else :
  gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html values and any .gr mentions
  if gr_desc_text.find('Vendor OEM:') > 0 :
   if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
    string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
   else :
    string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
   gr_desc_text = string.strip()  # keep only what is before the OEM
   oem = rest.strip()  # keep only what is after the OEM
   gr_vendor, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
   gr_vendor = gr_vendor.strip()
 print_text = "gr_price: " + str(gr_price)
 print_debug(print_text)

def get_search_term(cy_title, gr_vendor) :
 global search_term
 if gr_vendor != "" :
  search_term = gr_vendor
 elif cy_category == 'ΜΝΗΜΗ RAM' :
  firstf = cy_title.find(" ") + 1
  secondf = firstf + cy_title[firstf:].find(" ") + 1
  title_cut = cy_title[secondf:]
  search_term = title_cut[:title_cut.find(" ")]
 elif cy_category == 'ΜΗΤΡΙΚΗ ΚΑΡΤΑ' :
  if cy_title.find('RETAIL') >= 0 :
   title_cut = cy_title[cy_title.find(" "):cy_title.rfind(" ")].strip()
  else :
   title_cut = cy_title[cy_title.find(" "):]
  search_term = title_cut
 print_text = "search_term: " + search_term
 print_debug(print_text)

def get_sin_details(search_term) :
 global si_price, si_pcode, si_psku, si_plink, si_pavail
 si_search_url = "https://www.singular.com.cy/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&search_id=&q=" + search_term + "&dispatch=products.search"
 try :
  page_soup = load_soup(si_search_url)
  if print_debug == True :
   print("Singular read OK.")
   print("")
  si_price_container = page_soup.findAll("span", {"id" : re.compile('sec_product_price*')})
  if len(si_price_container) == 0 :
   si_price = "-"
   si_pcode = "-"
   si_psku = "-"
   si_plink = "-"
   si_pavail = "-"
  else :
   si_price_text = si_price_container[0].text.replace("\xa0€","").replace(".", ",")
   if si_price_text.count(',') > 1 :  # since price value on singular site has comma as a digit group seperator replace it with dot
    si_price = si_price_text.replace(',', '', 1)
   else :
    si_price = si_price_text
   si_em = page_soup.findAll('em')  # contains all EM tags that have the product ID SKU and other info
   for em in si_em :
    if em.text.find('Product Code') > 0 :
     si_pcode = em.text.strip().replace('Product Code', '')
     break
   si_psku = page_soup.find('span', {'class': 'ty-control-group__item'}).text.strip()
   si_plink = page_soup.find("input", {"name": re.compile('list_image_update*')})['value']
   si_pavail = page_soup.find("span", {"class" : "delivery-time"})
   if si_pavail == None :
    si_avail_text = "Out of stock"
   else :
    si_avail_text = si_pavail.text.strip()
   si_pavail = si_avail_text
 except Exception as exc :
  print("Άλα της, μόλις πέσαμε πάνω στο exception:")
  print(str(exc))
  print("")
 
def get_cpc_details(search_term) :
 global cp_price, cp_pcode, cp_avail, cp_plink
 cp_search_url = "https://www.custompc.com.cy/search/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&scode_from_q=Y&cid=0&q=" + search_term
 try :
  page_soup = load_soup(cp_search_url)
  # print("Custom PC read OK.")
  # print("")
  custom_price = page_soup.findAll("span", {"id" : re.compile('sec_discounted_price*')})
  if len(custom_price) == 0 :
   custom_price_text = "-"
   cp_pcode = "-"
   cp_plink = "-"
   cp_avail = "-"
  else :
   custom_price = page_soup.findAll('span', {'class' : 'ty-price-num'})
   custom_price_text = custom_price[1].text.replace('.', ',')
   cp_prod_url = page_soup.findAll('a', {'class' : 'product-title'})
   if len(cp_prod_url) == 0 :
    cp_plink = "-"
   else :
    cp_plink = cp_prod_url[0]['href']
    # print("cp_prod_url: " + cp_prod_url)
    attempt = 0
    while attempt < 3 :
     try :
      cp_prod_soup = load_soup(cp_plink)
      break
     except http.client.IncompleteRead :
      attempt += 1
     # else :
      # pass
    cp_pcode = cp_prod_soup.find('div', {'class' : 'ty-control-group ty-sku-item cm-hidden-wrapper'}).text  # extract the product code container from the product page
    cp_pcode = cp_pcode[cp_pcode.find(':') + 1:].strip() # extract only the product code from the product page
    # print("cp_pcode: " + cp_pcode)
    try :
     cp_avail = cp_prod_soup.find('span', {'class' : 'ty-qty-in-stock ty-control-group__item'}).text.strip()  # if in stock extract availability from the product page
    except :
     cp_avail = cp_prod_soup.findAll('div', {'class' : 'ty-control-group product-list-field'})  # if not then try the no stock container
     cp_avail = cp_avail[1].text.strip()[cp_avail[1].text.strip().find(':')+2:]  # remove unecessary text
  
  cp_price = custom_price_text
 except Exception as exc :
  print("Άλα της, μόλις πέσαμε πάνω στο exception:")
  print(str(exc))
  print("")

def margin_check(page_soup) :
 global margin
 margin_exist = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
 stock_exist = page_soup.findAll("font", {"style" : "color:#ff0000;font-weight:bold;font-size:9px;font-family:arial black;"})
 if len(stock_exist) != 0 :  # if stock_exist not empty then stock sign exists
  margin = "STOCK"
 elif len(margin_exist) != 0 :  # if margin_exist not empty then stock doesn't exist and margin sign exists
  margin = "MARGIN"
 else :  # if both stock sign doesn't exist and high margin exist then no changes
  margin = "-"
  # continue

def write_results(e) :
 # print("e = " + str(e))
 ws_write.write(e, 0, cy_code)
 ws_write.write(e, 1, cy_title)
 ws_write.write(e, 2, cy_price)
 ws_write.write(e, 3, gr_price)
 ws_write.write(e, 4, si_price)
 ws_write.write(e, 5, si_psku)
 ws_write.write(e, 6, si_plink)
 ws_write.write(e, 7, cp_price)
 ws_write.write(e, 8, cp_pcode)
 ws_write.write(e, 9, cp_plink)

def write_it_down(e) :
 # print("Γράφω: " + str(e))
 if e > 1 :
  try :
   wb_write.save(write_file)
   print(write_file + ", το έχω γραμμένο στο " + write_path)
  except :
   wb_write.save(alt_write_file)
   print("Πιθανώς κάποιος παίζει με το αρχείο. Προχωράω στο παρασύνθημα.")
   print(alt_write_file + ", το έχω γραμμένο στο " + write_path)
 else :
  print("Δεν έχει γίνει καμία αλλαγή στο αρχείο.")

try :
 choice()
 set_files()
 list_pages()
 print("")
 for page in pages_list :
  offset = 0  # starting offset value set to 0 and in each for loop, 10 will be added
  get_cy_mainpage(page)
  print("")
  get_total_products()
  for q in range(0, int(total_next_pages)) :
   single_pages(cat_offset_url)
   for container in containers :
    attempt = 0
    tp -= 1
    while attempt < 3 :
     try :
      # print("Μπαίνω CY")
      get_cy_details(container)
      # print("CY OK")
      if choice == 2 :
       # print("Μπαίνω GR")
       get_gr_details(cy_code)
       # print("GR OK")
       get_search_term(cy_title, gr_vendor)
       # print("search_term: " + search_term)
       get_sin_details(search_term)
       get_cpc_details(search_term)
      write_results(e)
      # print(str(e))
      e += 1
      if total_prod - (total_prod - tp) > 0 :
       print("Τα πίνω με το: " + cy_code +". " + str(total_prod - tp) + "/" + str(total_prod) + ". Έχω ακόμα: " + str(total_prod - (total_prod - tp)))
      else :
       print("Τα πίνω με το: " + cy_code +". " + str(total_prod - tp) + "/" + str(total_prod) + ".")
      break
     except Exception as exc :
      print("")
      print("Όχι ρε φίλε. Μόλις σκόνταψα γιατί:")
      print(str(exc))
      print("Κάτσε να σκουπιστώ και ξαναπροσπαθώ σε 3 δεύτερα.")
      attempt += 1
      nani(5)
     if attempt >= 3 :
      print("")
      print("Ρε φίλε προσπάθησα 3 φορές. Φαίνεται δεν ταιριάζουμε. Να περάσει ο επόμενος.")
      print("")
      continue
   offset += 10
   cat_offset_url = cat_page + query_mark + "offset=" + str(offset) + "&" + categories

 try :
  write_it_down(e)
 except :
  print("Δεν γράφει.")
 try :
  get_elapsed_time()
 except :
  print("Δεν είναι έτοιμο το χρονόμετρο.")
except KeyboardInterrupt as exc :
 # os.system('cls')
 print("")
 print("Ρε μην τον παίζεις έχουμε δουλειά!")
 try :
  input("Τι να σε κάνω; Πάτα οποιοδήποτε κουμπί για να τελειώσεις... !")
  write_it_down(e)
 except EOFError :
  print("Κάτι σίγουρα δεν πάει καλά. EOFError Και τέτοιες αηδίες.")
 sys.exit(0)
except Exception as exc:
 try :
  input("Κάτι δεν πάει καλά. Δες πάλι τι μου έδωσες και ξανατρέξε.")
  print(str(exc))
 except EOFError :
  print("Κάτι σίγουρα δεν πάει καλά. EOFError Και τέτοιες αηδίες.")
  # sys.exit(0)
 sys.exit(0)
