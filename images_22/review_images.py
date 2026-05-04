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
    print("-" * 40)

    kept_count = 0
    discarded_count = 0

    for filename in files_to_review:
        src_filepath = os.path.join(class_source_path, filename)
        relative_path = os.path.join(class_name, filename)

        # Read image (just to check if valid)
        img = cv2.imread(src_filepath)
        if img is None:
            print(f"Warning: Could not read {filename}. Skipping.")
            continue

        # Automatically open the image in VS Code for inspection
        print(f"Opening image for inspection: {src_filepath}")
        os.system(f"code {src_filepath}")

        decision = input("Keep this image? (y/n/q): ").strip().lower()

        status = None
        if decision == 'y':
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
        
        elif decision == 'n':
            status = 'discarded'
            discarded_count += 1
            print(f"  ✗ Discarded: {filename}")
        
        elif decision == 'q':
            print("\nQuitting... Progress saved.")
            # Calculate totals
            total_kept = len(progress_df[(progress_df['status'] == 'kept') & (progress_df['class_name'] == class_name)])
            total_discarded = len(progress_df[(progress_df['status'] == 'discarded') & (progress_df['class_name'] == class_name)])
            total_reviewed = len(progress_df[progress_df['class_name'] == class_name])
            print("\n" + "=" * 50)
            print(f"Class '{class_name}' finished (quit early)!")
            print(f"Kept this session: {kept_count}")
            print(f"Discarded this session: {discarded_count}")
            print(f"Reviewed this session: {kept_count + discarded_count}")
            print(f"Kept total: {total_kept}")
            print(f"Discarded total: {total_discarded}")
            print(f"Reviewed total: {total_reviewed}")
            print(f"Progress saved to: {csv_path}")
            print("=" * 50)
            # Save progress before quitting
            save_progress(progress_df, csv_path)
            return

        # Update progress DataFrame
        if status:
            new_row = pd.DataFrame([[relative_path, class_name, status]], columns=CSV_COLUMNS)
            progress_df = pd.concat([progress_df, new_row], ignore_index=True)
            
            # Save progress incrementally (safe against crashes)
            save_progress(progress_df, csv_path)

            if status == 'kept':
                total_kept = len(progress_df[(progress_df['status'] == 'kept') & (progress_df['class_name'] == class_name)])
                print(f"You have kept {total_kept} images for this class so far!")


def main():
    parser = argparse.ArgumentParser(description="Interactive Image Review Tool")
    parser.add_argument('--source', type=str, default='./crop_images_22_sorted',
                        help='Source directory containing class folders')
    parser.add_argument('--dest', type=str, default='./crop_images_22_selected',
                        help='Destination directory for kept images')
    parser.add_argument('--class', type=str, required=True, dest='class_name',
                        help='Class name to review')
    
    args = parser.parse_args()

    # Set class-specific CSV in dest directory
    csv_path = os.path.join(args.dest, f'review_progress_{args.class_name}.csv')

    print(f"Source: {args.source}")
    print(f"Destination: {args.dest}")
    print(f"CSV: {csv_path}")
    
    review_class(
        source_dir=args.source,
        dest_dir=args.dest,
        class_name=args.class_name,
        csv_path=csv_path
    )


if __name__ == "__main__":
    main()