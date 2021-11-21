# arguments test

import sys  # for exit purposes in case of error

if len(sys.argv) > 1 :
 print(len(sys.argv))
 for i in range(1, len(sys.argv)) :
  print(str(sys.argv[i]))