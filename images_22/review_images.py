import os
import shutil
import pandas as pd
import cv2
import argparse
from tqdm import tqdm


# Configuration
CSV_COLUMNS = ['filepath', 'class_name', 'status']
KEY_KEEP = ord('y')      # Press 'y' to keep
KEY_DISCARD = ord('n')   # Press 'n' to discard
KEY_QUIT = ord('q')      # Press 'q' to quit


def load_progress(csv_path):
    """Load existing progress from CSV or create new DataFrame."""
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        processed = set(df['filepath'].tolist())
        print(f"Resuming from existing progress: {len(processed)} images already reviewed.")
        return df, processed
    return pd.DataFrame(columns=CSV_COLUMNS), set()


def save_progress(df, csv_path):
    """Save current progress to CSV."""
    df.to_csv(csv_path, index=False)


def review_class(source_dir, dest_dir, class_name, csv_path):
    class_source_path = os.path.join(source_dir, class_name)
    class_dest_path = os.path.join(dest_dir, class_name)

    if not os.path.exists(class_source_path):
        print(f"Error: Class folder '{class_source_path}' not found.")
        return

    # Create destination folder
    os.makedirs(class_dest_path, exist_ok=True)

    # Load progress
    progress_df, processed_files = load_progress(csv_path)

    # Get all image files
    valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    all_files = [f for f in os.listdir(class_source_path) if f.lower().endswith(valid_exts)]
    
    # Filter out already processed files
    files_to_review = [f for f in all_files if os.path.join(class_name, f) not in processed_files]

    if not files_to_review:
        print("No new images to review for this class.")
        return

    total_files = len(all_files)
    already_done = len(processed_files)
    print(f"\nStarting review for class: {class_name}")
    print(f"Progress: {already_done}/{total_files} ({already_done/total_files:.1%} done)")
    print(f"Remaining: {len(files_to_review)}")
    print("-" * 40)
    print("Controls: [Y] = Keep, [N] = Discard, [Q] = Quit")

    kept_count = 0
    discarded_count = 0

    for filename in files_to_review:
        src_filepath = os.path.join(class_source_path, filename)
        relative_path = os.path.join(class_name, filename)

        # Read image
        img = cv2.imread(src_filepath)
        if img is None:
            print(f"Warning: Could not read {filename}. Skipping.")
            continue

        # Display image
        window_title = f"{class_name} | {filename} | [K]eep [D]iscard [Q]uit"
        cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
        
        # Resize if image is too large for screen
        h, w = img.shape[:2]
        if h > 800 or w > 1200:
            scale = min(1200 / w, 800 / h)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))
        
        cv2.imshow(window_title, img)
        
        # Wait for key press
        key = cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()

        status = None
        if key == KEY_KEEP:
            # Copy to destination
            dst_filepath = os.path.join(class_dest_path, filename)
            # Handle duplicate filenames (unlikely in same class, but safe)
            if os.path.exists(dst_filepath):
                base, ext = os.path.splitext(filename)
                dst_filepath = os.path.join(class_dest_path, f"{base}_{kept_count}{ext}")
            
            shutil.copy2(src_filepath, dst_filepath)
            status = 'kept'
            kept_count += 1
            print(f"  ✓ Kept: {filename}")
        
        elif key == KEY_DISCARD:
            status = 'discarded'
            discarded_count += 1
            print(f"  ✗ Discarded: {filename}")
        
        elif key == KEY_QUIT:
            print("\nQuitting... Progress saved.")
            # Save progress before quitting
            save_progress(progress_df, csv_path)
            return

        # Update progress DataFrame
        if status:
            new_row = pd.DataFrame([[relative_path, class_name, status]], columns=CSV_COLUMNS)
            progress_df = pd.concat([progress_df, new_row], ignore_index=True)
            
            # Save progress incrementally (safe against crashes)
            save_progress(progress_df, csv_path)

    print("\n" + "=" * 50)
    print(f"Class '{class_name}' finished!")
    print(f"Total reviewed this session: {kept_count + discarded_count}")
    print(f"Kept: {kept_count}, Discarded: {discarded_count}")
    print(f"Progress saved to: {csv_path}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Interactive Image Review Tool")
    parser.add_argument('--source', type=str, default='./crop_images_all',
                        help='Source directory containing class folders')
    parser.add_argument('--dest', type=str, default='./crop_images_selected',
                        help='Destination directory for kept images')
    parser.add_argument('--class', type=str, required=True, dest='class_name',
                        help='Class name to review')
    parser.add_argument('--csv', type=str, default='review_progress.csv',
                        help='CSV file to track progress')
    
    args = parser.parse_args()

    print(f"Source: {args.source}")
    print(f"Destination: {args.dest}")
    
    review_class(
        source_dir=args.source,
        dest_dir=args.dest,
        class_name=args.class_name,
        csv_path=args.csv
    )


if __name__ == "__main__":
    main()