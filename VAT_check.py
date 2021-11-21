
### VAT_check.py version 1 Beta
# checks the copied VAT on the VIES site and
# Returns a dict-like object with the fields 'countryCode', 'vatNumber',
# 'requestDate', 'valid' (boolean), 'name', and 'address'.

from zeep import Client, helpers

import clipboard, ctypes

vat = clipboard.paste().strip()
# not valid VAT
vat = '10208496Z'
###
# valid VAT
# vat = '10208496D'


client = Client('http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl')
country = 'CY'

result = client.service.checkVat(country, vat)

result_dict = helpers.serialize_object(result)
# for dick in result_dict:
#  print(dick)
#  result_dict.get(dick)

is_valid = result_dict.get("valid")

if is_valid == True :
 print_text = "Ο αριθμός ΦΠΑ ισχύει"
 details = " " + vat + ", " + result_dict.get("name") + " - " + result_dict.get("address").replace("\n", "").replace(" ,", ",").replace("  ", " ")
else :
 print_text = "Μη έγκυρος αριθμός ΦΠΑ"
 details = " " + vat

print(print_text)
clipboard.copy(print_text)
if is_valid == True :
 ctypes.windll.user32.MessageBoxW(0, print_text + ": " + details, "OK", 0)
else:
 ctypes.windll.user32.MessageBoxW(0, print_text + ": " + details, "Efastin", 0)

