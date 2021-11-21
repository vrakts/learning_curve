from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import quote  # enables encoding greek characters in url
from urllib.parse import unquote  # enables decoding of greek characters
import urllib.request
import xlwt  # for the ability to write to excel files
from datetime import date  # for the ability to easily measure date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

# gr_a_page = 'https://www.e-shop.gr/laptop-lenovo-ideapad-s145-15iwl-81mv00rdrm-156-hd-intel-dual-core-4205u-4gb-128gb-ssd-freedos-p-PER.917037'  # άμεσα διαθέσιμο
# gr_a_page = 'https://www.e-shop.gr/laptop-asus-vivobook-x540ma-go550-156-hd-intel-dual-core-n4000-4gb-ssd-256gb-free-dos-p-PER.913946'  # Κατόπιν παραγγελίας σε 4-7 εργάσιμες ημέρες
# gr_a_page = 'https://www.e-shop.gr/laptop-dell-inspiron-3582-156-hd-intel-quad-core-n5000-4gb-1tb-linux-p-PER.903610'  # Αναμένεται νέα παραλαβή στις 30 Δεκεμβρίου
# gr_a_page = 'https://www.e-shop.gr/laptop-lenovo-ideapad-s145-15ast-81n300cdpb-156-fhd-amd-a6-9225-4gb-256gb-free-dos-p-PER.917038'  # Κατόπιν παραγγελίας
gr_a_page = 'https://www.e-shop.gr/tablet-samsung-galaxy-tab-s5e-t720-105-wifi-64gb-4gb-android-9-silver-p-PER.909843'  # description test

req = urllib.request.Request(gr_a_page, headers = headers)
gr_a_uClient = uReq(req)
gr_a_pagesoup = soup(gr_a_uClient.read(), "html5lib")
gr_a_uClient.close()

gr_a = gr_a_pagesoup.find("td", {"style" : "text-align:left;padding:5px 0 5px 0;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})
# gr_a_text = gr_a.text[gr_a.text.find(":")+2:]
if gr_a.text.find('Κατόπιν') <= 16 :
 gr_a_text = gr_a.text
else :
 # gr_a_text = gr_a.text[gr_a.text.find(":")+2:gr_a.text.find("\r")].strip()
 gr_a_text = gr_a.text[gr_a.text.find(":")+2:gr_a.text.find("\n")].strip()

print(gr_a_text)

gr_d_soup = gr_a_pagesoup.find('td', {'class': 'product_table_body'})
if gr_d_soup.text.find('Σύνολο ψήφων') > 0 :
 gr_desc_text = ""
else :
 gr_desc_text = gr_d_soup.decode_contents().strip().replace('\n', '').replace('\t', '').replace("<br/>", "<br>").replace(".gr", "")
 if gr_desc_text.find('2 χρόνια!') > 0 :
  string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="page-11-warranty-2-years">2 χρόνια! Τον 1ο χρόνο παρέχεται άμεση αντικατάσταση με καινούριο και τον 2ο χρόνο δωρεάν επισκευή!</a>')
  gr_desc_text = string + "." + rest
 elif gr_desc_text.find("Εφ' όρου ζωής") > 0 or gr_desc_text.find("Lifetime") > 0 or gr_desc_text.find("Εφόρου ζωής") > 0 or gr_desc_text.find("Εφ\x92 όρου ζωής") > 0 :
  if gr_desc_text.find("Εγγύηση") > 0 :
   string, warranty, rest = gr_desc_text.rpartition('Εγγύηση')
  elif gr_desc_text.find("Warranty") > 0 :
   string, warranty, rest = gr_desc_text.rpartition('Warranty')
  gr_desc_text = string + "Εγγύηση:</b> Εφ' όρου ζωής.</li>"
 else :
  if gr_desc_text.find('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>') :
   string, warranty, rest = gr_desc_text.rpartition('<a class="navy_link" href="support.phtml#doa">DOA 7 ημερών</a>')
   gr_desc_text = string + rest
  elif gr_desc_text.find('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>') :
   string, warranty, rest = gr_desc_text.rpartition('<a href="support.phtml#doa" class="navy_link">DOA 7 ημερών</a>')
   gr_desc_text = string + rest
  else :
   print("No Warranty found. Will keep text as is.")

print(gr_desc_text)

