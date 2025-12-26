import os
import shutil
import pandas as pd


# Path to the CSV files containing balanced train and test image paths
train_csv = 'images_22/train_crop_images.csv'
test_csv = 'images_22/test_crop_images.csv'

# Define path to train and test folder
output_base = r'./crop_images_balanced'
train_folder = os.path.join(output_base, 'train')
test_folder = os.path.join(output_base, 'test')

# Import selected classes as defined in config_selected_classes.py
crop_classes = ["B11", "B12", "B13", "B14", "B15", "B16", "B21", "B22", "B31", "B32", "B33", "B55"] 

# Function to create class folders, which will contain the images
def create_class_folders(base_path, classes):
    for cls in classes:
        cls_path = os.path.join(base_path, cls)
        os.makedirs(cls_path, exist_ok=True)

# Read in train and test csv
train_df = pd.read_csv(train_csv)
test_df = pd.read_csv(test_csv)

# Create folders
create_class_folders(train_folder, crop_classes)
create_class_folders(test_folder, crop_classes)

# Function to copy images into the folders
def copy_images(df, dest_folder):
    for _, row in df.iterrows():
        class_folder = os.path.join(dest_folder, row['SURVEY_LC1'])
        src_path = row['FILEPATH']
        if os.path.exists(src_path):
            shutil.copy(src_path, class_folder)
        else:
            print(f"Warning: File not found: {src_path}")

# Copy images
print("Copy train images...")
copy_images(train_df, train_folder)

print("Copy test images...")
copy_images(test_df, test_folder)

print("Done. All images of the selected classes were copied.")
