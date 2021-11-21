# gr_cy_mobiles.py
### Ψάχνει για όλα τα κινητά στο ελληνικό site
### και αν υπάρχει στο κυπριακό ελέγχει αν υπάρχουν specs
# Current Version 1 beta
#########
### ToDo
#########
""" κολλάει σε ένα συγκεκριμένο προϊόν: TEL.092759 """
""" φτιάχτηκε αλλά κολλάει σε ένα exception """
### Να βρίσκει μόνο τις διαφορές από το GR  σε σχέση με το CY
### Να κρατάει το HTML format στα extra
### Ανάλυση camera και αφαίρεση ότι δεν χρειάζεται
""" έγινε προσπάθεια """
""" μεγαλύτερο από 50 στο Οπίσθια: 12MP (f1.5-2.4/Dual Pixel PDAF, OIS) + 12MP (f2.4) + 16MP (f2.2). Εμπρόσθια: 10MP (f1.9/D PDAF) """
""" δεν λειτουργεί στο Οπίσθια: 13MP /1.4''/autofocus/LED flash/panorama/HDR. Εμπρόσθια: 8MP /1.4'' """
""" δεν λειτουργεί στο Οπίσθια: 16MP /f1.7/PDAF/LED flash/panorama/HDR. """
""" δεν λειτουργεί στο Οπίσθια: 16MP (f1.7) + 5MP (f1.9), phase detect autofocus/LED flash. Εμπρόσθια: 24MP /f1.9 """
""" δεν λειτουργεί στο Οπίσθια: Dual: 12MP (f1.8, OIS) + 20MP (f1.6) phase & laser autofocus/dual-LED. Εμπρόσθια: 24MP """
""" δεν λειτουργεί στο Οπίσθια: 12.2MP(f1.7/PDAF/OIS/LED flash/Auto-HDR. Εμπρόσθια: 8MP(f2.0) """
""" δεν λειτουργεί στο Οπίσθια: 40MP(f1.6) + 20MP(f2.2/16mm) + 8MP (f3.4/80mm) + TOF camera. Εμπρόσθια: 32MP (f2.0) """
""" δεν λειτουργεί στο Οπίσθια: 40MP(f1.6) + 8MP(f2.4) + 40MP(f1.8) + TOF 3D, Leica optics, dual-LED. Εμπρόσθια: 32MP(f2.0) """
""" δεν λειτουργεί Mpixels στο 12MP (f1.8/26mm/OIS/PDAF) + 12MP (f2.4/52mm/OIS/PDAF/2x opt zoom),Quad-LED. Εμπρόσθια: 7MP (f2.2/32mm) """
### Ανάλυση CPU και αφαίρεση ότι δεν χρειάζεται
""" έγινε προσπάθεια - μέγιστος αριθμός χαρακτήρων 50 ?"""
""" δεν λειτουργεί στο Octa-core (4x2.0 GHz Cortex-A55 & 4x2.0 GHz Cortex-A55), GPU:Mali-G52 """
""" δεν λειτουργεί στο Octa-core (2 x 2.7GHz & 2 x 2.3GHz & 4 x 1.9GHz), GPU:Mali-G76 MP12 """
""" δεν λειτουργεί στο Hexa-core 2x Vortex + 4x Tempest, GPU:Apple GPU 4-core graphics """
### Αφαίρεση εγγύησης από τα extra 
""" έγινε προσπάθεια - φαίνεται πως δουλεύει """
### Αφαίρεση περιττών κενών στα extra
""" έγινε προσπάθεια  - φαίνεται πως δουλεύει (replace("\n")) """
### Ξεχωριστά boolean ή ναι/όχι στη λίστα για τα check boxes
""" έγινε προσπάθεια - φαίνεται πως δουλεύει (ναι/όχι) """
### Να γράφει το πεδίο στη λίστα ακόμα και αν είναι κενά τα specs του
""" έγινε προσπάθεια """
### Λίστα προτεραιότητας specs:
""" έγινε προσπάθεια - φαίνεται πως δουλεύει 
# Διαστάσεις
# Βάρος
# Χρόνος Ομιλίας
# Xρόνος Αναμονής
# Οθόνη
# Κάρτα μνήμης
# Mobile Internet
# Ασύρματη επικοινωνία
# Camera
# Ειδοποιήσεις
# MPixels
# Εσωτερική μνήμη
# Video
# Μνήμη RAM
# Μπαταρία	Τύπος
# Ημερομηνία κυκλοφορίας	ΜΗΝΑΣ	ΧΡΟΝΙΑ
# Extra
# MMC
# JAVA
# NFC
# GPS
# Radio
# Fingerprint
# Αποσπώμενη μπαταρία
# CPU
# Ενσωματωμένοι Αισθητήρες
# Λειτουργικό Σύστημα
# ΠΕΡΙΓΡΑΦΗ
"""

try :
 from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
 from random import randint
 from time import sleep as nani
 import requests, os, sys, re, xlwt #, unicodedata
except Exception as exc :
 import sys
 print("Κάτι πάθαμε κατά το import.")
 print(str(exc))
 sys.exit(0)

def files_setup() :
 global read_file_exist, wb_write, ws_write, read_file, write_file, alt_write_file, write_path
 try :
  if os.path.exists(r'Z:\OneDrive\eShop Stuff\PRODUCT\Product') == True :
   write_path = (r'Z:\OneDrive\eShop Stuff\PRODUCT\Product')
  elif os.path.exists(r'Y:\OneDrive\eShop Stuff\PRODUCT\Product') == True :
   write_path = (r'Y:\OneDrive\eShop Stuff\PRODUCT\Product')
  os.chdir(write_path)
  if os.path.exists('GRvsCY_mobiles.ods') :
   read_file = ('GRvsCY_mobiles.ods')  # path to ods read file
  print("Προσπάθεια να ανοίξω το αρχείο: " + read_file + "...")
  ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
  spreadsheet = ezodf.opendoc(read_file)  # open file
  ezodf.config.reset_table_expand_strategy()  # reset ezodf config
  sheets = spreadsheet.sheets
  sheet = sheets[0]
  rowcount = sheet.nrows()
  colcount = sheet.ncols()
  ac_row = 1
  for i in range(1, rowcount):
   if str(sheet[i, 1].value) != "None" :
    ac_row += 1
   else :
    break
  print('Τα καταφέραμε.')
  print("")
  print('Φύλλο ' + str(i) + ': ' + sheets[i].name)
  print('Σύνολο γραμμών: ' + str(ac_row))
  read_file_exist = True
 except Exception as exc :
  print("Δεν βρίσκω το αρχείο GRvsCY_mobiles.ods")
  # print(str(exc))
 try :
  write_file = ("GRvsCY_mobiles_results.xls")  # name of xls write file
  alt_write_file = ("GRvsCY_mobiles_results_alt.xls")  # alternate name of xls write file
  print("Προσπάθεια για δημιουργία εικονικού αρχείου: " + write_file)
  wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
  ws_write = wb_write.add_sheet("GRMOBS", cell_overwrite_ok = True)  # add 1st sheet in virtual workbook
  print("Γιούπι, τα καταφέραμε.")
  print("")
  ws_write.write(0, 0, "ΚΩΔΙΚΟΣ")
  ws_write.write(0, 1, "ΤΙΤΛΟΣ")
 except Exception as exc :
  print("Δεν κατάφερα να γράψω το αρχείο. Έχουμε δικαιώματα;")
  print(str(exc))
  print("")

def load_soup(page) :
 # temp_product = page[page.rfind("=") + 1:]
 # print("Loading soup for " + temp_product)
 # print("")
 result = requests.get(page, headers = headers)
 webpage = result.content
 page_soup = soup(webpage, "html5lib")
 return(page_soup)

def get_all_products(page_url, page_soup) :
 while attempt < retries :
  try :
   offset = 0
   cat_pages = []
   trs = []
   prod_count = page_soup.find('div', {'class': 'web-product-num'}).text
   prod_count = int(prod_count[:prod_count.find(" ")].strip())
   total_next_pages = int(prod_count / 10) + 1
   print("Συνολο σελιδών: " + str(total_next_pages))
   cat_page, query_mark, categories = str(page_url).partition("?")
   while offset < prod_count :
   # while offset < 3 :
    # print("inside while loop")
    cat_pages.append(cat_page + query_mark + "offset=" + str(offset) + "&" + categories)
    offset += 10
    # print(str(offset))
   print("Σύνολο cat_pages: " + str(len(cat_pages)))
   p = 0
   for page in cat_pages :
   # for idx in range(2, 4) :
    # page = cat_pages[idx]
    p += 1
    print_text = "Μετρώντας τα προϊόντα της σελίδας: " + str(p)
    os.system("title " + "Getting page " + str(p) + "/" + str(len(cat_pages)) + " items")
    if p != len(cat_pages) :
     print(print_text, end='\r')
    else :
     print(print_text)
   # print(page)
    # sys.stdout.write('\x1b[1A')
    # # sys.stdout.write('\x1b[1A')
    # # sys.stdout.write('\x1b[2K')
    single_page_soup = load_soup(page)
    # print(single_page_soup.title)
    containers = single_page_soup.findAll('table', {'class': 'web-product-container'})
    for container in containers :
     gr_code = container.font.text.replace("(", "").replace(")", "")
     all_products.append(gr_code)
   break
  except Exception as exc :
   print("")
   print("Ώπα πέσαμε πάνω στο:")
   print(str(exc))
   print("Ξαναπροσπαθώ σε 3.")
   nani(3)
 if attempt == retries :
  print("Προσπάθησα " + str(retries) + " φορές και δεν τα κατάφερα.")
  input()
  sys.exit(0)

def write_it_down(e, null) :
 # print("Γράφω: " + str(e))
 if null == 0 :
  try :
   wb_write.save(write_file)
  except :
   wb_write.save(alt_write_file)
 elif e > 1 or null != 0 :
  try :
   wb_write.save(write_file)
   print(write_file + ", το έχω γραμμένο στο " + write_path)
  except :
   print("Πιθανώς κάποιος παίζει με το αρχείο. Προχωράω στο παρασύνθημα.")
   wb_write.save(alt_write_file)
   print(alt_write_file + ", το έχω γραμμένο στο " + write_path)
 else :
  print("Δεν έχει γίνει καμία αλλαγή στο αρχείο.")

try :
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
 os.system("title " + "Loading soup")
 page_soup = load_soup(page_url)
 os.system("title " + "Getting all items")
 try :
  get_all_products(page_url, page_soup)
 except Exception as exc :
  print("Exception: " + str(exc))
 p_id = 0
 for product in all_products :
  p_id += 1
  title_text = "Item: " + str(p_id) + "/"+ str(len(all_products))
  os.system("title " + title_text)
  e = 1
  page_url = 'https://www.e-shop.gr/product?id=' + product
  print(page_url)
  # print("Loading soup for " + product)
  gr_soup = load_soup(page_url)
  print("Getting description for " + product)
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
  print("Initializing variables")
  temp_title = prefix = battery_temp = battery_type = mpixels_text = mpixels_temp = mpixels = battery_cap = delim = rest = removable = month = year = ctext1 = ctext2 = camera_text = cptext1 = cptext2 = cpu_text = ctext1 = ctext2 = camera_text = talk_text = wait_text = storage_text = ram_text = ""
  spec_title = []
  spec_specs = []
  all_specs = {}
  specs1 = []
  specs2 = []
  specs2 = gr_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details2'})
  specs1 = gr_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details1'})
  # print("Specs 2 - Titles")
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
   # print("Added " + prefix + temp_title[:-1])
  # print("Specs 1 - Specs")
  for i in range(len(specs1)) :
   # print(specs1[i].text)
   if specs1[i].text.strip().find("2 χρόνια ") >= 0 :
    print("Warranty found")
    temp_spec = specs1[i].text.strip()
    extra, warranty, doa = temp_spec.rpartition("2 χρόνια ")
    spec_specs.append(extra.strip())
   else :
    spec_specs.append(specs1[i].text.strip().replace("\n", ""))
   # print(specs1[i].text.strip().replace("\n", ""))
  for i in range(len(spec_title)) :
   # print("i: " + str(i))
   # print(spec_title[i] + ": " + spec_specs[i])
   if spec_specs[i].find("mAh") >= 0 :
    battery_cap, delim, rest = spec_specs[i].partition("mAh")
    all_specs["15. Μπαταρία"] = battery_cap.strip()
    print("found mAh")
    if rest.strip().find("Μη αποσπώμενη") == 0 :
     all_specs["26. Removable"] = "Οχι"
    elif rest.strip().find("Αποσπώμενη") == 0 :
     all_specs["26. Removable"] = "Ναί"
    else :
     battery_type, delim, removable = rest.strip().partition(" ")
     all_specs["16. Τύπος"] = battery_type.strip()
     if removable.strip().find("Μη αποσπώμενη") == 0 :
      all_specs["26. Removable"] = "Οχι"
     elif removable.strip().find("Αποσπώμενη") == 0 :
      all_specs["26. Removable"] = "Ναί"
   elif spec_title[i].find("Ημερομηνία κυκλοφορίας") >= 0 :
    month, partition, year = spec_specs[i].partition("-")
    all_specs["17. Μήνας"] = month
    all_specs["18. Χρόνος"] = year
   else :
    all_specs[spec_title[i]] = spec_specs[i]

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
   print("found 09. Camera")
   mpixels_text = all_specs["09. Camera"]
   mpixels_temp = mpixels_text[:mpixels_text.find("MP")]
   if mpixels_temp.find(" ") >= 0 :
    mpixels = mpixels_temp[mpixels_temp.find(" ") + 1:]
   else :
    mpixels = mpixels_temp[:mpixels_temp.find("MP")]
   mpixels = mpixels.strip()
   prefix = "11. "
   all_specs[prefix + "MPixels"] = mpixels
   
   """camera fix procedure"""
   camera_text = all_specs.get("09. Camera")
   print("camera_text: " + camera_text)
   
   while camera_text.find("(") >= 0 :
    ctext1 = camera_text[:camera_text.find("(")].strip()
    ctext2 = camera_text[camera_text.find(")") + 1:].strip()
    print("ctext1: " + ctext1)
    print("ctext2: " + ctext2)
    if ctext2.find("(") >= 0 and ctext2.find(")") < 0 :  # υπάρχει το "(" αλλά δεν υπάρχει το ")"
     if ctext2.find(".") > 0 and ctext2.find("MP") > 15 :  # υπάρχει τελεία και τα MP είναι μακριά
      ctext2 = ctext2[ctext2.find("."):]
     else :
      ctext2 = ""
    print("ctext2: " + ctext2)
    camera_text = ctext1.strip() + ctext2.strip()
    print("camera_text: " + camera_text)
    # input()

   print("camera_text.find(",") >= 0 = " + str(camera_text.find(",") >= 0))
   
   while camera_text.find(",") >= 0 :
    ctext1 = camera_text[:camera_text.find(",")].strip()
    ctext2 = camera_text[camera_text.find(","):]
    if ctext2.find(".") >= 0 :
     ctext2 = ctext2[ctext2.find("."):].strip()
    else :
     ctext2 = ""
    print("ctext1: " + ctext1)
    print("ctext2: " + ctext2)
    camera_text = (ctext1 + ctext2).replace("+ ", " + ")
    # input()
    print("camera_text: " + camera_text)

   while camera_text.find("/") >= 0 :
    ctext1 = camera_text[:camera_text.find("/")].strip()
    ctext2 = camera_text[camera_text.find("/"):].strip()
    if ctext2.find(".") >= 0 :
     ctext2 = ctext2[ctext2.find("."):].strip()
    elif ctext2.find("/") >= 0 :
     ctext2 = ctext2[:ctext2.find("/")].strip()
    else :
     continue
    print("ctext1: " + ctext1)
    print("ctext2: " + ctext2)
    camera_text = (ctext1 + ctext2).replace("+ ", " + ")
    # input()
    print("camera_text: " + camera_text)
   
   all_specs["09. Camera"] = camera_text.replace("  ", " ").strip()

  """CPU fix procedure"""
  if "27. CPU" in all_specs :
   cpu_text = all_specs.get("27. CPU")
   print("cpu_text: " + cpu_text)
   cpu_text = cpu_text.replace("(", "")
   cpu_text = cpu_text.replace(")", "")
   if len(cpu_text) >= 50 :
    cpu_text = cpu_text.replace("GHz & ", "& ")
   all_specs["27. CPU"] = cpu_text
   print("cpu_text: " + cpu_text)

  """talk time fix procedure"""
  if "03. Χρόνος Ομιλίας" in all_specs : 
   talk_text = all_specs.get("03. Χρόνος Ομιλίας")
   print("talk_text: " + talk_text)
   talk_text = talk_text[:talk_text.find(" ")].strip()
   all_specs["03. Χρόνος Ομιλίας"] = talk_text
   print("talk_text: " + talk_text)

  if "04. Xρόνος Αναμονής" in all_specs : 
   wait_text = all_specs.get("04. Xρόνος Αναμονής")
   print("wait_text: " + wait_text)
   wait_text = wait_text[:wait_text.find(" ")].strip()
   all_specs["04. Xρόνος Αναμονής"] = wait_text
   print("wait_text: " + wait_text)

  """memory fix procedure"""
  if "12. Εσωτερική μνήμη" in all_specs : 
   storage_text = all_specs.get("12. Εσωτερική μνήμη")
   print("storage_text: " + storage_text)
   storage_text = storage_text[:storage_text.find(" ")].strip()
   all_specs["12. Εσωτερική μνήμη"] = storage_text
   print("storage_text: " + storage_text)

  if "14. Μνήμη RAM" in all_specs : 
   ram_text = all_specs.get("14. Μνήμη RAM")
   print("ram_text: " + ram_text)
   ram_text = ram_text[:ram_text.find(" ")].strip()
   all_specs["14. Μνήμη RAM"] = ram_text
   print("ram_text: " + ram_text)

  """ adding empty fields before sorting """
  if len(all_specs) < 29 :
   if all_specs.get("01. Διαστάσεις (mm)") == None :
    all_specs["01. Διαστάσεις (mm)"] = ""
   if all_specs.get("02. Βάρος (γραμ.)") == None :
    all_specs["02. Βάρος (γραμ.)"] = ""
   if all_specs.get("03. Χρόνος Ομιλίας") == None :
    all_specs["03. Χρόνος Ομιλίας"] = ""
   if all_specs.get("04. Xρόνος Αναμονής") == None :
    all_specs["04. Xρόνος Αναμονής"] = ""
   if all_specs.get("05. Οθόνη") == None :
    all_specs["05. Οθόνη"] = ""
   if all_specs.get("06. Κάρτα μνήμης") == None :
    all_specs["06. Κάρτα μνήμης"] = ""
   if all_specs.get("07. Mobile Internet") == None :
    all_specs["07. Mobile Internet"] = ""
   if all_specs.get("08. Ασύρματη επικοινωνία") == None :
    all_specs["08. Ασύρματη επικοινωνία"] = ""
   if all_specs.get("09. Camera") == None :
    all_specs["09. Camera"] = ""
   if all_specs.get("10. Ειδοποιήσεις") == None :
    all_specs["10. Ειδοποιήσεις"] = ""
   if all_specs.get("11. MPixels") == None :
    all_specs["11. MPixels"] = ""
   if all_specs.get("12. Εσωτερική μνήμη") == None :
    all_specs["12. Εσωτερική μνήμη"] = ""
   if all_specs.get("13. Video") == None :
    all_specs["13. Video"] = ""
   if all_specs.get("14. Μνήμη RAM") == None :
    all_specs["14. Μνήμη RAM"] = ""
   if all_specs.get("15. Μπαταρία") == None :
    all_specs["15. Μπαταρία"] = ""
   if all_specs.get("16. Τύπος") == None :
    all_specs["16. Τύπος"] = ""
   if all_specs.get("17. Μήνας") == None :
    all_specs["17. Μήνας"] = ""
   if all_specs.get("18. Χρόνος") == None :
    all_specs["18. Χρόνος"] = ""
   if all_specs.get("19. Extra") == None :
    all_specs["19. Extra"] = ""
   if all_specs.get("20. MMC") == None :
    all_specs["20. MMC"] = ""
   if all_specs.get("21. JAVA") == None :
    all_specs["21. JAVA"] = ""
   if all_specs.get("22. NFC") == None :
    all_specs["22. NFC"] = ""
   if all_specs.get("23. GPS") == None :
    all_specs["23. GPS"] = ""
   if all_specs.get("24. Radio") == None :
    all_specs["24. Radio"] = ""
   if all_specs.get("25. Fingerprint") == None :
    all_specs["25. Fingerprint"] = ""
   if all_specs.get("26. Removable") == None :
    all_specs["26. Removable"] = ""
   if all_specs.get("27. CPU") == None :
    all_specs["27. CPU"] = ""
   if all_specs.get("28. Ενσωματωμένοι Αισθητήρες") == None :
    all_specs["28. Ενσωματωμένοι Αισθητήρες"] = ""
   if all_specs.get("29. Λειτουργικό Σύστημα") == None :
    all_specs["29. Λειτουργικό Σύστημα"] = ""

  sorted_specs = {}
  # print("")
  for x, y in sorted(all_specs.items()) :
   # print("Sorting " + x.strip() + ": " + y.strip().replace("\n", ""))
   if x.find(":") >= 0 :
    sorted_specs[x[:-1]] = y.strip().replace("\n", "")
   else :
    sorted_specs[x] = y.strip().replace("\n", "")
  page_url = 'https://www.e-shop.cy/product?id=' + product
  cy_soup = load_soup(page_url)
  cy_specs2 = cy_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details2'})
  print("")
  print("len(cy_specs2): " + str(len(cy_specs2)))
  print("len(gr_specs2): " + str(len(specs2)))
  if len(cy_specs2) != len(specs2) :
   """write it on the excel file with a new sheet name"""
   print("difference found between sites")
   # print("")
   found += 1
   title = gr_soup.h1.text.strip()
   ws_write.write(found, 0, product)
   ws_write.write(found, 1, title)
   new_sheet = True
   ws_write_product = wb_write.add_sheet(product, cell_overwrite_ok = True)
   ws_write_product.write(0, 0, "ΤΙΤΛΟΣ")
   ws_write_product.write(0, 1, "ΠΕΡΙΓΡΑΦΗ")
   for x, y in sorted_specs.items() :
    # print(x + ": " + y)
    # print("writing title")
    ws_write_product.write(e, 0, x)
    # print("writing specs")
    ws_write_product.write(e, 1, y)
    write_it_down(e, 0)
    e += 1
   # print("writing description")
   ws_write_product.write(e, 0, "ΠΕΡΙΓΡΑΦΗ")
   ws_write_product.write(e, 1, desc_text)
   print("")
 
except KeyboardInterrupt :
 try :
  # print("")
  input("Διαλλειματάκι;")
  print("")
 except :
  sys.exit(0)
except Exception as exc:
 print("Εξαίρεση: " + str(exc))
finally :
 # print("")
 try :
  print("Save? ")
  answer = input()
  if answer == "y" or answer == "Y" :
   write_it_down(new_sheet, 1)
  else :
   print("Δεν αποθηκεύτηκε το αρχείο.")
   sys.exit(0)
 except KeyboardInterrupt :
  sys.exit(0)
 except Exception as exc :
  print("Finally exception: " + str(exc))
  sys.exit(0)