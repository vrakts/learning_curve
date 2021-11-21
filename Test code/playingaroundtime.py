from datetime import datetime
from time import sleep as nani
from random import randint as rand

time_aver = []  # κρατάει τα συνολικά δευτερόλεπτα του κάθε γύρου σε λίστα για να υπολογιστεί ο μέσος όρος (aver)
est_lefts = []  # κρατάει όλες τις εκτιμήσεις ανά γύρο
run_time = 0    # εδώ θα κρατιέται ο συνολικός χρόνος που τρέχει σε δευτερόλεπτα
totals = 20     # πόσους γύρους θα τρέξει
randoms = 3     # τα μέγιστα δευτερόλεπτα που θα μπορεί τυχαία να περιμένει μέχρι τον επόμενο γύρο

# Καθαρά για αισθητικούς σκοπούς, αποθηκεύει την ώρα εκκίνησης και τη διαμορφώνεί:
# 2020-10-09 15:46:21
start = datetime.now()  
startf = start.strftime("%Y-%m-%d %H:%M:%S")

print("Started at: " + startf)
print("")

for i in range (1, totals) :
 # ώρα εκκίνησης του γύρου
 begin_now = datetime.now()
 begin_f = begin_now.strftime("%Y-%m-%d %H:%M:%S")
 # ορισμός του τυχαίου χρόνου αναμονής σε δευτερόλεπτα
 tyx = rand(1, randoms)
 print("Run " + str(i))
 print(begin_f)
 print("Random = " + str(tyx))
 nani(tyx)
 # ώρα συνέχισης μετά την τυχαία αναμονή
 # σε πραγματικό script θα συνεχίζει μετά την εκτέλεση μιας ή περισσοτέρων διαδικασιών
 end_now = datetime.now()
 end_f = end_now.strftime("%Y-%m-%d %H:%M:%S")
 # if len(time_aver) < 10 :
  # time_aver.append(total_seconds)
 # else :
  # time_aver.pop(1)
  # time_aver.append(total_seconds)
 # for item in time_aver :
  # print(item)
 try :
  # διαφορά της εκκίνησης του γύρου μέχρι μετά τις ενέργειες.
  time_dif = end_now - begin_now
  # κρατάμε μόνο τα δευτερόλεπτα
  total_seconds = time_dif.total_seconds()
  # προσθέτουμε τα δευτερόλεπτα στον συνολικό χρόνο
  run_time += total_seconds
  # Υπολογισμός λεπτών, δευτερολέπτων και αναλυτικά (anal) συνολικού χρόνου
  run_mins = int(run_time / 60)   
  run_secs = int(run_time - (run_mins * 60))
  run_anal = str(run_mins).zfill(2) + ":" + str(run_secs).zfill(2)
  # προσθήκη των δευτερολέπτων του γύρου στο time_aver για να υπολογιστεί ο μέσος όρος
  time_aver.append(total_seconds)
  # μέσος όρος μέχρι τώρα
  aver = sum(time_aver) / len(time_aver)
  # υπολογίζει περίπου πόσα δευτερόλεπτα θα διαρκέσει το script βάσει των totals που θα τρέξουν
  estimation_average = int(aver * totals)
  est_average_mins = int(estimation_average / 60)  # λεπτά
  est_average_secs = int(estimation_average - (est_average_mins * 60))  # δευτερόλεπτά
  est_average_anal = str(est_average_mins).zfill(2) + ":" + str(est_average_secs).zfill(2)  # λεπτά δευτερόλεπτα αναλυτικά
  # υπολογίζει περίπου πόσος χρόνος απομένει για το τέλος του script
  estimation_left = int(estimation_average - run_time)
  est_left_mins = int(estimation_left / 60)  # λεπτά
  est_left_secs = int(estimation_left - (est_left_mins * 60))  # δευτερόλεπτά
  est_left_anal = str(est_left_mins).zfill(2) + ":" + str(est_left_secs).zfill(2)  # λεπτά δευτερόλεπτα αναλυτικά
  # προσθήκη του υπολιεπόμενου χρόνου για στατιστικούς λόγους
  est_lefts.append(est_left_anal)
  print("List sum = " + str(sum(time_aver)))
  print("List length = " + str(len(time_aver)))
  print("Average = " + str(aver))
  print("Run time = " + str(run_time) + " seconds (" + run_anal + ")")
  print("###")
  print("Actual average estimation = " + str(estimation_average) + " seconds (" + est_average_anal + ")")
  print("estimation_average - run_time = " + str(estimation_average - run_time))
  print("###")
  if estimation_average - run_time >= 0 :
   print("Estimation = " + str(estimation_left) + " seconds (" + est_left_anal + ")")
  else :
   print("Estimation = Less than 10 seconds.")
  print("")
 except Exception as exc :
  str(exc)
  continue

for i in range(1, len(est_lefts)) :
 print(str(i) + ". " + est_lefts[i])

# total_seconds = 172800
hours = int((run_time / 60) / 60)
minutes = int(run_time / 60) - (hours * 60)
seconds = int(run_time - (int(run_time / 60) * 60))

print(str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2))
