import sys
import os

args = sys.argv
lang = args[1]
data_type = args[2] 

input_filepath = f"auto_align/{lang}/splitted_data/MSD-{data_type}.tsv"
output_dir = f"results/{lang}/"
os.makedirs(output_dir, exist_ok=True)

def preprocess(filepath: str):
    output_filepath = os.path.join(output_dir, f"MSD-{data_type}.tsv")
    
    with open(filepath, "r", encoding="utf-8") as input_file, open(output_filepath, "w", encoding="utf-8") as output_file:
        sentences = []
        for line in input_file:
            parts = line.strip().split("\t")
            # Remove if either sentence has 5 or fewer characters.
            if len(parts[0]) < 6 or len(parts[1]) < 6:
                continue
            # Remove if the simple and difficult sentences are identical.
            if parts[0] == parts[1]:
                continue
            sentences.append(parts[0] + "\t" + parts[1] + "\n")
        
        for sentence in set(sentences):
            output_file.write(sentence)
            
def main():
    preprocess(input_filepath)

if __name__ == '__main__':
    main()