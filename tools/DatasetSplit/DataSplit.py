"""
This tool is used to split up a dataset of .png and .txt file pairs into a folder structure that is used by 
the ModelGen tool. It takes the matching pairs from the "annot_images" folder, keeps the matching pairs together 
but shuffles the order, then splits them into three folders with 70% going towards training, 15% towards testing, 
and 15% towards validation.
"""

import os
import random
import shutil

def move_files(pairs, subset_name, base_dir, output_dir):
    for img_file, txt_file in pairs:
        # Move image files
        shutil.move(os.path.join(base_dir, img_file), os.path.join(output_dir, subset_name, 'images', img_file))
        # Move label files
        shutil.move(os.path.join(base_dir, txt_file), os.path.join(output_dir, subset_name, 'labels', txt_file))

def main():
    base_dir = 'tools/DatasetSplit/annot_images/'
    output_dir = 'tools/DatasetSplit/dataset/model_data'

    sub_dirs = ['train', 'valid', 'test']
    for sub_dir in sub_dirs:
        os.makedirs(os.path.join(output_dir, sub_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, sub_dir, 'labels'), exist_ok=True)

    all_images = [f for f in os.listdir(base_dir) if f.endswith('.png')]
    all_txts = [f for f in os.listdir(base_dir) if f.endswith('.txt')]

    pairs = []
    for img in all_images:
        txt_file = img.replace('.png', '.txt')
        if txt_file in all_txts:
            pairs.append((img, txt_file))

    random.shuffle(pairs)

    total_pairs = len(pairs)
    train_split = int(total_pairs * 0.70)
    val_split = int(total_pairs * 0.15)
    test_split = total_pairs - train_split - val_split

    train_pairs = pairs[:train_split]
    val_pairs = pairs[train_split:train_split + val_split]
    test_pairs = pairs[train_split + val_split:]

    move_files(train_pairs, 'train', base_dir, output_dir)
    move_files(val_pairs, 'valid', base_dir, output_dir)
    move_files(test_pairs, 'test', base_dir, output_dir)

    print("Files have been split and moved to the respective directories.")

if __name__ == "__main__":
    main()
