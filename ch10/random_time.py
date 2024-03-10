from random import *
from time import *

date1 = (2016, 1, 1, 0, 0, 0, -1, -1, -1)
time1 = mktime(date1)
date2 = (2017, 1, 1, 0, 0, 0, -1, -1, -1)
time2 = mktime(date2)

random_time = uniform(time1, time2)
print(asctime(localtime(random_time)))
