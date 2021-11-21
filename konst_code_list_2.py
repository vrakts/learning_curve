import os
try:
    codes_list = []
    while True:
        code = input("Δώσε: ")
        codes_list.append(code)
except KeyboardInterrupt:
    codes_list.sort()
    code_set = set(codes_list)

path = "Z:\\OneDrive\\eShop Stuff\\Synced\\Κουτσοδούλια\\KonstaStock\\11-2021"
os.chdir(path)

with open("codes.txt", "w") as f:
    f.write('\n'.join(code_set))
