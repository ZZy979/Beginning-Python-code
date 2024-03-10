import fileinput
import random

fortunes = list(fileinput.input())
print(random.choice(fortunes), end='')
