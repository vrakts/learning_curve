from datetime import datetime
import os, sys

### listing files and renaming
write_path = r"S:\VIDEO"
try :
 os.chdir(write_path)
 dirs = os.scandir(write_path)
 for file in dirs :
  info = file.stat()
  file_name = file.name
  extent = file_name[file_name.rfind("."):]
  d = datetime.fromtimestamp(info.st_mtime)
  formatted_date = d.strftime('%Y-%m-%d_%H-%M-%S')
  print("File name: " + file_name + ", Time: " + formatted_date)
  os.rename(file, formatted_date + extent)
except :
 print("Video folder not found.")

### arranging date for the txt file
now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)

### write the formatted date to the txt file
write_path = r"S:\\"
try :
 os.chdir(write_path)
 file = open("time.txt", "w")
 file.write(formatted)
 file.close()
except :
 input("Write path not found. Insert USB or check the drive letter.")
 sys.exit(1)
