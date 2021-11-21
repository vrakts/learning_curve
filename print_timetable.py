import sys


def ti_paizei():
    version = "Version 1.0 beta"
    # Current version 1.6 beta
    # print_timetable.py
    #####################
    # Changelog v1.0
    # - Τυπώνει σε προκαθορισμένο εκτυπωτή το παρουσιολόγιο
    # - Φαίνεται πως τυπώνει μόνο την 1η σελίδα !!!
    ### - Correct command line: soffice --pt "ET-4500 Series(Δίκτυο)" "FILE"
    ### - Libre path: C:\Program Files\LibreOffice\program
    #####################
    # To do:
    # - Αλλαγή ημερομηνίας σύμφωνα με τον τρέχων μήνα
    # - Για καλύτερη χρήση να ρωτάει αν είναι για τον τρέχων ή τον επομενο
    # - Backup των αρχείων σε zip??? για ανάκτηση αν κάτι πάει στραβα.
    # - Να τυπώνει όλες τις σελίδες.
    print(version)


try:
    import os
    import subprocess
    from openpyxl import Workbook
    from openpyxl.styles import Font
except KeyboardInterrupt:
    sys.exit(0)
except Exception as exc:
    import sys
    print("Κάτι πάθαμε κατά το import.")
    print(str(exc))
    sys.exit(0)


def print_function(time_table):
    """ correct command:  soffice --headless --convert-to ods *.xls"""
    EXE = 'C:\\Program Files\\LibreOffice\\program\\soffice.exe'
    lib_switches = "--pt"
    printer_name = "ET-4500 Series(Δίκτυο)"
    # printer_name = "Foxit Reader PDF Printer"
    subprocess.run([EXE, lib_switches, printer_name, time_table])
    # subprocess.run([EXE, '--pt', 'ET-4500 Series(Δίκτυο)', time_table])
    print("Έτοιμος... λογικά")


def initialize():
    global read_path, xl_file, time_table
    if os.path.exists("K:\\SALES\\ΧΡΗΣΤΕΣ\\MANAGER - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\\Περί υπαλλήλων\\Ωράρια\\Παρουσιολόγιο"):
        read_path = "K:\\SALES\\ΧΡΗΣΤΕΣ\\MANAGER - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\\Περί υπαλλήλων\\Ωράρια\\Παρουσιολόγιο"
    elif os.path.exists("Z:\\OneDrive\\HTML Parser\\Python\\Test_Path"):
        read_path = "Z:\\OneDrive\\HTML Parser\\Python\\Test_Path"
    else:
        print("Μα που είμαι?")
        sys.exit(1)
    xl_file = "Παρουσιολόγιο Λευκωσίας.xlsx"
    time_table = os.path.join(read_path, xl_file)


try:
    initialize()
    os.chdir(read_path)
    if os.path.exists(time_table):
        print_function(time_table)
    else:
        print("Not there")
except KeyboardInterrupt:
    sys.exit()
except Exception as exc:
    print(str(exc))