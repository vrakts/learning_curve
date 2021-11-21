import pyperclip
import sys


def cy_temp_price(gr_price, add):
    if add == 0:
        percent = 1.15
    else:
        percent = 1
    transport = 15
    if gr_price <= 1620:
        temp_price = (((gr_price / 1.24) + add + transport) * percent) * 1.19
    else:
        temp_price = gr_price + 100
    return(temp_price)


gr_price = ""
answer_text = ""

while answer_text == "":
    print_text = "Δώσε τιμή GR: "
    try: 
        answer_text = input(print_text)
        gr_price = float(answer_text.replace(" €", "").strip())
        if gr_price < 400:
            add = 0
            temp_price = cy_temp_price(gr_price, add)
        elif gr_price >= 400 and gr_price < 500:
            add = 50
            temp_price = cy_temp_price(gr_price, add)
        elif gr_price >= 500 and gr_price < 600:
            add = 60
            temp_price = cy_temp_price(gr_price, add)
        elif gr_price >= 600 and gr_price < 700:
            add = 70
            temp_price = cy_temp_price(gr_price, add)
        elif gr_price >= 700 and gr_price < 800:
            add = 80
            temp_price = cy_temp_price(gr_price, add)
        elif gr_price >= 800 and gr_price < 1000:
            add = 80
            temp_price = cy_temp_price(gr_price, add)
        elif gr_price >= 1000 and gr_price < 1300:
            add = 100
            temp_price = cy_temp_price(gr_price, add)
        elif gr_price >= 1300 and gr_price < 1400:
            add = 110
            temp_price = cy_temp_price(gr_price, add)
        elif gr_price >= 1400:
            add = 120
            temp_price = cy_temp_price(gr_price, add)

        price_15 = round(int((gr_price / 1.24) * 1.15) * 1.19, 2)
        price_15_round = round(price_15, -1) - 1
        cy_price = int(round(temp_price, -1) - 1)
        price_diff = round(cy_price - gr_price, 2)
        pyperclip.copy(cy_price)
        if gr_price < 100:
            print("Προσοχή. Πολύ μικρή τιμή ενδεχομένως έχει γίνει λάθος;")
        elif gr_price > 2000:
            print("Τιμή GR λίγο μεγάλη. Ενδεχομένως να χρειαστεί λίγο παραπάνω margin.")
        print("Προτεινόμενη CY: " + str(cy_price))
        print("Διαφορα CY - GR: " + str(price_diff))
        if len(str(add)) > 2:
            print("add " + str(add) + ":         " + str(price_15))
        elif len(str(add)) == 2:
            print("add " + str(add) + ":          " + str(price_15))
        print("* 15%:           " + str(price_15))
        print("* 15% round:     " + str(price_15_round))
        print("")
        answer_text = ""
    except KeyboardInterrupt:
        print("")
        print("Bye bye")
        sys.exit()
    except Exception as exc:
        if str(exc).find("not supported between instances of 'str' and 'int'"):
            answer_text = ""
        else:
            print("Exception: " + str(exc))
