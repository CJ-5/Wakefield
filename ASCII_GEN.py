import sys

i = 0
sys.stdout = open('ASCII_LIST.txt', 'w')
while i <= 20000:
    try:
        char = chr(i)
        if not str.isspace(char) or char == "퟽":
            print(f"{chr(i)} : {i}")
    except:
        pass
while True:
    continue
