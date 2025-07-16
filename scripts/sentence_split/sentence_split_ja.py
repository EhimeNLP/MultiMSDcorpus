import os
import functools
from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import concatenate_matching
from ja_sentence_segmenter.normalize.neologd_normalizer import normalize
from ja_sentence_segmenter.split.simple_splitter import split_newline, split_punctuation

DATA_DIR = "raw_data/ja"
CLEANED_DIR = "cleaned_data/ja"

split_punc2 = functools.partial(split_punctuation, punctuations=r"。!?:")
concat_tail_no = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(の)$", remove_former_matched=False)
concat_tail_te = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(て)$", remove_former_matched=False)
concat_decimal = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(\d.)$", latter_matching_rule=r"^(\d)(?P<result>.+)$", remove_former_matched=False, remove_latter_matched=False)
segmenter = make_pipeline(normalize, split_newline, concat_tail_no, concat_tail_te, split_punc2, concat_decimal)

def _process_and_write(input_file, output_file):
    article = ""
    for line in input_file:
        article += line.strip()
    
    parsed_sentences = list(segmenter(article))
    
    for sentence in parsed_sentences:
        sentence = sentence.replace('参照のこと。)', '参照のこと。)\n')
        output_file.write(sentence+"\n")

def sentence_split(section, pro_files, ama_files):
   for pro_file, ama_file in zip(pro_files, ama_files):
        pro_input_path = f"{DATA_DIR}/professional/section{section}/{pro_file}"
        ama_input_path = f"{DATA_DIR}/amateur/section{section}/{ama_file}"
        pro_output_path = f"{CLEANED_DIR}/professional/section{section}/{pro_file}"
        ama_output_path = f"{CLEANED_DIR}/amateur/section{section}/{ama_file}"

        with open(pro_input_path, "r", encoding="utf-8") as pro_in, \
             open(ama_input_path, "r", encoding="utf-8") as ama_in, \
             open(pro_output_path, "w", encoding="utf-8") as pro_out, \
             open(ama_output_path, "w", encoding="utf-8") as ama_out:
            
            _process_and_write(pro_in, pro_out)
            _process_and_write(ama_in, ama_out)

def main():
   pro_base_dir = f"{DATA_DIR}/professional/section"
   ama_base_dir = f"{DATA_DIR}/amateur/section"
   for section in range(1, 25):
        os.makedirs(f"{CLEANED_DIR}/professional/section{section}", exist_ok=True)
        os.makedirs(f"{CLEANED_DIR}/amateur/section{section}", exist_ok=True)
        pro_files = [f for f in os.listdir(pro_base_dir + str(section)) if os.path.isfile(os.path.join(pro_base_dir + str(section), f))]
        ama_files = [f for f in os.listdir(ama_base_dir + str(section)) if os.path.isfile(os.path.join(ama_base_dir + str(section), f))]
        print("section"+ str(section) + "：" + str(len(pro_files)))
        sentence_split(section, pro_files, ama_files)

if __name__ == '__main__':
    main()