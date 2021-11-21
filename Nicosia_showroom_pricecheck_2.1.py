def ti_paizei():
    version = "Version 2.1"
    # Current Version 2.1
    ######################
    # Changelog V 2.1
    # - ETA
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
    from time import sleep as nani, time  # for the ability to measure time
except KeyboardInterrupt:
    import sys
    sys.exit(0)
except Exception as exc:
    import sys
    print("Κάτι πάθαμε κατά το import.")
    print(str(exc))
    sys.exit(0)


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
    
    start_date = datetime.now().strftime("%d-%m-%Y")

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
    global run_time, run_time_start, run_time_end, title_time
    attempt = 0  # how many attempts to re-read the url in case of failure
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    wait = 1
    retries = 3
    cur_color = "White"
    test_mode = 0
    total_list = []
    title_time = ""
    run_time = run_time_start = run_time_end = 0
    return(attempt, headers, wait, retries, cur_color, test_mode, total_list)


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


def get_start_time():
    global start_time, start_date, start
    start = time()
    start_date = datetime.now().strftime("%d-%m-%Y")
    start_time = datetime.now().strftime("%H:%M:%S")
    print("Εκκίνηση:", start_date + ",", start_time)
    print("")


def get_total_time(elapsed_days, elapsed_hours, elapsed_minutes, elapsed_seconds):
    if elapsed_minutes == 0 and elapsed_seconds == 0:
        print("Όσο πάει χειροτερεύει. Τελείωσε σε χρόνο 0")
    elif elapsed_hours > 0:
        if elapsed_days > 0:
            print("Όσο πάει χειροτερεύει. Τελείωσε σε " + str(elapsed_hours) + " μέρες, " + str(elapsed_hours) + " ώρες, " + str(elapsed_minutes) +
              " λεπτά και " + str(elapsed_seconds) + " δευτερόλεπτα")
        else:
            print("Όσο πάει χειροτερεύει. Τελείωσε σε " + str(elapsed_hours) + " ώρες, " + str(elapsed_minutes) +
              " λεπτά και " + str(elapsed_seconds) + " δευτερόλεπτα")
    else:
        print("Όσο πάει χειροτερεύει. Τελείωσε σε " + str(elapsed_minutes) + " λεπτά και " +
              str(elapsed_seconds) + " δευτερόλεπτα")
    
    formatted_run_time = format_time(elapsed_days, elapsed_hours, elapsed_minutes, elapsed_seconds)
    
    return(formatted_run_time)


def get_average_old(run_time_start, run_time_end, run_time):
    run_diff = run_time_end - run_time_start
    run_seconds = run_diff.seconds
    # print("Total seconds: " + str(run_seconds))
    run_time += run_seconds
    # print("Runtime: " + str(run_time))
    total_list.append(run_seconds)
    # print("sum totallist: " + str(sum(total_list)))
    # print("len total_list: " + str(len(total_list)))
    total_aver = sum(total_list) / len(total_list)
    # print("total_aver: " + str(total_aver))
    # print("ac_row: " + str(ac_row))
    # υπολογίζει περίπου πόσα δευτερόλεπτα θα διαρκέσει το script βάσει των totals που θα τρέξουν
    est_average = int(total_aver * ac_row)
    est_average_mins = int(est_average / 60)  # λεπτά
    est_average_secs = int(est_average - (est_average_mins * 60))  # δευτερόλεπτά
    est_average_anal = str(est_average_mins).zfill(2) + ":" + str(est_average_secs).zfill(2)  # λεπτά δευτερόλεπτα αναλυτικά
    # υπολογίζει περίπου πόσος χρόνος απομένει για το τέλος του script
    est_left = int(est_average - run_time)
    est_left_mins = int(est_left / 60)  # λεπτά
    est_left_secs = int(est_left - (est_left_mins * 60))  # δευτερόλεπτά
    est_left_anal = str(est_left_mins).zfill(2) + ":" + str(est_left_secs).zfill(2)  # λεπτά δευτερόλεπτα αναλυτικά

    # print("Μέσος όρος:", est_average_anal, "- Εκτίμηση:", est_left_anal)
    # print()
    return(est_left_anal)


def get_average(time_diff, current_run, total_runs):
    # average of time difference till current run
    aver = round(time_diff / current_run, 2)
    # ETA
    est_total = round(aver * total_runs, 2)
    # estimated remaning time in seconds
    est_rem = round(est_total - time_diff, 2)
    
    return(est_total, est_rem)


def time_calc(seconds):
    total_minutes = int(seconds / 60)
    total_hours = int(total_minutes / 60)
    cur_days = int(total_hours / 24)
    days_to_hours = int(cur_days * 24)
    cur_hours = int(total_hours - days_to_hours)
    cur_minutes = total_minutes - ((days_to_hours + cur_hours) * 60)
    cur_seconds = int(seconds - (total_minutes * 60))
    
    return(cur_days, cur_hours, cur_minutes, cur_seconds)


def format_time(days, hours, minutes, seconds):
    if seconds < 5:
        frm_time = "< 05''"
    else:
        frm_hours = str(hours).zfill(2)
        frm_minutes = str(minutes).zfill(2)
        frm_seconds = str(seconds).zfill(2)
        frm_time = str(frm_hours) + ":" + str(frm_minutes) + ":" + str(frm_seconds)
        if days > 0:
            frm_time = str(days) + "days, " + frm_time

    return(frm_time)


def get_elapsed_time():
    global elapsed_days, elapsed_hours, elapsed_minutes, elapsed_seconds
    total_seconds = max(time() - start, 1)  # διαφορά χρόνου σε σχέση με την αρχή, = 1 αν μόλις ξεκίνησε το script
    elapsed_days, elapsed_hours, elapsed_minutes, elapsed_seconds = time_calc(total_seconds)
    formatted_run_time = format_time(elapsed_days, elapsed_hours, elapsed_minutes, elapsed_seconds)

    if quit is True:
        formatted_run_time = get_total_time(elapsed_days, elapsed_hours, elapsed_minutes, elapsed_seconds)
        return(formatted_run_time)
    else:
        estimated_end, est_remaining = get_average(total_seconds, i, ac_row)
        rem_days, rem_hours, rem_minutes, rem_seconds =  time_calc(est_remaining)
        formatted_est_time = format_time(rem_days, rem_hours, rem_minutes, rem_seconds)
    
    return(formatted_run_time, formatted_est_time)


try:
    os.system('cls')
    attempt, headers, wait, retries, cur_color, test_mode, total_list = initialize()
    color_it("Green")

    set_files()
    get_start_time()

    if test_mode != 0:
        ac_row = test_mode

    # last_for_row = ac_row - 1

    ### for test purposes, start from:
    # start_from = ac_row - 11
    # for i in range(start_from, last_for_row):
    ###
    for i in range(1, ac_row):
        cur_code = sheet[i, 0].value.strip()
        cur_count = i
        rem_count = ac_row - i

        # if title_time == "":
        #     title_time, est_left_anal = ("00:00:00", "--:--")
        title_time, est_left_anal = get_elapsed_time()
        print_text = (str(cur_count) + ". Απομένουν: " +
                      str(rem_count) + "/" + str(ac_row) + ". Time: " + title_time + ", eta: " + est_left_anal)
        os.system("title " + print_text)
        if rem_count > 1:
            print("Τρέχω το " + str(cur_count) + ". Απομένουν: " +
              str(rem_count) + "/" + str(ac_row) + " - " + est_left_anal)
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
        else:
            print("Το προσπερνάω αυτό. Ίδια τιμή.")
            write_results(cur_code, old_price_text, new_price_text, avail_text)
            continue
        
        write_results(cur_code, old_price_text, new_price_text, avail_text)
        # title_time, est_left_anal = get_elapsed_time()

    print("")
    write_it_down()

    quit = True
    formatted_run_time = get_elapsed_time()
    print(formatted_run_time)
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
