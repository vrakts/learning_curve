# logintest_selenium.py
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as soup
import sys

driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
driver.get("https://www.e-shop.gr/internal/")
sleep(2)

assert "INTERNAL" in driver.title
# username = driver.find_element_by_id("uid")
username = driver.find_element_by_name("user")
username.clear()
username.send_keys("gvrakas")

password = driver.find_element_by_name("pass")
password.clear()
password.send_keys("75jd993")

# driver.find_element_by_type("Image").click()
# driver.find_element_by_link_text("Grumpy cats").click()
try :
    # driver.find_element_by_css_selector("type.Image").click()
    driver.find_element_by_css_selector("input[type='Image'][src='https://www.e-shop.gr/clipartfds/submit.gif']").click()
 
    # <input type="Image" src="https://www.e-shop.gr/clipartfds/submit.gif" alt="" width="23" height="10" border="0">
 
    # find_element_by_css_selector("input[name='filePath'][type='file']")
except Exception as exc :
    print(str(exc))
    driver.quit()
    sys.exit(0)

sleep(2)

pageSource = driver.page_source
# print(pageSource)

sleep(2)

driver.get("https://www.e-shop.gr/internal/competition_cy.phtml?table=PER&category=%D3%CA%CB%C7%D1%CF%D3+%C4%C9%D3%CA%CF%D3&developer=&competitor=1&pososto=&order=6")

page_soup = soup(driver.page_source)
# print(page_soup)

lines = []
rows_tr = page_soup.findAll("tr")
rows_td = page_soup.findAll("td")


for row in rows_td:
    lines.append(row.text.strip().replace(" Ø", ""))

per_dicts = {}
per_info = []
l_index = 0
# for l in range (9, 17):
for l in range (9, len(lines)):
    print("l_index before: " + str(l_index))
    # print(lines[l])
    l_index += 1
    print("l_index after: " + str(l_index))
    if l_index == 1 or l_index == 5 or l_index == 6:
        print(str(l_index))
        print(str(lines[l]))
        try:
            per_info.append(float(lines[l]))
        except:
            per_info.append(lines[l])
        # input()
    if l % 8 == 0:
        per_dicts[per_info[0]] = per_info[1:]
        per_info = []
        l_index = 0
        # input()
        print("")

for per in per_dicts:
    print(per, " -> ",  per_dicts[per])

driver.quit()
# 
# https://www.e-shop.gr/internal/competition_cy.phtml?table=PER&category=%CC%CD%C7%CC%C7+RAM&developer=&competitor=1&pososto=&order=6