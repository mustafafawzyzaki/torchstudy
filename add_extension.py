import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def process_batch(batch, target_ext, pbar):
    """
    Processes a batch of files, renaming them to have the target extension.

    Args:
        batch (list): List of file paths to process.
        target_ext (str): The target file extension to add.
        pbar (tqdm): Progress bar to update with the number of processed files.

    Returns:
        int: Number of files successfully processed.
    """
    processed = 0
    for file_path in batch:
        try:
            current_ext = os.path.splitext(file_path)[1]
            if current_ext != target_ext:
                new_path = f"{file_path}{target_ext}"
                os.rename(file_path, new_path)
                processed += 1
        except Exception as e:
            pass  # Error logging would go here
    pbar.update(processed)
    return processed

def main():
    """
    Main function to execute the batch processing of files in a folder.
    Prompts the user for folder path and target extension, then processes
    the files in batches using multiple threads.
    """
    folder_path = input('Enter the folder path: ').strip().replace('"', '')
    extension = input('Enter the extension: ').strip().lstrip('.')
    target_ext = f".{extension}"
    
    batch_size = 5000  # Optimized for modern NVMe drives
    workers = 32       # Optimal for high-IOPs storage
    
    file_generator = (os.path.join(root, f)
                     for root, _, files in os.walk(folder_path)
                     for f in files)
    
    with tqdm(unit="files", desc="Processing") as pbar:
        batches = []
        batch = []
        for file_path in file_generator:
            batch.append(file_path)
            if len(batch) >= batch_size:
                batches.append(batch)
                batch = []
        if batch:
            batches.append(batch)
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(process_batch, b, target_ext, pbar) for b in batches]
            for future in as_completed(futures):
                future.result()

if __name__ == "__main__":
    main()