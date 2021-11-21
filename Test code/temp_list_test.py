from random import randint
from time import sleep

def aver_time() :
 global aver
 mylist = [randint(1, 15)]
 for i in range (0, 100) :
  if len(mylist) == 10 :
   mylist = mylist[1:]
  mylist.append(randint(1, 20))
  mylist
  aver = sum(mylist) / len(mylist)
  print("Average: " + str(aver))


# mylist = [randint(1, 15)]

# for i in range (0, 100) :
 # if len(mylist) == 10 :
  # mylist = mylist[1:]
  # mylist.append(randint(1, 15))
  # aver = sum(mylist) / len(mylist)
  # print("Average: " + str(aver))
 # if len(mylist) >= 2 :
  # mylist.append(randint(1, 15))
 # else :
  # aver = mylist[0]
  # print("Average: " + str(aver))
  # mylist.append(randint(1, 15))

# mylist = [randint(1, 15)]
# for i in range (0, 100) :
 # if len(mylist) == 10 :
  # mylist = mylist[1:]
 # mylist.append(randint(1, 20))
 # mylist
 # aver = sum(mylist) / len(mylist)
 # print("Average: " + str(aver))

aver_time()
print("Average: " + str(aver))
