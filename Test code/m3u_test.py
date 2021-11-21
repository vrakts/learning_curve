import m3u8
import requests

class RequestsClient():
    def download(self, uri, timeout=None, headers={'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}, verify_ssl=True):
        o = requests.get(uri, timeout=timeout, headers=headers)
        return o.text, o.url



m3u8_obj = m3u8.load('https://videostream.skai.gr/skaivod/_definst_/mp4:skai/2_Do-Not-Delete_Shows/Kalo-Meshmeraki/kalomeshmeraki20211013.mp4/chunklist.m3u8', http_client=RequestsClient())
# playlist = m3u8_obj.dumps()
playlist=[el['uri'] for el in m3u8_obj.data['segments']]
print(playlist)


# m3u8_obj = m3u8.load('https://videostream.skai.gr/skaivod/_definst_/mp4:skai/2_Do-Not-Delete_Shows/Kalo-Meshmeraki/kalomeshmeraki20211013.mp4/chunklist.m3u8')
# playlist=[el['uri'] for el in m3u8_obj.data['segments']]

# print(playlist)



