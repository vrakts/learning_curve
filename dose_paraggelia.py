import pyperclip
import sys

while True:
    try:
        order = input("Δώσε παραγγελιά: ")
        result = order.replace("-", "").replace("_", "").replace(" ", "").strip()
        pyperclip.copy(result)
        print(result)
        print("")
    except KeyboardInterrupt:
        print("Bye...")
        sys.exit()
    except Exception as exc:
        print("Πάμε πάλι...")
        print("")