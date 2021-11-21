import os
try:
    orders_single = []
    answer = ""
    print("Orders single...")
    while answer != "-":
        code = input("Δώσε: ")
        orders_single.append(code)
    
    print("")
    orders_email = []
    answer = ""
    print("Orders e-mail...")
    while answer != "-":
        code = input("Δώσε: ")
        orders_email.append(code)
    
    for o in orders_email:
        for s in orders_single:
            if o != s:
                print(o)
except KeyboardInterrupt:
    print("Bye")