import pydicom

def extract_dicom_data(dicom_file_path):
    # Load the DICOM file
    dicom_data = pydicom.dcmread(dicom_file_path)
    
    # Extract the required data elements
    data = {
        "StudyInstanceUID": dicom_data.get((0x0020, 0x000D)).value if dicom_data.get((0x0020, 0x000D)) else None,
        "AccessionNumber": dicom_data.get((0x0008, 0x0050)).value if dicom_data.get((0x0008, 0x0050)) else None,
        "PatientName": dicom_data.get((0x0010, 0x0010)).value if dicom_data.get((0x0010, 0x0010)) else None,
        "PatientID": dicom_data.get((0x0010, 0x0020)).value if dicom_data.get((0x0010, 0x0020)) else None,
        "PatientSex": dicom_data.get((0x0010, 0x0040)).value if dicom_data.get((0x0010, 0x0040)) else None,
        "PatientDateBirth": dicom_data.get((0x0010, 0x0030)).value if dicom_data.get((0x0010, 0x0030)) else None,
        "OtherPatientIDs": dicom_data.get((0x0010, 0x1000)).value if dicom_data.get((0x0010, 0x1000)) else None,
        "PatientAge": dicom_data.get((0x0010, 0x1010)).value if dicom_data.get((0x0010, 0x1010)) else None,
        "PatientWeight": dicom_data.get((0x0010, 0x1030)).value if dicom_data.get((0x0010, 0x1030)) else None,
        "StudyID": dicom_data.get((0x0020, 0x0010)).value if dicom_data.get((0x0020, 0x0010)) else None,
        "StudyDate": dicom_data.get((0x0008, 0x0020)).value if dicom_data.get((0x0008, 0x0020)) else None,
        "InstitutionName": dicom_data.get((0x0008, 0x0080)).value if dicom_data.get((0x0008, 0x0080)) else None,
        "DeviceSerialNumber": dicom_data.get((0x0018, 0x1000)).value if dicom_data.get((0x0018, 0x1000)) else None,
        "DeviceName": dicom_data.get((0x0018, 0x1001)).value if dicom_data.get((0x0018, 0x1001)) else None,
        "ReferencedSeriesSequence": dicom_data.get((0x0008, 0x1115)).value if dicom_data.get((0x0008, 0x1115)) else None,
        "SeriesInstanceUID": dicom_data.get((0x0020, 0x000E)).value if dicom_data.get((0x0020, 0x000E)) else None,
        "SeriesDescription": dicom_data.get((0x0008, 0x103E)).value if dicom_data.get((0x0008, 0x103E)) else None,
        "Modality": dicom_data.get((0x0008, 0x0060)).value if dicom_data.get((0x0008, 0x0060)) else None,
        "RetrieveAETitle": dicom_data.get((0x0008, 0x0054)).value if dicom_data.get((0x0008, 0x0054)) else None,
        "RetrieveLocationUID": dicom_data.get((0x0008, 0x0058)).value if dicom_data.get((0x0008, 0x0058)) else None,
        "ReferencedSOPSequence": dicom_data.get((0x0008, 0x1199)).value if dicom_data.get((0x0008, 0x1199)) else None,
        "IconImageSequence": dicom_data.get((0x0088, 0x0200)).value if dicom_data.get((0x0088, 0x0200)) else None,
        "ReferencedSOPClassUID": dicom_data.get((0x0008, 0x1150)).value if dicom_data.get((0x0008, 0x1150)) else None,
        "ReferencedSOPInstanceUID": dicom_data.get((0x0008, 0x1155)).value if dicom_data.get((0x0008, 0x1155)) else None,
        "InstanceNumber": dicom_data.get((0x0020, 0x0013)).value if dicom_data.get((0x0020, 0x0013)) else None,
        "SopInstanceUID": dicom_data.get((0x0008, 0x0018)).value if dicom_data.get((0x0008, 0x0018)) else None
    }
    
    # Convert data elements to string if they are not None
    for key, value in data.items():
        if value is not None:
            data[key] = str(value)
    
    return data

# Example usage
dicom_file_path = r"D:\VNA_Test\DICOM_Convert\input_o\1.2.840.4892943.343.20210517123357131.74.588.1.dcm"
dicom_data = extract_dicom_data(dicom_file_path)
for key, value in dicom_data.items():
    print(f"{key}: {value}")