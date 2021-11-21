# works.
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlrd  # for the ability to read excel files
import xlwt  # for the ability to write to excel files
from openpyxl import load_workbook
# from pyexcel_ods import get_data  # for the ability to read ods files

path = (r"C:\Users\Manager\Documents\Html Parser - Python\test.xlsx")  # path to xslx file

wb_read = xlrd.open_workbook(path)  # open workbook as wb
sheet = wb_read.sheet_by_index(0)  # open 1st sheet from wb
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet('PriceResults')  # add sheet in virtual workbook

# sheet.cell_value(1, 2)  # show row 1 and column 2 data
	
#for i in range(1, sheet.nrows):
for i in range(17, 22):
 # print(sheet.cell_value(i,2)) # Read through all available rows, save them in i and print result
 # page_url = "https://www.e-shop.gr/s/" + sheet.cell_value(i,2)
 page_url = "http://www.eshopcy.com.cy/product?id=" + sheet.cell_value(i,2)
 print(page_url)
 uClient = uReq(page_url)
 page_soup = soup(uClient.read(), "html.parser")
 uClient.close()
 gr_price = page_soup.findAll("span", {"class" : "web-price-value-new"})
 if len(gr_price) == 0:
  gr_price_text = "Εξαντλημένο"
  print("CODE = " + sheet.cell_value(i,2) + ", εξαντλημένο.")
  ws_write.write(i,0, sheet.cell_value(i,2))
  ws_write.write(i,1, gr_price_text)
 else: 
  gr_price_text = gr_price[0].text.replace("\xa0€","").replace(".", ",")
  print("CODE = " + sheet.cell_value(i,2) + ", PRICE = " + gr_price_text)
  ws_write.write(i,0, sheet.cell_value(i,2))
  ws_write.write(i,1, gr_price_text)

wb_write.save(r'C:\Users\Manager\Documents\Html Parser - Python\ExperimentData.xls')
