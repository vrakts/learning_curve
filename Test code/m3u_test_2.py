import time
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import requests
import m3u8

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}


def get_real_url(url):
    playlist = m3u8.load(uri=url, headers=headers)
    return playlist.playlists[0].absolute_uri


def AESDecrypt(cipher_text, key, iv):
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=key)
    cipher_text = aes.decrypt(cipher_text)
    return cipher_text


def download_m3u8_video(url, save_name):
    real_url = get_real_url(url)
    playlist = m3u8.load(uri=real_url, headers=headers)
    key = requests.get(playlist.keys[-1].uri, headers=headers).content

    n = len(playlist.segments)
    size = 0
    start = time.time()
    for i, seg in enumerate(playlist.segments, 1):
        r = requests.get(seg.absolute_uri, headers=headers)
        data = r.content
        data = AESDecrypt(data, key=key, iv=key)
        size += len(data)
        with open(save_name, "ab" if i != 1 else "wb") as f:
            f.write(data)
        print(
            f"\r Download Progress({i}/{n})，Downloaded:{size/1024/1024:.2f}MB，Download time consumed:{time.time()-start:.2f}s", end=" ")


download_m3u8_video('https://videostream.skai.gr/skaivod/_definst_/mp4:skai/2_Do-Not-Delete_Shows/Kalo-Meshmeraki/moutsinas20211013.mp4/chunklist.m3u8','moutsinas20211013.mp4')