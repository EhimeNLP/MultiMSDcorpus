import sys
import os

lang = sys.argv[1]

# Directory paths
INPUT_BASE_DIR = os.path.join("auto_align", lang, "aligned_data")
OUTPUT_BASE_DIR = os.path.join("auto_align", lang, "splitted_data")
DEV_TEST_LIST_DIR = os.path.join("auto_align", "ja", "splitted_data")

def split_and_concat_files(section_num: int, article_dir_names: list, dev_files: list, test_files: list):
    for article_dir in article_dir_names:
        input_filepath = os.path.join(INPUT_BASE_DIR, f"section{section_num}", article_dir, "pattern1.tsv")
        train_output_path = os.path.join(OUTPUT_BASE_DIR, "train", f"section{section_num}.tsv")
        dev_output_path = os.path.join(OUTPUT_BASE_DIR, "dev", f"section{section_num}.tsv")
        test_output_path = os.path.join(OUTPUT_BASE_DIR, "test", f"section{section_num}.tsv")

        try:
            with open(input_filepath, "r", encoding="utf-8") as f_in:
                content = f_in.read()
        except FileNotFoundError:
            continue

        if article_dir in dev_files:
            with open(dev_output_path, "a", encoding="utf-8") as f_dev:
                f_dev.write(content)
        elif article_dir in test_files:
            with open(test_output_path, "a", encoding="utf-8") as f_test:
                f_test.write(content)
        else:
            with open(train_output_path, "a", encoding="utf-8") as f_train:
                f_train.write(content)

def combine_final_sets(output_base_dir: str):
    for data_type in ["train", "dev", "test"]:
        final_output_path = os.path.join(output_base_dir, f"MSD-{data_type}.tsv")
        with open(final_output_path, "w", encoding="utf-8") as f_out:
            for section_num in range(1, 25):
                section_filepath = os.path.join(output_base_dir, data_type, f"section{section_num}.tsv")
                if os.path.exists(section_filepath):
                    with open(section_filepath, "r", encoding="utf-8") as f_in:
                        f_out.write(f_in.read())

def main():
    for data_type in ["train", "dev", "test"]:
        os.makedirs(os.path.join(OUTPUT_BASE_DIR, data_type), exist_ok=True)
    
    with open(os.path.join(DEV_TEST_LIST_DIR, "devfile.txt"), "r", encoding="utf-8") as f_in:
        dev_files = [line.strip() for line in f_in]
    with open(os.path.join(DEV_TEST_LIST_DIR, "testfile.txt"), "r", encoding="utf-8") as f_in:
        test_files = [line.strip() for line in f_in]

    for section_num in range(1, 25):
        section_dir = os.path.join(INPUT_BASE_DIR, f"section{section_num}")
        if os.path.isdir(section_dir):
            article_dir_names = [f for f in os.listdir(section_dir) if os.path.isdir(os.path.join(section_dir, f))]
            split_and_concat_files(section_num, article_dir_names, dev_files, test_files)

    combine_final_sets(OUTPUT_BASE_DIR)

if __name__ == '__main__':
    main()