import MeCab
import re
import random
import configparser

# config.iniの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
cfg = config_ini['DEFAULT']

def extract_message(path, username, state_size, random_linebreak):
    name = "\t" + username + "\t"
    name_length = len(username)

    wakati = MeCab.Tagger('-Owakati')

    # 特定の人のメッセージだけ取り出す
    with open(path, 'r') as file:
        lines = [line for line in file.read().split('\n') if name in line]
    
    # 学習に適した本文だけを取り出す
    messages = []

    for line in lines:
        message = line[line.index('\t')+name_length+2:]

        # スタンプや写真、URLを除外
        if re.search(r'\[.*?\]|https?://[^\s]+', message) is not None:
            continue

        w_message = wakati.parse(message).split(' ')

        # 単語の少ない文章を除外
        if len(w_message) <= int(state_size) + 1:
            continue
        
        # 文末に改行を入れるかどうかをランダムに決定
        if random.random()*10 <= int(random_linebreak):
            messages.append(" ".join(w_message[:-1]))
        else:
            messages.append(" ".join(w_message))

    return "".join(messages)

# 学習用のデータを保存
def save_message(messages, state, path):
    with open(path, state) as file:
        file.write(messages) 

text = extract_message(cfg['load_path'], cfg['username'], cfg['state_size'], cfg['random_linebreak'])
save_message(text, 'w', cfg['save_path'])
text = extract_message(cfg['load_path'], cfg['username'], cfg['state_size'], cfg['random_linebreak'])
save_message(text, 'a', cfg['save_path'])
text = extract_message(cfg['load_path'], cfg['username'], cfg['state_size'], cfg['random_linebreak'])
save_message(text, 'a', cfg['save_path'])