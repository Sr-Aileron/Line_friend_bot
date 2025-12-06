[解説記事](https://zenn.dev/sr_aileron/articles/4f2c10e13c91c2)

## config.ini
state_size : Markovify.NewLineText() の state_size に対応
random_linebreak : 改行をスキップする確率(0-10)
username : 学習させたい送信者の名前
load_path : 整形前のテキストファイルのパス
save_path : 整形後のテキストファイルのパス
number_of_generation : 生成する文章の数

## raw.txt
LINEでエクスポートしたトーク履歴をそのまま貼り付ける

## text_extraction.py
raw.txtを変換する

## extracted.txt
変換後の学習用データ

## main.py
bot本体

