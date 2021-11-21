def ti_paizei() :
 # com_Kotsovolos_1.0.py
 ### Πιθανό link προϊόντος: https://www.kotsovolos.cy/sound-vision/televisions/led-lcd/229135-null ###
 print("Τρέχουσα έκδοση: 1.0 beta.")
 """
 Επιστρέφει όλα τα προϊόντα της σελίδας του Κοτσώβολου σε ένα excel.
 """
 ############################
 # Current Version 1.0 beta
 ############################
 # Changelog V1.0 beta
 # - Προσθήκη νέου κώδικα για arguments 
 # - Διόρθωση κώδικα σε περίπτωση αναζήτησης με λέξεις (πχ. Corsair) 
 # - Σε περίπτωση query με **, τα αφαιρεί πριν αποθηκεύσει το αρχείο
 # - Προσπάθεια ανάλυσης του στοκ στο CY
 # https://www.e-shop.gr/antallaktikes-sakoyles-aerostegeis-pc-vk-1015eb-28x40cm-50tmx-p-HAP.130298 

try :
 from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
 from random import uniform
 from time import sleep as nani
 from datetime import datetime
 from urllib.request import quote  # enables encoding greek characters in url
 from urllib.parse import unquote  # enables decoding of greek characters
 import requests
 import os
 import sys
 import re
 import xlwt
 import ezodf
except KeyboardInterrupt :
 import sys
 sys.exit(0)
except Exception as exc :
 import sys
 print("Κάτι πάθαμε κατά το import.")
 print(str(exc))
 sys.exit(0)

def get_start_time() :
 global start_time, start_date, file_time
 start = datetime.now()
 start_date = start.strftime("%d-%m-%Y")
 start_time = start.strftime("%H:%M:%S")
 file_time = start.strftime("%H-%M-%S")
 print("Εκκίνηση: " + start_date)
 print("")

def set_files() :
 global ws_write, wb_write, write_file, alt_write_file
 write_file = ("Kotsovolos_list_" + start_date + "_" + file_time + ".xls")
 alt_write_file = ("Kotsovolos_list_ALT_" + start_date + "_" + start_time + ".xls")
 wb_write = xlwt.Workbook()
 ws_write = wb_write.add_sheet("allproducts", cell_overwrite_ok = True)
 ws_write.write(0, 0, "CODE")		# write on A1 cell
 ws_write.write(0, 1, "TITLE")		# write on B1 cell
 ws_write.write(0, 2, "PRICE")		# write on C1 cell
 ws_write.write(0, 3, "DISCOUNT")	# write on D1 cell
 ws_write.write(0, 4, "CATEGORY")	# write on E1 cell
 ws_write.write(0, 5, "AVAIL 1")	# write on F1 cell
 ws_write.write(0, 6, "AVAIL 2")	# write on G1 cell
 ws_write.write(0, 7, "AVAIL 3")	# write on H1 cell
 ws_write.write(0, 8, "AVAIL 4")	# write on I1 cell
 ws_write.write(0, 9, "AVAIL 5")	# write on J1 cell
 ws_write.write(0, 10, "AVAIL 6")	# write  on K1 cell
 ws_write.write(0, 11, "LINK")		# write on L1 cell
 ws_write.write(0, 12, "UP LINK")	# write on L1 cell

def write_results(e, page_url) :
 # print("e in: " + str(e))
 ws_write.write(e, 0, code)
 ws_write.write(e, 1, title)
 ws_write.write(e, 2, init_price)
 ws_write.write(e, 3, discount_price)
 ws_write.write(e, 4, cat)
 ws_write.write(e, 5, ready_to_ship)
 ws_write.write(e, 6, ready_to_deliver)
 ws_write.write(e, 7, ready_pick_up)
 ws_write.write(e, 8, avail_15_days)
 ws_write.write(e, 9, avail_expected)
 ws_write.write(e, 10, avail_upon_order)
 ws_write.write(e, 11, link)
 ws_write.write(e, 12, page_url)

def write_it_down(write_file, noprint) :
 if os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 elif os.path.exists(r"Y:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :
  write_path = (r"Y:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 else :
  write_path = (r"C:\TEMPYTH")
 if noprint == 1 :
  print("Τρέχων φάκελος: " + os.getcwd())
 os.chdir(write_path)
 if noprint == 1 :
  print("Χρησιμοποιώ το " + os.getcwd())
 # wb_write.save(write_file)
 try :
  wb_write.save(write_file)
 except Exception as exc :
  print("Πρόβλημα κατά την αποθήκευση.")
  print(str(exc))
  print("Δοκιμή εγγραφής με το ALT αρχείο.")
  write_file = alt_write_file
  wb_write.save(write_file)
  print("Επιτυχία !!!")
 if noprint == 1 :
  print("")
  print("Το αρχείο: " + write_file + " δημιουργήθηκε στο " + os.getcwd())
 else :
  print('Checkpoint...')

def load_soup(page, wait, retries, headers) :
 global exit_mode
 exit_mode = 0
 # print("Μέσα στη σούπα.")
 temp_wait = round(uniform(0.1, 1.6), 2)
 print('Αναμονή για ' + str(temp_wait) + ' δευτερόλεπτα.')
 print('')
 nani(temp_wait)
 attempt = 0
 while attempt < retries :
  try :
   result = requests.get(page, headers = headers)
   webpage = result.content
   page_soup = soup(webpage, "lxml")
   exit_mode = 0
   break   
  except Exception as exc :
   print("")
   print("Στο φόρτωμα της σελίδας, πέσαμε πάνω στο:")
   print(str(exc))
   print("Ξαναπροσπαθώ σε " + str(retries)+ ".")
   nani(wait)
   attempt += 1
 if attempt == retries :
  print("Προσπάθησα " + str(attempt) + " φορές και δεν τα κατάφερα.")
  exit_mode = 1
  # input()
  # sys.exit(0)
 return(page_soup)

def fill_headers(header_links_container) :
 idx = 0
 for hlink in header_links_container :
  idx += 1
  header_link = hlink.a['href']
  if header_link.find('https://www.kotsovolos.cy') != 0 :
   header_link = 'https://www.kotsovolos.cy' + header_link
  else :
   pass
  if header_link.find('kotsovoloscyprus') >= 0 :
   header_link = header_link.replace('kotsovoloscyprus/', '')
  else :
   pass
  if header_link.find('https://www.kotsovolos.cy/') != 0 :
   print('missing //')
   header_link
   header_link = header_link.replace('https://www.kotsovolos.cy', 'https://www.kotsovolos.cy/')
   header_link
  else :
   pass
  header_links.append(header_link)
  print(str(idx) + ': ' + header_link)
  
 print('') 
 return(header_links)

def fill_subs(sub_links_container) :
 temp_subs = []
 idx = 0
 for i in range(0, len(sub_links_container)) :
  temp_subs = sub_links_container[i].findAll('a')
  for l in range(0, len(temp_subs)) :
   temp_link = temp_subs[l]['href']
   if temp_link == '#' :
    continue
   elif temp_link.find('https://www.kotsovolos.cy') != 0 :
    temp_link = 'https://www.kotsovolos.cy' + temp_link
   else :
    pass
   if temp_link.find('kotsovoloscyprus') >= 0 :
    temp_link = temp_link.replace('kotsovoloscyprus/', '')
    # print('-----------------------')
    # print('Βρήκα: kotsovoloscyprus')
    # print('-----------------------')
   else :
    pass
   if temp_link.find('https://www.kotsovolos.cy/') != 0 :
    # print('missing //')
    # header_link
    temp_link = temp_link.replace('https://www.kotsovolos.cy', 'https://www.kotsovolos.cy/')
    # header_link
   sub_links.append(temp_link)
 for link in sub_links :
  idx += 1
  print(str(idx) + ': ' + link)
 print('')
 return(sub_links)

def get_totals(sub_soup) :
 total_products = sub_soup.find('div', {'class' : 'tools_left'}).div.text.strip()
 total_products = total_products[:total_products.find(' ')]
 pagination = sub_soup.find('ul', {'class', 'pagination'}).text.strip()
 if pagination == '' :
  total_pages = '1'
 else :
  total_pages = pagination[pagination.rfind('\n') + 1:]
 print(total_products + ' Προϊόντα')
 print(str(total_pages))
 print("")
 
 return(int(total_products), int(total_pages))

def get_products(products_containers, page_url, e) :
 global code, link, title, cat, init_price, discount_price, ready_to_ship, ready_to_deliver, ready_pick_up,avail_15_days, avail_expected, avail_upon_order
 for product in products_containers :
  code = '-'
  link = '-'
  title = '-'
  cat = '-'
  init_price = '-'
  discount_price = '-'
  discount = '-'
  ready_to_ship = '-'
  ready_to_deliver = '-'
  ready_pick_up = '-'
  avail_15_days = '-'
  avail_expected = '-'
  avail_upon_order = '-'
  code = product.find('span', {'class', 'prCode'}).text.strip()
  link = product.h2.a['href']
  if link.find('kotsovoloscyprus') >= 0 :
   link = link.replace('kotsovoloscyprus/', '')
  title = product.h2.text.strip()
  title = title.replace('  ',' ')
  if product.find('h2').find('div') :
   cat = product.h2.div.text.strip()
  else :
   cat = "-"
  if product.text.find('κερδίζεις') >= 0 :
   discount = True
   price = product.find('div', {'class' : 'price'}).text.strip().replace('\n', '').replace('\t', '')[4:]
   init_price = price[:price.find('€')]
   discount_price = price[price.find('€') + 1:price.find('ΤΙΜΗ')]
  else :
   discount = False
   price = product.find('div', {'class' : 'price'}).text.strip().replace('\n', '').replace('\t', '')
   init_price = price[1:price.find('ΤΙΜΗ')]
  availabity = product.findAll('div', {'class', 'availability__title'})
  for avail in availabity :
   avail_text = avail.text.strip()
   if avail_text.find('Διαθέσιμο για αποστολή') == 0 :
    ready_to_ship = 'Διαθέσιμο για αποστολή'
   if avail_text.find('Διαθέσιμο για παράδοση σε 24 ώρες') == 0 :
    ready_to_deliver = 'Διαθέσιμο για παράδοση σε 24 ώρες'
   if avail_text.find('Διαθέσιμο για παραλαβή σε 20') == 0 :
    ready_pick_up = 'Διαθέσιμο για παραλαβή σε 20'
   if avail_text.find('Διαθέσιμο εντός 15 ημερών') == 0 :
    avail_15_days = 'Διαθέσιμο εντός 15 ημερών'
   if avail_text.find('Αναμένεται Σύντομα') == 0 :
    avail_expected = 'Αναμένεται Σύντομα'
   if avail_text.find('Κατόπιν Παραγγελίας') == 0 :
    avail_upon_order = 'Κατόπιν Παραγγελίας'
  write_results(e, page_url)
  e += 1
  print(code)
  print(link)
  print(title)
  print(cat)
  print(init_price)
  if discount != '-' :
   print(discount_price)
  if ready_to_ship != '-' :
   print(ready_to_ship)
  if ready_to_deliver != '-' :
   print(ready_to_deliver)
  if ready_pick_up != '-' :
   print(ready_pick_up)
  if avail_15_days != '-' :
   print(avail_15_days)
  if avail_expected != '-' :
   print(avail_expected)
  if avail_upon_order != '-' :
   print(avail_upon_order)
  print('')
 
 return(e) 

def initialize():
 ti_paizei = False
 trial_run = 0
 start_from = 1
 wait = 5
 retries = 3
 header_links = []
 sub_links = []
 index_text = '?beginIndex='
 index = 0
 e = 1
 headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
 if ti_paizei == True :
  ti_paizei()
 else:
  pass
 return ti_paizei, trial_run, start_from, wait, retries, header_links, sub_links, index_text, index, e, headers

try :
 ti_paizei, trial_run, start_from, wait, retries, header_links, sub_links, index_text, index, e, headers = initialize()
 get_start_time()
 set_files()
 page = 'https://www.kotsovolos.cy/'
 page_soup = load_soup(page, wait, retries, headers)
 header_links_container = page_soup.findAll('ul', {'class' : 'level3'})
 sub_links_container = page_soup.findAll('ul', {'class' : 'level4'})
 header_links = fill_headers(header_links_container)
 sub_links = fill_subs(sub_links_container) 
 # for page_url in sub_links :
 for p in range(start_from - 1, len(sub_links)) :
  page_url = sub_links[p]
  index = 0
  print('')
  print('')
  print('')
  print("index: " + str(index))
  print('Upper page: ' + page_url)
  print('')
  sub_soup = load_soup(page_url, wait, retries, headers)
  if exit_mode == 1 :
   continue
  else :
   pass
  try :
   if sub_soup.find('h2') :
    h2_is_there = True
   else :
    h2_is_there = False
  except :
   h2_is_there = False
  if h2_is_there == True :
   if sub_soup.h2.text.find('Κάτι δεν πήγε καλά') >= 0 :
    continue
   else :
    pass
  else :
   continue
  total_products, total_pages = get_totals(sub_soup)
  if total_products == 0 :
   continue
  for i in range (0, total_pages) :
   print("Σελίδα " + str(i + 1))
   products_containers = sub_soup.findAll('div', {'class' : 'productWrap'})
   print(str(e))
   e = get_products(products_containers, page_url, e)
   print(str(e))
   index += 15
   current_url = page_url + index_text + str(index)
   print("index: " + str(index))
   print(current_url)
   print('')
   sub_soup = load_soup(current_url, wait, retries, headers)
  write_it_down(write_file, 0)
 write_it_down(write_file, 1)
 # page_url = sub_links[0]
 # sub_soup = load_soup(page_url, wait, retries, headers)
 # print('')
 # print('')
 # print('')
 # print(sub_links[0])
 # print('')
 # total_products, total_pages = get_totals(sub_soup)
 # for i in range (0, int(total_pages)) :
  # print("Σελίδα " + str(i + 1))
  # products_containers = sub_soup.findAll('div', {'class' : 'productWrap'})
  # get_products(products_containers)
  # index += 15
  # current_url = page_url + index_text + str(index)
  # sub_soup = load_soup(current_url, wait, retries, headers)
except KeyboardInterrupt :
 try :
  print("")
  input("Διαλλειματάκι;")
  print("")
 except :
  write_it_down(write_file, 1)
  sys.exit(0)
except Exception as exc:
 print("Εξαίρεση: " + str(exc))
 write_it_down(write_file, 1)

