# Preprocessing LUCAS Cover Photos

This GIT repository can be used to download LUCAS cover photos for the campaigns 2006 to 2022 and generate balanced train and test data sets. 


# How to run  

To run this script the lucas_cover_attr.csv and EU_LUCAS_2022.csv need to be downloaded and placed into the images_22 or images_06to18 folders:  

[Data for all 27 countries](https://ec.europa.eu/eurostat/web/lucas/database/2022) <br>

[lucas_cover_attr.csv](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/LUCAS/LUCAS_COVER/tables/)  

## LUCAS 2022

1. download_lucas22.sh  

You can run the download_lucas22.sh which will download all images with the crop class B from the 2022 LUCAS campaign. The corresponding urls are saved in the 22_image_urls.txt file. If images from other classes, are desired: adjust and run create_urls.py. 

2. preparing_folders.py  

This script will use test_crop_images.csv and train_crop_images.csv and copy all images selected as train or test data into a crop_images_balanced folder. Only the following crop classes were selected:

"B11", "B12", "B13", "B14", "B15", "B16", "B21", "B22", "B31", "B32", "B33", "B55"

If a different choice of crop classes is desired rerun: 
selecting_images.py
preparing_folder.py

And adjust the selected_classes in both scripts.

3. image_count.ipynb  

This script can be used to verify if all classes recieved equal amounts of images or if errors appeard during the download or selection of images.

## LUCAS 2006 to 2018 data

1. download_lucas.sh  

You can run the download_lucas.sh which will download all images with the crop class B from the 2006 to 2018 LUCAS campaigns. The corresponding urls are saved in the 06to18_image_urls.txt file. If images from other classes, are desired: adjust and run filter_urls.py. 

2. preparing_folders.sh  

This script will use test_crop_images.csv and train_crop_images.csv and copy all images selected as train or test data into a crop_images_balanced folder. Only the following crop classes were selected:

"B11", "B12", "B13", "B14", "B15", "B16", "B21", "B22", "B31", "B32", "B33", "B55"

If a different choice of crop classes is desired rerun: 
selecting_images.py
preparing_folder.sh

And adjust the selected_classes in both scripts.

3. image_count.ipynb  

This script can be used to verify if all classes recieved equal amounts of images or if errors appeard during the download or selection of images.

# Final data sets  

## Train Images  

For the selected 12 crop classes, the final train image count is 2218 images per class, 26.616 in total.

## Test images  

For the selected 12 crop classes, the final train image count is 556 images per class, 6.672 in total.

# Background information  

For the 2022 data set, there are 3524 images which appear in the EU_LUCAS_2022.csv but which do not appear on the LUCAS website and can therefore not be downloaded. It is likely, that these positions were classified and images collected, but the images were not published due to privacy regulations. Similar processes are described in the paper for the 2006 to 2018 campaign. 

More information on the 2006 to 2018 data can be found here: [Harmonised LUCAS in-situ land cover and use database for field surveys from 2006 to 2018 in the European Union](https://www.nature.com/articles/s41597-020-00675-z)