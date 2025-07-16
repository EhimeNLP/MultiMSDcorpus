python3 scripts/preprocess/file_concat_base.py ja
for lang in de en es fr it pt ru zh;
do
    python3 scripts/preprocess/file_concat.py $lang
done

for lang in de en es fr it ja pt ru zh;
do
    python3 scripts/preprocess/preprocess.py $lang train
    python3 scripts/preprocess/preprocess.py $lang dev
    python3 scripts/preprocess/preprocess.py $lang test
done