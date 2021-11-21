from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
from urllib.request import urlopen as uReq  # Web client to read the HTML code as uReq
from urllib.request import urlretrieve
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error
import time

attempt = 0
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
page_url = input("Type the URL: ")
req = urllib.request.Request(page_url, headers = headers)
attempt = 0
while attempt < 3 :
 try :
  # print("On try :" + str(attempt))
  uClient = uReq(req)
  page_soup = soup(uClient.read(), "html5lib")
  uClient.close()
  break
 # except http.client.IncompleteRead :
 except Exception as exc :
  # print("On except :" + str(attempt))
  print("Oops, just bumped into the following exception: " + str(exc))
  print("Retrying in 5 seconds.")
  attempt += 1

video_url = page_soup.find('div', {'class' : 'video'}).iframe

print('Beginning file download with urllib2...')

url = 'https://d375stp2rt9ssf.cloudfront.net/synthcourses_mp4/massive/MassCoursesMod1.mp4?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kMzc1c3RwMnJ0OXNzZi5jbG91ZGZyb250Lm5ldC9zeW50aGNvdXJzZXNfbXA0L21hc3NpdmUvTWFzc0NvdXJzZXNNb2QxLm1wNCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU3OTk5NDE2N319fV19&Signature=OJvlFDe94dbtQQmNf4QBMpkcNoiKVQuTCsioX-Bh7-yi3B1MsfHa3AGMuE74qcqXi9vcd7Ye9NiEQTI7J~lHUjg6KXsTrcGxNwAAt4siYA5gw5ZHJR6hpiSpXcncGX~1RX9U8w6HEDVkqPy96gbV8d-Pob5fY-664XRnbGWcG~M_&Key-Pair-Id=APKAJZEVY7CKZ7HAJ23A'
urllib.request.urlretrieve(url, r'Z:\Users\Vrakts\Desktop\test')