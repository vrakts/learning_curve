# works. Need to trap the out of range error
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
# from pyexcel_ods import get_data  # for the ability to read ods files
path = (r"Z:\Users\Vrakts\Desktop\Html Parser - Python\test.xlsx")  # path to xslx file

wb = xlrd.open_workbook(path)  # open workbook as wb
sheet = wb.sheet_by_index(0)  # open 1st sheet from wb
# sheet.cell_value(1, 2)  # show row 1 and column 2 data
	
for i in range(1, sheet.nrows):
 # print(sheet.cell_value(i,2)) # Read through all available rows, save them in i and print result
 page_url = "https://www.e-shop.gr/s/" + sheet.cell_value(i,2)
 print(page_url)
 uClient = uReq(page_url)
 page_soup = soup(uClient.read(), "html.parser")
 uClient.close()
 gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 gr_price_text = gr_price[0].text.replace("\xa0€","")
 print("CODE = " + sheet.cell_value(i,2) + ", PRICE = " + gr_price_text)
