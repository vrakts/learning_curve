from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
import ezodf  # for the ability to write to open document format files
from datetime import date
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder

# Input search term
answer_term = "no"

# Setting date and time values
start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)

file_path = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\GR - CY')  # path to read and write file
file_name = "2019 OCTOBER 24 - ΠΡΟΪΟΝΤΑ ΓΙΑ ΑΝΟΙΓΜΑ.ods"
write_path = os.chdir(file_path)  # change active directory to file_path

# opening ods file for reading
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(file_name)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config

# opening xls file for writing
write_date = file_name[:file_name.find("-")-1]