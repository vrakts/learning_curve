# not working
from datetime import date
from datetime import datetime  # for the ability to easily measure both date and time.
import time  # for the ability to measure time
from random import random
from random import randint

######################
# OLD METHOD WORKING #
######################

# start_time = time.time()  # set starting time
# today = date.today()  # set starting date
# start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy

# elapsed_time = time.time() - start_time
# minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
# mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
# seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
# seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
# formatted_time = str(mins) + "." + str(seconds)
# print("Script executed in: " + str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")

##############
# NEW METHOD #
##############

# now = datetime.now()
# start_time = now.strftime("%H:%M:%S")
# start_date = now.strftime("%d-%m-%y")
# start_hour = now.strftime("%H")
# start_minutes = now.strftime("%M")
# start_seconds = now.strftime("%S")
# stime = start_hour + ":" + start_minutes + ":" + start_seconds
# stime
# print("Script started at " + start_date + ", " + start_time)

# time.sleep(randint(25, 40))

# end_time = now.strftime("%H:%M:%S")
# end_hour = now.strftime("%H")
# end_minutes = now.strftime("%M")
# end_seconds = now.strftime("%S")

start_hour = "12"
start_minutes = "10"
start_seconds = "10"
start_time = start_hour + ":" + start_minutes + ":" + start_seconds
start_time

end_hour = "13"
end_minutes = "09"
end_seconds = "09"
end_time = end_hour + ":" + end_minutes + ":" + end_seconds 

fin_hour = int(end_hour) - int(start_hour)
if int(end_hour) == 1 and int(end_minutes) <= int(start_minutes) :
 if int(end_minutes) >= int(start_minutes) :
 fin_minutes = int(end_minutes) - int(start_minutes)
else:
 fin_minutes = (60 - int(start_minutes)) + int(end_minutes)

if int(end_minutes) >= int(start_minutes) :
 fin_minutes = int(end_minutes) - int(start_minutes)
else:
 fin_minutes = (60 - int(start_minutes)) + int(end_minutes)

if int(end_seconds) >= int(start_seconds) :
 fin_seconds = int(end_seconds) - int(start_seconds)
else:
 fin_seconds = (60 - int(start_seconds)) + int(end_seconds)

fin_time = str(fin_hour) + ":" + str(fin_minutes) + ":" + str(fin_seconds)
fin_time
