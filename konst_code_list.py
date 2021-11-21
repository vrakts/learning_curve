import os

l = []
while True:
    try:
        code = input("Code: ")
        l.append(code.strip())
    except KeyboardInterrupt:
        break

s = set(l)
if len(s) != len(l):
    print("Found dups.")

path = "Z:\\OneDrive\\eShop Stuff\\Synced\\Κουτσοδούλια\\KonstaStock\\11-2021"
os.chdir(path)

with open("codes.txt", "w") as f:
    f.write('\n'.join(s))
