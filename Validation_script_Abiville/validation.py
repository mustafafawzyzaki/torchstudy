import pyodbc 
import os 
import sys 
from tqdm import tqdm

class validation():
    def __init__(self, db_info):
        super().__init__()
        self.sqlserver_ip = db_info[0]
        self.sqlserver_port = db_info[1]
        self.sqlserver_user = db_info[2]
        self.sqlserver_password = db_info[3]
        
    def retreive_study_data(self , db_name ):
        query = 'exec migration_sp_retrieve_study_data'
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.sqlserver_ip+';DATABASE='+db_name+';UID='+self.sqlserver_user+';PWD='+ self.sqlserver_password)
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
        conn.close()
    
    def retreive_file_data(self , db_data):
        data_list = []
        for row in tqdm(db_data , desc = 'Retreiving study info' , unit=' rows'):
            patient_id = row[0] 
            accession_number = row[1] 
            study_uid  = row[2] 
            study_folder_path = row[3] 
            study_folder_path_list = study_folder_path.split('\\')
            patient_folder = study_folder_path_list[-2]
            study_folder = study_folder_path_list[-1]
            root_path = study_folder_path.replace(study_folder, '').replace(patient_folder, '').replace('\\\\', '\\')
            try : 
                if not os.path.exists(study_folder_path):
                    continue
                if os.path.exists(study_folder_path):
                    for root, dirs, files in tqdm(os.walk(study_folder_path) , desc='Retreive study files' , unit=' files'):
                        for dir in dirs:
                            if dir.startswith('M') or dir.startswith('R'):
                                series_folder = dir
                                series_folder_path = os.path.join(root, series_folder)
                                if os.path.exists(series_folder_path):
                                    for file in os.listdir(series_folder_path):
                                        file_name = file
                                        # print(patient_id, accession_number, study_uid, patient_folder, study_folder, root_path, study_folder_path, series_folder, file_name)
                                        data_list.append([patient_id, accession_number, study_uid,study_folder_path ,  root_path , patient_folder, study_folder, series_folder, file_name])
            except Exception as e:
                print(e)
                continue
        return data_list

    def write_to_sql(self, dbname , tablename , db_data):
        data = self.retreive_file_data(db_data)
        for row in data:
            query = f"exec migration_sp_insert_study_data @tablename='{tablename}', @patient_id = '{row[0]}', @accession_number = '{row[1]}', @study_uid = '{row[2]}', @study_folder_path = '{row[3]}', @root_path = '{row[4]}', @patient_folder = '{row[5]}', @study_folder = '{row[6]}', @series_folder = '{row[7]}', @file_name = '{row[8]}'"
            # print (query)
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.sqlserver_ip+';DATABASE='+dbname+';UID='+self.sqlserver_user+';PWD='+ self.sqlserver_password)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            
sqlserver_ip = '192.168.1.249'
sqlserver_port = 1433
sqlserver_user = 'sa'
sqlserver_password = 'PAXDB@dm1n'

db_info = [sqlserver_ip, sqlserver_port, sqlserver_user, sqlserver_password]

valid_obj = validation(db_info)
data = valid_obj.retreive_study_data('PXMAIN')
valid_obj.write_to_sql('PXMAIN', 'study_data', data)





            
