def get_start_time() :
 global start_time, start_date
 start_time = time()  # set starting time
 today = date.today()  # set starting date
 start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
 print("")
 print("Script started at " + start_date)

def get_elapsed_time() :
 elapsed_time = time() - start_time
 minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
 mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
 seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
 seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
 formatted_time = str(mins) + "." + str(seconds)
 print("")
 # print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
 sys.exit("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")

def get_gr_details(page_soup) :
 global gr_prod_per, gr_prod_title, gr_price_dif, gr_price_text, gr_a_text, gr_cat, gr_subcat, gr_brand, sxetika_list
 gr_price_dif = '0'
 # pd = 0
 gr_prod_per = page_soup.find('td', {'style' : 'text-align:left;color:#4f4f4f;font-family:Tahoma;font-size:14px;padding:0 10px 0 0;'}).text.strip()
 gr_prod_title = page_soup.h1.text
 gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(gr_price) == 0 :
  gr_price_text = "Εξαντλημένο"
  gr_price_dif = "-"
 else : 
  gr_price_dif = gr_price[0].text.replace("\xa0€", "")
  # print(gr_price_dif)
  gr_price_text = gr_price_dif.replace(".", ",")
 if page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"}) == None :
  gr_a_text = "Εξαντλημένο"
 else :
  gr_a = page_soup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
  if gr_a.text.find('Κατόπιν') <= 16 :
   gr_a_text = gr_a.text[gr_a.text.find(":") + 2:]
  else :
   gr_a_text = gr_a.text[gr_a.text.find(":") + 2:gr_a.text.find("\n")].strip()
 gr_categories = page_soup.findAll('td', {'class': 'faint1'})
 if gr_categories[1].text.find(' •') > 0 :
  gr_cat = gr_categories[1].text[:gr_categories[1].text.find(' •')]
  gr_brand = gr_categories[1].text[gr_categories[1].text.find(' •')+2:gr_categories[1].text.find('στην')].strip()
  if len(gr_categories) > 2 :
   gr_subcat = gr_categories[3].text.strip()
  else :
   gr_subcat = ""
 else :
  gr_cat = gr_categories[1].text.strip()
  if len(gr_categories) > 2 :
   gr_subcat = gr_categories[3].text.strip()
  else :
   gr_subcat = ""
  gr_brand = "-"
 if len(page_soup.findAll('div', {'class': 'also_box'})) > 0 :
  gr_sxetika = page_soup.findAll('div', {'class': 'also_box'})
  sxetika_list = ""
  for sxetika in gr_sxetika :
   sxetika_per_link = sxetika.a['href']
   sxetika_per = sxetika_per_link[sxetika_per_link.rfind('-')+1:]
   if len(sxetika_list) == 0 :
    sxetika_list = sxetika_per
   else :
    sxetika_list = sxetika_list + "," + sxetika_per
 else :
  sxetika_list = ""

def get_cy_details(cy_page_soup) :
 global cy_prod_title, cy_price_dif, cy_price_text, cy_cat, cy_subcat, cy_brand, price_dif, pd
 gr_price_dif = '0'
 # pd = 0
 # print("Just initialized pd.")
 cy_prod_title = cy_page_soup.h1.text
 cy_price = cy_page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(cy_price) == 0 :
  cy_price_text = "Εξαντλημένο"
  cy_price_dif = "-"
 else :
  cy_price_dif = cy_price[0].text.replace("\xa0€", "")
  # print(cy_price_dif)
  cy_price_text = cy_price_dif.replace(".", ",")
 if len(cy_prod_title) == 0 :
  cy_price_text = "Θέλει άνοιγμα"
  cy_cat = ""
  cy_subcat = ""
  cy_brand = ""
 else :
  cy_categories = cy_page_soup.findAll('td', {'class': 'faint1'})
  if cy_categories[1].text.find(' •') > 0 :
   cy_cat = cy_categories[1].text[:cy_categories[1].text.find(' •')]
   cy_brand = cy_categories[1].text[cy_categories[1].text.find(' •')+2:cy_categories[1].text.find('στην')].strip()
   if len(cy_categories) > 2 :
    cy_subcat = cy_categories[3].text.strip()
   else :
    cy_subcat = ""
  else :
   cy_cat = cy_categories[1].text.strip() 
   if len(cy_categories) > 2 :
    cy_subcat = cy_categories[3].text.strip()
   else :
    cy_subcat = ""
   cy_brand = "-"
 try :
  price_dif = round(float(cy_price_text.replace(',', '.')) - float(gr_price_text.replace(',', '.')),2)
  # print("Price Difference: " + str(price_dif) + ".")
  # print("Changing pd to 1.")
  # pd = 1
 except :
  print("No price detected on either GR or CY")
  price_dif = "-"
  # print("pd is 0")
  # pd = 0

def get_gr_description(page_soup) :
 # global string, warranty, rest, gr_oem, barcode, gr_desc_result
 global gr_oem, barcode, gr_desc_result
 gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
 gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
 if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text.strip() != "Περιγραφή" :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
  gr_desc_text = ""
 else :
  gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html values and any .gr mentions
  # print(gr_desc_text)
  gr_oem = ""
  if gr_desc_text.find('Eγγύηση') > 0 :
   gr_desc_text.replace('Εγγύηση', '')
  if gr_desc_text.find('Vendor OEM:') > 0 :
   print("Contacting Vendors...")
   if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
    string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
   else :
    string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
   gr_desc_text = string.strip()  # keep only what is before the OEM
   oem = rest.strip()  # keep only what is after the OEM
   gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
   gr_oem = gr_oem.strip()
  if gr_desc_text.find('Barcode:') > 0 or gr_desc_text.find('EAN-13:') > 0 :  # if both barcode and OEM exists
   print("Calculating barcodes...")
   if gr_desc_text.find('<br><br>Barcode:') > 0 :
    string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode:')  # seperate the text
   elif gr_desc_text.find('<br><br>EAN-13:') > 0 :
    string, barcode, rest = gr_desc_text.rpartition('<br><br>EAN-13:')  # seperate the text
   elif gr_desc_text.find('EAN-13:') > 0 :
    string, barcode, rest = gr_desc_text.rpartition('EAN-13:')  # seperate the text
   else :
    string, barcode, rest = gr_desc_text.rpartition('Barcode:')  # seperate the text
   gr_desc_text = string.strip() # keep only what is before the barcode
  if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
   print("Doing some crazy stuff...")
   crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
   gr_desc_text = rest.strip()  # keep only the rest of the text
  if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
   print("Aligning edges...")
   p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
   gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
  else :
   gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
  if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
   print("Writing warranties...")
   if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
    string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
   elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
    string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
   if gr_prod_title.find('ASUS') > 0 or gr_prod_title.find('DELL') > 0 :
    # warranty_text = ' <a href="http://www.eshopcy.com.cy/page?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b></li>'
    warranty_text = ' '
   else :
    warranty_text = ' .</b> </li>'
   gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
  elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
   if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
    string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
   elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
    string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
   gr_desc_text = string + "Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
  elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
   print("Arrival defects...")
   string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
   gr_desc_text = string + rest.strip()  # and keep the before and after text
  elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
   print("Arrival defects...")
   string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
   gr_desc_text = string + rest.strip()  # and keep the before and after text
  else :
   print("No special Warranty found.")
  if gr_desc_text.find('<p></p>') > 0 :
   gr_desc_text.replace('<p></p>', '') 
  if gr_desc_text.find('<b>Εγγύηση') >= 0 :
   war_start = gr_desc_text.find('<b>Έγγύηση')
   if gr_desc_text[war_start:].find('1 χρόνο') > 0 or gr_desc_text[war_start:].find('1 Χρόνο') > 0 or gr_desc_text[war_start:].find('1 χρονο') > 0 or gr_desc_text[war_start:].find('1 Χρονο') > 0 or gr_desc_text[war_start:].find('1 Χρόνος') > 0 or gr_desc_text[war_start:].find('1 χρόνος') > 0 or gr_desc_text[war_start:].find('1 Έτος') > 0 or gr_desc_text[war_start:].find('1 έτος') > 0 or gr_desc_text[war_start:].find('1 Ετος') > 0 or gr_desc_text[war_start:].find('1 ετος') > 0 or gr_desc_text[war_start:].find('2 Χρόνος') > 0 or gr_desc_text[war_start:].find('2 χρόνος') > 0 or gr_desc_text[war_start:].find('2 Έτη') > 0 or gr_desc_text[war_start:].find('2 έτη') > 0 or gr_desc_text[war_start:].find('24 μήνες. ') > 0 or gr_desc_text[war_start:].find('24 Μήνες.') > 0 :   # if the years are misspelled it is not autocorrected in the CY site. Not looking for "." at the end.
    print("Year adjustment...")
    gr_desc_text = gr_desc_text.replace('1 Χρόνος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 χρόνος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 Χρόνο', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 χρόνο', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 Έτος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('1 έτος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('2 Χρόνος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('2 χρόνος', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('2 Έτη', '2 χρόνια')
    gr_desc_text = gr_desc_text.replace('2 έτη', '2 χρόνια')
  if gr_desc_text.find("Ά") > 0 or gr_desc_text.find("’") > 0 or gr_desc_text.find('face="Constantia" size="3"') > 0 or gr_desc_text.find('size="3" face="Constantia"') > 0 :
   print("Taking out the trash...")
   gr_desc_text = gr_desc_text.replace("Ά", "&#902;")
   gr_desc_text = gr_desc_text.replace("’", "&#902;")
   gr_desc_text = gr_desc_text.replace('face="Constantia" size="3"', '')
   gr_desc_text = gr_desc_text.replace('size="3" face="Constantia"', '')
  if gr_desc_text == '<p align="justify">' or gr_desc_text == '<p align="justify"><br><br>' :
   print("Throwing away left overs...")
   gr_desc_text = ""
 gr_desc_result = gr_desc_text

def write_results(e) :
 # print("e in: " + str(e))
 ws_write.write(e, 0, gr_prod_per) 		# OK
 ws_write.write(e, 1, gr_prod_title)	# OK
 ws_write.write(e, 2, gr_oem.strip())	# OK
 ws_write.write(e, 3, gr_price_text)	# OK
 ws_write.write(e, 4, gr_cat)			# OK
 ws_write.write(e, 5, gr_subcat)		# OK
 ws_write.write(e, 6, gr_brand)			# OK
 ws_write.write(e, 7, sxetika_list)		# OK
 ws_write.write(e, 8, gr_desc_result)	# OK
 ws_write.write(e, 9, gr_a_text)		# OK
 ws_write.write(e, 10, cy_prod_title)	# OK
 ws_write.write(e, 11, cy_price_text)	# OK
 ws_write.write(e, 12, cy_cat)			# OK
 ws_write.write(e, 13, cy_subcat)		# OK
 ws_write.write(e, 14, cy_brand)		# OK
 try :
  ws_write.write(e, 15, price_dif)		# OK
 except :
  ws_write.write(e, 15, "-")	 		# OK
 # if pd == 1 :
  # ws_write.write(e, 15, price_dif)		# OK
 # else :
  # ws_write.write(e, 15, "-")

def write_it_down() :
 try :
  wb_write.save(write_file)
  print("")
  print(write_file + " created on " + write_path)
 except :
  print("")
  wb_write.save(alt_write_file)
  print(alt_write_file + " created on " + write_path)

