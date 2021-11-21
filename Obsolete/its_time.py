from datetime import datetime
import os, sys

write_path = r"S:\\"

now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

print(formatted)

try :
 os.chdir(write_path)
 file = open("time.txt", "w")
 file.write(formatted)
 file.close()
except :
 sys.exit("Write path not found. Insert USB or check the drive letter.")
