import os
import shutil
import pandas as pd
from tqdm import tqdm


# Configuration
csv_files = [
    'images_22/train_crop_images.csv',
    'images_22/test_crop_images.csv'
]
output_folder = r'./crop_images_all'

# Import selected classes as defined in config_selected_classes.py
crop_classes = [
    "B11", "B12", "B13", "B14", "B15", "B16",
    "B21", "B22", "B31", "B32", "B33", "B55"
]


def create_class_folders(base_path, classes):
    """Create class folders if they don't exist."""
    for cls in classes:
        os.makedirs(os.path.join(base_path, cls), exist_ok=True)


def copy_images(csv_paths, dest_folder):
    """
    Copy images from multiple CSV files into class-organized folders.
    Returns counts of copied and missing files.
    """
    # Combine all dataframes
    dfs = [pd.read_csv(csv) for csv in csv_paths]
    combined_df = pd.concat(dfs, ignore_index=True)

    # Filter to selected classes only
    filtered_df = combined_df[combined_df['SURVEY_LC1'].isin(crop_classes)]

    copied_count = 0
    missing_count = 0
    missing_files = []

    print(f"Processing {len(filtered_df)} images...")

    for _, row in tqdm(filtered_df.iterrows(), total=len(filtered_df)):
        class_folder = os.path.join(dest_folder, row['SURVEY_LC1'])
        src_path = row['FILEPATH']

        if os.path.exists(src_path):
            shutil.copy(src_path, class_folder)
            copied_count += 1
        else:
            missing_count += 1
            missing_files.append(src_path)

    return copied_count, missing_count, missing_files


def main():
    print("Creating output folder structure...")
    create_class_folders(output_folder, crop_classes)

    print("Copying images...")
    copied, missing, missing_files = copy_images(csv_files, output_folder)

    # Print summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Images copied:  {copied}")
    print(f"  Files missing:  {missing}")
    print("=" * 50)

    if missing_files:
        print("\nMissing files:")
        for f in missing_files[:10]:
            print(f"  - {f}")
        if len(missing_files) > 10:
            print(f"  ... and {len(missing_files) - 10} more")

    print("\nDone!")


if __name__ == "__main__":
    main()