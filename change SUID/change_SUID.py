"""
This script changes the Study Instance UID (SUID) of DICOM files in a specified directory.
Modules:
    os: Provides a way of using operating system dependent functionality.
    sys: Provides access to some variables used or maintained by the interpreter.
    pydicom: A pure Python package for working with DICOM files.
    pynetdicom: A Python package for DICOM networking.
Functions:
    change_suid(study_directory, new_suid):
        Changes the Study Instance UID of all DICOM files in the specified directory.
        Parameters:
            study_directory (str): The path to the directory containing the DICOM files.
            new_suid (str): The new Study Instance UID to be set for the DICOM files.
        Returns:
            None
Usage:
    The script prompts the user to enter the path to the study directory and the new Study Instance UID.
    It then updates the Study Instance UID for all DICOM files in the specified directory.
"""

import os 
import sys
import pydicom 
import pynetdicom 

"""
        Change the Study Instance UID (SUID) for all DICOM files in a given directory.

        This function traverses through the specified study directory and its subdirectories,
        identifies DICOM files, and updates their Study Instance UID to the provided new SUID.

        Args:
            study_directory (str): The path to the directory containing the DICOM files.
            new_suid (str): The new Study Instance UID to be assigned to the DICOM files.

        Returns:
            None

        Raises:
            FileNotFoundError: If the specified study directory does not exist.
            pydicom.errors.InvalidDicomError: If a file is not a valid DICOM file.
            Exception: For any other errors encountered during the process.

        Example:
            change_suid('/path/to/study_directory', '1.2.840.113619.2.55.3.604688.1234.5678.91011')
        """

def change_suid(study_directory , new_suid):
    for root , dirs, files in os.walk(study_directory):
        for file in files:
            if file.endswith(".dcm"):
                ds = pydicom.dcmread(os.path.join(root, file), force=True)
                if (0x0020, 0x000D) in ds:
                    old_suid = ds[0x0020, 0x000D].value
                    if ds[0x0020, 0x000D].value != new_suid:
                        ds[0x0020,0x000D].value = new_suid
                        # Ensure only the Study Instance UID is converted to a string
                        ds[0x0020, 0x000D].value = str(ds[0x0020, 0x000D].value)
                        ds.save_as(os.path.join(root, file))
                        print(f"Updated Study Instance UID for {file} from SUID :{old_suid} to SUID: {ds[0x0020,0x000D].value}")

study_directory = input("Enter the path to the study directory: ")
suid = input("Enter the new Study Instance UID: ")
change_suid(study_directory , suid)                 
