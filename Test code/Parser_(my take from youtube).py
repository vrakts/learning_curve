from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

# URl to web scrap from.
# in this example we web scrap graphics cards from Newegg.com
page_url = "https://www.e-shop.gr/search?q=spigen"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# finds each product from the store page
trs = page_soup.findAll("tr")

# what I found is
# trs contains indexes [] so eg.
# trs55 = trs[55].findAll("a", {"class": "faint_link2"})
# then trs55[1].text will bring the text of the link which is the title.
# a loop function should bring all trs.

#  for url in page_soup.find_all('a'):
# print(url.get('href'))
# prints all actual links of all a tags (urls)
for tr in trs:
	prod_name = trs[0].findAll("a", {"class": "faint_link2"})
	prod_name = trs[0].findAll("a", {"class": "faint_link2"})
	print(prod_name)