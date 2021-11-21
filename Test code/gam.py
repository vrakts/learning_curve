from bs4 import BeautifulSoup as soup  # με αυτή τη βιβλιοθήκη θα μπορεί να τραβήξεις τον κώδικα της σελίδας που θέλεις
from urllib.request import urlopen as uReq  # αυτός θα είναι ο Browser σου
import urllib.request  # αυτό θα βοηθήσει σε κάποιες λειτουργίες του Browser σου
import xlrd  # δίνει την δυνατότητα να "διαβάζεις" αρχεία XLS
import xlwt  # δίνει την δυνατότητα να "γράφεις" αρχεία XLS
import ezodf  # δίνει την δυνατότητα να "διαβάζεις" και "γράφεις" αρχεία ods, odf
import os  # δίνει τη δυνατότητα να παίζεις με φακέλους στα Windows

# Οι δύο γραμμές παρακάτω επιτρέπουν στο πρόγραμμα σου να αανγωνρίζεται ώς Mozilla, Chrome ή Safari στη σελίδα που τραβάς δεδομένα
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

work_path = (r"C:\TEMP")  # ορίζεις τον φάκελο
os.chdir(work_path)  # λες στο σύστημα ότι γράψει να τα γράψει σε αυτό τον φάκελο
# Οι παρακάτω γραμμές έχουν να κάνουν με το αν διαβάζεις από κάποιο αρχείο τα στοιχεία σου. Αν όχι δεν χρειάζονται
file_name = ('TEST.ods')  # όνομα αρχείου για να πάρεις τα δεδομένα
ezodf.config.set_table_expand_strategy('all')  # λες στο σύστημα να διαβάζει ΟΛΑ ΤΑ ΔΕΔΟΜΕΝΑ του αρχείου
spreadsheet = ezodf.opendoc(file_name)  # ανοίγει το αρχείο στη μνήμη
ezodf.config.reset_table_expand_strategy()  # επαναφέρει το σύστημα ανάγνωσης στο Default
# Οι παρακάτω γραμμές έχουν να κάνουν με το αν γράφεις τα αποτελέσματα σε κάποιο αρχείο. Αν όχι δεν χρειάζονται
write_file = ('TEST_1.ods')  # όνομα αρχείου εγγραφής
wb_write = xlwt.Workbook()  # Φτιάχνει ένα εικονικό "Excel" στη μνήμη
ws_write = wb_write.add_sheet('test')  # προσθέτει ένα φύλο 'test' στο εικονικό excel
ws_write.write(0,0, 'CODE')  # φράφει τον τίτλο CODE στη γραφμμή 0 και στήλη 1 (αρα στο κελί Α1)
ws_write.write(0,1, 'OEM')
ws_write.write(0,2, 'GR_PRICE')
ws_write.write(0,3, 'CATEGORY')
ws_write.write(0,4, 'BRAND')
ws_write.write(0,5, 'SUBCAT')
ws_write.write(0,6, 'DESCRIPTION')

page_url = "https://www.e-shop.gr/s/PER.901547"  # αυτή είναι η σελίδα την οποία θα διαβάσεις
# παρακάτω ξεκινάς να ανοίξεις την σελίδα, να τραβήξεις τον κώδικα της σελίδα και να κλείσεις τη σύνδεση με τη σελίδα
req = urllib.request.Request(page_url, headers = headers)
uClient = uReq(req)
page_soup = soup(uClient.read(), "html5lib")  # το "html5lib" αναλόγως το πως έχει γραφτεί η σελίδα μπορεί να μην δίνει σωστά αποτελέσματα.
uClient.close()

page_soup.findAll("span", {"class" : "web-price-value-new"})  # ψάχνει στον κώδικα της σελίδας (page_soup) να βρεί το element "span" με ιδιότητες class="web-price-value-new". Εδώ κρατάει την τιμή το GR. Προσοχή το findAll δημιουργεί πίνακα και θέλει προσοχή στο πως θα τραβήξεις τα δεδομένα από μέσα. Μιλάμε για αυτό σε άλλη φάση.
page_soup.find('td', {'class': 'product_table_body'})  # ψάχνει στον κώδικα της σελίδας (page_soup) να βρεί το element "td" με ιδιότητες class="product_table_body". Εδώ κρατάει την περιγραφή το GR. Το find φέρνει μόνο 1 αποτέλεσμα και μπορείς να το διαχειριστείς άμεσα.
page_soup.find('td', {'class': 'product_table_body'}).text  # με αυτόν τον τρόπο θα πάρεις μόνο το κείμενο (text) που βρίσκεται μέσα στον κώδικα.



amoiropoulos@gmail.com