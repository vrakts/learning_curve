def timecalc() :
 try :
  time_dif = now2 - now
  total_seconds = time_dif.total_seconds()
  run_time += total_seconds
  run_mins = int(run_time / 60)
  run_secs = int(run_time - (run_mins * 60))
  run_anal = str(run_mins).zfill(2) + ":" + str(run_secs).zfill(2)
  time_aver.append(total_seconds)
  aver = sum(time_aver) / len(time_aver)
  estimation_average = int(aver * totals)
  est_average_mins = int(estimation_average / 60)
  est_average_secs = int(estimation_average - (est_average_mins * 60))
  est_average_anal = str(est_average_mins).zfill(2) + ":" + str(est_average_secs).zfill(2)
  estimation_left = int(estimation_average - run_time)
  est_left_mins = int(estimation_left / 60)
  est_left_secs = int(estimation_left - (est_left_mins * 60))
  est_left_anal = str(est_left_mins).zfill(2) + ":" + str(est_left_secs).zfill(2)
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
