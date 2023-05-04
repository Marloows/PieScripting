from math import sin

from initialize import initialize

m = 140
l = 1.8
k = 16
g = 9.81
rounded = lambda x: round(x, 6)

@initialize(0, 1, -1, h=.1, rounded2=12)
def swing(x, *y):
   return -k/m*y[1] - g/l*sin(y[0])

