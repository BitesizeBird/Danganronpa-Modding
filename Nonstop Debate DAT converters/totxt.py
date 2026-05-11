from struct import *
import sys
import os

def ConvertFile(file):
    #define arrays
    functions = ["TextID", "Type", "Slashes", "Shoot With Evidence", "Shoot With Argue Point", "Advance When Slashed", "Has Weak Point", "Advance", "0x08", "Entry Effect", "Exit Effect", "Fade Out", "Horizontal", "Vertical", "Angle Acceleration", "Angle", "Scale", "Final Scale", "Text Shake", "Rotation", "Rotation Speed", "Character", "Sprite", "Camera", "Portrait Shake", "Voice", "Time Bonus", "Chapter", "Vertical Characters", "Nonstop Sprite Position"]
    dr2_functions = ["Music", "Slashed Text Mood Effect", "Missed Text Mood Effect", "0x21"]
    rebuttal_functions = ["Loop Length", "Starting Favour", "Favour To Advance", "Sharpness Gentle", "Sharpness Kind", "Sharpness Mean", "Cross Sword Frames", "Cross Sword Clicks", "Always Cross Swords"]
    list_of_values = []

    #open file
    f = open("dat files to convert\\" + file, "rb")
    file = file[:-4] #remove .dat from file variable
    w = open(file + ".txt", "w")
    w.write(file)

    #unpack data from .dat file to list so it's easier to work with
    while(1):
        try:
            value = str(unpack('<h', f.read(2)))
            value = value[1:-2]
            list_of_values.append(value)
            
        except:
            break
           
    #write first two header values
    for i in range(2):
        w.write("\nHeader|" + list_of_values.pop(0))
        
    #check if file belongs to dr2 and extend list of functions if so
    
    
    #rename functions for clarity
    if "hanron" in file:
        functions.extend(dr2_functions)
        functions[4] = "Player Next Section ID"
        functions[23] = "Camera Left Half"
        functions[24] = "Camera Right Half"
        
    elif not len(list_of_values) % 30 == 0:
        functions.extend(dr2_functions)
        
    #TEMP FIX
    else:
        functions.extend(dr2_functions)
        
    #loop through data and loop through functions to write to file
    i = 0
    while (len(list_of_values) >= len(functions)):
        w.write("\n\n[Section " + str(i) + "]")
        i += 1
        for function in functions:
            #write to file: function|value 
             w.write("\n" + function + "|" + list_of_values.pop(0))

    #loop through remaining data for rebuttal showdown loop sections
    i = 0
    while (len(list_of_values) >= len(rebuttal_functions)):
        w.write("\n\n[Loop Section " + str(i) + "]")
        i += 1
        for function in rebuttal_functions:
            #write to file: function|value 
             w.write("\n" + function + "|" + list_of_values.pop(0))

#main
for filename in os.listdir("dat files to convert"):
    if filename.endswith(".dat"):
        ConvertFile(filename)
    print("Converted " + filename)
