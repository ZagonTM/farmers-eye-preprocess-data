#!/usr/bin/env python3
import pandas as pd
import os

# Read CSV and image directory
df = pd.read_csv("images_22/EU_LUCAS_2022.csv")
image_dir = "crop_images_22"

# Filter: only keep rows where SURVEY_LC1 starts with 'B' (crops), excluding 'Bx1' and 'Bx2'
df = df[df['SURVEY_LC1'].str.startswith('B', na=False) & 
        ~df['SURVEY_LC1'].isin(['Bx1', 'Bx2'])]

# Get all downloaded filenames
downloaded_files = set(os.listdir(image_dir)) if os.path.exists(image_dir) else set()

# Extract POINT_ID from filenames (positions 4-12: 8 digits after '2022')
downloaded_ids = set()
for filename in downloaded_files:
    if filename.startswith('2022') and len(filename) >= 12:
        downloaded_ids.add(filename[4:12])  # Extract 8-digit ID

# Filter CSV: keep only rows where POINT_ID is NOT in downloaded_ids
df['POINT_ID'] = df['POINT_ID'].astype(str).str.zfill(8)
missing_df = df[~df['POINT_ID'].isin(downloaded_ids)]

# Save result
missing_df.to_csv("images_22/missing_crop_images_metadata.csv", index=False)

# Print summary
print(f"Total crop rows (B* except Bx1/Bx2): {len(df)}")
print(f"Downloaded: {len(df) - len(missing_df)}")
print(f"Missing: {len(missing_df)}")
print(f"Saved to: missing_crop_images_metadata.csv")