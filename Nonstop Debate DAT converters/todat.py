from struct import *
import sys
import os

def ConvertFile(file):
    f = open("txt files to convert\\" + file, "r")
    file = file[:-4] #remove .txt from file variable
    w = open(file + ".dat", "wb")

    for line in f:
        n = ""
        passed_bar = False
        for char in line:
            if passed_bar == True and (char.isdigit() == True or char is "-"):
                n += char
            if char is "|":
                passed_bar = True
            
        if n.lstrip('-').isdigit() == True:
            n = int(n)#%65536
            m = pack('<h', n)
            o = unpack('<h', m)
            w.write(m)

#main
for filename in os.listdir("txt files to convert"):
    if filename.endswith(".txt"):
        ConvertFile(filename)
    print("Converted " + filename)
