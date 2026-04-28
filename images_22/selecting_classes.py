import numpy as np
import pandas as pd
import os
import shutil

# Load metadata
metadata = pd.read_csv('images_22/EU_LUCAS_2022.csv')

# Get image IDs from filenames
folder = r"./crop_images_22"
filenames = os.listdir(folder)

ids = np.fromiter(
    (int(name[4:12]) for name in filenames),
    dtype=np.int64
)

# Filter dataframe for filenames
filtered_metadata = metadata[metadata['POINT_ID'].isin(ids)]

# Filter dataframe for crop classes
crop_classes = ["B11", "B12", "B13", "B14", "B15", "B16", "B21", "B22", "B31", "B32", "B33", "B55"]
selected_metadata = filtered_metadata[filtered_metadata['SURVEY_LC1'].isin(crop_classes)].copy()

# Add column with full filepath for each image
selected_metadata['FILEPATH'] = (
    folder
    + r'/2022'
    + selected_metadata['POINT_ID'].astype(str)
    + r'LCLU_CropLC1.jpg'
)

# Save all selected images metadata
selected_metadata.to_csv('images_22/all_crop_images.csv', index=False)

# Define output folder for all sorted images
output_folder = r'./crop_images_22_sorted'

# Function to create class folders, which will contain the images
def create_class_folders(base_path, classes):
    for cls in classes:
        cls_path = os.path.join(base_path, cls)
        os.makedirs(cls_path, exist_ok=True)

# Function to copy images into the folders
def copy_images(df, dest_folder):
    for _, row in df.iterrows():
        class_folder = os.path.join(dest_folder, row['SURVEY_LC1'])
        src_path = row['FILEPATH']
        if os.path.exists(src_path):
            shutil.copy(src_path, class_folder)
        else:
            print(f"Warning: File not found: {src_path}")

# Create folders and copy all selected images
create_class_folders(output_folder, crop_classes)
print("Copy all images...")
copy_images(selected_metadata, output_folder)
print("Done. All images were copied into class folders.")

# Print summary of images per class
print("\nSummary of images per class:")
for cls in crop_classes:
    class_folder = os.path.join(output_folder, cls)
    if os.path.exists(class_folder):
        num_images = len([f for f in os.listdir(class_folder) if os.path.isfile(os.path.join(class_folder, f))])
        print(f"Class {cls}: {num_images} images")
    else:
        print(f"Class {cls}: 0 images")
