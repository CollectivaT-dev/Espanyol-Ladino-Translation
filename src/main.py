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


def translate(phrase, dic1, dic2):      
    phrase = phrase[0].lower() + phrase[1:]
    doc = nlp(phrase)
    jud_phrase = ""
    w = ""
    aux = 0
    pers = ""
    for sent in doc.sentences:
        for word in sent.words:
            flag1 = 0
            flag2 = 0
            w = ""
            if word.upos in ["VERB","AUX"] and (word.lemma)[-2:] not in ["ar","er","ir"]:
                w = util.judeo_parse(word.text)
                flag1 = 1
                flag2 = 0
            
            word_esp = word.text
            mixed_case = not word_esp.islower() and not word_esp.isupper()
            if mixed_case:
                flag2 = 1
            if word.upos in ["VERB","AUX"] and flag1 == 0:
                for d in dic1:
                    if word_esp.lower() == d["src"] or word_esp.lower() == util.elimina_tildes(d["src"]):
                        word_lad = d["target"].replace("\n", "")
                        if word_esp.lower() in ["he","has","ha","han","hemos"]:
                            pers = word_esp.lower()
                            w = ""
                            aux = 1
                        else:
                            w = word_lad
                        flag1 = 1
            elif flag1 == 0:
                for d in dic2:
                    if word_esp.lower() == d["src"] or word_esp.lower() == util.elimina_tildes(d["src"]):
                        word_lad = d["target"].replace("\n", "")
                        w = word_lad
                        flag1 = 1
            if flag1 == 0:
                if word.upos in ["VERB","AUX"]: 
                    for d in dic1:
                        if word.lemma == d["src"] or word.lemma == util.elimina_tildes(d["src"]):
                            word_lad = d["target"].replace("\n", "")
                            w = util.conj_verb(word, word_lad,aux, pers)
                            w = util.judeo_parse(w.lower())
                            aux = 0
                            flag1 = 1
                            break
                    if flag1 == 0:
                        w = util.conj_verb(word, word.lemma,aux, pers)
                        w = util.judeo_parse(w)
                        aux = 0
                        flag1 = 1
                else: 
                    for d in dic2:
                        if word.lemma == d["src"] or word.lemma == util.elimina_tildes(d["src"]):
                            word_lad = d["target"].replace("\n", "")
                            if word.lemma == word_lad or word_esp.lower() == word_lad:
                                w = word_esp
                            elif word.upos in ["NOUN", "ADJ"]:
                                w = util.conj_adj_noun(word, word_lad)
                            elif word.upos == "DET":
                                w = word_esp
                            else:
                                w = word_lad
                            flag1 = 1
                            break           
            if flag1 == 0:
                if word.upos == "PROPN" or word.upos == "DET":
                    w = util.judeo_parse(word.text)
                else:
                    w = util.judeo_parse(word_esp)
            if flag2 == 1:
                jud_phrase += w.replace("\n", "").capitalize() + " "
            else:
                jud_phrase += w.replace("\n", "") + " "
    return unidecode.unidecode(util.fix_phrase(jud_phrase)).capitalize()


def main():
    parser = argparse.ArgumentParser("translate Spanish <> Judeo-Spanish (Ladino)")
    parser.add_argument("-dv", "--lad_dic_verb", help="Dictionary of verbs.", default=None, required=True)
    parser.add_argument("-dw", "--lad_dic_noun", help="Dictionary of words.", default=None, required=True)
    parser.add_argument("-i", "--input", help="Sentence segmented text file to translate", default=None)
    parser.add_argument("-o", "--output", help="Output path", default=None)
    parser.add_argument("-v", "--interactive", help="Interactive translator", default=False, action='store_true')
    parser.add_argument("-c", "--csv", help="Translate dataset CSV with EN, ES columns", default=False, action='store_true')
    args = parser.parse_args()

    root_dic = args.lad_dic_verb
    root_dic_n = args.lad_dic_noun
    root_dataset = args.input
    root_translate = args.output
    iscsv = args.csv

    if not args.lad_dic_verb:
        print("ERROR: No dictionary given.")
        sys.exit()
        
    if not args.lad_dic_noun:
        print("ERROR: No dictionary given.")
        sys.exit()   
        

    print("Reading dictionary of verbs", args.lad_dic_verb)
    

    with open(root_dic, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        dic_verb = []
        for line in lines:
            p = {"src": line.split(";")[0], "target": line.split(";")[1]}
            dic_verb.append(p)
    print("%i entries"%len(dic))


    print("Reading dictionary of nouns", args.lad_dic_noun)
    
    with open(root_dic_n, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        dic_noun = []
        for line in lines:
            p = {"src": line.split(";")[0], "target": line.split(";")[1]}
            dic_noun.append(p)
    print("%i entries"%len(dic))


    if args.interactive:
        print("Enter sentence to translate (type 0 to exit):")
        while True:
            in_sent = input()
            if in_sent == '0':
                sys.exit()
            print(translate(in_sent, dic_verb, dic_noun) + '\n')

    elif root_dataset and root_translate and not iscsv:
        print("Translate text")
        with open(root_dataset, 'r') as f_in, open(root_translate, 'w') as f_out:
            translate_iter = f_in.readlines()
            with tqdm(total=len(translate_iter)) as pbar:
                for l in translate_iter:
                    f_out.write(translate(l, dic_verb, dic_noun) + '\n')
                    pbar.update(1)

    elif root_dataset and root_translate and iscsv:
        df = pd.read_csv(root_dataset, sep='\t')
        translate_iter = df[CSV_SPANISH_TAG]
        lad_translations = []
        with tqdm(total=translate_iter) as pbar:
            for a in translate_iter:
                lad_translations.append(translate(a, dic_verb, dic_noun))
                pbar.update(1)
        df[CSV_LADINO_TAG] = lad_translations
        df.to_csv(root_translate, sep='\t', index=False)
    else:
        print("ERROR: No sentence or dataset given.")

if __name__ == '__main__':
    main()
