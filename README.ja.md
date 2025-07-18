# MultiMSDコーパス
* [MSDマニュアル](https://www.msdmanuals.com/)から専門家向けおよび一般向けの記事対を収集し、埋め込みベースの文アライメントを実施することで構築しました。
* ドイツ語、英語、スペイン語、フランス語、イタリア語、日本語、ポルトガル語、ロシア語、中国語の9言語に対応しています。
* ここではMultiMSDコーパスを自動構築するためのコードを公開します。

# ディレクトリ構造
以下のように、`run.sh`と`scripts`ディレクトリを同じルートディレクトリに配置してください。
```
├── requirements.txt
├── run.sh
└── scripts
    ├── alignment
    ├── collection
    ├── preprocess
    └── sentence_split
```

# 本コードの使い方
run.shを実行すると、resultsというディレクトリが作成され、各言語それぞれにMSD-{train, dev, test}.tsvが作成されます。
>本スクリプトはWeb上のMSDマニュアルに基づいてデータを収集しますが、収集元のHTML構造が変更されている可能性があります。
>そのため、論文で使用した当時のデータセットと同一の内容が得られるとは限りません。
>ただし、各ファイルの件数が当時のデータセットと近いサイズであれば、正常に動作していると判断できます。
```
pip install -r requirements.txt

bash ./run.sh
```

# 文献情報
* Koki Horiguchi, Tomoyuki Kajiwara, Takashi Ninomiya, Shoko Wakamiya, Eiji Aramaki.  
  MultiMSD: A Corpus for Multilingual Medical Text Simplification from Online Medical References.  
  ACL 2025 Findings. Vienna, Austria. July 2025. [to appear]

* 堀口 航輝, 梶原 智之, 二宮 崇, 若宮 翔子, 荒牧 英治.  
  日本語医療テキスト平易化の訓練用データセットの構築.  
  人工知能学会第38回全国大会, 3S1-OS-7b, 2024. [[PDF](https://confit.atlas.jp/guide/event-img/jsai2024/3S1-OS-7b-04/public/pdf?type=in)]
