import os
import stanza

DATA_DIR = "raw_data/zh"
CLEANED_DIR = "cleaned_data/zh"

stanza.download('zh')
segmenter = stanza.Pipeline('zh')

def _process_and_write(input_file, output_file):
    text = ""
    for line in input_file:
        text += line.strip()
    doc = segmenter(text)
    
    tmp = None
    tmp1 = None
    for i in doc.sentences:
        i = i.text
        if i.count("（") > i.count("）"):
            tmp = i
            continue
        if i.startswith("）"):
            if tmp:
                tmp += "）"
                tmp = tmp.replace("））", "）")
                tmp = tmp.replace("）。）", "）。")
                output_file.write(tmp + "\n")
                tmp = None
            i = i[1:]
        
        if not i: continue

        if i.count("(") > i.count(")"):
            tmp1 = i
            continue
        if i.startswith(")"):
            if tmp1:
                tmp1 += ")"
                tmp1 = tmp1.replace("))", ")")
                output_file.write(tmp1 + "\n")
                tmp1 = None
            i = i[1:]
        
        if not i: continue

        output_file.write(i + "\n")

def sentence_split(section, pro_files, ama_files):
   for pro_file, ama_file in zip(pro_files, ama_files):
        pro_input_path = f"{DATA_DIR}/professional/section{section}/{pro_file}"
        ama_input_path = f"{DATA_DIR}/amateur/section{section}/{ama_file}"
        pro_output_path = f"{CLEANED_DIR}/professional/section{section}/{pro_file}"
        ama_output_path = f"{CLEANED_DIR}/amateur/section{section}/{ama_file}"

        with open(pro_input_path, "r") as pro_in, \
             open(ama_input_path, "r") as ama_in, \
             open(pro_output_path, "w") as pro_out, \
             open(ama_output_path, "w") as ama_out:
            
            _process_and_write(pro_in, pro_out)
            _process_and_write(ama_in, ama_out)

def main():
   pro_base_dir = f"{DATA_DIR}/professional/section"
   ama_base_dir = f"{DATA_DIR}/amateur/section"
   for section in range(1, 25):
        os.makedirs(f"{CLEANED_DIR}/professional/section{section}", exist_ok=True)
        os.makedirs(f"{CLEANED_DIR}/amateur/section{section}", exist_ok=True)
        pro_files = sorted([f for f in os.listdir(pro_base_dir + str(section)) if os.path.isfile(os.path.join(pro_base_dir + str(section), f))])
        ama_files = sorted([f for f in os.listdir(ama_base_dir + str(section)) if os.path.isfile(os.path.join(ama_base_dir + str(section), f))])
        print("section"+ str(section) + "：" + str(len(pro_files)))
        sentence_split(section, pro_files, ama_files)

if __name__ == '__main__':
    main()
