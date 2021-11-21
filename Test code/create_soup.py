# needs a lot of refining

from bs4 import BeautifulSoup as soup  # import the BeatifulSoup function from bs4 as soup
import requests
import os  # for the ability to use os function like change folder
import sys  # for exit purposes in case of error

cookies = {'language': 'el'}
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
answer = ""
choice = ""
manual = ""
find_what = ""

page_url = input("Enter URL to analyze: ")
result = requests.get(page_url, cookies = cookies, headers = headers)
webpage = result.content
page_soup = soup(webpage, "html5lib")

while answer != "exit" and choice != "exit" :
 answers = []
 print("")
 print("1. Single element.")
 print("2. Element with class.")
 print("3. Enter manual query.")
 choice = input("")
 if choice == "1" :
  print("")
  answer = input("Give element to check value: ")
  answers.append(answer)
 elif choice == "2" :
  print("")
  answer1 = input("Give element 1: ")
  answer2 = input("Give element 2: ")
  answer3 = input("Give element 3: ")
  answers.append(answer1)
  answers.append(answer2)
  answers.append(answer3)
  # answers.append("{'" + answer2 + "': '" + answer3 + "'}")
  answer = answers[0] + ", {" + answers[1] + ": " + answers[2] + "}"
  # answer = "'" + answer1 + "', {'" + answer2 + "': '" + answer3 + "'}"
 else :
  answer = input("Enter manual query: ")
 print("")
 print("Searching for " + answer + ".")
 find_what = input("Find what? Press enter for text. ")
 if len(find_what) < 1 :
  find_what = "text"
 print("find_what: '" + find_what + "'")
 print("")
 print("Searching for page_soup.find(" + answer + ")." + find_what)

 if choice == 2 :
  soup_result = page_soup.find(answers[0], {answers[1] : answers[2]}).text
 else :
  soup_result = page_soup.find(answers[0]).text
 # else :
  # print("Searching for page_soup.find(" + answer + ")." + find_what)
  # soup_result = page_soup.find(answer).find_what
 print(soup_result)