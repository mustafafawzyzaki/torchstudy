import os 
import sys
import pydicom 
import pynetdicom 

#hello world
# My Name is Mustafa

def change_suid(study_directory , new_suid):
    for root , dirs, files in os.walk(study_directory):
        for file in files:
            if file.endswith(".dcm"):
                ds = pydicom.dcmread(os.path.join(root, file), force=True)
                if (0x0020, 0x000D) in ds:
                    if ds[0x0020, 0x000D].value != new_suid:
                        print(f"Study Instance UID for {file} is not {new_suid}. Updating...")
                        print(ds[0x0020, 0x000D])
                        ds[0x0020,0x000D].value = new_suid
                        # Ensure only the Study Instance UID is converted to a string
                        ds[0x0020, 0x000D].value = str(ds[0x0020, 0x000D].value)
                        ds.save_as(os.path.join(root, file))
                        print(f"Updated Study Instance UID for {file}: {ds[0x0020,0x000D].value}")

study_directory = r"D:\VNA_Test\DICOM_Convert"  
suid = "1.3.6.1.4.1.5962.1.2.0.1175775772.5716.0"  
change_suid(study_directory , suid)                 
