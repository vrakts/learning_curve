sheets = spreadsheet.sheets
for i in range(0, len(sheets)) :
 print('Φύλλο ' + str(i) + ': ' + sheets[i].name)

answer = 'Διάλεξε φύλλο: '
sheet_index = input(answer)
if sheet_index == "" :
 sheet = sheets[0]
else :
 sheet = sheets[int(sheet_index)]
print("")

rowcount = sheet.nrows()
colcount = sheet.ncols()
ac_row = 1
for i in range(0, colcount) :
 print('Στήλη ' + str(i) + ': ' + str(sheet[0, i].value))

answer = 'Διάλεξε στήλη: '
col_index = input(answer)
if col_index == "" :
 col_index = 0
else :
 col_index = int(col_index)
print("")

for i in range(1, rowcount):
 if str(sheet[i, col_index].value) != "None" :
  ac_row += 1
 else :
  print('Σύνολο γραμμών: ' + str(ac_row))
  break

answer = 'Αρχική γραμμή: '
row_index = input(answer)
if row_index == "" :
 row_index = 1
else :
 row_index = int(row_index)
print("")
