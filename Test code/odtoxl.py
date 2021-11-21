import subprocess
import os

# path to yout LibreOffice executable
EXE = 'C:\Program Files\LibreOffice\program\soffice.exe'

# path to file
PATH = r"Z:\OneDrive\HTML Parser\Python"
# file name
file = "Αλλαγή τιμών.ods"
# full file path
full_file = os.path.join(PATH, file)

subprocess.run([EXE, '--convert-to', 'xlsx', full_file, '-outdir', PATH])

# # loop files, convert and get converted filename for outputting
# for file in os.listdir(PATH):
    # if file.lower().endswith("xls"):
        # subprocess.run([EXE, '--convert-to','xlsx',os.path.join(PATH, file),'-outdir',PATH])
        # filename, file_extension = os.path.splitext(file)
        # data['Files'].append(os.path.join(PATH, filename, file_extension.lower().replace("xls", "xlsx")))

