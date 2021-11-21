import urllib.parse
import urllib.request
import urllib
from urllib.request import urlopen as uReq  # Web client
import time  # for the ability to measure time


# as a better solution for web page reader try the following
# from requests import get as uReq
# or import requests
# or better import requests
# req = requests.get('https://www.eshopcy.com.cy')
# soup = bs4.BeautifulSoup(req.text, 'lxml')

# New url Read method with arguments
url = 'https://www.eshopcy.com.cy/search?'
values = {'q' : 'ubiquiti'}
data = urllib.parse.urlencode(values)
data = data.encode('utf-8') # data should be bytes
req = urllib.request.Request(url, data)
resp = urllib.request.urlopen(req)
respData = resp.read()

# parsing without headers
try:
    x = uReq('https://www.google.com/search?q=test')
    # print(x.read())
    # saveFile = open('noheaders.txt','w')
    # saveFile.write(str(x.read()))
    # saveFile.close()
except Exception as e:
    print("Caught this one: " + str(e))

# parsing with headers
try:
    url = 'https://www.google.com/search?q=python'
    # now, with the below headers, we defined ourselves as a simpleton who is
    # still using internet explorer.
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    saveFile = open('withHeaders.txt','w')
    saveFile.write(str(respData))
    saveFile.close()
except Exception as e:
    print("Caught this one: " + str(e))


# random requests exaple
r = Request(url='http://www.mysite.com')
r.add_header('User-Agent', 'awesome fetcher')
r.add_data(urllib.urlencode({'foo': 'bar'})
response = urlopen(r)

si_search_url = "https://www.singular.com.cy/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&search_id=&q=03%3A520983&dispatch=products.search"
req = urllib.request.Request(si_search_url, headers = headers)
print("req is: " + str(req))
attempt = 0
sorry = 0
while attempt < 3 :
 try :
  # print("On try :" + str(attempt))
  si_uClient = uReq(req)
  break
 except ValueError as e :
  print("1")
  print("Oops, just bumped into the following ValueError exception: " + str(e))
  attempt += 1
  sorry += 1
  print("Retrying in 5 seconds.")
  time.sleep(5)
 except urllib.error.URLError as e:
  print("2")
  print("Oops, just bumped into the following Requests exception: " + str(e))
  attempt += 1
  sorry += 1
  print("Retrying in 5 seconds.")
  time.sleep(5)
 except Exception as e :
  print("3")
  print("Oops, just bumped into the following exception: " + str(e))
  attempt += 1
  sorry += 1
  print("Retrying in 5 seconds.")
  time.sleep(5)
# si_uClient.close()

si_search_url = "https://www.singular.com.cy/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&search_id=&q=03%3A520983&dispatch=products.search"
req = urllib.request.Request(si_search_url, headers = headers)
print("req is: " + str(req))
try :
 # print("On try :" + str(attempt))
 si_uClient = uReq(req)
 # break
# except ValueError as e :
 # print("1")
 # print("Oops, just bumped into the following ValueError exception: " + str(e))
 # si_uClient.close()
 # attempt += 1
 # sorry += 1
# except requests.exceptions.RequestException as e:
 # print("2")
 # print("Oops, just bumped into the following Requests exception: " + str(e))
 # si_uClient.close()
 # attempt += 1
 # sorry += 1
except Exception as e :
 print("3")
 print("Oops, just bumped into the following exception: " + str(e))
 # si_uClient.close()
