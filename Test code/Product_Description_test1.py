### not working. The description table is not "text"

# Current Version 1.0
# Changelog: 1.0
# - Retrieves product codes from an excel file, verifies that no description exists and gets description from GR.
# - Uses the new read / write procdures and anwser procedures.

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
import ezodf  # for the ability to write to open document format files
from datetime import date
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder

##########################################
# Setting starting date and time values. #
##########################################

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)

################################
# End of date and time setting #
################################

###############################
# Setting correct read paths. #
###############################

if os.path.exists(r'K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ') == True :  # does work folder exist?
 read_path = (r'K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ')
 print("Using " + read_path + " for reading files.")
elif os.path.exists(r"Z:\Users\Vrakts\Desktop\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does home folder exist?
 read_path = (r"Z:\Users\Vrakts\Desktop\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Using " + read_path + " for writing files.")

##############################
# End of read paths setting. #
##############################

################################
# Setting correct write paths. #
################################

if os.path.exists(r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Using " + write_path + " for writing files.")
elif os.path.exists(r"Z:\Users\Vrakts\Desktop\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does home folder exist?
 write_path = (r"Z:\Users\Vrakts\Desktop\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Using " + write_path + " for writing files.")
else :
 if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Using " + write_path + " for writing files.")
 else :  # if not create it
  os.makedirs(r"C:\TEMPYTH")
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Creating and using " + write_path + " for writing files.")

###############################
# End of write paths setting. #
###############################

# Opening files
# For reading
os.chdir(read_path)
read_file = ('DESCRIPTION_CONTROL.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# for writing
os.chdir(write_path)
write_file = ("DESCRIPTION_CONTROL_RES.xls")  # name of xls write file
alt_write_file = ("DESCRIPTION_CONTROL_RES_ALT.xls")  # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet(start_date)  # add 1st sheet in virtual workbook
ws_write.write(0, 0, "PCODE")  # write title on A1 cell
ws_write.write(0, 1, "DESCRIPTION")  # write title on B1 cell

##################################
# Sheet and row/columns setting. #
##################################

sheets = spreadsheet.sheets
sheet = sheets[1]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1  # actual rows with data on them
dirty = 0  # did something change? then dirty will change to 1

e = 1  # this is the counter for the excel write file

#########################################
# End of sheet and row/columns setting. #
#########################################

#############################
# Parsing code starts here. #
#############################

for i in range(1, rowcount) :
 # print(ac_row)
 if str(sheet[i, 2].value) != "None" :
  ac_row = ac_row + 1
 else:
  break

print("")
print("Starting Description Control check ...")
for i in range(1, ac_row) :
 if str(sheet[i, 1].value.strip()) == "None" :
  break
 else :
  page_url = "https://www.e-shop.gr/product?id=" + sheet[i, 1].value.strip()
  # print(page_url)
  uClient = uReq(page_url)
  page_soup = soup(uClient.read(), "html.parser")
  try :
   uClient.close()
   description = page_soup.find("td", {"class" : "product_table_body"})
  except :
   print("URL read error probably occured. Skipping this row.")
   pass	
 ws_write.write(e, 0, sheet[i, 1].value.strip())
 ws_write.write(e, 1, description)
 e = e + 1
 print("")
 print("Description copied for " + str(sheet[i, 1].value.strip()))

wb_write.save(write_file)

########################
# End of parsing code. #
########################

#############################
# Calculating elapsed time. #
#############################

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = (str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
print("Script executed in: " + formatted_time)

################
# End of flie. #
################

