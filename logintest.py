import requests
from bs4 import BeautifulSoup as soup

headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
payload = {'user': 'gvrakas', 'pass': '75jd993'}
login_url = 'https://www.e-shop.gr/internal/default.phtml'
url = 'https://www.e-shop.gr/internal/competition_cy.phtml?table=PER&category=ACTION+CAMERAS&developer=&competitor=1&pososto=&order=6'
# requests.post(url, data=payload)

with requests.Session() as s:
 login_result = s.post(login_url, data = payload, headers = headers)
 # print the html returned or something more intelligent to see if it's a successful login page.
 result = s.get(url, headers = headers)
 webpage = result.content
 page_soup = soup(webpage, "html5lib")
 tds = page_soup.findAll("td")
 for t in tds :
  print(t.text)
 # print(p.text)

 # An authorised request.
 # # r = s.get('A protected web page url')
 # # print(r.text)
 # etc...