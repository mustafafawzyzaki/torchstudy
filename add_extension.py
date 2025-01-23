import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def process_batch(batch, target_ext, pbar):
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
    folder_path = input('Enter the folder path: ').strip().replace('"', '')
    extension = input('Enter the extension: ').strip().lstrip('.')
    target_ext = f".{extension}"
    
    batch_size = 5000  # Optimized for modern NVMe drives
    workers = 32       # Optimal for high-IOPs storage
    
    file_generator = (os.path.join(root, f)
                     for root, _, files in os.walk(folder_path)
                     for f in files)
    
    with tqdm(unit="files", desc="Processing") as pbar:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            batch = []
            for file_path in file_generator:
                batch.append(file_path)
                if len(batch) >= batch_size:
                    executor.submit(process_batch, batch, target_ext, pbar)
                    batch = []
            if batch:  # Process remaining files
                executor.submit(process_batch, batch, target_ext, pbar)

if __name__ == '__main__':
    main()