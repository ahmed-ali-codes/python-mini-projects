import os
import shutil

downloads = "/Users/apple/Downloads"
subfolders = ["Images", "Documents", "Executables", "Archives", "Video", "Others"]

moved_back = 0
for folder in subfolders:
    folder_path = os.path.join(downloads, folder)
    if not os.path.exists(folder_path):
        continue
    for filename in os.listdir(folder_path):
        src = os.path.join(folder_path, filename)
        dst = os.path.join(downloads, filename)
        if os.path.exists(dst):
            print(f"Skipped (conflict): {filename}")
            continue
        shutil.move(src, dst)
        print(f"Restored: {filename}")
        moved_back += 1

print(f"\nDone! Restored {moved_back} file(s).")
