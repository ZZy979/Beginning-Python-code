import fileinput                                   #  1
                                                   #  2
for line in fileinput.input(inplace=True):         #  3
    line = line.rstrip()                           #  4
    num = fileinput.lineno()                       #  5
    print('{:<50} # {:2d}'.format(line, num))      #  6
