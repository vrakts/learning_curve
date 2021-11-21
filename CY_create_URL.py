### Given a list of codes it creates a URL to show all codes as a query page.
### Helps with other scripts to check for descriptions, prices, translations etc.

import clipboard

codelist = []
i = 0
answer = "x"
while answer != "" :
 answer = input("Paste values (leave empty to terminate process): ")
 codelist.append(answer.strip())

page_url = "https://www.e-shop.cy/search_main.phtml?table=PER,ANA,TLS,TEL,HAP,EPI,PCF,PCG,XB3,XB1,PS4,PS3,PSV,WII,NSW,WIU,NDS,TDS,PSP&id="
for code in codelist :
 if i == 0 :
  page_url = page_url + code
 else :
  page_url = page_url + ',' + code
 i += 1

page_url = page_url[:-1]
print("")
print("Your link is:")
print(page_url)
clipboard.copy(page_url)
print("")
input("Link copied just paste it somewhere. Press any key to exit.")
