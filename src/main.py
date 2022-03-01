import stanza
import unidecode
import util
import argparse
import pandas as pd

stanza.download('es')
nlp = stanza.Pipeline('es')


def translate(phrase, dic):
    doc = nlp(phrase)
    jud_phrase = ""
    w = ""
    for sent in doc.sentences:
        for word in sent.words:
            flag1 = 0
            flag2 = 0
            w = ""
            word_esp = word.text
            mixed_case = not word_esp.islower() and not word_esp.isupper()
            if mixed_case:
                flag2 = 1
            for d in dic:
                if word.text.lower() == d["src"]:
                    word_lad = d["target"].replace("\n", "")
                    word_lad = " ".join(word_lad.split())
                    if word.lemma == word_lad or word_esp.lower() == word_lad:
                        w = word_esp
                    else:
                        w = word_lad
                    flag1 = 1
            if flag1 == 0:
                for d in dic:
                    if word.lemma == d["src"]:
                        word_lad = d["target"].replace("\n", "")
                        word_lad = " ".join(word_lad.split())
                        if word.lemma == word_lad or word_esp.lower() == word_lad:
                            w = word_esp
                        elif word.upos == "VERB":
                            w = util.conj_verb(word, word_lad)
                            flag2 = 0
                        elif word.upos in ["NOUN", "ADJ"]:
                            w = util.conj_adj_noun(word, word_lad)
                        elif word.upos == "AUX":
                            w = util.conj_aux(word, word_lad)
                        elif word.upos == "DET":
                            w = word_esp
                        else:
                            w = word_lad
                        flag1 = 1
            if flag1 == 0:
                if word.upos == "PROPN" or word.upos == "DET":
                    w = word.text
                else:
                    w = util.judeo_parse(word_esp)
            if flag2 == 1:
                jud_phrase += w.replace("\n", "").capitalize() + " "
            else:
                jud_phrase += w.replace("\n", "") + " "
    return unidecode.unidecode(util.fix_phrase(jud_phrase))


def main():
    parser = argparse.ArgumentParser("translate Spain <> Ladino")
    parser.add_argument("--d", "--lad_dic", help="Dictionary root.")
    parser.add_argument("--i", "--dataset", help="Dataset to translate.")
    parser.add_argument("--o", "--translate", help="Dataset to translate.")
    args = parser.parse_args()

    if args.lad_dic and args.dataset and args.translate:
        root_dic = args.lad_dic
        root_dataset = args.dataset
        root_translate = args.translate
        file = open(root_dic, 'r', encoding="utf-8")
        lines = file.readlines()
        dic = []
        for line in lines:
            p = {"src": line.split(";")[0], "target": line.split(";")[1]}
            dic.append(p)

        df = pd.read_csv(root_dataset)
        en = []
        es = []
        la = []

        for a in df.index:
            en.append(df["English"][a])
            es.append(df["Spanish"][a])
            la.append(translate(df["Spanish"][a]))
        p = {'English': en, 'Spanish': es, 'Ladino': la}
        df_1 = pd.DataFrame(p)
        df_1.to_csv(root_translate)

if __name__ == '__main__':
    main()
