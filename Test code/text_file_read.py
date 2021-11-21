text_file = open(r"K:\SALES\Stock\Scripts\urlcheck.txt","r")
lines = text_file.readlines()
for line in lines :
 if line != "\n" :
  print(line.strip())

text_file.close()
