set -euo pipefail
IFS=$'\n\t'

# Paths
TRAIN_CSV="images_06to18/train_crop_images.csv"
TEST_CSV="images_06to18/test_crop_images.csv"
OUT_BASE="./crop_images_balanced"

TRAIN_DIR="$OUT_BASE/train"
TEST_DIR="$OUT_BASE/test"

# Crop classes
CLASSES=(B11 B12 B13 B14 B15 B16 B21 B22 B31 B32 B33 B55)

# Create directory structure
for cls in "${CLASSES[@]}"; do
    mkdir -p "$TRAIN_DIR/$cls"
    mkdir -p "$TEST_DIR/$cls"
done

echo "Folders created."

# Function to copy images from CSV
copy_from_csv () {
    local csv_file="$1"
    local dest_base="$2"

    echo "Processing $csv_file → $dest_base"

    csvcut -c lc1,FILEPATH "$csv_file" | tail -n +2 | while IFS=',' read -r cls path; do
        if [[ -f "$path" ]]; then
            cp -n "$path" "$dest_base/$cls/"
        else
            echo "Warning: File not found: $path"
        fi
    done
}

# Copy images
copy_from_csv "$TRAIN_CSV" "$TRAIN_DIR"
copy_from_csv "$TEST_CSV"  "$TEST_DIR"

echo "Done. All images copied."
