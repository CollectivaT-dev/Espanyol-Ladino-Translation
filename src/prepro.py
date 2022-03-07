import nltk
import pandas as pd
import main as m
from tqdm import tqdm

def get_dataset(url):
    text = []
    file = open(url, 'r', encoding="utf-8")
    lines = file.readlines()
    for line in lines:
        text.append(line.replace("\n", ""))
    return text


def main():

    file1 = open('resource/dic_esp_lad_v3.txt', 'r', encoding="utf-8")
    Lines = file1.readlines()
    dic = []
    for l in Lines:
        p = {"src": l.split(";")[0], "target": l.split(";")[1]}
        dic.append(p)

    sentences_es = get_dataset("resource/Europarl.en-es.es")
    sentences_en = get_dataset("resource/Europarl.en-es.en")

    en = []
    es = []
    la = []
    s = []
    flag = 0
    print("Now translate...")
    count = 1
    translate_iter = zip(sentences_es, sentences_en)
    total = min(len(sentences_es), len(sentences_en))
    with tqdm(total=total) as pbar:
        for a, b in translate_iter:
            if count > 0:
                en.append(b)
                es.append(a)
                la.append(m.translate(a, dic))
                s.append("Europarl")
                flag = flag + 1
                if flag % 500 == 0:
                    p = {'Source': s, 'English': en, 'Spanish': es, 'Ladino': la}
                    df_1 = pd.DataFrame(p)
                    df_1.to_csv("resource/dataset.csv")
                    print("Save...")
            else:
                break
            count = count + 1
            pbar.update(1)
        pbar.close()
    p = {'Source': s, 'English': en, 'Spanish': es, 'Ladino': la}
    df_1 = pd.DataFrame(p)
    df_1.to_csv("resource/dataset.csv")

if __name__ == '__main__':
    main()
