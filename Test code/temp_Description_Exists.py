# check if the product is uploaded in the CY website but out of stock

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
from urllib.request import Request
import ezodf  # for the ability to open and write open document format (ODF) files
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

def get_details(page_soup) :
 global desc_result, price_text
 d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup
 price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 prod_title = page_soup.h1.text
 if len(prod_title) == 0 :
  price_text = "Θέλει άνοιγμα"
 elif len(price) == 0 :
  price_text = "Ανεβασμένο - Εξαντλημένο"
 else :
  price_text = "Ανεβασμένο"
 if d_soup == None or d_soup.text.find('Σύνολο ψήφων') > 0 or product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  desc_result = "DESCRIPTION EMPTY"
 else :
  desc_result = "DESCRIPTION OK"

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

if os.path.exists(r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY') == True :  # does work folder exist?
 read_path = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY')
 print("Using " + read_path + " for reading files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder exist?
 read_path = (r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
 print("Using home path 1 for reading files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY") == True :  # does home folder 1 exist?
 read_path = (r"W:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY")
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
read_file = ('ΠΡΟΪΟΝΤΑ ΓΙΑ ΑΝΟΙΓΜΑ NEW.ods')  # path to ods read file
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
sheet = sheets[1]
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
write_file = ("DESCRIPTION_EXISTS.xls")  # name of xls write file
alt_write_file = ("DESCRIPTION_EXISTS_ALT.xls")  # alternate name of xls write file
wb_write = xlwt.Workbook()
ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok = True)

ws_write.write(0, 0, "PER_CODE")  	# write title on A1 cell
ws_write.write(0, 1, "PRICE_TEXT")  # write title on B1 cell
ws_write.write(0, 2, "DESCRIPTION")	# write title on C1 cell

#############################
# Parsing code starts here. #
#############################

for i in range(1, ac_row):
 if str(sheet[i, 0].value) == "None" :
  break
 else :
  print("Rows left: " + str(ac_row-i) + "/" + str(ac_row-1))
  page_url = "http://www.eshopcy.com.cy/product?id=" + sheet[i, 0].value.strip()
  req = Request(page_url, headers = headers)
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
  get_details(page_soup)
  ws_write.write(i, 0, sheet[i, 0].value.strip())	# OK
  ws_write.write(i, 1, price_text)					# OK
  ws_write.write(i, 2, desc_result)					# OK

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

