import pandas as pd
import requests, clipboard, ctypes

vat = clipboard.paste().strip()

headers = {'User-Agent': 'Mozilla/5.0 (Windows 10; 82.0.3) Gecko/82.0.3 Firefox/82.0.3'}
cookies = {
'has_js': '1',
'JSESSIONID': 'RrnmvM85o2eaQr428hJ5YP6-udJydG0gBOyGiyIpRF2VfMCa9yAN!-1507289196',
'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE': 'el'
}

payload = {
'countryCombobox': 'CY',
'number': '10208496D',
'submit': 'Επαλήθευση'}

r = requests.post('https://ec.europa.eu/taxation_customs/vies/?locale=el', data = payload, headers = headers, cookies = cookies)
print(r.text)

tables = pd.read_html(r.text)
table = tables[0]