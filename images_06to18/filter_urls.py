import pandas as pd

"""
This script filter the 'lucas_cover_attr.csv' file to extract URLs of images belonging to the cropland landcover class "B".
"""

# Read the CSV file, considering the delimiter is ; but also appears inside quotes
df = pd.read_csv('images_06to18/lucas_cover_attr.csv', 
                 na_values=['NA', 'N/A', ''],
                 keep_default_na=True,
                 quotechar='"',
                 doublequote=True,
                 engine='python')

# Filter rows for landcover group "B" : Cropland
# Using na=False to handle NaN values
b_rows = df[df['lc1'].str.startswith('B', na=False)]

# Extract URLs from file_path_ftp_cover column
urls = b_rows['file_path_ftp_cover'].dropna().tolist()

# Save URLs to a text file
with open('images_06to18/06to18_image_urls.txt', 'w') as f:
    for url in urls:
        f.write(f"{url}\n")

print(f"Saved {len(urls)} URLs to 'images_06to18/06to18_image_urls.txt'")
print(f"Found {len(b_rows)} rows with letter_group == 'B'")