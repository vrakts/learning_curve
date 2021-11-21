# aei_na_doume.py

import sys


try:
    from bs4 import BeautifulSoup as soup
    from random import randint
    from time import sleep as nani
    from datetime import datetime
    import requests
    import os
    import sys
    from openpyxl import Workbook
    from openpyxl import load_workbook
    from openpyxl.styles import Font
    import xlwt  # , unicodedata
except KeyboardInterrupt:
    sys.exit(0)
except Exception as exc:
    print("Κάτι πάθαμε κατά το import.")
    print(str(exc))
    sys.exit(0)



def load_soup(page, wait, retries):
    # temp_product = page[page.rfind("=") + 1:]
    # print("Loading soup for " + temp_product)
    # print("")
    # print("Μέσα στη σούπα.")
    attempt = 0
    while attempt < retries:
        try:
            result = requests.get(page, headers=headers)
            webpage = result.content
            page_soup = soup(webpage, "html5lib")
            break
            # print("Έξω από τη σούπα.")
            # print("")
        except Exception as exc:
            print("")
            print("Στο φόρτωμα της σελίδας, πέσαμε πάνω στο:")
            print(str(exc))
            print("Ξαναπροσπαθώ σε " + str(retries) + ".")
            nani(wait)
            attempt += 1
    if attempt == retries:
        print("Προσπάθησα " + str(attempt) + " φορές και δεν τα κατάφερα.")
        input()
        sys.exit(0)
    
    return(page_soup)


def get_specs(gr_soup, cy_soup):
    """ Find all specs in code, the else part is for the old html code"""
    gr_specs = gr_specs1 = gr_specs2 = cy_specs = cy_specs1 = cy_specs2 = []
    if gr_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details2'}):
        gr_specs1 = gr_soup.find('td', {'class': 'product_table_body'}).findAll(
            'td', {'class': 'details1'})
        gr_specs2 = gr_soup.find('td', {'class': 'product_table_body'}).findAll(
            'td', {'class': 'details2'})
    else:
        gr_specs = gr_soup.find('td', {'class': 'product_table_body'}).findAll(
            'td', {'class': 'details1'})
        for i in range(0, len(gr_specs), 2):
            gr_specs2.append(gr_specs[i])
        for i in range(1, len(gr_specs), 2):
            gr_specs1.append(gr_specs[i])
    
    if cy_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details2'}):
        cy_specs1 = cy_soup.find('td', {'class': 'product_table_body'}).findAll(
            'td', {'class': 'details1'})
        cy_specs2 = cy_soup.find('td', {'class': 'product_table_body'}).findAll(
            'td', {'class': 'details2'})
    else:
        cy_specs = cy_soup.find('td', {'class': 'product_table_body'}).findAll(
            'td', {'class': 'details1'})
        for i in range(0, len(cy_specs), 2):
            cy_specs2.append(cy_specs[i])
        for i in range(1, len(cy_specs), 2):
            cy_specs1.append(cy_specs[i])
    
    if len(cy_specs1) == len(gr_specs1):
        print("len(cy_specs1 / gr_specs1): " + str(len(cy_specs1)))
    else:
        print("len(cy_specs1): " + str(len(cy_specs1)))
        print("len(gr_specs1): " + str(len(gr_specs1)))
    
    if len(cy_specs2) == len(gr_specs2):
        print("len(cy_specs2 / gr_specs2): " + str(len(cy_specs2)))
    else:
        print("len(cy_specs2): " + str(len(cy_specs2)))
        print("len(gr_specs2): " + str(len(gr_specs2)))
    
    return(gr_specs1, gr_specs2, cy_specs1, cy_specs2)



headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
product = "TEL.091004"
# gr_page_url = "https://www.e-shop.gr/kinito-leeco-le-2-x527-4g-lte-3gb-32gb-grey-p-TEL.091004"
gr_page_url = 'https://www.e-shop.gr/product?id=' + product  # gr page
cy_page_url = 'https://www.e-shop.cy/product?id=' + product  # cy page
gr_soup = load_soup(gr_page_url, 3, 3)
cy_soup = load_soup(cy_page_url, 3, 3)

# gr_specs1, gr_specs2, cy_specs1, cy_specs2 = get_specs(gr_soup, cy_soup)

# gr_specs = gr_specs1 = gr_specs2 = cy_specs = cy_specs1 = cy_specs2 = []
gr_specs = []
gr_specs1 = []
gr_specs2 = []
cy_specs = []
cy_specs1 = []
cy_specs2 = []
txt_gr_specs1 = []
txt_gr_specs2 = []
txt_cy_specs1 = []
txt_cy_specs2 = []


gr_specs = gr_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details1'})
cy_specs = cy_soup.find('td', {'class': 'product_table_body'}).findAll('td', {'class': 'details1'})

print("gr_specs2")
for i in range(0, len(gr_specs), 2):
    print("i:", i, "spec:", gr_specs[i].text.strip())
    gr_specs2.append(gr_specs[i].text.strip())

print()

print("gr_specs1")

for l in range(1, len(gr_specs), 2):
    print("L:", l, "spec:", gr_specs[l].text.strip())
    gr_specs1.append(gr_specs[l])

print()



print("txt_gr_specs1")
print("before:")
for spec in gr_specs1:
    try:
        print(spec)
        txt_gr_specs1.append(spec.text.strip())
    except Exception as exc:
        txt_gr_specs1.append(spec)

print()
print("after:")
for spec in txt_gr_specs1:
    print(spec)

print()
print("txt_gr_specs2")

for spec in gr_specs2:
    try:
        txt_gr_specs2.append(spec.text.strip())
    except Exception as exc:
        txt_gr_specs2.append(spec)

print()

### cy_specs
for i in range(0, len(cy_specs), 2):
    print("i:", i, "spec:", cy_specs[i].text.strip())
    cy_specs2.append(cy_specs[i].text.strip())

for l in range(1, len(cy_specs), 2):
    print("L:", l, "spec:", cy_specs[l].text.strip())
    cy_specs1.append(cy_specs[l])


for spec in cy_specs1:
    try:
        txt_cy_specs1.append(spec.text.strip())
    except Exception as exc:
        txt_cy_specs1.append(spec)

print()


for spec in cy_specs2:
    try:
        txt_cy_specs2.append(spec.text.strip())
    except Exception as exc:
        txt_cy_specs2.append(spec)


meion = 0
for test in range(len(txt_cy_specs1)):
    gr_value = txt_gr_specs1[test]
    cy_value = txt_cy_specs1[test]
    print("GR:", gr_value, ", CY:", cy_value)
    if gr_value == cy_value:
        print(test+1, "pass")
    else:
        print(test+1, "fail")
    print()

