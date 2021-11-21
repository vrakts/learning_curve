# where_is_python.py

import sys
import os

try:
    os.system("cls")
    print("Python exe: " + sys.executable)
    print("")
    print("Python path: " + sys.exec_prefix)
    print("")

    print("All python folders:")
    # 
    # print('\n'.join(sys.path))
    for p in sys.path:
        print(p)

except Exception as exc :
	print("Exception: " + str(exc))

print("")
input("Press any key to exit...")
sys.exit(0)