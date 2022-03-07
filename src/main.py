import stanza
import unidecode
import util
import argparse
import pandas as pd
import sys
from tqdm import tqdm


stanza.download('es')
nlp = stanza.Pipeline('es')

CSV_SPANISH_TAG = "Spanish"
CSV_LADINO_TAG = "Ladino"

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
    parser = argparse.ArgumentParser("translate Spanish <> Judeo-Spanish (Ladino)")
    parser.add_argument("-d", "--lad_dic", help="Dictionary root.", default=None, required=True)
    parser.add_argument("-i", "--input", help="Sentence segmented text file to translate", default=None)
    parser.add_argument("-o", "--output", help="Output path", default=None)
    parser.add_argument("-v", "--interactive", help="Interactive translator", default=False, action='store_true')
    parser.add_argument("-c", "--csv", help="Translate dataset CSV with EN, ES columns", default=False, action='store_true')
    args = parser.parse_args()

    root_dic = args.lad_dic
    root_dataset = args.input
    root_translate = args.output
    iscsv = args.csv

    if not args.lad_dic:
        print("ERROR: No dictionary given.")
        sys.exit()

    print("Reading dictionary", args.lad_dic)

    with open(root_dic, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        dic = []
        for line in lines:
            p = {"src": line.split(";")[0], "target": line.split(";")[1]}
            dic.append(p)
    print("%i entries"%len(dic))

    if args.interactive:
        print("Enter sentence to translate (type 0 to exit):")
        while True:
            in_sent = input()
            if in_sent == '0':
                sys.exit()
            print(translate(in_sent, dic) + '\n')

    elif root_dataset and root_translate and not iscsv:
        print("Translate text")
        with open(root_dataset, 'r') as f_in, open(root_translate, 'w') as f_out:
            translate_iter = f_in.readlines()
            with tqdm(total=translate_iter) as pbar:
                for l in translate_iter:
                    f_out.write(translate(l, dic) + '\n')
                    pbar.update(1)

    elif root_dataset and root_translate and iscsv:
        df = pd.read_csv(root_dataset, sep='\t')
        translate_iter = df[CSV_SPANISH_TAG]
        lad_translations = []
        with tqdm(total=translate_iter) as pbar:
            for a in translate_iter:
                lad_translations.append(translate(a, dic))
                pbar.update(1)
        df[CSV_LADINO_TAG] = lad_translations
        df.to_csv(root_translate, sep='\t', index=False)
    else:
        print("ERROR: No sentence or dataset given.")

if __name__ == '__main__':
    main()
