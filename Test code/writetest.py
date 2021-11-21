# read write and overwrite tests

import os
import xlwt
import ezodf

if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
	write_path = (r"C:\TEMPYTH")
	print("Predefined paths don't exist. Using " + write_path + " for writing files.")
else :  # if not create it
	os.makedirs(r"C:\TEMPYTH")
	write_path = (r"C:\TEMPYTH")
	print("Predefined paths don't exist. Creating and using " + write_path + " for writing files.")

os.chdir(write_path)
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet("SHEET1", cell_overwrite_ok=True)  # add 1st sheet in virtual workbook
# ws_write = wb_write.add_sheet("SHEET1")  # add 1st sheet in virtual workbook
ws_write.write(0, 0, "ESHOPCY")  # write title on A1 cell
ws_write.write(0, 0, "ESHOPCY")  # write title on A1 cell

try :
	wb_write.save("write_test.xls")
	print("File used: write_test.xls")
except :
	wb_write.save("write_test_2.xls")
	print("File write_test.xls seems to be open. Used: write_test_2.xls")

