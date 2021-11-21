import os  # for the ability to use os function like change folder

ac_row = 100

answer_term = "no"
while (answer_term == "no") :
 input_row = input("Found " + str(ac_row) + " rows. Enter start row (press enter for default (1)): ")
 if int(input_row) > ac_row :
  input_row = input("Start row is larger than total rows. Try again: ")
 elif input_row == "" :
  start_row = 1
 else :
  os.system('cls')
  print("Wrong selection. Please try again.")
 print("")


print(input_row)