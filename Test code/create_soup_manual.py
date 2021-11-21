# needs a lot of refining

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
import requests, os, sys, re

# cookies = {'language': 'el'}
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

# page_url = 'https://www.stephanis.com.cy/el/products/gaming/video-games/pc?view=thumbnails&sortBy=newest&Quantity=min&PriceMin=&PriceMax=&SF_945=3658&recordsPerPage=100'
page_url = 'https://www.e-shop.cy/kinito-samsung-galaxy-note-20-ultra-256gb-12gb-n985-mystic-white-p-TEL.093060'
# result = requests.get(page_url, cookies = cookies, headers = headers)
result = requests.get(page_url, headers = headers)
webpage = result.content
page_soup = soup(webpage, "html5lib")

regex = re.compile('.*property-spotlight-slide-2.*')
containers = page_soup.findAll("div", {"class" : regex})
for container in containers :
 print(container.text.strip())

price_containers = containers[1].findAll('div', {'class': 'listing-details-heading'})
for price in price_containers :
 print(price.text.strip().replace('€', ''))

