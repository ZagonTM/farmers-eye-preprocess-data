import os
import random
import shutil
from PIL import Image
import matplotlib.pyplot as plt

# folders
source_folder = r"crop_images_all"
target_folder = r"crop_images_selected"

os.makedirs(target_folder, exist_ok=True)

# collect images
images = [f for f in os.listdir(source_folder)
          if f.lower().endswith((".png", ".jpg", ".jpeg"))]

random.shuffle(images)

for img_name in images:
    path = os.path.join(source_folder, img_name)

    # show image
    img = Image.open(path)
    plt.imshow(img)
    plt.axis("off")
    plt.title(f"{img_name} (y = keep, n = skip)")
    plt.show()

    decision = input("Keep this image? (y/n): ").strip().lower()

    if decision == "y":
        shutil.copy(path, os.path.join(target_folder, img_name))