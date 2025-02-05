import os
import shutil
from datetime import datetime
from tqdm import tqdm
import sys
import logging

source_folder = r"C:\PAXERAMED\SendHL7Temp"

if len(sys.argv) > 1:
    source_folder = sys.argv[1]

if not os.path.exists(source_folder):
    print(f"Error: The source folder '{source_folder}' does not exist.")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def organize_files(source_folder):
    try:
        while True : 
            # List all files in the source folder
            logging.info(f"Scanning directory: {source_folder}")
            files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

            for file in tqdm(files, desc="Organizing files into folders", unit="files"):
                file_path = os.path.join(source_folder, file)
                modified_time = os.path.getmtime(file_path)
                modified_date = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d')
                
                # Create a new folder named with the modified date if it doesn't exist
                date_folder = os.path.join(source_folder, modified_date)
                os.makedirs(date_folder, exist_ok=True)
                
                # Move the file to the corresponding date folder
                shutil.move(file_path, os.path.join(date_folder, file))
            print ("The files have been organized successfully for this round.")
                
    except KeyboardInterrupt:
        logging.warning("Process interrupted by user.")
    except Exception as e:
        logging.error(f"Error while organizing files: {e}")
    finally:
        logging.info("The files have been organized successfully.")
        input("Press Enter to continue...")

# Call the function to organize files
organize_files(source_folder)