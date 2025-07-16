import os

LANG = "ja"

ALL_LANGS = ["de", "en", "es", "fr", "it", "ja", "pt", "ru", "zh"]

# Directory paths
INPUT_BASE_DIR = os.path.join("auto_align")
OUTPUT_BASE_DIR = os.path.join(INPUT_BASE_DIR, LANG, "splitted_data")

def split_and_concat_files(section_num: int, article_dir_names: list):
    num_articles = len(article_dir_names)
    if num_articles < 20:
        max_len = 2
    elif num_articles < 40:
        max_len = 4
    else:
        max_len = 6
    
    assigned_count = 0
    
    with open(os.path.join(OUTPUT_BASE_DIR, "devfile.txt"), "a", encoding="utf-8") as dev_list_file, \
         open(os.path.join(OUTPUT_BASE_DIR, "testfile.txt"), "a", encoding="utf-8") as test_list_file:

        for article_dir in article_dir_names:
            is_in_all_langs = True
            for other_lang in ALL_LANGS:
                path_to_check = os.path.join(INPUT_BASE_DIR, other_lang, "aligned_data", f"section{section_num}", article_dir)
                if not os.path.isdir(path_to_check):
                    is_in_all_langs = False
                    break
            
            input_filepath = os.path.join(INPUT_BASE_DIR, LANG, "aligned_data", f"section{section_num}", article_dir, "pattern1.tsv")
            train_output_path = os.path.join(OUTPUT_BASE_DIR, "train", f"section{section_num}.tsv")
            dev_output_path = os.path.join(OUTPUT_BASE_DIR, "dev", f"section{section_num}.tsv")
            test_output_path = os.path.join(OUTPUT_BASE_DIR, "test", f"section{section_num}.tsv")

            try:
                with open(input_filepath, "r", encoding="utf-8") as f_in:
                    content = f_in.read()
            except FileNotFoundError:
                continue

            if assigned_count < max_len and is_in_all_langs:
                with open(test_output_path, "a", encoding="utf-8") as f_test:
                    f_test.write(content)
                test_list_file.write(article_dir + "\n")
                assigned_count += 1
            elif assigned_count < max_len * 2 and is_in_all_langs:
                with open(dev_output_path, "a", encoding="utf-8") as f_dev:
                    f_dev.write(content)
                dev_list_file.write(article_dir + "\n")
                assigned_count += 1
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
    
    if os.path.exists(os.path.join(OUTPUT_BASE_DIR, "devfile.txt")):
        os.remove(os.path.join(OUTPUT_BASE_DIR, "devfile.txt"))
    if os.path.exists(os.path.join(OUTPUT_BASE_DIR, "testfile.txt")):
        os.remove(os.path.join(OUTPUT_BASE_DIR, "testfile.txt"))

    for section_num in range(1, 25):
        section_dir = os.path.join(INPUT_BASE_DIR, LANG, "aligned_data", f"section{section_num}")
        if os.path.isdir(section_dir):
            article_dir_names = [f for f in os.listdir(section_dir) if os.path.isdir(os.path.join(section_dir, f))]
            split_and_concat_files(section_num, article_dir_names)

    combine_final_sets(OUTPUT_BASE_DIR)

if __name__ == '__main__':
    main()