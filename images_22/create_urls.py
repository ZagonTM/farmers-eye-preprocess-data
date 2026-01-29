#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# Configuration
CSV_PATH = "images_22/EU_LUCAS_2022.csv"
OUTPUT_TXT = "images_22/22_image_urls.txt"
YEAR = "2022"
BASE_URL = "https://gisco-services.ec.europa.eu/lucas/photos"
IMAGE_SUFFIX = "LCLU_CropLC1.jpg"

# Load CSV
df = pd.read_csv(CSV_PATH)

# Ensure required columns exist
required_cols = {"POINT_ID", "SURVEY_LC1", "POINT_NUTS0"}
missing_cols = required_cols - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing required columns in CSV: {missing_cols}")


# Filter Landuse Class, only Crops (B) remain. Exclude Bx1 and Bx2 as these include multiple crops in one image.
df = df[
    df["SURVEY_LC1"].str.startswith("B", na=False)
    & ~df["SURVEY_LC1"].isin(["Bx1", "Bx2"])
]


# Build URLs using metainformation from EU_LUCAS_2022.csv
urls = []

for _, row in df.iterrows():
    pid = str(row["POINT_ID"])
    country = row["POINT_NUTS0"]

    # Directory structure derived from POINT_ID
    dir1 = pid[0:3]
    dir2 = pid[3:6]

    # Construct URL
    url = f"{BASE_URL}/{YEAR}/{country}/{dir1}/{dir2}/{YEAR}{pid}{IMAGE_SUFFIX}"
    urls.append(url)

# Write URL list
output_path = Path(OUTPUT_TXT)
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w") as f:
    f.write("\n".join(urls) + "\n")

# Summary
print(f"Total crop URLs created: {len(urls)}")
print(f"Saved to: {output_path.resolve()}")
