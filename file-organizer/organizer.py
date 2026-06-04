import os
import shutil
import argparse

# Dictionary mapping folder names to their associated file extensions
FILE_CATEGORIES = {
    'Images': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx', '.xls', '.xlsx', '.csv'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac'],
    'Video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
    'Executables': ['.exe', '.dmg', '.pkg', '.deb']
}

def organize_files(target_dir):
    """
    Organizes files in the target directory into subfolders based on their file extensions.
    """
    if not os.path.exists(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.")
        return

    # Keep track of how many files we moved
    moved_count = 0

    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)

        # Skip directories, we only organize files
        if os.path.isdir(item_path):
            continue

        # Get the file extension (e.g., '.jpg') in lowercase
        _, file_extension = os.path.splitext(item)
        file_extension = file_extension.lower()

        # Find the category for this extension
        destination_folder = 'Others' # Default folder for unknown extensions
        for folder, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                destination_folder = folder
                break
        
        # If the file has no extension or it's a hidden file (starts with .), skip it or put in Others
        if not file_extension and not item.startswith('.'):
            destination_folder = 'Others'
        elif item.startswith('.'):
            # Skip hidden files
            continue

        # Create the destination folder if it doesn't exist
        dest_dir_path = os.path.join(target_dir, destination_folder)
        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path)

        # Move the file
        dest_file_path = os.path.join(dest_dir_path, item)
        
        # Handle filename collisions (if a file with the same name already exists)
        if os.path.exists(dest_file_path):
            base, ext = os.path.splitext(item)
            counter = 1
            while os.path.exists(dest_file_path):
                new_name = f"{base}_{counter}{ext}"
                dest_file_path = os.path.join(dest_dir_path, new_name)
                counter += 1

        try:
            shutil.move(item_path, dest_file_path)
            print(f"Moved: {item} -> {destination_folder}/")
            moved_count += 1
        except Exception as e:
            print(f"Error moving {item}: {e}")

    print(f"\nOrganization complete! Successfully moved {moved_count} file(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory by their extensions.")
    parser.add_argument(
        "directory", 
        nargs="?", 
        default=".", 
        help="The directory to organize (defaults to the current directory)"
    )
    args = parser.parse_args()

    organize_files(args.directory)
