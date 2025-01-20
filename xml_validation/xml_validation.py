import os
import pyodbc
import csv
import sys 


def get_connection(sql_ip, db_name, sql_un, sql_pw):
    """Establish a connection to the SQL Server."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};SERVER={sql_ip};DATABASE={db_name};UID={sql_un};PWD={sql_pw}"
        )
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def get_studies_data(conn):
    """Fetch study data from the database."""
    try:
        cursor = conn.cursor()
        query = """
        SELECT study_inc_id, accessionno_det_str, study_UID, study_directory
        FROM studies where study_directory is not null
        """
        cursor.execute(query)
        return cursor.fetchall()
    except pyodbc.Error as e:
        print(f"Error fetching data: {e}")
        return []


def write_csv(csv_file, data):
    """Write data to a CSV file."""
    try:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except IOError as e:
        print(f"Error writing to CSV file: {e}")


def count_xml_files(directory):
    """Count XML files in a directory, excluding 'DoseInfo.xml'."""
    xml_count = 0
    try:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.endswith('.xml') and 'DoseInfo.xml' not in file:
                    xml_count += 1
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
    return xml_count


# Configuration
csv_file = 'studies_data.csv'
header = ['StudyIncID', 'Accession', 'StudyUID', 'StudyDirectory', 'XMLCount']
sql_ip = input("Enter the SQL Server IP: ")
sql_un = input("Enter the SQL Server username: ")
sql_pw = input("Enter the SQL Server password: ")
csv_folder_path = input("Enter the path to the folder where you want to save the CSV file: ").replace('"', '')
csv_file = os.path.join(csv_folder_path, 'xml_validation.')

# Main logic
if __name__ == "__main__":
    sql_connection = get_connection(sql_ip, 'pxmain', sql_un, sql_pw)
    if sql_connection:
        # Remove the existing CSV file if it exists
        if os.path.exists(csv_file):
            os.remove(csv_file)

        # Write the header to the CSV file
        write_csv(csv_file, [header])

        # Fetch data and process each study
        studies = get_studies_data(sql_connection)
        for row in studies:
            study_inc_id = row[0]
            accession = row[1]
            study_UID = row[2]
            study_directory = row[3]
            xml_count = count_xml_files(study_directory)

            # Log and save the data
            print(
                f"Study ID: {study_inc_id}, Accession: {accession}, "
                f"Study UID: {study_UID}, XML Count: {xml_count}"
            )
            study_data = [study_inc_id, accession, study_UID, study_directory, xml_count]
            write_csv(csv_file, [study_data])

        sql_connection.close()
