# MultiMSD Corpus
* This corpus was constructed by collecting article pairs from the professional and consumer versions of the [MSD Manuals](https://www.msdmanuals.com/) and performing embedding-based sentence alignment.
* It supports nine languages: German, English, Spanish, French, Italian, Japanese, Portuguese, Russian, and Chinese.
* Here, we release the code to automatically build the MultiMSD corpus.

# Directory Structure
Please place the `run.sh` script and the `scripts` directory in the same root directory as shown below.
```
├── requirements.txt
├── run.sh
└── scripts
    ├── alignment
    ├── collection
    ├── preprocess
    └── sentence_split
```

# Usage
When you run run.sh, a directory named results is created, which contains MSD-{train, dev, test}.tsv for each language.
> This script collects data from the MSD Manual website. However, the HTML structure of the website may have changed since the time of the original data collection.
> Therefore, the dataset you obtain may not be identical to the one used in the paper.
> That said, if the number of sentence pairs in each TSV file is close to the original dataset size, the script can be considered to have run successfully.
```
pip install -r requirements.txt

bash ./run.sh
```

# References
* Koki Horiguchi, Tomoyuki Kajiwara, Takashi Ninomiya, Shoko Wakamiya, Eiji Aramaki.  
  MultiMSD: A Corpus for Multilingual Medical Text Simplification from Online Medical References.  
  ACL 2025 Findings. Vienna, Austria. July 2025. [[PDF](https://aclanthology.org/2025.findings-acl.481.pdf)]

* 堀口 航輝, 梶原 智之, 二宮 崇, 若宮 翔子, 荒牧 英治.  
  日本語医療テキスト平易化の訓練用データセットの構築.  
  人工知能学会第38回全国大会, 3S1-OS-7b, 2024. [[PDF](https://confit.atlas.jp/guide/event-img/jsai2024/3S1-OS-7b-04/public/pdf?type=in)]
