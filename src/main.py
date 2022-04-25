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
            word_esp = word.text
            mixed_case = not word_esp.islower() and not word_esp.isupper()
            if mixed_case:
                flag2 = 1
            if word.upos in ["VERB","AUX"] and flag1 == 0:
                for d in dic1:
                    if word_esp.lower() == d or word_esp.lower() == util.elimina_tildes(d):
                        word_lad = dic1[d]
                        if word_esp.lower() in ["he","has","ha","han","hemos"]:
                            pers = word_esp.lower()
                            w = ""
                            aux = 1
                        else:
                            w = word_lad
                        flag1 = 1
            elif flag1 == 0:
                for d in dic2:
                    if word_esp.lower() == d or word_esp.lower() == util.elimina_tildes(d):
                        word_lad = dic2[d]
                        w = word_lad
                        flag1 = 1
            if word.upos in ["VERB","AUX"] and (word.lemma)[-2:] not in ["ar","er","ir"] and flag1 == 0:
                w = util.judeo_parse(word.text)
                flag1 = 1
                flag2 = 0  
            if flag1 == 0:
                if word.upos in ["VERB","AUX"]: 
                    for d in dic1:
                        if word.lemma == d or word.lemma == util.elimina_tildes(d):
                            word_lad = dic1[d]
                            w = util.conj_verb(word, word_lad,aux, pers)
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
                        if word.lemma == d or word.lemma == util.elimina_tildes(d):
                            word_lad = dic2[d]
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
                jud_phrase += w.capitalize() + " "
            else:
                jud_phrase += w + " "
    jud_phrase = unidecode.unidecode(util.fix_phrase(jud_phrase))
    return jud_phrase[0].capitalize()+ jud_phrase[1:]


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
    
    dic_verb = util.get_dic(root_dic)
    print("%i entries"%len(dic_verb))


    print("Reading dictionary of nouns", args.lad_dic_noun)
    
    dic_noun = util.get_dic(root_dic_n)
    print("%i entries"%len(dic_noun))
    

    if args.interactive:
        print("Enter sentence to translate (type 0 to exit):")
        while True:
            in_sent = input()
            if in_sent == '0':
                sys.exit()
            print(translate(in_sent, dic_verb, dic_noun) + '\n')

    elif root_dataset and root_translate and not iscsv:
        print("Translate text")
        with open(root_dataset, 'r', encoding="utf-8") as f_in, open(root_translate, 'w') as f_out:
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
