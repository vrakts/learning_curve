def ti_paizei() :
 # GR_CY_Query_availability
 """
 # Τρέχει ανταγωνισμό GR vs CY πάνω σε όρους αναζήτησης ή ολόκληρη σελίδα
 # ή από προκαθορισμένο αρχείο με έτοιμη λίστα κωδικών.
 # Επιστρέφει τίτλο, κατηγορία υποκατηγορία μάρκα και τιμή και για τα 2 site
 # παίρνει την περιγραφή από το GR και διορθώνει όλα τα λάθη.
 """
 ############################
 # Current Version 1.5.1 beta
 ############################
 # Changelog V1.5.1 beta
 # - Συμμάζεμα επαναλαμβανόμενου κώδικα μέσα στο def totals()
 # - Βρίσκει αν η σελίδα περιέχει το κουμπι "Όλα τα προϊόντα" και διορθώνει
 """# - Χρήση νέου κώδικα για την επιλογή φύλλου και στήλης"""
 ##########################
 # Changelog V1.5 beta
 # - Προσθήκη κώδικα μέσα σε defs
 # - Βρίσκει αν η σελίδα περιέχει το κουμπι "Όλα τα προϊόντα" και διορθώνει
 # - Χρήση νέου κώδικα για τις εξαιρέσεις
 # - Χρήση νέου κώδικα για το άνοιγμα της σελίδας
 # - Χρήση νέου κώδικα για το μέτρημα του χρόνου (θέλει λίγη δουλίτσα)
 # - Χρήση νέου κώδικα για την επιλογή/δημιουργία φακέλων
 # - Χρήση νέου κώδικα για την αποθήκευση του αρχείου
 # - Σωστή χρήση Imports
 ##########################
 # Changelog V1.4.3 beta
 # - Updated for https and e-shop.cy
 ### recent description changes:
 # added a line for the gr_desc_text.find for DOA conditions
 # added correction lines for 1 year warranties
 # added correction for '΄' hyphen in Ά
 # removes the Red constantia fonts from the gr description
 # corrected the categories and brand calculation
 # included the new EAN and barcode methods as well
 ##########################
 # Changelog V1.4.2 beta
 # - More improvments in the description process
 # - All of the script uses the def functions now. Still trying it out
 # - URL read errors are now caught more accurately
 #	and in the same while loop the soup function is included
 #	as it seems that some errors are not caused by the URL read.
 # - Calculates price difference if product found in both sites.
 ##########################
 # Changelog V1.4.1 beta
 # - Improved the gr_desc_text process a bit
 # - Uses functions for details and description
 #	currently testing only on the file option (early beta test)
 # - Tries to catch file name errors
 ##########################
 # Changelog V1.4 beta
 # - Small warranty corrections made in predefined file.
 # - Gets category, subcategory and brand from GR and CY 
 #	plus availability from the GR website
 # - Reads the description from GR, seperates the OEM code and barcode
 # - Recognises Lifetime and laptop warranty and removes the 2nd DOA link
 # - Recognises ASUS laptops warranty and corrects the text
 # - Strips the align and crazy codes from description
 # - Corrects wrong warranty texts
 # - Gets the relevant products
 # - Experimental: Uses a catch for errors while reading the URL
 # - In progress: corrections in the description procedure
 #	to auto correct the years of warranty and "." at the end.
 ##########################
 # Changelog V1.3
 # - Can determine if the result is a search result page
 #	a category search page, a single item result or 
 #	an empty search result.
 # - Updated xls writing functions - Need to check
 # - URL read error trap.
 ##########################
 # Changelog V1.2
 # - Can decode and encode Greek characters for correct URL binding
 ##########################
 # Changelog V1.1
 # - Included the updated more accurate next page sequence
 # - Asks for query term
 # - Can now save both GR and CY results to a preconfigured xls file
 # - Calculates total number of products accurately (not used currently but might be useful)
 # - Returns availability for GR and CY
 # - New folder calculation function decides 
 #	which folder to read from and write on
 # - Will try to write to the default file and 
 #	if error occurs will write to a 2nd one
 ##########################
 # Changelog V1.0
 # - Returns all products from the GR and CY page 
 #	from a preconfigured query term only
 # - Writes 2 seperate files for GR and CY with results
 ##########################
 # To Do: Add sort specs on pages that support it in results
 # To Do: To further enhance the above, try and find the category 
 #		  of the product and get sort specs for all results
 # To Do: calculate the correct price for the CY page for upload
 # To Do: Refine the description code for the align justify BS from GR
 #		  for now it erases the crazy tag and adds p align at the start
 #		  but can't recognise if the description is empty.
 #		  17/01 update: align and crazy tags are correct.
 # To Do: Refine the warranty text. The "." should be always at the end
 # To Do: add </li> at the end of some warranties
 # To Do: Να ζητάει τον φάκελο που περιέχει το αρχειο
 #		  να εμφανίζει όλα τα αρχεία του φακέλου αριθμημένα και επιλογή χρήστη.
 # To Do: Να κρατάει logs
 # To Do: Time keeping
 # To Do: Να μαζεύει όλα τα προϊόντα σε λίστα και να τα τρέχει
 # To Do: Κατηγορία με μάρκα μόνο - works
 # https://www.e-shop.gr/esperanza-ep118kg-bluetooth-speaker-piano-black-green-p-TEL.046138
 # To Do: Κατηγορία με υποκατηγορία και μάρκα - works
 # https://www.e-shop.gr/ilektrikos-triftis-karykeymaton-esperanza-ekp003k-p-HAP.262314
 # To Do: Κατηγορία με υποκατηγορία χωρίς μάρκα - works
 # https://www.e-shop.gr/ziggurat-p-XB1.00278
 # To Do: Κατηγορία μόνο - works
 # https://www.e-shop.gr/antallaktikes-sakoyles-aerostegeis-pc-vk-1015eb-28x40cm-50tmx-p-HAP.130298 
 print("Τρέχουσα έκδοση: 1.5 beta.")

try :
 from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
 from random import randint
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

""" needs new code """
def get_start_time_old() :
 global start_time, start_date
 start_time = time()  # set starting time
 today = date.today()  # set starting date
 start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
 print("Script started at " + start_date)
 print("")

""" new start date code """
def get_start_time() :
 global start_time, start_date
 start = datetime.now()
 start_date = start.strftime("%d-%m-%Y")
 start_time = start.strftime("%H:%M:%S")
 print("Εκκίνηση: " + start_date)
 print("")
 
""" needs new code """
def get_elapsed_time() :
 elapsed_time = time() - start_time
 minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
 mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
 seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
 seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
 formatted_time = str(mins) + "." + str(seconds)
 print("")
 # print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
 sys.exit("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")

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

def get_cy_details(page_soup) :
 global cy_prod_title, cy_price_dif, cy_price_text, cy_cat, cy_subcat, cy_brand, price_dif, pd
 gr_price_dif = '0'
 # pd = 0
 # print("Just initialized pd.")
 cy_prod_title = page_soup.h1.text
 cy_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(cy_price) == 0 :
  cy_price_text = "Εξαντλημένο"
  cy_price_dif = "-"
 else :
  cy_price_dif = cy_price[0].text.replace("\xa0€", "")
  # print(cy_price_dif)
  cy_price_text = cy_price_dif.replace(".", ",")
 if len(cy_prod_title) == 0 :
  cy_price_text = "Θέλει άνοιγμα"
  cy_cat = ""
  cy_subcat = ""
  cy_brand = ""
 else :
  cy_categories = page_soup.findAll('td', {'class': 'faint1'})
  if len(cy_categories) == 0 :
   gr_cat = "-"
   gr_brand = "-"
   gr_subcat = ""
  elif cy_categories[1].text.find(' •') > 0 :
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
 try :
  price_dif = round(float(cy_price_text.replace(',', '.')) - float(gr_price_text.replace(',', '.')),2)
  # print("Price Difference: " + str(price_dif) + ".")
  # print("Changing pd to 1.")
  # pd = 1
 except :
  print("Δεν βρέθηκε τιμή ούτε στο GR ούτε στο CY.")
  price_dif = "-"

def get_gr_description(page_soup, prod_per, gr_cat) :
 # global string, warranty, rest, gr_oem, barcode, gr_desc_result
 global gr_oem, barcode, gr_desc_result
 gr_desc_text = ""
 gr_oem = ""
 barcode = ""
 gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  gr_desc_text = ""
  gr_oem = ""
  barcode = ""
  # print("initialized gr_desc_text, oem and barcode")
 else :
  gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html values and any .gr mentions
  # print(gr_desc_text)
  if gr_desc_text.find('Eγγύηση') > 0 :
   gr_desc_text.replace('Εγγύηση', '')
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
  if gr_desc_text.find('Barcode:') > 0 or gr_desc_text.find('EAN-13:') > 0 :  # if both barcode and OEM exists
   print("Υπολογίζω barcodes...")
   if gr_desc_text.find('<br><br>Barcode:') > 0 :
    string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode:')  # seperate the text
   elif gr_desc_text.find('<br><br>EAN-13:') > 0 :
    string, barcode, rest = gr_desc_text.rpartition('<br><br>EAN-13:')  # seperate the text
   elif gr_desc_text.find('EAN-13:') > 0 :
    string, barcode, rest = gr_desc_text.rpartition('EAN-13:')  # seperate the text
   else :
    string, barcode, rest = gr_desc_text.rpartition('Barcode:')  # seperate the text
   gr_desc_text = string.strip() # keep only what is before the barcode
  if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
   print("Κάνω μερικά crazy πράγματα...")
   crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
   gr_desc_text = rest.strip()  # keep only the rest of the text
  if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
   print("Aligning στις γωνίες...")
   p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
   gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
  else :
   gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
  if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
   print("Γράφω warranties...")
   if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
    string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
   elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
    string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
   if gr_prod_title.find('ASUS') > 0 or gr_prod_title.find('DELL') > 0 :
    # warranty_text = ' <a href="https://www.e-shop.cy/page?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b></li>'
    warranty_text = ' '
   else :
    warranty_text = ' .</b> </li>'
   gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
  elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
   if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
    string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
   elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
    string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
   gr_desc_text = string + "Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
  elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
   print("Ελαττώματα DOA...")
   string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
   gr_desc_text = string + rest.strip()  # and keep the before and after text
  elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
   print("Ελαττώματα DOA...")
   string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
   gr_desc_text = string + rest.strip()  # and keep the before and after text
  else :
   print("Τίποτα το ιδιαίτερο σε αυτή την εγγύηση.")
  if gr_desc_text.find('<p></p>') > 0 :
   gr_desc_text.replace('<p></p>', '') 
  if gr_desc_text.find('<b>Εγγύηση') >= 0 or gr_desc_text.find('Εγγύηση:') >= 0 :
   war_start = gr_desc_text.find('Εγγύηση:')
   ### if the years are misspelled it is not autocorrected in the CY site. Not looking for "." at the end.
   if gr_desc_text[war_start:].find("1 Χρόνος") > 0 or gr_desc_text[war_start:].find("1 χρόνος") > 0 or gr_desc_text[war_start:].find("1 Χρόνο") > 0 or gr_desc_text[war_start:].find("1 χρόνο") > 0 or  gr_desc_text[war_start:].find("1 Χρονο") > 0 or gr_desc_text[war_start:].find("1 χρονο") > 0 or gr_desc_text[war_start:].find("1 Έτος") > 0 or gr_desc_text[war_start:].find("1 έτος") > 0 or gr_desc_text[war_start:].find("1 Ετος") > 0 or gr_desc_text[war_start:].find("1 ετος") > 0 or  gr_desc_text[war_start:].find("2 Έτη") > 0 or gr_desc_text[war_start:].find("2 έτη") > 0 or gr_desc_text[war_start:].find("24 Μήνες") > 0 or gr_desc_text[war_start:].find("24 μήνες") > 0 :
    print("Χρονικό προσαρμογής...")
    gr_desc_text = gr_desc_text.replace('1 Χρόνος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 χρόνος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 Χρόνο', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 χρόνο', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 Χρονο', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 χρονο', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 Έτος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 έτος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 Ετος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 ετος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('2 Έτη', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('2 έτη', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('24 Μήνες', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('24 μήνες', '2 χρόνια')
    # if gr_desc_text[war_start:].find("2 χρόνια.") >= 0  or gr_desc_text[war_start:].find("2 χρόνια.") >= 0 :
     # print("Dot avoided.")
    # # elif gr_desc_text[war_start:].find("2 χρόνια") >= 0 or gr_desc_text[war_start:].find("2 χρόνια") >= 0 :
    # else :
     # desc, war, rest = gr_desc_text.partition('2 χρόνια')
     # gr_desc_text = desc + war + "." + rest
     # print("Dotted.")
  if gr_desc_text.find("Ά") > 0 or gr_desc_text.find("’") > 0 or gr_desc_text.find('face="Constantia" size="3"') > 0 or gr_desc_text.find('size="3" face="Constantia"') > 0 :
   print("Πετάω τα σκουπίδια...")
   gr_desc_text = gr_desc_text.replace("Ά", "&#902;")
   gr_desc_text = gr_desc_text.replace("’", "&#902;")
   gr_desc_text = gr_desc_text.replace('face="Constantia" size="3"', '')
   gr_desc_text = gr_desc_text.replace('size="3" face="Constantia"', '')
  if gr_desc_text == '<p align="justify">' or gr_desc_text == '<p align="justify"><br><br>' :
   print("Πετάω τα αποφάγια...")
   gr_desc_text = ""
  if gr_desc_text.find('Μάυρο') >= 0 :
   print('Κοίτα κάτι χρώματα...')
   gr_desc_text.replace('Μάυρο', 'Μαύρο')
 if prod_per.find('EPI.') >= 0 :
  if gr_cat.find('ΟΠΛΑ ΜΕ ΑΦΡΩΔΗ ΒΕΛΑΚΙΑ') >= 0 :
   gr_desc_text = gr_desc_text + '<p align="justify"><b><u><font style="color:#ff0000;">ΠΡΟΣΟΧΗ!</font></u></b> Δεν είναι κατάλληλο για παιδιά κάτω των 36 μηνών. Απαραίτητη η επίβλεψη ενηλίκου. Μην στοχεύετε στα μάτια ή το πρόσωπο. <b>ΓΙΑ ΑΠΟΦΥΓΗ ΤΡΑΥΜΑΤΙΣΜΟΥ</b>: Χρησιμοποιήστε μόνο τα βελάκια που είναι σχεδιασμένα για αυτό το προϊόν. Μην τροποποιήσετε τα βελάκια ή τον εκτοξευτή.</p>'
  elif gr_cat.find('DARTBOARD') >= 0 :
   gr_desc_text = gr_desc_text + '<p align="justify"><b><u><font style="color:#ff0000;">ΠΡΟΣΟΧΗ!</font></u></b> Δεν είναι κατάλληλο για παιδιά κάτω των 36 μηνών. Κίνδυνος πνιγμού λόγω ύπαρξης μικρών και μυτερών κομματιών. Απαραίτητη η επίβλεψη ενηλίκου. Συνιστώμενη ελάχιστη ηλικία 8 ετών και άνω.</p>'
  else :
   gr_desc_text = gr_desc_text + '<p align="justify"><b><u><font style="color:#ff0000;">ΠΡΟΣΟΧΗ!</font></u></b> Δεν είναι κατάλληλο για παιδιά κάτω των 36 μηνών.</p>'
 while gr_desc_text.find('  ') >= 0 :
  print("Σε ένα άδειο loop")
  gr_desc_text = gr_desc_text.replace('  ', '')
  # print(gr_desc_text)
 gr_desc_result = gr_desc_text.strip()

def write_results(e) :
 # print("e in: " + str(e))
 ws_write.write(e, 0, gr_prod_per) 		# OK
 ws_write.write(e, 1, gr_prod_title)	# OK
 ws_write.write(e, 2, gr_oem.strip())	# OK
 ws_write.write(e, 3, gr_price_text)	# OK
 ws_write.write(e, 4, gr_cat)			# OK
 ws_write.write(e, 5, gr_subcat)		# OK
 ws_write.write(e, 6, gr_brand)			# OK
 ws_write.write(e, 7, sxetika_list)		# OK
 ws_write.write(e, 8, gr_desc_result)	# OK
 ws_write.write(e, 9, gr_a_text)		# OK
 ws_write.write(e, 10, cy_prod_title)	# OK
 ws_write.write(e, 11, cy_price_text)	# OK
 ws_write.write(e, 12, cy_cat)			# OK
 ws_write.write(e, 13, cy_subcat)		# OK
 ws_write.write(e, 14, cy_brand)		# OK
 try :
  ws_write.write(e, 15, price_dif)		# OK
 except :
  ws_write.write(e, 15, "-")	 		# OK
 try :
  ws_write.write(e, 16, str(sheet[i, 3].value.replace('+', '')))
 except :
  ws_write.write(e, 16, "")

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
 wb_write.save(write_file)
 try :
  wb_write.save(write_file)
 except Exception as exc :
  print(str(exc))
  write_file = alt_write_file
  wb_write.save(write_file)
 print("")
 print("Το αρχείο: " + write_file + " δημιουργήθηκε στο " + os.getcwd())

def choices() :
 global your_choice, answer_term, query_term, upload_file, read_sheet, read_column, gr_url, ws_write, wb_write, write_file
 answer_term = "no"
 while (answer_term == "no") :
  print("Τι ψάχνουμε?")
  print("")
  print("1. Από αρχείο.")
  print("2. Όρος αναζήτησης ή σύνδεσμος.")
  your_choice = input("Δώσε την επιλογή σου: ")
  if your_choice == "1" :
   upload_file = input("Δώσε το όνομα του αρχείου: ")
   if upload_file[-4:] != ".ods" :
    upload_file = upload_file + ".ods"
   answer_text = "Το όνομα του αρχείου είναι: " + upload_file + ". Σωστά? Πάτα enter για 'ναι'. "
   answer_term = input(answer_text)
   read_sheet = input("Δώσε τον αριθμό του φύλλου? (default 1): ")
   if read_sheet == "" :
    read_sheet = 0
    print("Κρατάω τον default αριθμό φύλλου: " + str(read_sheet + 1) + " (index: " + str(read_sheet) + ")")
    print("")
   else :
    print("Το φύλλο ανάγνωσης θα είναι " + str(read_sheet) + " (index: " + str(int(read_sheet) - 1) + ")")
    print("")
    read_sheet = int(read_sheet) - 1
   read_column = input("Δώσε αριθμό στήλης? (default 3): ")
   if read_column == "" :
    read_column = 2
    print("Κρατάω τον default αριθμό στήλης: " + str(read_column + 1) + " (index: " + str(read_column) + ")")
    print("")
   else :
    print("Η στήλη ανάγνωσης θα είναι " + read_column + " (index: " + str(int(read_column) - 1) + ")")
    print("")
    read_column = int(read_column) - 1
  elif your_choice == "2" :
   query_term = input("Δώσε τον όρο αναζήτησης: ")
   query_term = query_term.replace(" ", "+")
   answer_text = "Έδωσες: " + query_term + ". Σωστά? Πάτα enter για 'ναι'. "
   answer_term = input(answer_text)
  else :
   os.system('cls')
   print("Λάθος επιλογή. Προσπάθησε ξανά.")
  print("")

   
 if your_choice == "1" :
  try :
   ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
   spreadsheet = ezodf.opendoc(upload_file)  # open file
   ezodf.config.reset_table_expand_strategy()  # reset ezodf config
  except Exception as exc :
   type, value, traceback = sys.exc_info()
   print("Ώπα πέσαμε στην παρακάτω εξαίρεση:")
   # print(value)
   print(sys.exc_info())
   # print(exc)
   sys.exit("Πιθανώς λάθος στο όνομα του αρχείου. Έλεγξε το όνομα / επέκταση και προσπάθησε ξανά.")
  if upload_file.find("ods") > 0 or upload_file.find("xls") > 0 :
   analysis_file = upload_file[:upload_file.find(".")]
  else :
   analysis_file = upload_file
  write_file = (analysis_file + " - Products_Upload_Analysis.xls")  # path to xslx write file
  alt_write_file = (analysis_file + " - Products_Upload_Analysis_ALT.xls")   # alternate name of xls write file
  sheet_list = []
  sheets = spreadsheet.sheets
  sheet = sheets[read_sheet]
  rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
  # print("Rowcount: " + str(rowcount))
  colcount = sheet.ncols()
  # print("Colcount: " + str(colcount))
  ac_row = 1
  # Counting rows that contain actual data (ac_row)
  for i in range(1, rowcount):
   if str(sheet[i, read_column].value) != "None" :
    ac_row += 1
    # print("Actual rows: " + str(ac_row))
   else :
    break

 elif your_choice == "2" :
  if query_term.find("://") > 0 :  # if query_term is a full URL then use this as the gr_url.
   gr_url = query_term  # assign the url entered to the gr_url variable
   if query_term.find('search') > 0 :
    filename = query_term[query_term.rfind('=')+1:]
   else :
    filename = query_term[query_term.rfind('/')+1:query_term.rfind('?')]
   filename = unquote(filename, encoding='iso-8859-7', errors='replace')
  else :  # if query_term is a search term then add the base url to it
   query_term_2 = quote(query_term.encode('iso-8859-7')).replace('%2B', '+')
   gr_url = "https://www.e-shop.gr/search?q=" + query_term_2  # this is the base query url for GR
   filename = unquote(query_term_2, encoding='iso-8859-7', errors='replace')
  # page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
  # gr_offset_url = gr_url + page_offset + str(offset)  # this is the complete query url with offset. eg. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0
  write_file = ("GRvsCY_Search_Results_" + filename + ".xls")  # name of xls write file
  alt_write_file = ("GRvsCY_ALT_Search_Results_" + filename + ".xls")  # alternate name of xls write file
 
 wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
 ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok = True)  # add sheet in virtual workbook named after the search string ad run date
 ws_write.write(0, 0, "CODE")		# write CODE on A1 cell
 ws_write.write(0, 1, "TITLE")		# write TITLE on B1 cell
 ws_write.write(0, 2, "OEM")		# write OEM on C1 cell
 ws_write.write(0, 3, "GR-PRICE")	# write GR-PRICE on D1 cell
 ws_write.write(0, 4, "GR-CAT")		# write GR-CAT on E1 cell
 ws_write.write(0, 5, "GR-SUBCAT")	# write GR-SUBCAT on F1 cell
 ws_write.write(0, 6, "GR-BRAND")	# write GR-BRAND on G1 cell
 ws_write.write(0, 7, "SXETIKA")	# write SXETIKA on H1 cell
 ws_write.write(0, 8, "GR-DESC")	# write GR-DESC on I1 cell
 ws_write.write(0, 9, "GR-AVAIL")	# write GR-AVAIL on J1 cell
 ws_write.write(0, 10, "CY-TITLE")	# write CY-TITLE on K1 cell
 ws_write.write(0, 11, "CY-PRICE")	# write CY-PRICE on L1 cell
 ws_write.write(0, 12, "CY-CAT")	# write CY-CAT on M1 cell
 ws_write.write(0, 13, "CY-SUBCAT")	# write CY-SUBCAT on N1 cell
 ws_write.write(0, 14, "CY-BRAND")	# write CY-BRAND on O1 cell
 ws_write.write(0, 15, "PRICE-DIF")	# write PRICE-DIFF on P1 cell
 ws_write.write(0, 16, "MARGIN")	# write MARGIN on Q1 cell

def get_totals(page_soup, gr_url) :
 global total_next_pages, gr_offset_url, last_offset, total_prod, tp, last_offset_url, gr_cat_page, query_mark, categories
 """ Σύνολο επόμενων σελίδων """
 if page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'}) :  # this is a term based query page
  next_pages = page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons
  next_pages_container = next_pages[0].findAll('a')  # keep all <a> only as they keep the next page numbers
  next_pages_index = 2
 elif page_soup.findAll('a', {'class': 'mobile_list_navigation_link'}) :  # if the page has next buttons
  next_pages_container = page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons
  next_pages_index = 1
  
 if len(next_pages_container) == 0 :
  total_next_pages = 1
  print("Μόνο 1 σελίδα στα αποτελέσματα")
 else:
  total_next_pages = int(next_pages_container[len(next_pages_container) - next_pages_index].text)  # this holds the exact next pages that need to be offset
  print("Σύνολο σελίδων: " + str(total_next_pages))

 """ offsets """
 # calculating total products count
 # first we need to calculate the last offset page
 if total_next_pages != 0 :
  if next_pages_index == 2 :
   last_offset = int(total_next_pages - 1) * 50
  elif next_pages_index == 1 :
   last_offset = int(total_next_pages - 1) * 10
 else :
  last_offset = 0

 if next_pages_index == 1 :
  gr_cat_page, query_mark, categories = str(gr_url).partition("?")
  gr_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
  last_offset_url = gr_cat_page + query_mark + "offset=" + str(last_offset) + "&" + categories
 elif next_pages_index == 2 :
  gr_offset_url = gr_url + page_offset + str(offset)  # this is the complete query url with offset. eg. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0
  last_offset_url = gr_url + page_offset + str(last_offset)

 """ Σύνολο πληροφοριών και τιμών προϊόντων τελευταίας σελίδας """
 last_page_soup = load_soup(last_offset_url, wait, retries)
 if next_pages_index == 1 :
  last_prod_info = last_page_soup.findAll('table', {'class': 'web-product-container'})
 elif next_pages_index == 2 :
  last_prod_info = last_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 total_prod = tp = len(last_prod_info) + last_offset

def get_product_info(page_soup) :
 global gr_prod_info, gr_prod_price
 """ Σύνολο πληροφοριών και τιμών προϊόντων """
 gr_prod_info = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 gr_prod_price = page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})

def show_results() :
 print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
 print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
 print("Περιγραφή: " + gr_desc_result)
 print("Σχετικά: " + sxetika_list)
 print("")

def initialize() :
 global offset, e, attempt, retries, wait, total_next_pages, print_debug, headers, page_offset
 print("Αρχικοποίηση παραμέτρων.")
 offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
 e = 1  # represents the row inside the excel file.
 attempt = 0
 retries = 10
 wait = 3
 total_next_pages = 0
 print_debug = False
 show_version = False
 test_run = False
 headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
 page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
 print("retries: " + str(retries))
 print("wait: " + str(wait))
 if print_debug == True :
  print("print_debug: True. Θα σου τα ζαλίσουμε λίγο.")
 else :
  print("print_debug: False")
 if len(headers) > 0 :
  print("Headers set")
 if show_version == True :
  ti_paizei()
 print("Done")
 print("")


try :
 initialize()
 get_start_time()
 choices()
 # set_files()
 if your_choice == "1" :  # if this is a predefined file
  for i in range(0, ac_row):
   if str(sheet[i, read_column].value) == "None" :
    break
   else :
    print("Απομένουν: " + str(ac_row-i) + "/" + str(ac_row) + " γραμμές.")
    gr_url = "https://www.e-shop.gr/s/" + sheet[i, read_column].value.strip()
    gr_soup = load_soup(gr_url, wait, retries)
    get_gr_details(gr_soup)
    get_gr_description(gr_soup, sheet[i, read_column].value.strip(), gr_cat)
    cy_url = "https://www.e-shop.cy/product?id=" + gr_prod_per
    cy_soup = load_soup(cy_url, wait, retries)
    get_cy_details(cy_soup)
    write_results(e)
    e += 1
   print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
   print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
   if len(gr_oem) > 0 :
    print("OEM: " + gr_oem)
   if len(gr_desc_result) > 0 :
    print("Περιγραφή: " + gr_desc_result)
   if len(sxetika_list) > 0 :
    print("Σχετικά: " + sxetika_list)
   print("")
   write_it_down(write_file)
  write_it_down(write_file)
  # get_elapsed_time()
 elif your_choice == "2" :
  
  if gr_url.find("shop.cy") > 0 or gr_url.find("shopcy") > 0 :
   new_url = "https://www.e-shop.gr" + gr_url[gr_url.find(".cy") + len(".cy") :]  # αν η σελίδα είναι του CY, κρατάμε ότι βρίσκεται μετά το CY και προσθέτουμε το url του GR
   gr_url = new_url
   print("Ώπα Κυπριακή σελίδα. Την αλλάζω σε: " + gr_url)

   
  gr_page_soup = load_soup(gr_url, wait, retries)
  if gr_page_soup.find('h1', {'style': 'display:inline;font-size:16px;font-family:tahoma;font-color:inherit;'}) :  # σάμπως η σελίδα που δώσαμε είναι αρχική της κατηγορίας και όχι όλα τα προϊόντα;
   gr_page_soup.find('h1', {'style': 'display:inline;font-size:16px;font-family:tahoma;font-color:inherit;'})
   gr_url = gr_page_soup.find('td', {'class': 'shop_table_title'}).a['href']  # άρπαξε το πραγματικό url
   print("Αλλάζω τη σελίδα σε: " + gr_url)
   print("Φορτώνω νέα σούπα...")
   gr_page_soup = load_soup(gr_url, wait, retries)  # φόρτω...
  
  if gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'}) :  # search result page with next buttons
  # https://www.e-shop.gr/search?q=nilfisk
   print("Σελίδα με αποτελέσματα αναζήτησης.")
   print("")
   get_totals(gr_page_soup, gr_url)
   print("Βρήκα " + str(total_prod) + " προϊόντα. Ξεκινάμε.")
   print("")
   for q in range(0, total_next_pages) :
    print("Τρέχουσα σελίδα: " + gr_offset_url + " #" + str(q))
    get_product_info(gr_page_soup)
    for i in range (0, len(gr_prod_info)) :
     tp = tp - 1
     print("Επεξεργασία: " + str(total_prod - tp) + "/" + str(total_prod) + ". Απομένουν: " + str(total_prod - (total_prod - tp)))
     gr_prod_per = gr_prod_info[i].span.text.replace("(", "").replace(")", "")
     gr_a_page = "https://www.e-shop.gr/product?id=" + gr_prod_per
     print(gr_a_page)
     page_soup = load_soup(gr_a_page, wait, retries)
     get_gr_details(page_soup)
     get_gr_description(page_soup, gr_prod_per, gr_cat)
     cy_page = "https://www.e-shop.cy/product?id=" + gr_prod_per
     cy_page_soup = load_soup(cy_page, wait, retries)
     get_cy_details(cy_page_soup)
     write_results(e)
     e += 1
     show_results()
    offset += 50
    offset_url = gr_url + page_offset + str(offset)
    gr_page_soup = load_soup(offset_url, wait, retries)
    # get_product_info(gr_page_soup)
  elif gr_page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories
   # https://www.e-shop.gr/ilektrikes-syskeues-ilektrikes-skoupes-1001w-eos-1200w-list?table=HAP&category=%C7%CB%C5%CA%D4%D1%C9%CA%C5%D3+%D3%CA%CF%D5%D0%C5%D3&filter-12563=1
   print("Αυτή είναι σελίδα σε στυλ κατηγορίας.")
   print("")
   if gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'}) :  # if the page has next buttons
    get_totals(gr_page_soup, gr_url)
    print("Βρήκα " + str(total_prod) + " προϊόντα. Ξεκινάμε.")
    print("")
    for q in range(0, int(total_next_pages)) :
     # print("Current page: " + gr_offset_url + " #" + str(q))
     gr_page_soup = load_soup(gr_offset_url, wait, retries)
     containers = gr_page_soup.findAll('table', {'class': 'web-product-container'})
     for container in containers :
      tp = tp - 1
      print("Επεξεργασία: " + str(total_prod - tp) + "/" + str(total_prod) + ". Απομένουν: " + str(total_prod - (total_prod - tp)))
      gr_prod_per = container.font.text.replace("(", "").replace(")", "")
      # print(gr_prod_per)
      gr_prod_title = container.h2.text
      gr_a_page = "https://www.e-shop.gr/s/" + gr_prod_per
      page_soup = load_soup(gr_a_page, wait, retries)
      get_gr_details(page_soup)
      get_gr_description(page_soup, gr_prod_per, gr_cat)
      cy_page = "https://www.e-shop.cy/product?id=" + gr_prod_per
      cy_page_soup = load_soup(cy_page, wait, retries)
      get_cy_details(cy_page_soup)
      write_results(e)
      e += 1
      show_results()
     offset += 10  # ADD 10 TO THE URL OFFSET VALUE
     gr_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
   else :
    total_next_pages = 0  # single search result page with categories
    # https://www.e-shop.gr/ergaleia-aksesouar-tzakiou-list?table=TLS&category=%C5%C9%C4%C7+%D4%C6%C1%CA%C9%CF%D5
    containers = gr_page_soup.findAll('table', {'class' : 'web-product-container'})
    total_prod = tp = len(containers)
    print("Βρέθηκαν μόνο 1 σελίδα και " + str(total_prod) + " προϊόντα.")
    print("")
    for container in containers :
     tp = tp - 1
     print("Επεξεργασία: " + str(total_prod - tp) + "/" + str(total_prod) + ". Απομένουν: " + str(total_prod - (total_prod - tp)))
     gr_prod_per = container.font.text.replace("(", "").replace(")", "")
     # print(gr_prod_per)
     gr_prod_title = container.h2.text
     # print(gr_prod_title)
     gr_a_page = "https://www.e-shop.gr/s/" + gr_prod_per
     page_soup = load_soup(gr_a_page, wait, retries)
     get_gr_details(page_soup)
     get_gr_description(page_soup, gr_prod_per, gr_cat)
     cy_page = "https://www.e-shop.cy/product?id=" + gr_prod_per
     cy_page_soup = load_soup(cy_page, wait, retries)
     get_cy_details(cy_page_soup)
     write_results(e)
     e += 1
     show_results()
  elif gr_page_soup.findAll("h1", {"style": "color:#4f4f4f;font-family:Tahoma;font-size:18px;font-weight:bold;padding:0 0 0 0;"}) :  # single product found
   # https://www.e-shop.cy/search?q=PBE120GS25SSDR 
   print("Μόνο 1 προϊόν βρέθηκε.")
   print("")
   attempt = 0
   get_gr_details(gr_page_soup)
   get_gr_description(gr_page_soup, gr_prod_per, gr_cat)
   cy_page = "https://www.e-shop.cy/product?id=" + gr_prod_per
   cy_page_soup = load_soup(cy_page, wait, retries)
   get_cy_details(cy_page_soup)
   write_results(e)
   show_results()
  else :
   print("Τα αποτελέσματα της αναζήτησης είναι μάλλον κενά. Δοκίμασε ξανά με διαφορετικούς όρους.")
   print("")
   sys.exit()

 write_it_down(write_file)
 # get_elapsed_time()
 input("Πάτα ένα κουμπί για τερματισμό.")
except KeyboardInterrupt :
 try :
  print("")
  input("Διαλλειματάκι;")
  print("")
 except :
  sys.exit(0)
except Exception as exc:
 print("Εξαίρεση: " + str(exc))
finally :
 print("")
 print("Τέλος εξαίρεσης.")
 sys.exit(0)