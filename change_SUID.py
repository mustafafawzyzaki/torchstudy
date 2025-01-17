import os 
import sys
import pydicom 
import pynetdicom 


study_directory  = input("Enter the directory where the study is located: ")

for root , dirs, files in os.walk(study_directory):
    for file in files:
        if file.endswith(".dcm"):
            ds = pydicom.dcmread(os.path.join(root, file))
            print (ds[0x0020,0x000D])
            if ds[0x0020,0x000D].value != None:
                ds[0x0020,0x000D].value = "1.3.6.1.4.1.5962.1.2.0.1175775772.5717.0"
                ds.save_as(os.path.join(root, file))
                print (ds[0x0020,0x000D])