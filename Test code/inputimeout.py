from inputimeout import inputimeout, TimeoutOccurred

try:
 c = inputimeout(prompt='hello\n', timeout=3)
except TimeoutOccurred:
 c = 'timeout'
print(c)