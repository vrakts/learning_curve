"""
# -*- coding: iso-8859-7 -*-
"""
import sys

try :
    from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
    from time import sleep as nani
    import requests
    import os
except KeyboardInterrupt :
    sys.exit(1)
except Exception as exc :
    import sys
    print("Κάτι πάθαμε κατά το import.")
    print(str(exc))
    sys.exit(0)

def load_soup(page, wait, retries) :
    # print("Μέσα στη σούπα.")
    attempt = 0
    while attempt < retries :
        try :
            result = requests.get(page, headers = headers)
            webpage = result.content
            page_soup = soup(result.content, "html5lib")
            # print(headers)
            break   
            # print("Έξω από τη σούπα.")
            # print("")
        # except UnicodeDecodeError:
        #     print("Unicode error...")
        #     result = requests.get(page, headers = headers)
        #     webpage = result.content
        #     decoded = webpage.decode("iso-8859-7").encode("utf-8")
        #     page_soup = soup(decoded, "html5lib")
        except Exception as exc :
            print("")
            print("Στο φόρτωμα της σελίδας, πέσαμε πάνω στο:")
            print(str(exc))
            print("Ξαναπροσπαθώ σε " + str(retries)+ ".")
            nani(wait)
            
            if attempt == retries :
                print("Προσπάθησα " + str(attempt) + " φορές και δεν τα κατάφερα.")
                input()
                sys.exit(0)
            else:
                attempt += 1
    return(page_soup)

def initialize():
    print("Αρχικοποίηση παραμέτρων...")
    test_run = 0
    attempt = 0  # how many attempts to re-read the url in case of failure
    e = 2  # will add up in case of exceptions
    retries = 3
    wait = 3
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    cookies = {'language': 'en', '_myPublicID': 'G-ed9dbb98-2434-290f-2b01-af19a2e28e53', '_pic': '4257825144', 'JSESSIONID': 'O6FeVAjR0CFrOlopHaLplYcR.node2', 'roid': 'o014661427', 'snalyticsi': '17b2b49c11348ecf22f93d622eb14658'}
    office_run = False
    convert_xl = True
    show_version = False
    print("Done")
    return test_run, attempt, e, retries, wait, headers, cookies, office_run, convert_xl

test_run, attempt, e, retries, wait, headers, cookies, office_run, convert_xl = initialize()
page = "https://www.e-shop.cy/search_main.phtml?table=EPI"
# page = "https://www.e-shop.cy/search_main?table=PER&&category=%CF%C8%CF%CD%C7"
page_soup = load_soup(page, wait, retries)

total_products_text = page_soup.find("div", {"class": "web-product-num"}).text
total_products = int(total_products_text[:total_products_text.find(" ")].strip())
next_pages_soup = page_soup.findAll("a", {"class": "mobile_list_navigation_link"})
last_offset_page_text = page_soup.findAll("a", {"class": "mobile_list_navigation_link"})[-1]
last_offset_page = last_offset_page_text['href']
last_offset_page_number = int(last_offset_page_text.text.strip())

next_pages_soup_list = []
for href in next_pages_soup:
    # href["href"]
    next_pages_soup_list.append(href["href"])

# for href in next_pages_soup_list:
#     print(href)

first_offset = int(next_pages_soup_list[0][next_pages_soup_list[0].find("=") + 1:next_pages_soup_list[0].find("&")]  )
second_offset = int(next_pages_soup_list[1][next_pages_soup_list[1].find("=") + 1:next_pages_soup_list[1].find("&")]  )
offset_step = second_offset - first_offset
offset_url_start = "https://www.e-shop.cy/search_main?offset="
offset_url_end = "&&" + page[page.find("?") + 1:] 

current_prod = 0
next_pages = []

next_pages.append(page)
print("1: " + next_pages[0])

for i in range(1, last_offset_page_number):
    cur_offset = i * offset_step
    cur_url = offset_url_start + str(cur_offset) + offset_url_end
    print(str(i + 1) + ": " + cur_url)
    next_pages.append(cur_url)

print("")

# for page in next_pages:
for page in next_pages:
    print("Loading: " + page)
    page_soup = load_soup(page, wait, retries)
    product_containers = page_soup.findAll("table", {"class": "web-product-container"})
    for product in product_containers:
        current_prod += 1
        per = product.font.text.strip()
        print(str(current_prod) + ": "+ per)

