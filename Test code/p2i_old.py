# p2i.py
# simple pdf to image converter

from pdf2image import convert_from_path
import sys

try:
    if len(sys.argv) == 1:
        droppedFile = r"C:\Users\manager\Desktop\ESHOP - PROTIMOLOGIO.pdf"
        # raise Exception("No file specified.")
    else:
        droppedFile = sys.argv[1]

    images = convert_from_path('droppedFile', poppler_path = r"C:\Windows\System32\poppler-21.09.0\bin")
    for i in range(len(images)):
        images[i].save('page'+ str(i) +'.jpg', 'JPEG')

    print("Total pages converted: " + str(i))
except Exception as exc:
    print("Problema: " + str(exc))
    sys.exit(1)

