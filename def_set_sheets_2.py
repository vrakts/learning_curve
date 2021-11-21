def set_sheets() :
 global ac_row, col_index, row_index, sheet
 sheet_list = []
 sheets = spreadsheet.sheets
 # for i in range(0, len(sheets)) :
  # print('Φύλλο ' + str(i + 1) + ': ' + sheets[i].name)

 print("Μαζεύω τα φύλλα... υπομονή.")
 for i in range(0, len(sheets)) :
  sheet_list.append(sheets[i].name)
 
 for i in range(0, len(sheet_list)) :
  print('Φύλλο ' + str(i + 1) + ': ' + sheet_list[i])

 answer = 'Διάλεξε φύλλο: '
 sheet_index = input(answer)
 if sheet_index == "" :
  sheet = sheets[0]
 else :
  sheet = sheets[int(sheet_index) - 1]
 print("")

 rowcount = sheet.nrows()
 colcount = sheet.ncols()
 ac_row = 1
 for i in range(0, colcount) :
  print('Στήλη ' + str(i + 1) + ': ' + str(sheet[0, i].value))

 answer = 'Διάλεξε στήλη: '
 col_index = input(answer)
 if col_index == "" :
  col_index = 0
 else :
  col_index = int(col_index) - 1
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
