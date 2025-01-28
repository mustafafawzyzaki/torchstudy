import pydicom
import os
import sys
import pyodbc
import logging
from typing import Optional, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DICOMData:
    def __init__(self, dicom_file_path: str):
        self.dicom_file_path = dicom_file_path
        self._dicom_data: Optional[Dict] = None

    @property
    def dicom_data(self) -> Optional[Dict]:
        if self._dicom_data is None:
            self._dicom_data = self._load_dicom_data()
        return self._dicom_data

    def _load_dicom_data(self) -> Optional[Dict]:
        try:
            dicom_dataset = pydicom.dcmread(
                self.dicom_file_path,
                specific_tags=[(0x0010, 0x0020)],  # Load only PatientID tag
                stop_before_pixels=True
            )
            
            patient_id_elem = dicom_dataset.get((0x0010, 0x0020))
            if not patient_id_elem:
                logging.warning("Patient ID tag (0010,0020) not found in DICOM file")
                return None

            patient_id = patient_id_elem.value
            logging.info(f"Extracted Patient ID: {patient_id}")
            return {"patient_id": patient_id}

        except Exception as e:
            logging.error(f"Error reading DICOM file: {str(e)}", exc_info=True)
            return None

    def insert_into_database(
        self,
        server: str,
        database: str,
        username: str,
        password: str,
        connection: Optional[pyodbc.Connection] = None
    ) -> bool:
        data = self.dicom_data
        if not data:
            logging.warning("Skipping database insertion - no valid DICOM data")
            return False

        close_connection = False
        conn = connection

        try:
            if not conn:
                conn_str = (
                    f"DRIVER={{SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password}"
                )
                conn = pyodbc.connect(conn_str, timeout=10)
                close_connection = True

            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO patient (patient_id) VALUES (?)", data['patient_id'])
                conn.commit()

            logging.info("Successfully inserted patient record")
            return True

        except pyodbc.Error as e:
            logging.error(f"Database operation failed: {str(e)}", exc_info=True)
            if conn:
                conn.rollback()
            return False
        finally:
            if close_connection and conn:
                conn.close()

if __name__ == "__main__":
    dicom_file = r"D:\VNA_Test\DICOM_Convert\input_o\1.2.840.113619.2.401.160236239321180.13348.230816111826.1.dcm"
    
    # Example usage with connection reuse for multiple inserts
    try:
        db_conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=127.0.0.1;"
            "DATABASE=PXMAIN;"
            "UID=sa;"
            "PWD=PAXDB@dm1n",
            timeout=10
        )
        
        dicom_handler = DICOMData(dicom_file)
        success = dicom_handler.insert_into_database(
            server="127.0.0.1",
            database="PXMain",
            username="sa",
            password="PAXDB@dm1n",
            connection=db_conn
        )
        
        if success:
            logging.info("Database operation completed successfully")
            
    except Exception as e:
        logging.error(f"Main process failed: {str(e)}", exc_info=True)
    finally:
        if 'db_conn' in locals():
            db_conn.close()