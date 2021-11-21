def ti_paizei():
    version = "Version 2"
    # Current Version 2
    ######################
    # Changelog V 2
    # - Αλλαγή κώδικα σε Defs για καλύτερη χρήση
    # - Ανανεωμένος κώδικας γενικά
    # - Επιστρέφει το λευκό χρώμα στα fonts μόλις τελειώσει το script ή εμφανιστεί λάθος.
    # - Μιλάει Ελληνικά
    # - Μέτρηση χρόνου
    # - Μικροδιορθώσεις
    # - Προσπάθεια να καταλαβαίνει πότε υπάρχει έκπτωση στο site
    #   και αντίστοιχη ενημερώση στο write file
    ######################
    # Changelog V 1.6
    # - account for ËÅÌ: instead of ΛΕΜ: etc.
    ######################
    # Changelog V 1.6
    # - e-shop.cy domain changes
    # - some text strip adjustments
    ######################
    # Changelog V 1.5
    # - Updated for secure HTTP connection
    ######################
    # Changelog V 1.4
    # - Small bug fixes for retry and url access
    ######################
    # Changelog V 1.3
    # - Retries in case of error
    ######################
    # Changelog V 1.2
    # - Compares current value with previous. If same
    #	continues to the next value to save time.
    ######################
    # Changelog V1.1
    # - Reads all values from the Showroom ods and
    #	compares them to the site. If changes are
    #	present writes difference to excel file.
    ######################
    # ToDo:
    # - Χρήση openpyxl για εγγραφή σε xlsx και ενημέρωση του ods read.
    # - ETA
    print(version)


try:
    import sys  # for system and exit functions
    import os  # for the ability to use os function like change folder
    import requests
    import ezodf  # for the ability to write to open document format files
    import xlwt  # for the ability to write to excel files
    from bs4 import BeautifulSoup as soup  # HTML data structure
    from subprocess import call
    from datetime import datetime
    from time import sleep as nani  # for the ability to measure time
except KeyboardInterrupt:
    import sys
    sys.exit(0)
except Exception as exc:
    import sys
    print("Κάτι πάθαμε κατά το import.")
    print(str(exc))
    sys.exit(0)


def get_start_time():
    global start_time, start_date, start
    start = datetime.now()
    start_date = start.strftime("%d-%m-%Y")
    start_time = start.strftime("%H:%M:%S")
    print("Εκκίνηση: " + start_date)
    print("")


def get_total_time():
    formatted_time = get_elapsed_time()
    formatted_time +=  " (H:M:S)"

    if minutes == 0 and seconds == 0:
        print("Όσο πάει χειροτερεύει. Τελείωσε σε χρόνο 0")
    elif hours > 0:
        print("Όσο πάει χειροτερεύει. Τελείωσε σε " + str(hours) + " ώρες, " + str(minutes) +
              " λεπτά και " + str(seconds) + " δευτερόλεπτα (" + str(round(total_seconds, 2)) + " δευτερόλεπτα).")
    else:
        print("Όσο πάει χειροτερεύει. Τελείωσε σε " + str(minutes) + " λεπτά και " +
              str(seconds) + " δευτερόλεπτα (" + str(round(total_seconds, 2)) + " δευτερόλεπτα).")

    print("")
    print(formatted_time)
    print("")


def get_elapsed_time():
    global elapsed_time, days, hours, minutes, seconds, total_minutes, total_seconds
    elapsed_time = datetime.now() - start  # διαφορά χρόνου σε σχέση με την αρχή
    total_seconds = elapsed_time.seconds  # σύνολο διαφοράς σε δευτερόλεπτα
    total_minutes = int(total_seconds / 60)  # σύνολο διαφοράς σε λεπτά
    seconds = int(total_seconds - (total_minutes * 60))  # υπόλοιπα δευτερόλεπτα μετά τον υπολογισμό των λεπτών
    hours = int(total_minutes / 60)  # υπόλοιπες ώρες μετά τον υπολογισμό των λεπτών
    minutes = total_minutes - (hours * 60)  # υπόλοιπα λεπτά μετά τον υπολογισμό των ωρών
    days = elapsed_time.days  # μέρες διαφοράς
    
    frm_hours = str(hours).zfill(2)
    frm_minutes = str(minutes).zfill(2)
    frm_seconds = str(seconds).zfill(2)

    formatted_time = frm_hours + ":" + frm_minutes + ":" + frm_seconds
    
    return(formatted_time)


def load_soup(page, wait, retries):
    # print("Μέσα στη σούπα.")
    attempt = 0
    while attempt < retries:
        try:
            result = requests.get(page, headers=headers)
            webpage = result.content
            page_soup = soup(webpage, "html5lib")
            # print(headers)
            break
            # print("Έξω από τη σούπα.")
            # print("")
        except Exception as exc:
            print("")
            print("Στο φόρτωμα της σελίδας, πέσαμε πάνω στο:")
            print(str(exc))
            print("Ξαναπροσπαθώ σε " + str(retries) + ".")
            nani(wait)
            attempt += 1
    if attempt == retries:
        print("Προσπάθησα " + str(attempt) + " φορές και δεν τα κατάφερα.")
        input()
        call("color 07", shell=True)
        sys.exit(0)

    return(page_soup)


def set_files():
    global write_path, read_path, write_file, alt_write_file, wb_write, ws_write, ac_row, sheet
    if os.path.exists("K:\\SALES\\ΧΡΗΣΤΕΣ\\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\\Script Results") == True:
        write_path = (
            "K:\\SALES\\ΧΡΗΣΤΕΣ\\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\\Script Results")
        read_path = ("K:\\SALES\\Stock")
    elif os.path.exists("Z:\\OneDrive\\HTML Parser\\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\\Script Results") == True:
        write_path = (
            "Z:\\OneDrive\\HTML Parser\\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ\\Script Results")
        read_path = ("Z:\\OneDrive\\HTML Parser\\Stock")
    else:
        print("Where am I?")
        sys.exit()

    read_file = "Stock.ods"  # path to ods read file
    write_file = "Updated_Showroom_Prices.xls"  # path to xslx write file
    alt_write_file = "Updated_Showroom_Prices_ALT.xls"  # path to xslx write file
    full_read_file = os.path.join(read_path, read_file)

    # xls preparations xls file for writing
    wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
    # add sheet in virtual workbook
    ws_write = wb_write.add_sheet("prices", cell_overwrite_ok=True)
    ws_write.write(0, 0, "CODE")  # write date on D1 cell
    ws_write.write(0, 1, "PRICE")  # write date on D1 cell
    ws_write.write(0, 2, "DISCOUNT")  # write date on D1 cell
    ws_write.write(0, 3, "STOCK")  # write date on D1 cell
    ws_write.write(0, 4, start_date)  # write date on D1 cell

    # Read file preparations
    # config ezodf to capture all content
    ezodf.config.set_table_expand_strategy('all')
    spreadsheet = ezodf.opendoc(full_read_file)  # open file
    ezodf.config.reset_table_expand_strategy()  # reset ezodf config

    # sheet selection and row count
    sheets = spreadsheet.sheets
    sheet = sheets[0]
    # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them if needed
    rowcount = sheet.nrows()
    ac_row = 1

    for i in range(1, rowcount):
        # print(ac_row)
        if str(sheet[i, 2].value) != "None":
            ac_row += 1
        else:
            break


def initialize():
    attempt = 0  # how many attempts to re-read the url in case of failure
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    wait = 1
    retries = 3
    cur_color = "White"
    test_mode = False
    total_list = []
    title_time = ""
    return(attempt, headers, wait, retries, cur_color, test_mode, total_list, title_time)


def color_it(color_set):
    if color_set == "White":
        call("color 07", shell=True)  # this sets the color to default white
    else:
        call("color a", shell=True)  # this sets the color to light green


def write_results(cur_code, old_price_text, new_price_text, avail_text):
    ws_write.write(i, 0, cur_code)
    ws_write.write(i, 1, old_price_text)
    ws_write.write(i, 2, new_price_text)
    ws_write.write(i, 3, avail_text)


def get_avail(page_soup):
    old_price_text = "-"
    new_price_text = "-"
    avail_text = "-"

    new_price = page_soup.findAll(
        "span", {"class": "web-price-value-new"})
    old_price = page_soup.findAll(
        "span", {"class": "web-price-value-old"})
    avail = page_soup.find("td", {
        "style": "text-align:left;padding:5px 0 2px 5px;color:#4f4f4f;font-family:Tahoma;font-size:14px;font-weight:bold;"})

    if len(old_price) == 0:
        old_price_text = "0"
    else:
        old_price_text = old_price[0].text.replace(
            "\xa0€", "").replace(".", ",").strip()

    if len(new_price) == 0:
        new_price_text = "0"
        avail_text = "Εξαντλημένο"
    else:
        new_price_text = new_price[0].text.replace(
            "\xa0€", "").replace(".", ",").strip()
        avail_text = avail.text
        if avail_text.find('ËÅÌ:') >= 0:
            avail_text_lim = avail_text[avail_text.find(
                'ËÅÌ: ')+5:avail_text.find('ËÅÕ: ')-1].strip()
            avail_text_nic = avail_text[avail_text.find(
                'ËÅÕ: ')+5:avail_text.find('ËÁÑ: ')-1].strip()
            avail_text_lar = avail_text[avail_text.rfind(
                ': ')+1:].strip()
        else:
            avail_text_lim = avail_text[avail_text.find(
                'ΛΕΜ: ')+5:avail_text.find('ΛΕΥ: ')-1].strip()
            avail_text_nic = avail_text[avail_text.find(
                'ΛΕΥ: ')+5:avail_text.find('ΛΑΡ: ')-1].strip()
            avail_text_lar = avail_text[avail_text.rfind(
                ': ')+1:].strip()
    avail_text = avail_text_nic
    total_stock = int(avail_text_lim) + int(avail_text_nic) + int(avail_text_lar)

    return(old_price_text, new_price_text, avail_text, total_stock)


def write_it_down():
    try:
        full_xl = os.path.join(write_path, write_file)
        os.chdir(write_path)
        wb_write.save(full_xl)
        print("To", full_xl, "σώθηκε")
    except:
        full_xl = os.path.join(write_path, alt_write_file)
        wb_write.save(full_xl)
        print("Πιθανώς κάποιος παίζει με το αρχείο. Προχωράω στο παρασύνθημα.")
        print(alt_write_file + ", το έχω γραμμένο στο " + write_path)

    print("")

try:
    os.system('cls')
    attempt, headers, wait, retries, cur_color, test_mode, total_list, title_time = initialize()
    color_it("Green")

    get_start_time()
    set_files()

    if test_mode is True:
        ac_row = 10

    # last_for_row = ac_row - 1

    ### for test purposes, start from:
    # start_from = ac_row - 11
    # for i in range(start_from, last_for_row):
    ###
    for i in range(1, ac_row):
        if title_time == "":
            title_time = get_elapsed_time()

        cur_code = sheet[i, 0].value.strip()
        cur_count = i
        rem_count = ac_row - i
        print_text = (str(cur_count) + ". Απομένουν: " +
                      str(rem_count) + "/" + str(ac_row) + ". Time: " + title_time)
        os.system("title " + print_text)
        if rem_count > 1:
            print("Τρέχω το " + str(cur_count) + ". Απομένουν: " +
              str(rem_count) + "/" + str(ac_row))
        elif rem_count == 1:
            print("Απομένει 1.")

        if cur_code != sheet[i-1, 0].value.strip():
            page_url = "https://www.e-shop.cy/product?id=" + cur_code
            # print(page_url)
            page_soup = load_soup(page_url, wait, retries)
            # print("On try :" + str(attempt))
            old_price_text, new_price_text, avail_text, total_stock = get_avail(page_soup)
            if old_price_text != "0":
                print("Κωδικός: " + str(cur_code) + ", Αρχική τιμή: " + old_price_text +
                      ", Έκπτωση: " + new_price_text, ", Διαθεσιμότητα:", avail_text)
            else:
                print("Κωδικός: " + str(cur_code) + ", Τιμή: " +
                      new_price_text + ", Διαθεσιμότητα:", avail_text)
            title_time = get_elapsed_time()
        else:
            print("Το προσπερνάω αυτό. Ίδια τιμή.")
        
        write_results(cur_code, old_price_text, new_price_text, avail_text)

    print("")
    write_it_down()

    get_total_time()
    color_it("White")
except KeyboardInterrupt as exc:
    # os.system('cls')
    print("")
    print("Ρε μην τον παίζεις έχουμε δουλειά!")
    try:
        input("Τι να σε κάνω;")
        print("")
        color_it("White")
        sys.exit(0)
    except Exception as exc:
        color_it("White")
        sys.exit(0)
except Exception as exc:
    print("Κάτι δεν πάει καλά.")
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    print("Exception: " + str(exc))
    print("Exception type: ", exception_type)
    print("File name: ", filename)
    print("Line number: ", line_number)
    print("")
    input()
    color_it("White")
    sys.exit(0)
