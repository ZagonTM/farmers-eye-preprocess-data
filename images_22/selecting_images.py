import numpy as np
import pandas as pd
import os

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
selected_metadata = filtered_metadata[filtered_metadata['SURVEY_LC1'].isin(crop_classes)]

# Count pictures per class
class_counts = selected_metadata['SURVEY_LC1'].value_counts()
print(class_counts)

n_min_crop = class_counts.sort_values()[0]

# Draw random samples of size n_min_crop without replacement per class 
sampled_dict = {}

for crop in crop_classes:
    sampled_dict[crop] = selected_metadata[selected_metadata["SURVEY_LC1"] == crop]["POINT_ID"].sample(n=n_min_crop)
    sampled_dict[crop] = sampled_dict[crop].astype(np.int64).tolist()
    
sampled_df = pd.DataFrame.from_dict(sampled_dict)
print(sampled_df.head())
print(sampled_df.tail())

# Split into train and test sets (80% train, 20% test)
train = sampled_df.iloc[:int(0.8 * n_min_crop), :]
test = sampled_df.iloc[int(0.8 * n_min_crop):, :]

# Create two new dataframes filtered for train and test sets
train_filtered = selected_metadata[selected_metadata['POINT_ID'].isin(train.values.flatten())] 
test_filtered = selected_metadata[selected_metadata['POINT_ID'].isin(test.values.flatten())]

# Add column to both dataframes with whole filepath for each image
train_filtered['FILEPATH'] = (
    folder
    + r'/2022'
    + train_filtered['POINT_ID'].astype(str)
    + r'LCLU_CropLC1.jpg'
)

test_filtered['FILEPATH'] = (
    folder 
    + r'/2022'
    + test_filtered['POINT_ID'].astype(str)
    + r'LCLU_CropLC1.jpg'
)


print(train_filtered.head())


# Save dataframes as CSV files
train_filtered.to_csv('images_22/train_crop_images.csv', index=False)
test_filtered.to_csv('images_22/test_crop_images.csv', index=False)
