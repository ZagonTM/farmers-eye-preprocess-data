import numpy as np
import pandas as pd
import os

# Load metadata
metadata = pd.read_csv('images_06to18/lucas_cover_attr.csv', 
                 na_values=['NA', 'N/A', ''],
                 keep_default_na=True,
                 quotechar='"',
                 doublequote=True,
                 engine='python')

# Get image IDs from filenames
folder = r"./crop_images_06to18"
filenames = os.listdir(folder)

ids = np.fromiter(
    (int(name[10:18]) for name in filenames),
    dtype=np.int64
)

# Filter dataframe for filenames
filtered_metadata = metadata[metadata['point_id'].isin(ids)]

# Filter dataframe for crop classes

crop_classes = ["B11", "B12", "B13", "B14", "B15", "B16", "B21", "B22", "B31", "B32", "B33", "B55"] 
selected_metadata = filtered_metadata[filtered_metadata['lc1'].isin(crop_classes)]

# Count pictures per class
class_counts = selected_metadata['lc1'].value_counts()
print(class_counts)

n_min_crop = class_counts.sort_values()[0]
print(f"The lowest image count is {n_min_crop}")

# Draw random samples of size n_min_crop without replacement per class 
sampled_dict = {}

for crop in crop_classes:
    sampled_dict[crop] = (
        selected_metadata[selected_metadata["lc1"] == crop][["point_id", "year"]]
        .sample(n=n_min_crop, random_state=42)
        .to_records(index=False)
        .tolist()
    )
    
sampled_df = pd.DataFrame.from_dict(sampled_dict)
print(sampled_df.head())
print(sampled_df.tail())

sampled_long = sampled_df.melt(
    var_name='lc1',
    value_name='py'
)

sampled_long[['point_id', 'year']] = pd.DataFrame(
    sampled_long['py'].tolist(),
    index=sampled_long.index
)

sampled_long = sampled_long.drop(columns='py')


# Split into train and test sets (80% train, 20% test)
train = sampled_long.groupby('lc1', group_keys=False).head(int(0.8 * n_min_crop))
test  = sampled_long.groupby('lc1', group_keys=False).tail(n_min_crop - int(0.8 * n_min_crop))

# Create two new dataframes filtered for train and test sets
train_filtered = selected_metadata.merge(
    train,
    on=['lc1', 'point_id', 'year'],
    how='inner'
)

test_filtered = selected_metadata.merge(
    test,
    on=['lc1', 'point_id', 'year'],
    how='inner'
)

# Add column to both dataframes with whole filepath for each image
train_filtered['FILEPATH'] = (
    folder
    + r'/LUCAS'
    + train_filtered['year'].astype(str)
    + '_'
    + train_filtered['point_id'].astype(str)
    + r'_Cover.jpg'
)

test_filtered['FILEPATH'] = (
    folder 
    + r'/LUCAS'
    + test_filtered['year'].astype(str)
    + '_'
    + test_filtered['point_id'].astype(str)
    + r'_Cover.jpg'
)


print(train_filtered.head())


# Save dataframes as CSV files
train_filtered.to_csv('images_06to18/train_crop_images.csv', index=False)
test_filtered.to_csv('images_06to18/test_crop_images.csv', index=False)

print(train_filtered['lc1'].value_counts())
print(test_filtered['lc1'].value_counts())
