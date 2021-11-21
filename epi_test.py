# epi_check.py
# έλεγχος EPI προϊόντων για ηλικιακή σήμανση.
"""
- Πρέπει να προστεθούν τα Skate Boards και Hoverboards.
- Να βγαίνουν τα αποτελέσματα sorted ανα epi check
"""

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

def get_start_time() :
 global start_time, start_date
 start = datetime.now()
 start_date = start.strftime("%d-%m-%Y")
 start_time = start.strftime("%H:%M:%S")
 print("Εκκίνηση: " + start_date)
 print("")

def load_soup(page, wait, retries) :
 # print("Μέσα στη σούπα.")
 attempt = 0
 while attempt < retries :
  try :
   result = requests.get(page, headers = headers)
   webpage = result.content
   page_soup = soup(webpage, "html5lib")
   # print(headers)
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
  # print("Δεν βρέθηκε τιμή ούτε στο GR ούτε στο CY.")
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
   print("Γράφω εγγυήσεις...")
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

def get_cy_description(page_soup) :
 # global string, warranty, rest, gr_oem, barcode, gr_desc_result
 global cy_desc_text
 cy_desc_text = ""
 cy_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 cy_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if cy_d_soup == None or cy_d_soup.text.find('Σύνολο ψήφων') > 0 or cy_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  cy_desc_text = ""
  # print("initialized gr_desc_text, oem and barcode")
 else :
  cy_desc_text = cy_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html values and any .gr mentions

def set_files() :
 global write_file, alt_write_file, wb_write, ws_write
 write_file = ("EPI_Age_Check-" + start_date + ".xls")  # name of xls write file
 alt_write_file = ("EPI_Age_Check_ALT-" + start_date + ".xls")  # alternate name of xls write file
 wb_write = xlwt.Workbook()
 ws_write = wb_write.add_sheet("EPICHECK", cell_overwrite_ok = True)
 
 ws_write.write(0, 0, "CODE")		
 ws_write.write(0, 1, "TITLE")		
 ws_write.write(0, 2, "AGE_CHECK")
 ws_write.write(0, 3, "CAT")
 ws_write.write(0, 4, "SUBCAT")
 ws_write.write(0, 5, "BRAND")
 
def write_results(e, exist, not_exist) :
 ws_write.write(e, 0, prod_code)
 ws_write.write(e, 1, prod_title)
 ws_write.write(e, 2, age_text)
 ws_write.write(e, 3, cy_cat)
 ws_write.write(e, 4, cy_subcat)
 ws_write.write(e, 5, cy_brand)
 ws_write.write(0, 6, "y: " + str(exist))
 ws_write.write(0, 7, "n: " + str(not_exist))

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
 cur_dir = os.getcwd()
 if cur_dir != write_path :
  print("Τρέχων φάκελος: " + os.getcwd())
  os.chdir(write_path)
  print("Χρησιμοποιώ το " + os.getcwd())
 else :
  pass

 # wb_write.save(write_file)
 try :
  wb_write.save(write_file)
 except Exception as exc :
  print("Πρόβλημα κατά την αποθήκευση.")
  print(str(exc))
  print("Δοκιμή εγγραφής με το ALT αρχείο.")
  write_file = alt_write_file
  wb_write.save(write_file)
 print("")
 print("Το αρχείο: " + write_file + " δημιουργήθηκε στο " + os.getcwd())

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
 print("total_prod: " + str(total_prod))
 print("tp: " + str(tp))
 print("len(last_prod_info): " + str(len(last_prod_info)))
 print("last_offset: " + str(last_offset))
 print("total_next_pages: " + str(total_next_pages))
 input()

def print_deets():
 print(total_next_pages)
 print(total_prod)
 if page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'}) :  # search result page with next buttons
 # https://www.e-shop.gr/search?q=nilfisk
  print("Σελίδα με αποτελέσματα αναζήτησης.")
  print("")
 elif page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories
  # https://www.e-shop.gr/ilektrikes-syskeues-ilektrikes-skoupes-1001w-eos-1200w-list?table=HAP&category=%C7%CB%C5%CA%D4%D1%C9%CA%C5%D3+%D3%CA%CF%D5%D0%C5%D3&filter-12563=1
  print("Αυτή είναι σελίδα σε στυλ κατηγορίας.")
  print("")
 elif page_soup.findAll("h1", {"style": "color:#4f4f4f;font-family:Tahoma;font-size:18px;font-weight:bold;padding:0 0 0 0;"}) :  # single product found
  # https://www.e-shop.cy/search?q=PBE120GS25SSDR 
  print("Μόνο 1 προϊόν βρέθηκε.")
  print("")


try :
 trial_run = 0
 wait = 5
 retries = 3
 headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
 page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
 offset = 0
 exist = 0
 not_exist = 0
 e = 1
 total_next_pages = 0
 pages = []
 input_page = ""
 get_start_time()
 # set_files()
 page_url = "https://www.e-shop.cy/search_main.phtml?table=EPI"
 page_soup = load_soup(page_url, wait, retries)
 get_totals(page_soup, page_url)
 # deets()
 print("Βρήκα " + str(total_prod) + " προϊόντα. Ξεκινάμε.")
 print("")
 for q in range(0, int(total_next_pages)) :
  # page_soup = load_soup(gr_offset_url, wait, retries)
  # containers = page_soup.findAll('table', {'class': 'web-product-container'})
  containers = []
  if (total_prod - tp) + 10 > total_prod :
   test = 10 - (total_prod - tp)
  else :
   test = 10
  for i in range(0, test) :
   containers.append(i)
   print(str(i))
  input()
  for container in containers :
   tp = tp - 1
   print("Επεξεργασία: " + str(total_prod - tp) + "/" + str(total_prod) + ". Απομένουν: " + str(total_prod - (total_prod - tp)))
  offset += 10  # ADD 10 TO THE URL OFFSET VALUE
  gr_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
 
 # write_it_down(write_file)
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
# finally :
 # print("")
 # print("Τέλος εξαίρεσης.")
 # sys.exit(0)