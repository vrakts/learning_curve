import sys
import threading
import time
from collections import deque

import psutil


def calc_ul_dl(rate, dt=0.5, interface="Wi-Fi"):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True)[interface]
    tot = (counter.bytes_sent, counter.bytes_recv)

    while True:
        last_tot = tot
        time.sleep(dt)
        counter = psutil.net_io_counters(pernic=True)[interface]
        t1 = time.time()
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [
            (now - last) / (t1 - t0) / 1000.0
            for now, last in zip(tot, last_tot)
        ]
        rate.append((ul, dl))
        t0 = time.time()


def print_rate(rate):
    try:
        print_out = ("UL: {0:.0f} kB/s / DL: {1:.0f} kB/s".format(*rate[-1]))
        print(" " * 100, end = "\r")
        print("UL: {0:.0f} kB/s / DL: {1:.0f} kB/s".format(*rate[-1]), end = "\r")
    except IndexError:
        "UL: - kB/s/ DL: - kB/s"


try:
    # Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
    transfer_rate = deque(maxlen=1)
    t = threading.Thread(target=calc_ul_dl, args=(transfer_rate,))

    # The program will exit if there are only daemonic threads left.
    t.daemon = True
    t.start()

    # The rest of your program, emulated by me using a while True loop
    while True:
        print_rate(transfer_rate)
        time.sleep(0.5)
except KeyboardInterrupt:
    sys.exit(0)
except Exception as exc:
    print(str(exc))
    sys.exit(1)