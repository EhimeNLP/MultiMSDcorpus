from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os

args = sys.argv
lang = args[1]
threshold = float(args[2])

# LaBSE model
model = SentenceTransformer('sentence-transformers/LaBSE')

# Directory paths
cleaned_pro_dir = "cleaned_data/" + lang + "/professional/section"
cleaned_ama_dir = "cleaned_data/" + lang + "/amateur/section"
save_dir = "auto_align/" + lang + "/aligned_data/section"

def auto_align(file, section):
    os.makedirs(save_dir + str(section) + "/" + file[:-4], exist_ok=True)
    with open(cleaned_pro_dir + str(section) + "/" + file[:-4] + ".pro", "r") as pro_in, \
         open(cleaned_ama_dir + str(section) + "/" + file[:-4] + ".ama", "r") as ama_in:
        
        pro_sents = []
        for line in pro_in: pro_sents.append(line.strip())
        ama_sents = []
        for line in ama_in: ama_sents.append(line.strip())

        pro_embed = model.encode(pro_sents)
        ama_embed = model.encode(ama_sents)

        pro_similarities = cosine_similarity(pro_embed, ama_embed)
        ama_similarities = cosine_similarity(ama_embed, pro_embed)

        # Max alignment of cosine similarity (pro → ama)
        pro2ama_pair = []
        for idx, embed in enumerate(pro_similarities):
            max_idx, sim = max(enumerate(embed), key = lambda x:x[1])
            if sim > threshold:
                pro2ama_pair.append(pro_sents[idx] + "\t" + ama_sents[max_idx] + "\n")

        # Max alignment of cosine similarity (ama → pro)
        ama2pro_pair = []
        for idx, embed in enumerate(ama_similarities):
            max_idx, sim = max(enumerate(embed), key = lambda x:x[1])
            if sim > threshold:
                ama2pro_pair.append(pro_sents[max_idx] + "\t" + ama_sents[idx] + "\n")
        
        # Save the results
        with open(save_dir + str(section) + "/" + file[:-4] + "/pattern1.tsv", "w") as pattern1_out, \
             open(save_dir + str(section) + "/" + file[:-4] + "/pattern2.tsv", "w") as pattern2_out:
            # Pattern 1: Write pairs that are the same in both directions
            for pair in pro2ama_pair:
                if pair in ama2pro_pair:
                    pattern1_out.write(pair)
            # Pattern 2: Write the union of pairs from both directions
            pairs = set(pro2ama_pair) | set(ama2pro_pair)
            for pair in pairs:
                pattern2_out.write(pair)

def align_section(section_num, pro_filenames):
    for pro_filename in pro_filenames:
        auto_align(pro_filename, section_num)

def main():
    for section_num in range(1, 25):
        pro_files_dir = cleaned_pro_dir + str(section_num)
        if not os.path.isdir(pro_files_dir):
            continue
        pro_filenames = [f for f in os.listdir(pro_files_dir) if os.path.isfile(os.path.join(pro_files_dir, f))]
        align_section(section_num, pro_filenames)

if __name__ == '__main__':
    main()