# Program published on https://beginnersbook.com
# Python program to print Calendar using
# Python built-in function

import calendar

# Enter in format - 2018, 1997, 2003 etc.
year = int(input("Enter Year: "))

# Enter in format - 01, 06, 12 etc.
month = int(input("Enter Month: "))

# printing Calendar
print(calendar.month(year, month))