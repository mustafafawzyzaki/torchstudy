import os
import shutil
from datetime import datetime
import sys
from tqdm import tqdm
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

def chunker(seq, size):
    """
    Yield successive chunks of size `size` from list `seq`.
    """
    for pos in range(0, len(seq), size):
        yield seq[pos:pos + size]

def main():
    # Command-line argument: HL7Temp folder path
    hl7temp_path = r"C:\PAXERAMED\SendHL7Temp"

    if len(sys.argv) > 1:
        hl7temp_path = sys.argv[1]
        
    if not(os.path.exists(hl7temp_path)) : 
        print(f"Error: {hl7temp_path} does not exist.")
        sys.exit(1)

    # You can tune these based on your system
    MAX_WORKERS = 32     # Number of threads for concurrency
    CHUNK_SIZE = 1000 # Number of files per chunk
    
    print(f"Scanning directory: {hl7temp_path}")
    
    # -------------------------------------------------------------------------
    # 1) EFFICIENTLY SCAN FILES USING os.scandir
    #    Group them by their modification date
    # -------------------------------------------------------------------------
    files_by_date = defaultdict(list)
    
    with os.scandir(hl7temp_path) as it:
        for entry in it:
            # Only process files, skip subdirectories
            if not entry.is_file():
                continue
            
            file_stat = entry.stat()
            modified_time = file_stat.st_mtime
            modified_date = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d')
            files_by_date[modified_date].append(entry.name)
    
    # -------------------------------------------------------------------------
    # 2) CREATE FOLDERS FOR EACH DATE (SINGLE PASS)
    # -------------------------------------------------------------------------
    for date_folder in files_by_date:
        date_folder_path = os.path.join(hl7temp_path, date_folder)
        os.makedirs(date_folder_path, exist_ok=True)
    
    # -------------------------------------------------------------------------
    # 3) MOVE FUNCTION (RUN IN THREADS)
    # -------------------------------------------------------------------------
    def move_file(args):
        """Move a single file to its date-folder."""
        file_name, date_folder = args
        src_path = os.path.join(hl7temp_path, file_name)
        dst_path = os.path.join(hl7temp_path, date_folder, file_name)
        shutil.move(src_path, dst_path)
    
    # -------------------------------------------------------------------------
    # 4) BUILD ALL TASKS, THEN PROCESS IN CHUNKS
    #    Each task is a tuple: (file_name, date_folder)
    # -------------------------------------------------------------------------
    tasks = []
    for date_folder, file_list in files_by_date.items():
        for file_name in file_list:
            tasks.append((file_name, date_folder))
    
    total_files = len(tasks)
    print(f"Preparing to organize {total_files:,} files...")
    
    # We use a manual TQDM progress bar to track overall progress.
    progress_bar = tqdm(total=total_files, desc="Organizing files", unit="file")
    
    # Process each chunk in a new ThreadPoolExecutor or reuse the same one (either approach can work).
    # Here, we create a new executor per chunk to avoid potential issues with very long-living pools.
    # Alternatively, you can create one executor outside the loop and map over each chunk successively.
    for chunk in chunker(tasks, CHUNK_SIZE):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # For each file successfully moved in the chunk, update the progress bar
            for _ in executor.map(move_file, chunk):
                progress_bar.update(1)
    
    progress_bar.close()
    print("All files have been organized by modified date.")

if __name__ == "__main__":
    main()
