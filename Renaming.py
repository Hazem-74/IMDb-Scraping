import os
import shutil

def rename_and_move_images(root_folder, new_folder):
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    subfolders = sorted([f.path for f in os.scandir(root_folder) if f.is_dir()])

    image_index = 1100

    for subfolder in subfolders:
        images = sorted([f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))])

        for img in images:
            # Get file extension
            file_extension = os.path.splitext(img)[1]
            # Define new file name
            new_name = f"{image_index}{file_extension}"
            # Source and destination paths
            source = os.path.join(subfolder, img)
            destination = os.path.join(new_folder, new_name)
            # Rename and move the image
            shutil.copy2(source, destination)
            print(f"Moved: {source} to {destination}")
            image_index += 1


# Usage
root_folder = 'New folder'
new_folder = 'newfolder2'

rename_and_move_images(root_folder, new_folder)