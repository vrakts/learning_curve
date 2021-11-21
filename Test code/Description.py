gr_oem = ""
# if page_soup.find('td', {'class': 'product_table_body'}) == None or page_soup.find('td', {'class': 'product_table_body'}) != "Περιγραφή " :
 # gr_desc_text = ""
# else :
 # gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})
 # if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
  # gr_desc_text = ""
 # else :
  # gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
gr_d_soup = page_soup.find('td', {'class': 'product_table_body'})  # assign the product_table_body soup
gr_product_table_title = page_soup.find('td', {'class': 'product_table_title'})  # assign the product_table_title soup 
if gr_d_soup == None or gr_d_soup.text.find('Σύνολο ψήφων') > 0 or gr_product_table_title.text != "Περιγραφή " :  # if product_table_body is empty or contains votes or product_table_title doesn't contain Περιγραφή then there is no description
 gr_desc_text = ""
else :
 gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")  # decode description content replace wrong html calues and any .gr mentions
 if gr_desc_text.find('Vendor OEM:') > 0 :
  if gr_desc_text.find('<br><br>Vendor OEM:') > 0 :
   string, oem, rest = gr_desc_text.rpartition('<br><br>Vendor OEM:')  # seperate the text
  else :
   string, oem, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
  gr_desc_text = string.strip()  # keep only what is before the OEM
  oem = rest.strip()  # keep only what is after the OEM
  gr_oem, delim, oem_rest = oem.partition('<')  # seperate the OEM text from any < signs
  gr_oem = gr_oem.strip()
 # if gr_desc_text.find('<br><br>Barcode') > 0 :  # if barcode exists in GR
 if gr_desc_text.find('Barcode:') > 0 :  # if both barcode and OEM exists
  if gr_desc_text.find('<br><br>Barcode:') > 0 :
   string, barcode, rest = gr_desc_text.rpartition('<br><br>Barcode')  # seperate the text
  else :
   string, barcode, rest = gr_desc_text.rpartition('Vendor OEM:')  # seperate the text
  # gr_desc_text = string.strip() + rest.strip() # keep only what is before the barcode
  gr_desc_text = string.strip() # keep only what is before the barcode
  # while gr_desc_text.strip()[-4:] == "<br>" :  # if the 4 ending text characters are <br>
   # string, br, rest = gr_desc_text.rpartition('<br>')  # seperate the text
   # gr_desc_text = string.strip()  # keep ony what is before <br>
  # gr_oem = rest.replace("</li>", "").strip()
 if gr_desc_text.find('<!--CRAZY') == 0 :  # if description text has a Crazy tag
  crazy, align, rest = gr_desc_text.partition('-->')  # seperate the ending tag from the rest of the text
  gr_desc_text = rest.strip()  # keep only the rest of the text
 # if gr_desc_text.find('<p ') >= 0 :
  # p, align, rest = gr_desc_text.partition('>')
  # gr_desc_text = '<p align="justify">' + rest.strip()pyth
 if gr_desc_text.find('<palign') >= 0 or gr_desc_text.find('<p ') >= 0 or gr_desc_text.find('<p justify') >= 0 or gr_desc_text.find('<pjustify') >= 0 :  # if the wrong p align tag is found
  p, align, rest = gr_desc_text.partition('>')  # seperate the ending p tag from the rest of the text
  gr_desc_text = '<p align="justify">' + rest.strip()  # add the correct tag on the rest of the text
 else :
  gr_desc_text = '<p align="justify">' + gr_desc_text.strip()  # if no p tag found the add it to the text
 if gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find('2 χρόνια!') > 0 :  # if warranty found for laptops
  if gr_desc_text.find('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
   string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
  elif gr_desc_text.find('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>') > 0 :
   string, warranty, rest = gr_desc_text.rpartition('<a href="page-11-warranty-2-years" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')  # remove the doa a tag
  if gr_prod_title.find('ASUS') > 0 :
   warranty_text = ' <a href="page.phtml?id=3" class="navy_link">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a></b> </li>'
  else :
   warranty_text = ' .</b> </li>'
  gr_desc_text = string.strip() + warranty_text + rest.strip()  # keep only the text before and after and add a dot in between
 elif gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ' όρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Lifetime") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφόρου ζωής") > 0 or gr_desc_text[gr_desc_text.find("Εγγύηση:"):].find("Εφ\x92 όρου ζωής") > 0 :  # if after εγγυηση there is a lifetime quote written in different ways
  if gr_desc_text.find("Εγγύηση:") > 0 :  # and if written in GR
   string, warranty, rest = gr_desc_text.rpartition('Εγγύηση:')  # seperate the text with <b>Εγγύηση
  elif gr_desc_text.find("Warranty:") > 0 :  # or written in EN
   string, warranty, rest = gr_desc_text.rpartition('Warranty:')  # seperate the text with <b>Warranty
  gr_desc_text = string + "<b>Εγγύηση:</b> Εφ' όρου ζωής.</li>"  # keep the before text with correct terms added
 elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') > 0 :  # if DOA terms found 
  string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')  # seperate the DOA link
 elif gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') > 0 :
  string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')  # seperate the DOA link
  gr_desc_text = string + rest.strip()  # and keep the before and after text
 else :
  print("No Warranty found. Will keep text as is.")
