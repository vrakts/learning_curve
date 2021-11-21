import ezodf
import os


os.chdir(r"C:\Users\Manager\Documents\Html Parser - Python")

ezodf.config.set_table_expand_strategy('all')
spreadsheet = ezodf.opendoc("stock.ods")
ezodf.config.reset_table_expand_strategy()

sheets = spreadsheet.sheets
sheet = sheets[0]
print(sheets[0].name)
sheets[0].name

rowcount = sheet.nrows()
colcount = sheet.ncols()

sheet['A1'].value

for i in range(2, rowcount-1):
 print(sheet['A' + str(i)].value)
 



for cell in sheet:
    print(cell.value)

for sheet in sheets:
    print(sheet.name)