import pyperclip
import sys

while True:
    try:
        items = int(input("Δώσε ποσότητα: "))
        price = float(input("Δώσε τιμή:     "))
        result = str(round(items * (price / 1.19), 2)).replace(".", ",")
        pyperclip.copy(result)
        print(result)
        print("")
    except KeyboardInterrupt:
        print("Bye...")
        sys.exit()
    except Exception as exc:
        print("Μάλλον δεν έδωσες αριθμό...")
        print("")