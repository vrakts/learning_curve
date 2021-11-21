import os.path

###############################
# Setting correct read paths. #
###############################

if os.path.exists(r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας') == True :  # does work folder exist?
 read_path = (r'K:\SALES\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας')
 print("Using " + read_path + " for reading files.")
elif os.path.exists(r"Z:\Users\Vrakts\Desktop\Ανταγωνισμός Λευκωσίας") == True :  # does home folder exist?
 read_path = (r"Z:\Users\Vrakts\Desktop\Ανταγωνισμός Λευκωσίας")
 print("Using " + read_path + " for writing files.")

##############################
# End of read paths setting. #
##############################

################################
# Setting correct write paths. #
################################

if os.path.exists(r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\Script Results")
 print("Using " + write_path + " for writing files.")
elif os.path.exists(r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Home") == True :  # does home folder exist?
 write_path = (r"Z:\Users\Vrakts\Desktop\Html Parser - Python\Home")
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

os.chdir(read_path)
print("Current write path is: " + os.getcwd())
os.chdir(write_path)
print("Current write path is: " + os.getcwd())
