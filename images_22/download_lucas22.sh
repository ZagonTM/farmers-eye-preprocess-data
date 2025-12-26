#!/bin/bash
#SBATCH --partition=io
#SBATCH --qos=io
#SBATCH --time=10:00:00
#SBATCH --job-name=lucas_image22_dl
#SBATCH --output=images_22/lucas_image_dl_%j.log

# ============================================================================
# This script downloads images, selected in the 'create_urls.py' script.
# It can be sped up by using ftp or aria2c instead of wget, if available on the system.
# Row 1 to 6 only necessary for SLURM job scheduling.
# ============================================================================

# Set variables
cd images_22
URL_FILE="22_image_urls.txt"
OUTPUT_DIR="../crop_images_22"
FAILED_LOG="failed.log"

# Create output directory if it doesn't exist
mkdir -p ${OUTPUT_DIR}

# Count total URLs to download
TOTAL=$(wc -l < "${URL_FILE}")
echo "Starting download of ${TOTAL} images..."
echo "Start: $(date)"

# Count existing files
EXISTING=$(find "${OUTPUT_DIR}" -type f | wc -l)
echo "Already existing: ${EXISTING}"

# Show progress in log file
(
    while true; do
        CURRENT=$(find "${OUTPUT_DIR}" -type f | wc -l)
        echo "Progress: ${CURRENT}/${TOTAL} images downloaded"
        sleep 90  # Every 90 seconds
    done
) &
PROGRESS_PID=$!

wget -q --no-check-certificate -nc -T 20 -t 1 -w 0 -P "${OUTPUT_DIR}" -i "${URL_FILE}" 2> "${FAILED_LOG}"

# End progress display when done
kill $PROGRESS_PID 2>/dev/null || true

# Extract failed URLs if errors occurred
grep "ERROR" "${FAILED_LOG}" | grep -o "http[^ ]*" > "${FAILED_LOG}.tmp" 2>/dev/null || true
mv "${FAILED_LOG}.tmp" "${FAILED_LOG}"

# Final statistics
DOWNLOADED=$(find "${OUTPUT_DIR}" -type f | wc -l)
NEW=$((DOWNLOADED - EXISTING))
FAILED=$(wc -l < "${FAILED_LOG}" 2>/dev/null || echo 0)

echo ""
echo "Done: $(date)"
echo "Total downloaded: ${DOWNLOADED}"
echo "Newly added: ${NEW}"
echo "Failed: ${FAILED}"
echo "URLs in list: ${TOTAL}"