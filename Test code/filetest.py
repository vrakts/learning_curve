import ezodf
import os  # for the ability to use os function like change folder

if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
 file_path = (r"C:\TEMPYTH")
 print("Using " + write_path + " for writing files.")
 print("")
else :  # if not create it
 os.makedirs(r"C:\TEMPYTH")
 file_path = (r"C:\TEMPYTH")
 print("Creating and using " + write_path + " for writing files.")
 print("")

os.chdir(write_path)

read_file = ('eshopgr.ods')
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config

write_file = ('eshopgr_desc.ods')

spreadsheet = ezodf.newdoc(doctype="ods", filename=write_file)