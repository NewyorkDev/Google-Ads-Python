import re

txt = "The rain in Spain"
x = re.search("in", txt)

if x != None:
    print("It has a match")
else:
    print("No Match")
print(x)
