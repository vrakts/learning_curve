# p2i.py
# Current Version 1
# simple PDF to JPG converter
# if the produced file size is bigger than 600kb it resizes it
# to fit the documents for Admin upload.
# default folder is current user's Desktop.
# Convert this script to exe and drag and drop the PDF.

import sys
import os
import fitz
import PIL
from PIL import Image

def jpg_resize(jpeg_file, jpeg_size):
    image = Image.open(jpeg_file)
    while jpeg_size > 600:
        width, height = image.size
        # print(str(width))
        # print(str(height))
        size_ratio = width / height
        new_height = height / 1.01
        new_width = int(size_ratio * new_height)
        # print(str(new_width))
        # print(str(new_height))
        image = image.resize((int(new_width), int(new_height)), PIL.Image.LANCZOS)
        new_file = jpeg_file[: -4] + "_2" + ".jpg"
        # print(new_file)
        image.save(new_file, "JPEG")
        jpeg_size = int(os.path.getsize(new_file) / 1000)
        # print(str(jpeg_size))
    
    image.close()
    print("Removing " + jpeg_file)
    os.remove(jpeg_file)
    print("Renaming " + new_file + " to " + jpeg_file)
    os.rename(new_file, jpeg_file)

try:
    if len(sys.argv) == 1:
        # droppedFile = "C:\\Users\\manager\\Desktop\\test.pdf"
        raise Exception("No file specified.")
    else:
        droppedFile = sys.argv[1]
        if droppedFile[-4:].find(".pdf") != 0:
            raise Exception("Not a PDF file you rascal...")

    # # Set the maximum file size in KiloBytes
    file_size = 600
    # # Find current user's Desktop folder and change to it
    path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    os.chdir(path) 
    # # Get better resolution
    zoom_x = 2.0  # horizontal zoom
    zoom_y = 2.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension
    # # seperate filenames
    full_file = os.path.join(path, droppedFile)
    bare_file = droppedFile[:droppedFile.find(".")]
    jpeg_ext = ".jpg"
    # # open document
    doc = fitz.open(droppedFile)
    page_index = 1
    # # iterate through the pages
    for page in doc:
        jpeg_file = bare_file + "_" + str(page_index) + jpeg_ext  # set a jpeg filename
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        pix.save(jpeg_file)  # store image as a jpeg file
        page_index += 1
        # pix.save("page-%i.jpg" % page.number)  # store image as a PNG
    # input()
    jpeg_size = int(os.path.getsize(jpeg_file) / 1000)
    if jpeg_size < 600 :
        print("File should be OK with size: " + str(jpeg_size))
    else:
        print("Trying to resize...")
        jpg_resize(jpeg_file, jpeg_size)
except Exception as exc:
    print("Problema: " + str(exc))
    input()
    sys.exit(1)

