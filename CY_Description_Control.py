### Given a list of codes it creates a URL to show all codes as a query page.
### Helps with the other scripts to check for descriptions, prices etc.

import clipboard, xlwt, os

items = []
products = []
write_path = (r'C:\Users\manager\Desktop')
write_file = ('descctrl.xls')
os.chdir(write_path)
wb_write = xlwt.Workbook()
ws_write = wb_write.add_sheet("descctrl", cell_overwrite_ok = True)

i = 0
e = 0
answer = "x"
while answer != "" :
 answer = input("Paste values (leave empty to terminate process): ")
 items.append(answer.strip())

for item in items :
 if item == "" :
  continue
 code = item[0:item.find(' ')]
 title = item[item.find(' '):item.find(' GR CY')].strip()
 print(code + " - " + title)
 ws_write.write(e, 0, code)
 ws_write.write(e, 1, title)
 e += 1

wb_write.save(write_file)