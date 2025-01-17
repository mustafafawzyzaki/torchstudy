import os 
import sys
import pydicom 
import pynetdicom 


study_directory  = input("Enter the directory where the study is located: ")

for root , dirs, files in os.walk(study_directory):
    for file in files:
        if file.endswith(".dcm"):
            ds = pydicom.dcmread(os.path.join(root, file))
            print (ds)