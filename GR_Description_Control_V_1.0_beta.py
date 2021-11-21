# Current Version 1.0 beta
##########################
# Changelog V1.0 beta
# - Initial attempt to read the codes from a predefined file.
#	and get the details and description from the GR site.
# - Uses the new corrected description reading functions.

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
 if gr_categories[1].text.find(' •') > 0 :
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

def get_gr_description(page_soup, prod_per, gr_cat) :
 # global string, warranty, rest, gr_oem, barcode, gr_desc_result
 global gr_oem, barcode, gr_desc_result
 gr_desc_text = ""
 gr_oem = ""
 barcode = ""
 rest = ""
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
   print("Contacting Vendors...")
   if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
    string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
   else :
    string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
   gr_desc_text = string.strip()  # keep only what is before the OEM
   oem = rest.strip()  # keep only what is after the OEM
   gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
   gr_oem = gr_oem.strip()
  if gr_desc_text.find('Barcode:') > 0 or gr_desc_text.find('EAN-13:') > 0 :  # if both barcode and OEM exists
   print("Calculating barcodes...")
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
   print("Doing some crazy stuff...")
   crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
   gr_desc_text = rest.strip()  # keep only the rest of the text
  if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
   print("Aligning edges...")
   p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
   gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
  else :
   gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
  if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
   print("Writing warranties...")
   if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
    string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
   elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
    string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
   if gr_prod_title.find('ASUS') > 0 or gr_prod_title.find('DELL') > 0 :
    # warranty_text = ' <a href="http://www.eshopcy.com.cy/page?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b></li>'
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
   print("Arrival defects...")
   string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
   gr_desc_text = string + rest.strip()  # and keep the before and after text
  elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
   print("Arrival defects...")
   string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
   gr_desc_text = string + rest.strip()  # and keep the before and after text
  else :
   print("No special Warranty found.")
  if gr_desc_text.find('<p></p>') > 0 :
   gr_desc_text.replace('<p></p>', '') 
  if gr_desc_text.find('<b>Εγγύηση') >= 0 or gr_desc_text.find('Εγγύηση:') >= 0 :
   war_start = gr_desc_text.find('Εγγύηση:')
   ### if the years are misspelled it is not autocorrected in the CY site. Not looking for "." at the end.
   if gr_desc_text[war_start:].find("1 Χρόνος") > 0 or gr_desc_text[war_start:].find("1 χρόνος") > 0 or gr_desc_text[war_start:].find("1 Χρόνο") > 0 or gr_desc_text[war_start:].find("1 χρόνο") > 0 or  gr_desc_text[war_start:].find("1 Χρονο") > 0 or gr_desc_text[war_start:].find("1 χρονο") > 0 or gr_desc_text[war_start:].find("1 Έτος") > 0 or gr_desc_text[war_start:].find("1 έτος") > 0 or gr_desc_text[war_start:].find("1 Ετος") > 0 or gr_desc_text[war_start:].find("1 ετος") > 0 or  gr_desc_text[war_start:].find("2 Έτη") > 0 or gr_desc_text[war_start:].find("2 έτη") > 0 or gr_desc_text[war_start:].find("24 Μήνες") > 0 or gr_desc_text[war_start:].find("24 μήνες") > 0 :
    print("Year adjustment...")
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
  if gr_desc_text.find("Ά") > 0 or gr_desc_text.find("’") > 0 or gr_desc_text.find('face="Constantia" size="3"') > 0 or gr_desc_text.find('size="3" face="Constantia"') > 0 :
   print("Taking out the trash...")
   gr_desc_text = gr_desc_text.replace("Ά", "&#902;")
   gr_desc_text = gr_desc_text.replace("’", "&#902;")
   gr_desc_text = gr_desc_text.replace('face="Constantia" size="3"', '')
   gr_desc_text = gr_desc_text.replace('size="3" face="Constantia"', '')
  if gr_desc_text == '<p align="justify">' or gr_desc_text == '<p align="justify"><br><br>' :
   print("Throwing away left overs...")
   gr_desc_text = ""
 if prod_per.find('EPI.') >= 0 :
  if gr_cat.find('ΟΠΛΑ ΜΕ ΑΦΡΩΔΗ ΒΕΛΑΚΙΑ') >= 0 :
   gr_desc_text = gr_desc_text + '<p align="justify"><b><u><font style="color:#ff0000;">ΠΡΟΣΟΧΗ!</font></u></b> Δεν είναι κατάλληλο για παιδιά κάτω των 36 μηνών. Απαραίτητη η επίβλεψη ενηλίκου. Μην στοχεύετε στα μάτια ή το πρόσωπο. <b>ΓΙΑ ΑΠΟΦΥΓΗ ΤΡΑΥΜΑΤΙΣΜΟΥ</b>: Χρησιμοποιήστε μόνο τα βελάκια που είναι σχεδιασμένα για αυτό το προϊόν. Μην τροποποιήσετε τα βελάκια ή τον εκτοξευτή.</p>'
  elif gr_cat.find('DARTBOARD') >= 0 :
   gr_desc_text = gr_desc_text + '<p align="justify"><b><u><font style="color:#ff0000;">ΠΡΟΣΟΧΗ!</font></u></b> Δεν είναι κατάλληλο για παιδιά κάτω των 36 μηνών. Κίνδυνος πνιγμού λόγω ύπαρξης μικρών και μυτερών κομματιών. Απαραίτητη η επίβλεψη ενηλίκου. Συνιστώμενη ελάχιστη ηλικία 8 ετών και άνω.</p>'
  else :
   gr_desc_text = gr_desc_text + '<p align="justify"><b><u><font style="color:#ff0000;">ΠΡΟΣΟΧΗ!</font></u></b> Δεν είναι κατάλληλο για παιδιά κάτω των 36 μηνών.</p>'
 gr_desc_result = gr_desc_text

attempt = 0  # how many attempts to re-read the url in case of failure
sorry = 0  # will add up in case of exceptions
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

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

if os.path.exists(r'K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ') == True :  # does work folder exist?
 read_path = (r'K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ')
 print("Using " + read_path + " for reading files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does home folder exist?
 read_path = (r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Using home path 1 for reading files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does home folder 1 exist?
 read_path = (r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Using home path 2 for reading files.")
 print("")
else :
 print("No folders or files found. Where am I?")
 sys.exit(0)

#########################
# End of paths setting. #
#########################

#################
# Opening files #
#################

# For reading
os.chdir(read_path)
read_file = ('DESCRIPTION_CONTROL.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
try :
 spreadsheet = ezodf.opendoc(read_file)  # open file
except Exception as e:
 print("-----------------------------------------------")
 print("Oops. Just bumped into the following exception:")
 print(e)
 print("-----------------------------------------------")
 print("")
 print("Probably the file " + read_file + " is not valid or")
 print("not in " + read_path + " path.")
 sys.exit("Please check the file name and try again with a different one.")

ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# Counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[3]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1
# Counting rows that contain actual data (ac_row)
for i in range(2, rowcount):
 if str(sheet[i, 1].value) != "None" :
  ac_row += 1
 else:
  break

# for writing
os.chdir(read_path)
write_file = ("DESCRIPTION_CONTROL_RESULTS.xls")  # name of xls write file
alt_write_file = ("DESCRIPTION_CONTROL_RESULTS_alt.xls")  # alternate name of xls write file
wb_write = xlwt.Workbook()
ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok=True)

ws_write.write(0, 0, "PER_CODE")  # write title on A1 cell
ws_write.write(0, 1, "TITLE")  # write title on B1 cell
ws_write.write(0, 2, "OEM")  # write title on C1 cell
ws_write.write(0, 3, "SXETIKA")  # write title on D1 cell
ws_write.write(0, 4, "DESCRIPTION")  # write title on D1 cell

#############################
# Parsing code starts here. #
#############################

for i in range(2, ac_row + 1):
 if str(sheet[i, 1].value) == "None" :
  break
 else :
  # print("Rows left: " + str(ac_row-i) + "/" + str(ac_row-1))
  print("Current row: " + str(i) + ". Rows left: " + str(ac_row-i-1) + "/" + str(ac_row-1) + ".")
  page_url = "https://www.e-shop.gr/s/" + sheet[i, 1].value.strip()
  req = urllib.request.Request(page_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    uClient = uReq(req)
    page_soup = soup(uClient.read(), "html5lib")
    uClient.close()
    break
   except Exception as exc :
    # print("On except :" + str(attempt))
    print("Oops, just bumped into the following exception: " + str(exc))
    print("Retrying in 5 seconds.")
    attempt += 1
    time.sleep(5)
  # gr_prod_per = sheet[i, 1].value.strip()
  # gr_prod_title = page_soup.h1.text
  get_gr_details(page_soup)
  get_gr_description(page_soup, sheet[i, 1].value.strip(), gr_cat)
  # gr_oem = ""
  # gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
  # gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
  # if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
   # gr_desc_text = ""
  # else :
   # gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html calues and any .gr mentions
   # if gr_desc_text.find('Vendor OEM:') > 0 :
    # if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
     # string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
    # else :
     # string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
    # gr_desc_text = string.strip()  # keep only what is before the OEM
    # oem = rest.strip()  # keep only what is after the OEM
    # gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
    # gr_oem = gr_oem.strip()
   # # if gr_desc_text.find('<br><br>Barcode') > 0 :  # if barcode exists in GR
   # if gr_desc_text.find('Barcode:') > 0 :  # if both barcode and OEM exists
    # if gr_desc_text.find('<br><br>Barcode:') > 0 :
     # string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode')  # seperate the text
    # else :
     # string, barcode, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
    # gr_desc_text = string.strip() # keep only what is before the barcode
   # if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
    # crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
    # gr_desc_text = rest.strip()  # keep only the rest of the text
   # if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
    # p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
    # gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
   # else :
    # gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
   # if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
    # if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
     # string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
    # elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
     # string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
    # if gr_prod_title.find('ASUS') > 0 :
     # warranty_text = ' <a href="page.phtml?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b> </li>'
    # else :
     # warranty_text = ' .</b> </li>'
    # gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
   # elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
    # if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
     # string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
    # elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
     # string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
    # gr_desc_text = string + "<b>Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
   # elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
    # string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
    # gr_desc_text = string + rest.strip()  # and keep the before and after text
   # elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
    # string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
    # gr_desc_text = string + rest.strip()  # and keep the before and after text
   # else :
    # print("No Warranty found.")
  # if gr_desc_text == '<p align="justify">' :
   # gr_desc_text = ""
  # if gr_desc_text.find('1 χρόνο') > 0 or gr_desc_text.find('1 Χρόνο') > 0 or gr_desc_text.find('1 Χρόνος') > 0 or gr_desc_text.find('1 χρόνος') > 0 or gr_desc_text.find('1 Έτος') > 0 or gr_desc_text.find('1 έτος') > 0 :   # if the years are misspelled it is not autocorrected in the CY site. Not looking for "." at the end.
   # gr_desc_text = gr_desc_text.replace('1 Χρόνος', '2 χρόνια')
   # gr_desc_text = gr_desc_text.replace('1 χρόνος', '2 χρόνια')
   # gr_desc_text = gr_desc_text.replace('1 Χρόνο', '2 χρόνια')
   # gr_desc_text = gr_desc_text.replace('1 χρόνο', '2 χρόνια')
   # gr_desc_text = gr_desc_text.replace('1 Έτος', '2 χρόνια')
   # gr_desc_text = gr_desc_text.replace('1 έτος', '2 χρόνια')
  # if len(page_soup.findAll('div', {'class': 'also_box'})) > 0 :
   # gr_sxetika = page_soup.findAll('div', {'class': 'also_box'})
   # sxetika_list = ""
   # for sxetika in gr_sxetika :
    # sxetika_per_link = sxetika.a['href']
    # sxetika_per = sxetika_per_link[sxetika_per_link.rfind('-')+1:]
    # if len(sxetika_list) == 0 :
     # sxetika_list = sxetika_per
    # else :
     # sxetika_list = sxetika_list + "," + sxetika_per
  # else :
   # sxetika_list = ""
  print(gr_prod_per + " - " + gr_prod_title)
  if len(gr_desc_result) > 0 :
   print("Description: " + gr_desc_result)
  if len(sxetika_list) > 0 :
   print("Sxetika: " + sxetika_list)
  print("")

  ws_write.write(i-1, 0, gr_prod_per) 		# OK
  ws_write.write(i-1, 1, gr_prod_title)		# OK
  ws_write.write(i-1, 2, gr_oem)			# OK
  ws_write.write(i-1, 3, sxetika_list)		# OK
  ws_write.write(i-1, 4, gr_desc_result)	# OK

try :
 wb_write.save(write_file)
 print("")
 print(write_file + " created on " + read_path)
except :
 print("")
 wb_write.save(alt_write_file)
 print(alt_write_file + " created on " + read_path)
 
elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = str(mins) + "." + str(seconds)
print("")
print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")

