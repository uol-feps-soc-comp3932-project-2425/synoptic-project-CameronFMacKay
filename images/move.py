import os
import shutil

def collapse_folders_into_one(src_dir, dest_dir):
    # Create destination folder if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    existing_files = [f for f in os.listdir(dest_dir) if f.lower().endswith(".jpg")]
    file_counter = len(existing_files)


    # Walk through the directory
    for root, dirs, files in os.walk(src_dir):
        # Skip the root directory itself to avoid moving files from it
        if root == src_dir:
            continue
        
        # Process each file in the subdirectories
        for file in files:
            # Check if the file is a .jpg file
            if file.lower().endswith(".jpg"):
                # Construct the new file name
                new_file_name = f"{file_counter}.jpg"
                
                # Construct the full source and destination paths
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, new_file_name)

                # Move and rename the file
                shutil.move(src_file, dest_file)
                
                # print(f"Moved: {src_file} -> {dest_file}")
                
                # Increment the file counter
                file_counter += 1
        
        if not os.listdir(root):  # Check if the directory is empty
            os.rmdir(root)
            print(f"Removed empty directory: {root}")

    print("All files have been moved and renamed.")

# Example usage
src_directory =  "/vol/scratch/SoC/misc/2024/sc21cm/train_256_places365standard/data_256/c/camping_and_picnic"
dest_directory = src_directory  # Replace with the path to your destination directory

collapse_folders_into_one(src_directory, dest_directory)
