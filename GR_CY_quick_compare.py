from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote, Request  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
import ezodf  # for the ability to open and write open document format (ODF) files
from xlutils.copy import copy
from xlrd import open_workbook
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
from time import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

def get_start_time() :
 global start_time, start_date
 start_time = time()  # set starting time
 today = date.today()  # set starting date
 start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
 print("")
 print("Το script ξεκίνησε στις " + start_date)

def get_elapsed_time() :
 elapsed_time = time() - start_time
 minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
 mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
 seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
 seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
 formatted_time = str(mins) + "." + str(seconds)
 print("")
 # print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
 sys.exit("Το script χρειάστηκε: " + str(mins) + " λεπτά και " + str(seconds) + " δευτερόλεπτα (" + str(round(elapsed_time, 2)) + " δευτερόλεπτα).")

def write_results_gr(e) :
 # print("e in: " + str(e))
 ws_write_gr.write(e, 0, gr_prod_per) 		# OK
 ws_write_gr.write(e, 1, gr_prod_title)	# OK
 ws_write_gr.write(e, 2, gr_prod_price)	# OK

def write_results_cy(e) :
 # print("e in: " + str(e))
 ws_write_cy.write(e, 0, cy_prod_per) 	# OK
 ws_write_cy.write(e, 1, cy_prod_title)	# OK
 ws_write_cy.write(e, 2, cy_prod_price)	# OK

def save_progress() :
 try :
  wb_write.save(write_file)
 except :
  wb_write.save(alt_write_file)

def write_it_down() :
 try :
  wb_write.save(write_file)
  print("")
  print("Το αρχείο '" + write_file + "' δημιουργήθηκε στο φάκελο '" + write_path + "'")
 except :
  print("")
  wb_write.save(alt_write_file)
  print("Το αρχείο '" + alt_write_file + "' δημιουργήθηκε στο φάκελο '" + write_path + "'")

offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # represents the row inside the excel file.
attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
answer_term = "no"
os.system('cls')

while (answer_term == "no") :
 print("Δώσε link...")
 grpage = input()
 if grpage.find("http") >= 0 :
  query_term = grpage[grpage.rfind('/')+1:]
  print("")
  answer_text = "Έδωσες: " + grpage + ". Είναι σωστό; Πάτα ENTER για ναι. "
  answer_term = input(answer_text)
  print("Κρατάω τους όρους αναζήτησης: " + query_term)
 else :
  os.system('cls')
  print("Δεν είναι link αυτό. Για προσπάθησε πάλι.")
  print("")

get_start_time()

if os.path.exists(r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 print("Χρησιμοποιώ το '" + write_path + "' για την αποθήκευση των αρχείων.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
 write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 print("Χρησιμοποιώ το '" + write_path + "' για την αποθήκευση των αρχείων.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
 write_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 print("Χρησιμοποιώ το '" + write_path + "' για την αποθήκευση των αρχείων.")
 print("")
else :
 attempt = 0
 while attempt < 3 :
  write_path = input("Δεν βρέθηκαν οι προκαθορισμένοι φακέλοι. Που να το βάλω το αρχείο; ")
  if os.path.exists(write_path) == False :
   print("Δεν βρέθηκε ο φάκελος. Πάμε πάλι...")
   print("")
   attempt += 1
 print("Προσπάθησα 3 φορές. Τα παρατάω.")
 sys.exit(0)  

# Opening files
os.chdir(write_path)
write_file = ("gr-cy-analysi.xls")  # path to xslx write file
alt_write_file = ("gr-cy-analysi_alt.xls")   # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write_gr = wb_write.add_sheet("GR", cell_overwrite_ok = True)  # add sheet in virtual workbook named after the search string ad run date
ws_write_gr.write(0, 0, "CODE")		# write CODE on A1 cell
ws_write_gr.write(0, 1, "GR-TITLE")	# write TITLE on B1 cell
ws_write_gr.write(0, 2, "GR-PRICE")	# write OEM on C1 cell
ws_write_gr.write(0, 3, "CY-TITLE")	# write GR-PRICE on D1 cell
ws_write_gr.write(0, 4, "CY-PRICE")	# write GR-CAT on E1 cell
ws_write_gr.write(0, 5, "PRICE-DIF")# write GR-SUBCAT on F1 cell

### GR page processing starts

print("-----------------------------------")
print("| Ξεκινάμε την ελληνική σελίδα... |")
print("-----------------------------------")
req = Request(grpage, headers = headers)
attempt = 0
while attempt < 3 :
 try :
  # print("On try :" + str(attempt))
  gr_uClient = uReq(req)
  gr_page_soup = soup(gr_uClient.read(), "html5lib")
  gr_uClient.close()
  # gr last page preparations
  next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
  next_pages_single = gr_page_soup.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})  # find all next page buttons assuming this is a category based single query page
  break
 except Exception as exc :
  # print("On except :" + str(attempt))
  print("Ούπς, έπεσα πάνω στην ακόλουθη εξαίρεση: " + str(exc))
  print("Ξαναπροσαθώ σε 5 δευτερόλεπτα.")
  attempt += 1
  time.sleep(5)

if gr_page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories
# https://www.e-shop.gr/ilektrikes-syskeues-ilektrikes-skoupes-1001w-eos-1200w-list?table=HAP&category=%C7%CB%C5%CA%D4%D1%C9%CA%C5%D3+%D3%CA%CF%D5%D0%C5%D3&filter-12563=1
 print("Χειρίζομαι την σελίδα σαν αναζήτηση προϊόντων πίνακα με κατηγορίες.")
 print("")
 if gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'}) :  # if the page has next buttons 
  next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
  total_next_pages = next_pages_category[len(next_pages_category)-1].text  # total next pages is in the last total_next_pages (-1 for indexing)
  print("Σύνολο 'επόμενων' σελίδων: " + str(total_next_pages))
  gr_cat_page, query_mark, categories = str(grpage).partition("?")
  gr_cat_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
  last_offset = (int(total_next_pages) - 1) * 10
  gr_last_cat = gr_cat_page + query_mark + "offset=" + str(last_offset) + "&" + categories
  req = Request(gr_last_cat, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    gr_last_uClient = uReq(req)
    gr_last_page_soup = soup(gr_last_uClient.read(), "html5lib")
    gr_last_uClient.close()
    last_prod = gr_last_page_soup.findAll('table', {'class': 'web-product-container'})
    total_prod = len(last_prod) + last_offset
    tp = total_prod
    break
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("Ούπς, έπεσα πάνω στην ακόλουθη εξαίρεση: " + str(exc))
    print("Ξαναπροσαθώ σε 5 δευτερόλεπτα.")
    attempt += 1
    time.sleep(5)
  print("Βρήκα " + str(total_prod + 1) + " προϊόντα.")
  # print("")
  # for q in range(0, int(total_next_pages)) :
  for q in range(0, int(total_next_pages)) :
   # print("Τρέχουσα σελίδα: " + gr_cat_offset_url + " #" + str(q))
   req = Request(gr_cat_offset_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     gr_uClient = uReq(req)
     gr_page_soup = soup(gr_uClient.read(), "html5lib")
     gr_uClient.close()
     containers = gr_page_soup.findAll('table', {'class': 'web-product-container'})
     break
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("Ούπς, έπεσα πάνω στην ακόλουθη εξαίρεση: " + str(exc))
     print("Ξαναπροσαθώ σε 5 δευτερόλεπτα.")
     attempt += 1
     time.sleep(5)
   print("")
   print("Τρέχουσα σελίδα: " + str(q + 1) + " / " + str(total_next_pages))
   print("")
   for container in containers :
    tp = tp - 1
    print("Προϊόν: " + str(total_prod - tp) + " / " + str(total_prod + 1) + ". Απομένουν: " + str(total_prod + 1 - (total_prod - tp)))
    gr_prod_per = container.font.text.replace("(", "").replace(")", "")
    # print(gr_prod_per)
    gr_prod_title = container.h2.text
    if container.find("font", {"style": "color:#FF0000"}) :
     gr_prod_price = container.find("font", {"style": "color:#FF0000"}).text.strip().replace("\xa0€", "").replace('.',',')
    else :
     gr_prod_price = container.find("td", {"class": "web-product-price"}).text.strip().replace("\xa0€", "").replace('.',',')
    print("Κωδικός: " + gr_prod_per + ", Τίτλος: " + gr_prod_title + ", Τιμή: " + gr_prod_price + "€")
    write_results_gr(e)
    e += 1
   save_progress()
   offset += 10  # ADD 10 TO THE URL OFFSET VALUE
   gr_cat_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
 print("")
 print("--------------------------------------")
 print("| Τελειώσαμε με την ελληνική σελίδα. |")
 print("--------------------------------------")
 
 ### GR page processing finished
 ### CY page processing starts

 ws_write_cy = wb_write.add_sheet("CY", cell_overwrite_ok = True)  # add sheet in virtual workbook named after the search string ad run date
 ws_write_cy.write(0, 0, "CODE")		# write CODE on A1 cell
 ws_write_cy.write(0, 1, "CY-TITLE")	# write TITLE on B1 cell
 ws_write_cy.write(0, 2, "CY-PRICE")	# write PRICE on C1 cell
 offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
 e = 1  # represents the row inside the excel file.
 cypage = "https://www.eshopcy.com.cy/" + query_term
 attempt = 0  # how many attempts to re-read the url in case of failure
 print("")
 print("-----------------------------------")
 print("| Ξεκινάμε την κυπριακή σελίδα... |")
 print("-----------------------------------")
 req = Request(cypage, headers = headers)
 while attempt < 3 :
  try :
   # print("On try :" + str(attempt))
   cy_uClient = uReq(req)
   cy_page_soup = soup(cy_uClient.read(), "html5lib")
   cy_uClient.close()
   # gr last page preparations
   next_pages_category = cy_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
   next_pages_single = cy_page_soup.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})  # find all next page buttons assuming this is a category based single query page
   break
  except Exception as exc :
   # print("On except :" + str(attempt))
   print("Ούπς, έπεσα πάνω στην ακόλουθη εξαίρεση: " + str(exc))
   print("Ξαναπροσπαθώ σε 5 δευτερόλεπτα.")
   attempt += 1
   time.sleep(5)

 if cy_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'}) :  # if the page has next buttons 
  next_pages_category = cy_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
  total_next_pages = next_pages_category[len(next_pages_category)-1].text  # total next pages is in the last total_next_pages (-1 for indexing)
  print("Σύνολο 'επόμενων' σελίδων: " + str(total_next_pages))
  cy_cat_page, query_mark, categories = str(cypage).partition("?")
  cy_cat_offset_url = cy_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
  last_offset = (int(total_next_pages) - 1) * 10
  cy_last_cat = cy_cat_page + query_mark + "offset=" + str(last_offset) + "&" + categories
  req = Request(cy_last_cat, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    cy_last_uClient = uReq(req)
    cy_last_page_soup = soup(cy_last_uClient.read(), "html5lib")
    cy_last_uClient.close()
    last_prod = cy_last_page_soup.findAll('table', {'class': 'web-product-container'})
    total_prod = len(last_prod) + last_offset
    tp = total_prod
    break
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("Ούπς, έπεσα πάνω στην ακόλουθη εξαίρεση: " + str(exc))
    print("Ξαναπροσαθώ σε 5 δευτερόλεπτα.")
    attempt += 1
    time.sleep(5)
  print("Βρήκα " + str(total_prod + 1) + " προϊόντα.")
  # print("")
  # for q in range(0, int(total_next_pages)) :
  for q in range(0, int(total_next_pages)) :
   # print("Τρέχουσα σελίδα: " + cy_cat_offset_url + " #" + str(q))
   req = Request(cy_cat_offset_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     cy_uClient = uReq(req)
     cy_page_soup = soup(cy_uClient.read(), "html5lib")
     cy_uClient.close()
     containers = cy_page_soup.findAll('table', {'class': 'web-product-container'})
     break
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("Ούπς, έπεσα πάνω στην ακόλουθη εξαίρεση: " + str(exc))
     print("Ξαναπροσαθώ σε 5 δευτερόλεπτα.")
     attempt += 1
     time.sleep(5)
   print("")
   print("Τρέχουσα σελίδα: " + str(q + 1) + " / " + str(total_next_pages))
   print("")
   for container in containers :
    tp = tp - 1
    print("Προϊόν: " + str(total_prod - tp) + " / " + str(total_prod + 1) + ". Απομένουν: " + str(total_prod + 1 - (total_prod - tp)))
    cy_prod_per = container.font.text.replace("(", "").replace(")", "")
    # print(cy_prod_per)
    cy_prod_title = container.h2.text
    if container.find("font", {"style": "color:#FF0000"}) :
     cy_prod_price = container.find("font", {"style": "color:#FF0000"}).text.strip().replace("\xa0€", "").replace('.',',')
    else :
     cy_prod_price = container.find("td", {"class": "web-product-price"}).text.strip().replace("\xa0€", "").replace('.',',')
    print("Κωδικός: " + cy_prod_per + ", Τίτλος: " + cy_prod_title + ", Τιμή: " + cy_prod_price + "€")
    write_results_cy(e)
    e += 1
   save_progress()
   offset += 10  # ADD 10 TO THE URL OFFSET VALUE
   cy_cat_offset_url = cy_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
 print("")
 print("--------------------------------------")
 print("| Τελειώσαμε με την κυπριακή σελίδα. |")
 print("--------------------------------------")

else :
 print("Δεν είναι σωστή η δομή της σελίδας. Μήπως έβαλες λάθος το link;")
 sys.exit(0)
 
write_it_down()

get_elapsed_time()
