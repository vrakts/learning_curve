# Current Version 1.4
##########################
# Changelog V1.4
# - Gets category, subcategory and brand from GR and CY 
#	plus availability from the GR website
# - Reads the description from GR, seperates the OEM code and barcode
# - Recognises Lifetime and laptop warranty and removes the 2nd DOA link.
# - Gets the relevant products
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
#		 of the product and get sort specs for all results
# To Do: calculate the correct price for the CY page for upload
# To Do: Try the new error catcching method for read 
#		 and other common errors
# To Do: Refine the description code for the align justify BS from GR
#		 for now it erases the crazy tag and adds p align at the start
#		 but can't recognise if the description is empty.

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
import urllib.request
import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

offset = 0  # starting offset value set to 0 and in each for loop, 50 will be added
e = 1  # represents the row inside the excel file.
attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
# oneprod = 0  # is it a single item (1) or multiple items (0)

# Input search term
answer_term = "no"

# while (answer_term == "no") :
 # query_term = input("Please enter your query term: ")
 # # # print(query_term.count(' '))
 # # if query_term.find('http') :  # if query_term is a url...
  # # query_url = quote(text.encode('utf-8'))
 # if query_term.count(' ') > 0 :  # if query_term has at least one " "...
  # # print("in if loop. Has at least 1 space")
  # query_term = query_term.replace(" ", "+")
  # # print(query_term)
 # answer_text = "Your query term is: " + query_term + ". Is that correct? Press enter for yes. "
 # answer_term = input(answer_text)

while (answer_term == "no") :
 print("What are we looking at?")
 print("")
 print("1. Predefined file.")
 print("2. Query term or link.")
 your_choice = input("Please enter your choice: ")
 if your_choice == "1" :
  upload_file = input("Please enter file name: ")
  if upload_file[-4:] != ".ods" :
   upload_file = upload_file + ".ods"
  answer_text = "File name is: " + upload_file + ". Is that correct? Press enter for yes. "
  answer_term = input(answer_text)
 elif your_choice == "2" :
  query_term = input("Please enter your query term: ")
  query_term = query_term.replace(" ", "+")
  # print(query_term)
  answer_text = "You entered: " + query_term + ". Is that correct? Press enter for yes. "
  answer_term = input(answer_text)
 else :
  os.system('cls')
  print("Wrong selection. Please try again.")

#####################################################################
# The below needs refining. If ** is detected it's passed on to the #
# grpage but it breaks when it starts the BSoup functions probably  #
# because the element requested cannot be found in the soup.        #
#####################################################################
# if answer_term == '**' :
 # query_term = answer_term + query_term
 # print("Searching for: " + query_term)
# else :
 # print("Searching for: " + query_term)

##########################################
# Setting starting date and time values. #
##########################################

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("")
print("Script started at " + start_date)

##########################
# Setting correct paths. #
##########################

print("")

if your_choice == "1" :
 if os.path.exists(r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does work folder exist?
  write_path = (r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
  print("Using " + write_path + " for writing files.")
  print("")
 elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
  write_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
  print("Using " + write_path + " for writing files.")
  print("")
 elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
  write_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
  print("Using " + write_path + " for writing files.")
  print("")
 else :
  attempt = 0
  while attempt < 3 :
   write_path = input("No predefined paths found. Where da file? ")
   if os.path.exists(write_path) == False :
    print("Path not found. Try again...")
    print("")
    attempt += 1
  print("Tried 3 times. Quitting now.")
  sys.exit()  
elif os.path.exists(r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
 print("Using " + write_path + " for writing files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results") == True :  # does home folder 1 exist?
 write_path = (r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results")
 print("Using home path 1 for writing files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results") == True :  # does home folder 2 exist?
 write_path = (r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results")
 print("Using home path 2 for writing files.")
 print("")
else :
 if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Using " + write_path + " for writing files.")
  print("")
 else :  # if not create it
  os.makedirs(r"C:\TEMPYTH")
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Creating and using " + write_path + " for writing files.")
  print("")

###############################
# End of write paths setting. #
###############################

if your_choice == "2" :
 if query_term.find("://") > 0 :  # if query_term is a full URL then use this as the grpage.
  url_term = query_term  # assign query_term to url_term
  grpage = url_term  # assign the url entered to the grpage variable
  if url_term.find('search') > 0 :
   filename = url_term[url_term.rfind('=')+1:]
  else :
   filename = url_term[url_term.rfind('/')+1:url_term.rfind('?')]
  filename = unquote(filename, encoding='iso-8859-7', errors='replace')
 else :  # if query_term is a search term then add the base url to it
  url_term = quote(query_term.encode('iso-8859-7')).replace('%2B', '+')
  grpage = "https://www.e-shop.gr/search?q=" + url_term  # this is the base query url for GR
  filename = unquote(query_term, encoding='iso-8859-7', errors='replace')
 page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
 gr_offset_url = grpage + page_offset + str(offset)  # this is the complete query url with offset. eg. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0

# Opening files
os.chdir(write_path)
if your_choice == "1" :
 ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
 spreadsheet = ezodf.opendoc(upload_file)  # open file
 ezodf.config.reset_table_expand_strategy()  # reset ezodf config
 write_file = (upload_file[:upload_file.find("-")+1] + " Products_Upload_Analysis.xls")  # path to xslx write file
 alt_write_file = (upload_file[:upload_file.find("-")+1] + " Products_Upload_Analysis_ALT.xls")   # alternate name of xls write file
elif your_choice == "2" :
 write_file = ("GRvsCY_Search_Results_" + filename + ".xls")  # name of xls write file
 alt_write_file = ("GRvsCY_ALT_Search_Results_" + filename + ".xls")  # alternate name of xls write file

wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok=True)  # add sheet in virtual workbook named after the search string ad run date
ws_write.write(0, 0, "CODE")		# write CODE on A1 cell
ws_write.write(0, 1, "TITLE")		# write TITLE on B1 cell
ws_write.write(0, 2, "OEM")			# write OEM on C1 cell
ws_write.write(0, 3, "GR-PRICE")	# write GR-PRICE on D1 cell
ws_write.write(0, 4, "GR-CAT")		# write GR-CAT on E1 cell
ws_write.write(0, 5, "GR-SUBCAT")	# write GR-SUBCAT on F1 cell
ws_write.write(0, 6, "GR-BRAND")	# write GR-BRAND on G1 cell
ws_write.write(0, 7, "SXETIKA")		# write SXETIKA on H1 cell
ws_write.write(0, 8, "GR-DESC")		# write GR-DESC on I1 cell
ws_write.write(0, 9, "GR-AVAIL")	# write GR-AVAIL on J1 cell
ws_write.write(0, 10, "CY-PRICE")	# write CY-PRICE on K1 cell
ws_write.write(0, 11, "CY-CAT")		# write CY-CAT on L1 cell
ws_write.write(0, 12, "CY-SUBCAT")	# write CY-SUBCAT on M1 cell
ws_write.write(0, 13, "CY-BRAND")	# write CY-BRAND on N1 cell

attempt = 0
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

if your_choice == "1" :  # if this is a predefined file
 sheets = spreadsheet.sheets
 sheet = sheets[0]
 rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
 colcount = sheet.ncols()
 ac_row = 1
 # Counting rows that contain actual data (ac_row)
 for i in range(1, rowcount):
  if str(sheet[i, 2].value) != "None" :
   ac_row += 1
   # print("Actual rows: " + str(ac_row))
  else :
   break
 i = 1
 for i in range(1, ac_row):
  if str(sheet[i, 2].value) == "None" :
   break
  else:
   print("Rows left: " + str(ac_row-i) + "/" + str(ac_row))
   page_url = "https://www.e-shop.gr/s/" + sheet[i, 2].value.strip()
   req = urllib.request.Request(page_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     uClient = uReq(req)
     page_soup = soup(uClient.read(), "html5lib")
     uClient.close()
     break
    # except http.client.IncompleteRead :
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("Oops, just bumped into the following exception: " + str(exc))
     print("Retrying in 5 seconds.")
     attempt += 1
     time.sleep(5)
   # gr_code = page_url[page_url.rfind("/")+1:]
   gr_prod_per = page_url[page_url.rfind("/")+1:]
   gr_prod_title = page_soup.h1.text
   gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
   if page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"}) == None :
    gr_a_text = "Εξαντλημένο"
   else :
    gr_a = page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
    if gr_a.text.find('Κατόπιν') <= 16 :
     gr_a_text = gr_a.text[gr_a.text.find(":") + 2:]
    else :
     gr_a_text = gr_a.text[gr_a.text.find(":") + 2:gr_a.text.find("\n")].strip()
   gr_categories = page_soup.findAll('td', {'class': 'faint1'})
   gr_cat = gr_categories[1].text[:gr_categories[1].text.find(' •')]
   gr_brand = gr_categories[1].text[gr_categories[1].text.find(' •')+2:gr_categories[1].text.find('στην')].strip()
   if len(gr_categories) > 2 :
    gr_subcat = gr_categories[3].text.strip()
   else :
    gr_subcat = ""
   gr_oem = ""
   # if page_soup.find('td', {'class': 'product_table_body'}) == None or page_soup.find('td', {'class': 'product_table_body'}) != "Περιγραφή " :
    # gr_desc_text = ""
   # else :
    # gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
    # if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
     # gr_desc_text = ""
    # else :
     # gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
   gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
   gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
   if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text != "Περιγραφή " :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
    gr_desc_text = ""
   else :
    gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html calues and any .gr mentions
    if gr_desc_text.find('Vendor OEM:') > 0 :
     if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
      string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
     else :
      string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
     gr_desc_text = string.strip()  # keep only what is before the OEM
     oem = rest.strip()  # keep only what is after the OEM
     gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
     gr_oem = gr_oem.strip()
    # if gr_desc_text.find('<br><br>Barcode') > 0 :  # if barcode exists in GR
    if gr_desc_text.find('Barcode:') > 0 :  # if both barcode and OEM exists
     if gr_desc_text.find('<br><br>Barcode:') > 0 :
      string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode')  # seperate the text
     else :
      string, barcode, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
     # gr_desc_text = string.strip() + rest.strip() # keep only what is before the barcode
     gr_desc_text = string.strip() # keep only what is before the barcode
     # while gr_desc_text.strip()[-4:] == "<br>" :  # if the 4 ending text characters are <br>
      # string, br, rest = gr_desc_text.rpartition('<br>')  # seperate the text
      # gr_desc_text = string.strip()  # keep ony what is before <br>
     # gr_oem = rest.replace("</li>", "").strip()
    if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
     crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
     gr_desc_text = rest.strip()  # keep only the rest of the text
    # if gr_desc_text.find('<p ') >= 0 :
     # p, align, rest = gr_desc_text.partition('>')
     # gr_desc_text = '<p align="justify">' + rest.strip()pyth
    if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
     p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
     gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
    else :
     gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
    if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
     if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
      string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
     elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
      string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
     if gr_prod_title.find('ASUS') > 0 :
      warranty_text = ' <a href="page.phtml?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b> </li>'
     else :
      warranty_text = ' .</b> </li>'
     gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
    elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
     if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
      string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
     elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
      string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
     gr_desc_text = string + "<b>Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
    elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
     string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
    elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
     string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
     gr_desc_text = string + rest.strip()  # and keep the before and after text
    else :
     print("No Warranty found. Will keep text as is.")
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
   if len(gr_price) == 0 :
    gr_price_text = "Εξαντλημένο"
    # print("CODE = " + gr_code + ", εξαντλημένο.")
   else : 
    gr_price_text = gr_price[0].text.replace("\xa0€", "").replace(".", ",")
  cy_page = "http://www.eshopcy.com.cy/product?id=" + gr_prod_per
  req = urllib.request.Request(cy_page, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    cy_uClient = uReq(req)
    cy_page_soup = soup(cy_uClient.read(), "html5lib")
    cy_uClient.close()
    break
   # except http.client.IncompleteRead :
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("Oops, just bumped into the following exception: " + str(exc))
    print("Retrying in 5 seconds.")
    attempt += 1
    time.sleep(5)
  cy_prod_title = cy_page_soup.h1.text
  cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
  if len(cy_prod_title) == 0 :
   cy_price_text = "Θέλει άνοιγμα"
   cy_cat = ""
   cy_brand = ""
   cy_subcat = ""
  else :
   if len(cy_price) == 0 :
    cy_price_text = "Εξαντλημένο"
   else :
    cy_price_text = cy_price[0].text.replace("\xa0€", "").replace(".", ",")
   cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
   cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
   cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
   if len(cy_categories) > 2 :
    cy_subcat = cy_categories[3].text.strip()
   else :
    cy_subcat = ""

  print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
  print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
  if len(gr_desc_text) > 0 :
   print("Description: " + gr_desc_text)
  if len(sxetika_list) > 0 :
   print("Sxetika: " + sxetika_list)
  print("")
  ws_write.write(e, 0, gr_prod_per) 	# OK
  ws_write.write(e, 1, gr_prod_title)	# OK
  ws_write.write(e, 2, gr_oem.strip())	# OK
  ws_write.write(e, 3, gr_price_text)	# OK
  ws_write.write(e, 4, gr_cat)			# OK
  ws_write.write(e, 5, gr_subcat)		# OK
  ws_write.write(e, 6, gr_brand)		# OK
  ws_write.write(e, 7, sxetika_list)	# OK
  ws_write.write(e, 8, gr_desc_text)	# OK
  ws_write.write(e, 9, gr_a_text)		# OK
  ws_write.write(e, 10, cy_price_text)	# OK
  ws_write.write(e, 11, cy_cat)			# OK
  ws_write.write(e, 12, cy_subcat)		# OK
  ws_write.write(e, 13, cy_brand)		# OK
  e += 1

 try :
  wb_write.save(write_file)
  print("")
  print(write_file + " created on " + write_path)
 except :
  print("")
  wb_write.save(alt_write_file)
  print(alt_write_file + " created on " + write_path)
 
 elapsed_time = time.time() - start_time
 minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
 mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
 seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
 seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
 formatted_time = str(mins) + "." + str(seconds)
 print("")
 print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
 sys.exit()

#################################################################################
# Code below will run if the choice is not a predefined file (2. Link or query) #
#################################################################################
req = urllib.request.Request(grpage, headers = headers)
attempt = 0
while attempt < 3 :
 try :
  # print("On try :" + str(attempt))
  gr_uClient = uReq(req)
  gr_page_soup = soup(gr_uClient.read(), "html5lib")
  gr_uClient.close()
  break
 # except http.client.IncompleteRead :
 except Exception as exc :
  # print("On except :" + str(attempt))
  print("Oops, just bumped into the following exception: " + str(exc))
  print("Retrying in 5 seconds.")
  attempt += 1
  time.sleep(5)

# gr last page preparations
next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
next_pages_single = gr_page_soup.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})  # find all next page buttons assuming this is a category based query page

if gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'}) :  # search result page with next buttons
 print("Treating this as a search result page.")
 print("")
 # gr last page preparations
 next_pages_search = gr_page_soup.findAll('td', {'style': 'font-family:tahoma;font-size:14px;padding:0 0 10px 0;'})  # find all next page buttons assuming this is a term based query page
 next_pages_a = next_pages_search[0].findAll('a')  # keep all <a> only as they keep the next page numbers
 if len(next_pages_a) == 0 :
  total_next_pages = 1
  print("Only 1 page in the query results")
 else:
  total_next_pages = int(next_pages_a[len(next_pages_a)-2].text)  # this holds the exact next pages that need to be offset
  print("Total query pages: " + str(total_next_pages))
 gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})
 page_offset = "&t=&c=&offset="  # this holds the offset text of the query page
 gr_offset_url = grpage + page_offset + str(offset)  # this is the complete query url with offset. eg. https://www.e-shop.gr/search?q=spigen&t=&c=&offset=0
 # calculating total products count
 # first we need to calculate the last offset page
 last_offset = (total_next_pages - 1) * 50
 # then calculate the new url
 last_offset_url = grpage + page_offset + str(last_offset)
 # now we need to reload the last offset soup with all available products
 req = urllib.request.Request(last_offset_url, headers = headers)
 attempt = 0
 while attempt < 3 :
  try :
   # print("On try :" + str(attempt))
   last_uClient = uReq(req)
   last_page_soup = soup(last_uClient.read(), "html5lib")
   last_uClient.close()
   break
  # except http.client.IncompleteRead :
  except Exception as exc :
   # print("On except :" + str(attempt))
   print("Oops, just bumped into the following exception: " + str(exc))
   print("Retrying in 5 seconds.")
   attempt += 1
   time.sleep(5)
 last_prod_info = last_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
 # last step, add the gr_prod_info of the last offset page to the offset value
 total_prod = last_offset + len(last_prod_info)
 tp = total_prod
 print("Found " + str(total_prod) + " products. Starting process now.")
 print("")
 for q in range(0, total_next_pages) :
  for (i, p) in zip(gr_prod_info, gr_prod_price) :
   tp = tp - 1
   print("Processing item: " + str(total_prod - tp) + "/" + str(total_prod) + ". Remaining: " + str(total_prod - (total_prod - tp)))
   gr_prod_link = i.a['href']
   gr_prod_title = i.a.text
   gr_prod_per = i.span.text.replace("(", "").replace(")", "")
   gr_price_text = p.text  # save text of the price result in price_text
   if gr_price_text.count(' ') > 1 :  # if price " " is more than 1 then it has a discount ...
    gr_price_text = gr_price_text[gr_price_text.find(' ')+1:].replace(" €", "").replace(".", ",")  # ... so print the second price without the euro sign
   else :
    gr_price_text = gr_price_text.replace(" €","").replace(".", ",")  #... otherwise print the whole (single) price without the euro sign.
   gr_a_page = "https://www.e-shop.gr/product?id=" + gr_prod_per
   req = urllib.request.Request(gr_a_page, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     gr_a_uClient = uReq(req)
     gr_a_pagesoup = soup(gr_a_uClient.read(), "html5lib")
     gr_a_uClient.close()
     break
    # except http.client.IncompleteRead :
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("Oops, just bumped into the following exception: " + str(exc))
     print("Retrying in 5 seconds.")
     attempt += 1
     time.sleep(5)
   if gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"}) == None :
    gr_a_text = "Εξαντλημένο"
   else :
    gr_a = gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
    if gr_a.text.find('Κατόπιν') <= 16 :
     gr_a_text = gr_a.text[gr_a.text.find(":") + 2:]
    else :
     gr_a_text = gr_a.text[gr_a.text.find(":") + 2:gr_a.text.find("\n")].strip()
   gr_categories = gr_a_pagesoup.findAll('td', {'class' : 'faint1'})
   gr_cat = gr_categories[1].text[:gr_categories[1].text.find(' •')]
   gr_brand = gr_categories[1].text[gr_categories[1].text.find(' •')+2:gr_categories[1].text.find('στην')].strip()
   if len(gr_categories) > 2 :
    gr_subcat = gr_categories[3].text.strip()
   else :
    gr_subcat = ""
   gr_oem = ""
   # if page_soup.find('td', {'class': 'product_table_body'}) == None or page_soup.find('td', {'class': 'product_table_body'}) != "Περιγραφή " :
    # gr_desc_text = ""
   # else :
    # gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
    # if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
     # gr_desc_text = ""
    # else :
     # gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
   gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
   gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
   if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text != "Περιγραφή " :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
    gr_desc_text = ""
   else :
    gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html calues and any .gr mentions
    if gr_desc_text.find('Vendor OEM:') > 0 :
     if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
      string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
     else :
      string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
     gr_desc_text = string.strip()  # keep only what is before the OEM
     oem = rest.strip()  # keep only what is after the OEM
     gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
     gr_oem = gr_oem.strip()
    # if gr_desc_text.find('<br><br>Barcode') > 0 :  # if barcode exists in GR
    if gr_desc_text.find('Barcode:') > 0 :  # if both barcode and OEM exists
     if gr_desc_text.find('<br><br>Barcode:') > 0 :
      string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode')  # seperate the text
     else :
      string, barcode, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
     # gr_desc_text = string.strip() + rest.strip() # keep only what is before the barcode
     gr_desc_text = string.strip() # keep only what is before the barcode
     # while gr_desc_text.strip()[-4:] == "<br>" :  # if the 4 ending text characters are <br>
      # string, br, rest = gr_desc_text.rpartition('<br>')  # seperate the text
      # gr_desc_text = string.strip()  # keep ony what is before <br>
     # gr_oem = rest.replace("</li>", "").strip()
    if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
     crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
     gr_desc_text = rest.strip()  # keep only the rest of the text
    # if gr_desc_text.find('<p ') >= 0 :
     # p, align, rest = gr_desc_text.partition('>')
     # gr_desc_text = '<p align="justify">' + rest.strip()pyth
    if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
     p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
     gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
    else :
     gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
    if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
     if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
      string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
     elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
      string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
     if gr_prod_title.find('ASUS') > 0 :
      warranty_text = ' <a href="page.phtml?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b> </li>'
     else :
      warranty_text = ' .</b> </li>'
     gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
    elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
     if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
      string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
     elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
      string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
     gr_desc_text = string + "<b>Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
    elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
     string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
    elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
     string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
     gr_desc_text = string + rest.strip()  # and keep the before and after text
    else :
     print("No Warranty found. Will keep text as is.")
   if len(gr_a_pagesoup.findAll('div', {'class': 'also_box'})) > 0 :
    gr_sxetika = gr_a_pagesoup.findAll('div', {'class': 'also_box'})
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
   cy_page = "http://www.eshopcy.com.cy/product?id=" + gr_prod_per
   req = urllib.request.Request(cy_page, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     cy_uClient = uReq(req)
     cy_page_soup = soup(cy_uClient.read(), "html5lib")
     cy_uClient.close()
     break
    # except http.client.IncompleteRead :
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("Oops, just bumped into the following exception: " + str(exc))
     print("Retrying in 5 seconds.")
     attempt += 1
     time.sleep(5)
   cy_prod_title = cy_page_soup.h1.text
   cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
   if len(cy_prod_title) == 0 :
    cy_price_text = "Θέλει άνοιγμα"
    cy_cat = ""
    cy_brand = ""
    cy_subcat = ""
   else :
    if len(cy_price) == 0 :
     cy_price_text = "Εξαντλημένο"
    else :
     cy_price_text = cy_price[0].text.replace("\xa0€", "").replace(".", ",")
     cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
     cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
     cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
     if len(cy_categories) > 2 :
      cy_subcat = cy_categories[3].text.strip()
     else :
      cy_subcat = ""
   # if cy_price_text != ("Εξαντλημένο", "Θέλει άνοιγμα") :
    # difference = (int(cy_price_text(",", ".")) - int(gr_price_text.replace(",", ".")) / int(gr_price_text.replace(",", ".")) * 100)
    # print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + " (" + str(difference) + ").")
   # else :
   print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
   print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
   print("Description: " + gr_desc_text)
   print("Sxetika: " + sxetika_list)
   print("")
   # print("Products left: " + str(total_prod - tp) + "/" + str(total_prod))
   ws_write.write(e, 0, gr_prod_per)
   ws_write.write(e, 1, gr_prod_title)
   ws_write.write(e, 2, gr_oem.strip())
   ws_write.write(e, 3, gr_price_text)
   ws_write.write(e, 4, gr_cat)
   ws_write.write(e, 5, gr_subcat)
   ws_write.write(e, 6, gr_brand)
   ws_write.write(e, 7, sxetika_list)
   ws_write.write(e, 8, gr_desc_text)
   ws_write.write(e, 9, gr_a_text)
   ws_write.write(e, 10, cy_price_text)
   ws_write.write(e, 11, cy_cat)
   ws_write.write(e, 12, cy_subcat)
   ws_write.write(e, 13, cy_brand)
   e += 1
   # tp = tp - 1
  offset = offset + 50
  offset_url = grpage + page_offset + str(offset)
  req = urllib.request.Request(offset_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    gr_uClient = uReq(req)
    gr_page_soup = soup(gr_uClient.read(), "html5lib")
    gr_uClient.close()
    break
   # except http.client.IncompleteRead :
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("Oops, just bumped into the following exception: " + str(exc))
    print("Retrying in 5 seconds.")
    attempt += 1
    time.sleep(5)
  gr_prod_info = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "padding:3px 0 3px 0;border-bottom:#909090 1px solid;"})
  gr_prod_price = gr_page_soup.find("div", {"id": "web_body"}).tr.tr.tr.td.findAll("td", {"style": "font-size:14px;font-family:tahoma;color:#900100;width:120px;border-bottom:#909090 1px solid;"})
elif gr_page_soup.findAll('table', {'class': 'web-product-container'}) :  # search result page with categories
 print("Treating this as a category query page.")
 print("")
 if gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'}) :  # if the page has next buttons 
  next_pages_category = gr_page_soup.findAll('a', {'class': 'mobile_list_navigation_link'})  # find all next page buttons assuming this is a category based query page
  total_next_pages = next_pages_category[len(next_pages_category)-1].text  # total next pages is in the last total_next_pages (-1 for indexing)
  print("Total query pages: " + str(total_next_pages))
  gr_cat_page, query_mark, categories = str(grpage).partition("?")
  gr_cat_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
  last_offset = (int(total_next_pages) - 1) * 10
  gr_last_cat = gr_cat_page + query_mark + "offset=" + str(last_offset) + "&" + categories
  req = urllib.request.Request(gr_last_cat, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    gr_last_uClient = uReq(req)
    gr_last_page_soup = soup(gr_last_uClient.read(), "html5lib")
    gr_last_uClient.close()
    break
   # except http.client.IncompleteRead :
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("Oops, just bumped into the following exception: " + str(exc))
    print("Retrying in 5 seconds.")
    attempt += 1
    time.sleep(5)
  last_prod = gr_last_page_soup.findAll('table', {'class': 'web-product-container'})
  total_prod = len(last_prod) + last_offset
  tp = total_prod
  print("Found " + str(total_prod) + " products. Starting process now.")
  print("")
  for q in range(0, int(total_next_pages)) :
   req = urllib.request.Request(gr_cat_offset_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     gr_uClient = uReq(req)
     gr_page_soup = soup(gr_uClient.read(), "html5lib")
     gr_uClient.close()
     break
    # except http.client.IncompleteRead :
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("Oops, just bumped into the following exception: " + str(exc))
     print("Retrying in 5 seconds.")
     attempt += 1
     time.sleep(5)
   containers = gr_page_soup.findAll('table', {'class': 'web-product-container'})
   for container in containers :
    tp = tp - 1
    print("Processing item: " + str(total_prod - tp) + "/" + str(total_prod) + ". Remaining: " + str(total_prod - (total_prod - tp)))
    gr_prod_per = container.font.text.replace("(", "").replace(")", "")
    # print(gr_prod_per)
    gr_prod_title = container.h2.text
    # print(gr_prod_title)
    if container.find('font', {'style': 'color:#FF0000'}) != None:
     gr_price_text = container.find('font', {'style': 'color:#FF0000'}).text.replace(".", ",")
    else :
     gr_price_text = container.find('td', {'class': 'web-product-price'}).b.text.strip().replace('\xa0€', '').replace('.', ',')
    # print(gr_price_text)
    # gr_a_text = container.find('div', {'style': 'display:block;width:auto;padding:0 5px 7px 0;'}).text
    # print(gr_a_text)
    # ws_write.write(e, 4, cy_price_text)
    gr_categories = container.find('td', {'class' : 'web-product-info'}).text
    if gr_categories.find('Κατηγορία:') >= 0 :
     if gr_categories.find('Υποκατηγορία:') >= 0 :
      gr_cat = gr_categories[gr_categories.find("Κατηγορία:\xa0 ")+12:gr_categories.find("Υποκατηγορία:\xa0 ")-4]
      gr_subcat = gr_categories[gr_categories.find("Υποκατηγορία:\xa0 ")+15:gr_categories.find("Κατασκευαστής")-4]
      gr_brand = gr_categories[gr_categories.find("Κατασκευαστής:")+16:]
     else :
      gr_cat = gr_categories[gr_categories.find("Κατηγορία:\xa0 ")+12:gr_categories.find("Κατασκευαστής")-4]
      gr_subcat = ""
      gr_brand = gr_categories[gr_categories.find("Κατασκευαστής:")+16:]
    else :
     print("No categories found. Will leave the fields empty but will error out when uploading product.")
     gr_cat = ""
     gr_subcat = ""
     gr_brand = ""
    gr_a_page = "https://www.e-shop.gr/s/" + gr_prod_per
    req = urllib.request.Request(gr_a_page, headers = headers)
    gr_a_uClient = uReq(req)
    gr_a_pagesoup = soup(gr_a_uClient.read(), "html5lib")
    gr_a_uClient.close()
    if gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"}) == None :
     gr_a_text = "Εξαντλημένο"
    else :
     gr_a = gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
     if gr_a.text.find('Κατόπιν') <= 16 :
      gr_a_text = gr_a.text[gr_a.text.find(":") + 2:]
     else :
      gr_a_text = gr_a.text[gr_a.text.find(":") + 2:gr_a.text.find("\n")].strip()
     gr_oem = ""
     # if page_soup.find('td', {'class': 'product_table_body'}) == None or page_soup.find('td', {'class': 'product_table_body'}) != "Περιγραφή " :
      # gr_desc_text = ""
     # else :
      # gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
      # if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
       # gr_desc_text = ""
      # else :
       # gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
     gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
     gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
     if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text != "Περιγραφή " :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
      gr_desc_text = ""
     else :
      gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html calues and any .gr mentions
      if gr_desc_text.find('Vendor OEM:') > 0 :
       if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
        string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
       else :
        string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
       gr_desc_text = string.strip()  # keep only what is before the OEM
       oem = rest.strip()  # keep only what is after the OEM
       gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
       gr_oem = gr_oem.strip()
      # if gr_desc_text.find('<br><br>Barcode') > 0 :  # if barcode exists in GR
      if gr_desc_text.find('Barcode:') > 0 :  # if both barcode and OEM exists
       if gr_desc_text.find('<br><br>Barcode:') > 0 :
        string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode')  # seperate the text
       else :
        string, barcode, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
       # gr_desc_text = string.strip() + rest.strip() # keep only what is before the barcode
       gr_desc_text = string.strip() # keep only what is before the barcode
       # while gr_desc_text.strip()[-4:] == "<br>" :  # if the 4 ending text characters are <br>
        # string, br, rest = gr_desc_text.rpartition('<br>')  # seperate the text
        # gr_desc_text = string.strip()  # keep ony what is before <br>
       # gr_oem = rest.replace("</li>", "").strip()
      if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
       crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
       gr_desc_text = rest.strip()  # keep only the rest of the text
      # if gr_desc_text.find('<p ') >= 0 :
       # p, align, rest = gr_desc_text.partition('>')
       # gr_desc_text = '<p align="justify">' + rest.strip()pyth
      if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
       p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
       gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
      else :
       gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
      if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
       if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
        string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
       elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
        string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
       if gr_prod_title.find('ASUS') > 0 :
        warranty_text = ' <a href="page.phtml?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b> </li>'
       else :
        warranty_text = ' .</b> </li>'
       gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
      elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
       if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
        string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
       elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
        string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
       gr_desc_text = string + "<b>Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
      elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
       string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
      elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
       string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
       gr_desc_text = string + rest.strip()  # and keep the before and after text
      else :
       print("No Warranty found. Will keep text as is.")
     if len(gr_a_pagesoup.findAll('div', {'class': 'also_box'})) > 0 :
      gr_sxetika = gr_a_pagesoup.findAll('div', {'class': 'also_box'})
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
    cy_page = "http://www.eshopcy.com.cy/product?id=" + gr_prod_per
    req = urllib.request.Request(cy_page, headers = headers)
    attempt = 0
    while attempt < 3 :
     try :
      # print("On try :" + str(attempt))
      cy_uClient = uReq(req)
      cy_page_soup = soup(cy_uClient.read(), "html5lib")
      cy_uClient.close()
      break
     # except http.client.IncompleteRead :
     except Exception as exc :
      # print("On except :" + str(attempt))
      print("Oops, just bumped into the following exception: " + str(exc))
      print("Retrying in 5 seconds.")
      attempt += 1
      time.sleep(5)
    cy_prod_title = cy_page_soup.h1.text
    cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
    if len(cy_prod_title) == 0 :
     cy_price_text = "Θέλει άνοιγμα"
     cy_cat = ""
     cy_brand = ""
     cy_subcat = ""
    else :
     if len(cy_price) == 0 :
      cy_price_text = "Εξαντλημένο"
     else :
      cy_price_text = cy_price[0].text.replace("\xa0€", "").replace(".", ",")
     cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
     cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
     cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
     if len(cy_categories) > 2 :
      cy_subcat = cy_categories[3].text.strip()
     else :
      cy_subcat = ""
    ws_write.write(e, 0, gr_prod_per)
    ws_write.write(e, 1, gr_prod_title)
    ws_write.write(e, 2, gr_oem.strip())
    ws_write.write(e, 3, gr_price_text)
    ws_write.write(e, 4, gr_cat)
    ws_write.write(e, 5, gr_subcat)
    ws_write.write(e, 6, gr_brand)
    ws_write.write(e, 7, sxetika_list)
    ws_write.write(e, 8, gr_desc_text)
    ws_write.write(e, 9, gr_a_text)
    ws_write.write(e, 10, cy_price_text)
    ws_write.write(e, 11, cy_cat)
    ws_write.write(e, 12, cy_subcat)
    ws_write.write(e, 13, cy_brand)
    e += 1
    print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
    print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
    print("Description: " + gr_desc_text)
    print("Sxetika: " + sxetika_list)
    print("")
   offset += 10  # ADD 10 TO THE URL OFFSET VALUE
   gr_cat_offset_url = gr_cat_page + query_mark + "offset=" + str(offset) + "&" + categories
 else :
  total_next_pages = 0  # single search result page with categories
  containers = gr_page_soup.findAll('table', {'class' : 'web-product-container'})
  total_prod = len(containers)
  tp = total_prod
  print("Only 1 page and " + str(total_prod) + " products found.")
  print("")
  # len(containers)
  for container in containers :
   tp = tp - 1
   print("Processing item: " + str(total_prod - tp) + "/" + str(total_prod) + ". Remaining: " + str(total_prod - (total_prod - tp)))
   gr_prod_per = container.font.text.replace("(", "").replace(")", "")
   # print(gr_prod_per)
   gr_prod_title = container.h2.text
   # print(gr_prod_title)
   if container.find('font', {'style': 'color:#FF0000'}) != None :
    gr_price_text = container.find('font', {'style': 'color:#FF0000'}).text.replace(".", ",")
   else :
    gr_price_text = container.find('td', {'class': 'web-product-price'}).b.text.replace(".", ",")
   # print(gr_price_text)
   # gr_a_text = container.find('div', {'style': 'display:block;width:auto;padding:0 5px 7px 0;'}).text
   # print(gr_a_text)
   # ws_write.write(e, 4, cy_price_text
   gr_categories = container.find('td', {'class' : 'web-product-info'}).text
   if gr_categories.find('Κατηγορία:') >= 0 :
    if gr_categories.find('Υποκατηγορία:') >= 0 :
     gr_cat = gr_categories[gr_categories.find("Κατηγορία:\xa0 ")+12:gr_categories.find("Υποκατηγορία:\xa0 ")-4]
     gr_subcat = gr_categories[gr_categories.find("Υποκατηγορία:\xa0 ")+15:gr_categories.find("Κατασκευαστής")-4]
     gr_brand = gr_categories[gr_categories.find("Κατασκευαστής:")+16:]
    else :
     gr_cat = gr_categories[gr_categories.find("Κατηγορία:\xa0 ")+12:gr_categories.find("Κατασκευαστής")-4]
     gr_subcat = ""
     gr_brand = gr_categories[gr_categories.find("Κατασκευαστής:")+16:]
   else :
    print("No categories found. Will leave the fields empty but will error out when uploading product.")
    gr_cat = ""
    gr_subcat = ""
    gr_brand = ""
   gr_a_page = "https://www.e-shop.gr/s/" + gr_prod_per
   req = urllib.request.Request(gr_a_page, headers = headers)
   gr_a_uClient = uReq(req)
   gr_a_pagesoup = soup(gr_a_uClient.read(), "html5lib")
   gr_a_uClient.close()
   if gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"}) == None :
    gr_a_text = "Εξαντλημένο"
   else :
    gr_a = gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
    if gr_a.text.find('Κατόπιν') <= 16 :
     gr_a_text = gr_a.text[gr_a.text.find(":") + 2:]
    else :
     gr_a_text = gr_a.text[gr_a.text.find(":") + 2:gr_a.text.find("\n")].strip()
   gr_oem = ""
   # if page_soup.find('td', {'class': 'product_table_body'}) == None or page_soup.find('td', {'class': 'product_table_body'}) != "Περιγραφή " :
    # gr_desc_text = ""
   # else :
    # gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
    # if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
     # gr_desc_text = ""
    # else :
     # gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
   gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
   gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
   if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text != "Περιγραφή " :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
    gr_desc_text = ""
   else :
    gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html calues and any .gr mentions
    if gr_desc_text.find('Vendor OEM:') > 0 :
     if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
      string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
     else :
      string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
     gr_desc_text = string.strip()  # keep only what is before the OEM
     oem = rest.strip()  # keep only what is after the OEM
     gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
     gr_oem = gr_oem.strip()
    # if gr_desc_text.find('<br><br>Barcode') > 0 :  # if barcode exists in GR
    if gr_desc_text.find('Barcode:') > 0 :  # if both barcode and OEM exists
     if gr_desc_text.find('<br><br>Barcode:') > 0 :
      string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode')  # seperate the text
     else :
      string, barcode, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
     # gr_desc_text = string.strip() + rest.strip() # keep only what is before the barcode
     gr_desc_text = string.strip() # keep only what is before the barcode
     # while gr_desc_text.strip()[-4:] == "<br>" :  # if the 4 ending text characters are <br>
      # string, br, rest = gr_desc_text.rpartition('<br>')  # seperate the text
      # gr_desc_text = string.strip()  # keep ony what is before <br>
     # gr_oem = rest.replace("</li>", "").strip()
    if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
     crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
     gr_desc_text = rest.strip()  # keep only the rest of the text
    # if gr_desc_text.find('<p ') >= 0 :
     # p, align, rest = gr_desc_text.partition('>')
     # gr_desc_text = '<p align="justify">' + rest.strip()pyth
    if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
     p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
     gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
    else :
     gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
    if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
     if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
      string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
     elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
      string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
     if gr_prod_title.find('ASUS') > 0 :
      warranty_text = ' <a href="page.phtml?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b> </li>'
     else :
      warranty_text = ' .</b> </li>'
     gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
    elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
     if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
      string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
     elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
      string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
     gr_desc_text = string + "<b>Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
    elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
     string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
    elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
     string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
     gr_desc_text = string + rest.strip()  # and keep the before and after text
    else :
     print("No Warranty found. Will keep text as is.")
   if len(gr_a_pagesoup.findAll('div', {'class': 'also_box'})) > 0 :
    gr_sxetika = gr_a_pagesoup.findAll('div', {'class': 'also_box'})
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
   cy_page = "http://www.eshopcy.com.cy/product?id=" + gr_prod_per
   req = urllib.request.Request(cy_page, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     cy_uClient = uReq(req)
     cy_page_soup = soup(cy_uClient.read(), "html5lib")
     cy_uClient.close()
     break
    # except http.client.IncompleteRead :
    except Exception as exc :
     # print("On except :" + str(attempt))
     print("Oops, just bumped into the following exception: " + str(exc))
     print("Retrying in 5 seconds.")
     attempt += 1
     time.sleep(5)
   cy_prod_title = cy_page_soup.h1.text
   cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
   if len(cy_prod_title) == 0 :
    cy_price_text = "Θέλει άνοιγμα"
    cy_cat = ""
    cy_brand = ""
    cy_subcat = ""
   else :
    if len(cy_price) == 0 :
     cy_price_text = "Εξαντλημένο"
    else :
     cy_price_text = cy_price[0].text.replace("\xa0€", "").replace(".", ",")
    cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
    cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
    cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
    if len(cy_categories) > 2 :
     cy_subcat = cy_categories[3].text.strip()
    else :
     cy_subcat = ""
   print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
   print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
   print("Description: " + gr_desc_text)
   print("Sxetika: " + sxetika_list)
   print("")
   ws_write.write(e, 0, gr_prod_per)
   ws_write.write(e, 1, gr_prod_title)
   ws_write.write(e, 2, gr_oem.strip())
   ws_write.write(e, 3, gr_price_text)
   ws_write.write(e, 4, gr_cat)
   ws_write.write(e, 5, gr_subcat)
   ws_write.write(e, 6, gr_brand)
   ws_write.write(e, 7, sxetika_list)
   ws_write.write(e, 8, gr_desc_text)
   ws_write.write(e, 9, gr_a_text)
   ws_write.write(e, 10, cy_price_text)
   ws_write.write(e, 11, cy_cat)
   ws_write.write(e, 12, cy_subcat)
   ws_write.write(e, 13, cy_brand)
   e += 1
elif gr_page_soup.findAll("h1", {"style": "color:#4f4f4f;font-family:Tahoma;font-size:18px;font-weight:bold;padding:0 0 0 0;"}) :  # single product found
 print("Only 1 product found. Treating results as a single product page.")
 print("")
 gr_prod_per = gr_page_soup.find('td', {'style' : 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text
 gr_prod_link = 'https://www.e-shop.gr/product?id=' + gr_prod_per
 gr_prod_title = gr_page_soup.h1.text
 gr_price_text = gr_page_soup.find('span', {'class' : 'web-price-value-new'}).text.replace('\xa0€', '').replace('.', ',')
 if gr_page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"}) == None :
  gr_a_text = "Εξαντλημένο"
 else :
  gr_a = gr_page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
  if gr_a.text.find('Κατόπιν') <= 16 :
   gr_a_text = gr_a.text[gr_a.text.find(":") + 2:]
  else :
   gr_a_text = gr_a.text[gr_a.text.find(":") + 2:gr_a.text.find("\n")].strip()
 gr_categories = gr_page_soup.findAll('td', {'class' : 'faint1'})
 gr_cat = gr_categories[1].text[:gr_categories[1].text.find(' •')]
 gr_brand = gr_categories[1].text[gr_categories[1].text.find(' •')+2:gr_categories[1].text.find('στην')].strip()
 if len(gr_categories) > 2 :
  gr_subcat = gr_categories[3].text.strip()
 else :
  gr_subcat = ""
 gr_oem = ""
 # if page_soup.find('td', {'class': 'product_table_body'}) == None or page_soup.find('td', {'class': 'product_table_body'}) != "Περιγραφή " :
  # gr_desc_text = ""
 # else :
  # gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
  # if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
   # gr_desc_text = ""
  # else :
   # gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
 gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text != "Περιγραφή " :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  gr_desc_text = ""
 else :
  gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html calues and any .gr mentions
  if gr_desc_text.find('Vendor OEM:') > 0 :
   if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
    string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
   else :
    string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
   gr_desc_text = string.strip()  # keep only what is before the OEM
   oem = rest.strip()  # keep only what is after the OEM
   gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
   gr_oem = gr_oem.strip()
  # if gr_desc_text.find('<br><br>Barcode') > 0 :  # if barcode exists in GR
  if gr_desc_text.find('Barcode:') > 0 :  # if both barcode and OEM exists
   if gr_desc_text.find('<br><br>Barcode:') > 0 :
    string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode')  # seperate the text
   else :
    string, barcode, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
   # gr_desc_text = string.strip() + rest.strip() # keep only what is before the barcode
   gr_desc_text = string.strip() # keep only what is before the barcode
   # while gr_desc_text.strip()[-4:] == "<br>" :  # if the 4 ending text characters are <br>
    # string, br, rest = gr_desc_text.rpartition('<br>')  # seperate the text
    # gr_desc_text = string.strip()  # keep ony what is before <br>
   # gr_oem = rest.replace("</li>", "").strip()
  if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
   crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
   gr_desc_text = rest.strip()  # keep only the rest of the text
  # if gr_desc_text.find('<p ') >= 0 :
   # p, align, rest = gr_desc_text.partition('>')
   # gr_desc_text = '<p align="justify">' + rest.strip()pyth
  if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
   p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
   gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
  else :
   gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
  if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
   if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
    string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
   elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
    string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
   if gr_prod_title.find('ASUS') > 0 :
    warranty_text = ' <a href="page.phtml?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b> </li>'
   else :
    warranty_text = ' .</b> </li>'
   gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
  elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
   if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
    string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
   elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
    string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
   gr_desc_text = string + "<b>Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
  elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
   string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
  elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
   string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
   gr_desc_text = string + rest.strip()  # and keep the before and after text
  else :
   print("No Warranty found. Will keep text as is.")
 if len(gr_page_soup.findAll('div', {'class': 'also_box'})) > 0 :
  gr_sxetika = gr_page_soup.findAll('div', {'class': 'also_box'})
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
 cy_page = "http://www.eshopcy.com.cy/product?id=" + gr_prod_per
 req = urllib.request.Request(cy_page, headers = headers)
 attempt = 0
 while attempt < 3 :
  try :
   # print("On try :" + str(attempt))
   cy_uClient = uReq(req)
   cy_page_soup = soup(cy_uClient.read(), "html5lib")
   cy_uClient.close()
   break
  # except http.client.IncompleteRead :
  except Exception as exc :
   # print("On except :" + str(attempt))
   print("Oops, just bumped into the following exception: " + str(exc))
   print("Retrying in 5 seconds.")
   attempt += 1
   time.sleep(5)
 cy_prod_title = cy_page_soup.h1.text
 cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(cy_prod_title) == 0 :
  cy_price_text = "Θέλει άνοιγμα"
  cy_cat = ""
  cy_brand = ""
  cy_subcat = ""
 else :
  if len(cy_price) == 0 :
   cy_price_text = "Εξαντλημένο"
  else :
   cy_price_text = cy_price[0].text.replace("\xa0€", "").replace(".", ",")
  cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
  cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
  cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
  if len(cy_categories) > 2 :
   cy_subcat = cy_categories[3].text.strip()
  else :
   cy_subcat = ""
 print(gr_prod_per + " - " + gr_prod_title + " - GR: " + gr_price_text + " - CY: " + cy_price_text + ".")
 print(gr_cat + " - " + gr_subcat + " - " + gr_brand + " - " + gr_a_text)
 print("Description: " + gr_desc_text)
 print("Sxetika: " + sxetika_list)
 print("")
 ws_write.write(e, 0, gr_prod_per)
 ws_write.write(e, 1, gr_prod_title)
 ws_write.write(e, 2, gr_oem.strip())
 ws_write.write(e, 3, gr_price_text)
 ws_write.write(e, 4, gr_cat)
 ws_write.write(e, 5, gr_subcat)
 ws_write.write(e, 6, gr_brand)
 ws_write.write(e, 7, sxetika_list)
 ws_write.write(e, 8, gr_desc_text)
 ws_write.write(e, 9, gr_a_text)
 ws_write.write(e, 10, cy_price_text)
 ws_write.write(e, 11, cy_cat)
 ws_write.write(e, 12, cy_subcat)
 ws_write.write(e, 13, cy_brand)
else :
 # print("")
 print("Search result is probably empty. Try again with different terms.")
 print("")
 sys.exit()
 

# try to write to the 1st file. If it fails try the 2nd
try :
 wb_write.save(write_file)
 print("")
 print(write_file + " created on " + write_path)
except :
 print("")
 wb_write.save(alt_write_file)
 print(alt_write_file + " created on " + write_path)


elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("")
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
