from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import urllib.request
import xlrd  # for the ability to read excel (XLS) files
import xlwt  # for the ability to write to excel (XLS) files
import ezodf  # for the ability to write to open document format (ODF) files
from datetime import date  # for the ability to get dates
import time  # for the ability to measure time
import os  # for the ability to use os functions
import os.path  # for the ability to get information on folders
import re  # for regex

##########################################
# Setting starting date and time values. #
##########################################

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)
print("")

################################
# End of date and time setting #
################################

###############################
# Setting correct read paths. #
###############################

if os.path.exists(r'W:\OneDrive\Ανταγωνισμός Λευκωσίας') == True :  # does work folder exist?
 read_path = (r'W:\OneDrive\Ανταγωνισμός Λευκωσίας')
 print("Using " + read_path + " for reading files.")
 print("")
elif os.path.exists(r"Z:\Users\Vrakts\Desktop\Ανταγωνισμός Λευκωσίας") == True :  # does home folder exist?
 read_path = (r"Z:\Users\Vrakts\Desktop\Ανταγωνισμός Λευκωσίας")
 print("Using home path for reading files.")
 print("")

##############################
# End of read paths setting. #
##############################

################################
# Setting correct write paths. #
################################

if os.path.exists(r"W:\OneDrive\Ανταγωνισμός Λευκωσίας") == True :  # does work folder exist?
 write_path = (r"W:\OneDrive\Ανταγωνισμός Λευκωσίας")
 print("Using " + write_path + " for writing files.")
 print("")
elif os.path.exists(r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Home") == True :  # does home folder exist?
 write_path = (r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Home")
 print("Using home path for writing files.")
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

# Opening files
# For reading
os.chdir(read_path)
read_file = ('CUSTOMPC - ΒΛΑΔΙΜΗΡΟΣ.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# for writing
os.chdir(write_path)
write_file = ("CY_CustomPC_Difference.xls")  # name of xls write file
alt_write_file = ("CY_CustomPC_Difference_Alt.xls")  # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date)  # add 1st sheet in virtual workbook
ws_write.write(0, 0, "ESHOPCY")  # write title on A1 cell
ws_write.write(0, 1, "PRICE")  # write title on B1 cell
ws_write.write(0, 2, "CUSTOMPC")  # write title on C1 cell
ws_write.write(0, 3, "PRICE")  # write title on D1 cell
ws_write.write(0, 4, "AVAILABILITY")  # write title on E1 cell

##################################
# Sheet and row/columns setting. #
##################################

# Counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[0]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1
# Counting rows that contain actual data (ac_row)
for i in range(1, rowcount):
 if str(sheet[i, 0].value) != "None" :
  ac_row = ac_row + 1
 else:
  break

e = 1  # this is the counter for the excel write file
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"


#########################################
# End of sheet and row/columns setting. #
#########################################

#############################
# Parsing code starts here. #
#############################

pure_code = str(sheet[672, 2].value).strip().replace('.0', '')  # clean up the product code from . and 0s
# print("pure_code is: " + pure_code)
cp_search_url = "https://www.custompc.com.cy/search/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&scode_from_q=Y&cid=0&q=" + pure_code
# print("cp_search_url is: " + cp_search_url)
req = urllib.request.Request(cp_search_url, headers = headers)
cp_uClient = uReq(req)
cp_page_soup = soup(cp_uClient.read(), "html.parser")
cp_uClient.close()
cp_price = cp_page_soup.findAll('span', {'class' : 'ty-price-num'})  # find all price related info from the product page
cp_price_text = cp_price[1].text.replace('.', ',')  # keep only the price value of the first find (other values are for related products)
# print("cp_price_text: " + str(cp_price_text))
cp_prod_url = cp_page_soup.findAll('a', {'class' : 'product-title'})  # find all product URLs from the query page
cp_prod_url = cp_prod_url[0]['href']
# print("cp_prod_url: " + cp_prod_url)
cp_uClient = uReq(cp_prod_url)
cp_prod_soup = soup(cp_uClient.read(), "html.parser")
cp_uClient.close()
cp_pcode = cp_prod_soup.find('div', {'class' : 'ty-control-group ty-sku-item cm-hidden-wrapper'}).text  # extract the product code container from the product page
cp_pcode = cp_pcode.strip()[cp_pcode.find(':'):]  # extract only the product code from the product page
cp_avail = cp_prod_soup.findAll('div', {'class' : 'ty-control-group product-list-field'})  # if not then try the no stock container
cp_avail = cp_avail[1].text.strip()[cp_avail[1].text.strip().find(':')+2:]  # remove unecessary text

cy_page_url = "http://www.eshopcy.com.cy/product?id=" + sheet[672, 0].value.strip()  # add stripped product code to product url
cy_uClient = uReq(cy_page_url)
cy_page_soup = soup(cy_uClient.read(), "html.parser")
cy_uClient.close()
cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})  # extract price from the product url

cy_price_text = cy_price[0].text.replace("\xa0€","").replace(".", ",")  # otherwise get price stripped from euro signs and .
cy_temp_price = str(sheet[672, 3].value).strip().replace('€', '').strip()  # set a temp price for the CY price in the excel without zeros and stripped

if cy_temp_price == "None" :  # if temp price is empty
 cy_temp_price = ""  # set temp price as ""
 # print("cy_temp_price is empty. Not changed")
elif cy_temp_price.find(',') > 0 :  # if it has a , then it is a float
 if (cy_temp_price[:-1] != 0) and len(cy_temp_price[cy_temp_price.find(',')+1:]) == 1:  # if the last number is not a zero and there is only 1 digit after ,
  cy_temp_price = cy_temp_price + "0"  # then add a zero to the end.
  # print("cy_temp_price is a float with 1 digit at the end. Added 1 zero.")
else :
 cy_temp_price = str(sheet[672, 3].value).strip().replace('€', '').strip() + ",00"  # if cy_temp_price is not a float, add ,00
 # print("cy_temp_price not a float. Changed temp price to ,00")

cp_temp_price = str(sheet[672, 4].value).strip().replace('€', '').strip()  # set a temp price for the CP price in the excel without zeros and stripped
if cp_temp_price == "None" :  # if temp price is empty
 cp_temp_price = ""  # set temp price as ""
 # print("cp_temp_price is empty. Not changed")
elif cp_temp_price.find(',') > 0 :  # if it has a , then it is a float
 if (cp_temp_price[:-1] != 0) and len(cp_temp_price[cp_temp_price.find(',')+1:]) == 1 :  # if the last number is not a zero and there is only 1 digit after ,
  cp_temp_price = cp_temp_price + "0"  # then add a zero to the end.
  # print("cp_temp_price is a float with 1 digit at the end. Added 1 zero.")
else :
 cp_temp_price = str(sheet[672, 4].value).strip().replace('€', '').strip() + ",00"  # if cp_temp_price is not a float, add ,00
 # print("cp_temp_price not a float. Changed temp price to ,00")
