import pydicom 
import os 
import sys 
import pyodbc  # Ensure pyodbc is imported
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DICOMData:
    def __init__(self, dicom_file_path):
        self.dicom_file_path = dicom_file_path
        self.dicom_data = self.get_dicom_data()  # Read DICOM data once during initialization
    
    def get_dicom_data(self):
        try:
            dicom_data = pydicom.dcmread(self.dicom_file_path)
            data = {
                "patient_id": dicom_data.get((0x0010, 0x0020), None).value
            }
            for key, value in data.items():
                logging.info(f"{key} : {value}")
            return data
        except Exception as e:
            logging.error(f"Error reading DICOM file: {e}")
            return None

    def insert_in_study(self, sql_ip, sql_db_name, sql_un, sql_pw):
        if not self.dicom_data:
            logging.warning("No DICOM data to insert.")
            return
        
        connection = None
        try:
            connection = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={sql_ip};DATABASE={sql_db_name};UID={sql_un};PWD={sql_pw}")
            cursor = connection.cursor()
            query = "INSERT INTO patient (patient_id) VALUES (?)"
            cursor.execute(query, (self.dicom_data['patient_id'],))
            connection.commit()
        except pyodbc.Error as e:
            logging.error(f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

dicom_file_path = r"D:\VNA_Test\DICOM_Convert\input_o\1.2.840.113619.2.401.160236239321180.13348.230816111826.1.dcm"
dicom = DICOMData(dicom_file_path)
dicom.insert_in_study("192.168.1.249", "PXMain_BI", "sa", "PAXDB@dm1n")