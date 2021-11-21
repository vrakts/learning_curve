headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
offset = 0
attempt = 0
retries = 10
found = 0
all_products = []
all_specs = {}
prod_count = 0
new_sheet = False
os.system("title " + "Creating files")
files_setup()
page_url = "https://www.e-shop.gr/tilepikoinonies-kinita-smartphones-list?table=TEL&category=%CA%C9%CD%C7%D4%CF+%D4%C7%CB%C5%D6%D9%CD%CF"
page_soup = load_soup(page_url)
os.system("title " + "Loading soup")
get_all_products(page_url, page_soup)
os.system("title " + "Getting all items")
p_id = 0

###
product = all_products[1]
p_id += 1
os.system("title " + "Item: " + str(p_id) + "/"+ str(len(all_products)))
e = 1
page_url = 'https://www.e-shop.gr/product?id=' + product
print(page_url)
gr_soup = load_soup(page_url)
desc_text = ""
desc_soup = gr_soup.find('td', {'class': 'product_table_body'})
product_table_title = gr_soup.find('td', {'class': 'product_table_title'})
if desc_soup == None or desc_soup.text.find('Σύνολο ψήφων') > 0 or product_table_title.text.strip() != "Περιγραφή" :
 gr_desc_text = ""
else :
 desc_text = desc_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
 temp_text, partition, rest = desc_text.partition('<table border="0" cellpadding="0" cellspacing="0"')
 if temp_text == "<br>" :
  desc_text = ""
 else :
  desc_text = temp_text
temp_title = ""
prefix = ""
battery_temp = ""
battery_type = ""
mpixels_text = ""
mpixels = ""
battery_cap = ""
delim = ""
rest = ""
removable = ""
month = ""
year = ""
spec_title = []
spec_specs = []
all_specs = {}
specs1 = []
specs2 = []
specs2 = gr_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details2'})
specs1 = gr_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details1'})

###
for i in range(len(specs2)) :
 # print(specs2[i].text)
 temp_title = specs2[i].text.strip()
 if temp_title.find("Διαστάσεις") >= 0 :
  prefix = "01. "
 elif temp_title.find("Βάρος") >= 0 :
  prefix = "02. "
 elif temp_title.find("Χρόνος Ομιλίας") >= 0 :
  prefix = "03. "
 elif temp_title.find("Xρόνος Αναμονής") >= 0 :
  prefix = "04. "
 elif temp_title.find("Οθόνη") >= 0 :
  prefix = "05. "
 elif temp_title.find("Κάρτα μνήμης") >= 0 :
  prefix = "06. "
 elif temp_title.find("Mobile Internet") >= 0 :
  prefix = "07. "
 elif temp_title.find("Ασύρματη επικοινωνία") >= 0 :
  prefix = "08. "
 elif temp_title.find("Camera") >= 0 :
  prefix = "09. "
 elif temp_title.find("Ειδοποιήσεις") >= 0 :
  prefix = "10. "
 # elif temp_title.find("MPixels") >= 0 :
  # prefix = "11. "
 elif temp_title.find("Εσωτερική μνήμη") >= 0 :
  prefix = "12. "
 elif temp_title.find("Video") >= 0 :
  prefix = "13. "
 elif temp_title.find("Μνήμη RAM") >= 0 :
  prefix = "14. "
 elif temp_title.find("Μπαταρία") >= 0 :
  prefix = "15. "
  # battery_temp = specs1[i].text.strip()
  # battery_type = battery_temp[:battery_temp.find(" ") - 1]
 # elif temp_title.find("Τύπος") >= 0 :
  # prefix = "16. "
 elif temp_title.find("Ημερομηνία κυκλοφορίας") >= 0 :
  prefix = "17. "
 # elif temp_title.find("Έτος κυκλοφορίας") >= 0 :
  # prefix = "18. "
 elif temp_title.find("Extra") >= 0 :
  prefix = "19. "
 elif temp_title.find("MMC") >= 0 :
  prefix = "20. "
 elif temp_title.find("JAVA") >= 0 :
  prefix = "21. "
 elif temp_title.find("NFC") >= 0 :
  prefix = "22. "
 elif temp_title.find("GPS") >= 0 :
  prefix = "23. "
 elif temp_title.find("Radio") >= 0 :
  prefix = "24. "
 elif temp_title.find("Fingerprint") >= 0 :
  prefix = "25. "
 # elif temp_title.find("Αποσπώμενη μπαταρία") >= 0 :
  # prefix = "26. "
 elif temp_title.find("CPU") >= 0 :
  prefix = "27. "
 elif temp_title.find("Ενσωματωμένοι Αισθητήρες") >= 0 :
  prefix = "28. "
 elif temp_title.find("Λειτουργικό Σύστημα") >= 0 :
  prefix = "29. "
 spec_title.append(prefix + temp_title[:-1])

###
for i in range(len(specs1)) :
 # print(specs1[i].text)
 if specs1[i].text.strip().find("2 χρόνια ") >= 0 :
  temp_spec = specs1[i].text.strip()
  extra, warranty, doa = temp_spec.rpartition("2 χρόνια ")
  spec_specs.append(extra.strip())
 else :
  spec_specs.append(specs1[i].text.strip())

###
for i in range(len(spec_title)) :
 # print("i: " + str(i))
 # print(spec_title[i] + ": " + spec_specs[i])
 if spec_specs[i].find("mAh") >= 0 :
  battery_cap, delim, rest = spec_specs[i].partition("mAh")
  all_specs["15. Μπαταρία:"] = battery_cap.strip()
  if rest.strip().find("Μη αποσπώμενη") == 0 :
   all_specs["26. Removable:"] = "Οχι"
  elif rest.strip().find("Αποσπώμενη") == 0 :
   all_specs["26. Removable:"] = "Ναί"
  else :
   battery_type, delim, removable = rest.strip().partition(" ")
   all_specs["16. Τύπος:"] = battery_type.strip()
   if removable.strip().find("Μη αποσπώμενη") == 0 :
    all_specs["26. Removable:"] = "Οχι"
   elif removable.strip().find("Αποσπώμενη") == 0 :
    all_specs["26. Removable:"] = "Ναί"
 elif spec_title[i].find("Ημερομηνία κυκλοφορίας") >= 0 :
  month, partition, year = spec_specs[i].partition("-")
  all_specs["17. Μήνας:"] = month
  all_specs["18. Χρόνος:"] = year
 else :
  all_specs[spec_title[i]] = spec_specs[i]
 # if "MMC" in thisdict :

###
if all_specs.get("20. MMC") is None :
 all_specs["20. MMC"] = "Οχι"

if all_specs.get("21. JAVA") is None :
 all_specs["21. JAVA"] = "Οχι"

if all_specs.get("22. NFC") is None :
 all_specs["22. NFC"] = "Οχι"

if all_specs.get("23. GPS") is None :
 all_specs["23. GPS"] = "Οχι"

if all_specs.get("24. Radio") is None :
 all_specs["24. Radio"] = "Οχι"

if all_specs.get("25. Fingerprint") is None :
 all_specs["25. Fingerprint"] = "Οχι"

if "09. Camera" in all_specs and all_specs["09. Camera"] != "Ναι" :
 mpixels_text = all_specs["09. Camera"]
 mpixels = mpixels_text[mpixels_text.find(" ") + 1:mpixels_text.find("MP")]
 prefix = "11. "
 all_specs[prefix + "MPixels:"] = mpixels

###
sorted_specs = {}
# sorted_specs = sorted(all_specs)
# for x, y in sorted_specs.items() :
for x, y in sorted(all_specs.items()) :
 print(x + " " + y)
 if x.find(":") >= 0 :
  sorted_specs[x[:-1]] = y.strip().replace("\n", "")
 else :
  sorted_specs[x] = y.strip().replace("\n", "")

for x, y in sorted_specs.items() :
 print(x + " " + y)

###
page_url = 'https://www.e-shop.cy/product?id=' + product
cy_soup = load_soup(page_url)
# spec_title = []
# spec_specs = []
cy_specs2 = cy_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details2'})

###
if len(cy_specs2) != len(specs2) :
 """write it on the excel file with a new sheet name"""
 found += 1
 title = gr_soup.h1.text.strip()
 ws_write.write(found, 0, product)
 ws_write.write(found, 1, title)
 new_sheet = True
 ws_write_product = wb_write.add_sheet(product, cell_overwrite_ok = True)
 ws_write_product.write(0, 0, "ΤΙΤΛΟΣ")
 ws_write_product.write(0, 1, "ΠΕΡΙΓΡΑΦΗ")
 # ws_write_product.write(0, 2, "ΕΙΔΟΣ")
 # ws_write_product.write(0, 3, "ΠΡΟΔΙΑΓΡΑΦΗ")
 for x, y in sorted_specs.items() :
  # print(x)
  # print(y)
  ws_write_product.write(e, 0, x)
  ws_write_product.write(e, 1, y)
  write_it_down(e, 0)
  e += 1
 ws_write_product.write(e, 0, "ΠΕΡΙΓΡΑΦΗ")
 ws_write_product.write(e, 1, desc_text)

