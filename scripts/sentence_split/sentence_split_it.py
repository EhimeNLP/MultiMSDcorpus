import os
import re
import stanza

DATA_DIR = "raw_data/it"
CLEANED_DIR = "cleaned_data/it"

stanza.download('it')
segmenter = stanza.Pipeline('it')

def _process_and_write(input_file, output_file):
    text = ""
    for line in input_file:
        text += line.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s([?.!,:;])', r'\1', text)
    text = re.sub(r'(\() ', r'\1', text)
    text = re.sub(r' (\))', r'\1', text)
    doc = segmenter(text)
    
    tmp = ""
    for i in doc.sentences:
        i = i.text
        if i.count("(") > i.count(")"):
            tmp = i
            continue
        if i == ")":
            if tmp:
                tmp += ")"
                tmp = tmp.replace("))", ")")
                output_file.write(tmp + "\n")
                tmp = ""
            continue
        elif i[0] == ")":
            if tmp:
                tmp += ")"
                tmp = tmp.replace("))", ")")
                output_file.write(tmp + "\n")
                tmp = ""
            i = i[2:]
        i = re.sub(r': [A-Z]', lambda m: m.group(0).replace(' ', '\n'), i)
        output_file.write(i+"\n")

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
