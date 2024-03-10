import fileinput
import re

pat = re.compile('From: (.*) <.*?>$')
for line in fileinput.input():
    if m := pat.match(line):
        print(m.group(1))
