from util import translate, get_dic
import argparse
import pandas as pd
import sys
from tqdm import tqdm
import os
import stanza

stanza.download(lang='es')

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_VERB_DICT = os.path.join(SCRIPT_DIR, "../resource/lista_verbos_ladino_conjugados.txt")
PATH_NOUN_DICT = os.path.join(SCRIPT_DIR, "../resource/lista_palabras_ladino.txt")
PATH_PHRASE_DICT = os.path.join("", "resource/dic_esp_lad_phr_v2.txt")

CSV_SPANISH_TAG = "Spanish"
CSV_LADINO_TAG = "Ladino"

def main():
    parser = argparse.ArgumentParser("translate Spanish <> Judeo-Spanish (Ladino)")
    parser.add_argument("-dv", "--lad_dic_verb", help="Dictionary of verbs.", 
        default=PATH_VERB_DICT, required=False)
    parser.add_argument("-dw", "--lad_dic_noun", help="Dictionary of words.", 
        default=PATH_NOUN_DICT, required=False)
    parser.add_argument("-dp", "--lad_dic_phrase", help="Dictionary of phrases.", 
        default=PATH_PHRASE_DICT, required=False)
    parser.add_argument("-i", "--input", help="Sentence segmented text file to translate", 
        default=None)
    parser.add_argument("-o", "--output", help="Output path", default=None)
    parser.add_argument("-v", "--interactive", help="Interactive translator", 
        default=False, action='store_true')
    parser.add_argument("-c", "--csv", help="Translate dataset CSV with EN, ES columns", 
        default=False, action='store_true')
    args = parser.parse_args()

    root_dic_verb = args.lad_dic_verb
    root_dic_noun = args.lad_dic_noun
    root_dic_phrase = args.lad_dic_phrase
    root_dataset = args.input
    root_translate = args.output
    iscsv = args.csv


    print("Reading dictionary of verbs", root_dic_verb)
    
    dic_verb = get_dic(root_dic_verb)
    print("%i entries"%len(dic_verb))


    print("Reading dictionary of nouns", root_dic_noun)
    
    dic_noun = get_dic(root_dic_noun)
    print("%i entries"%len(dic_noun))

    print("Reading dictionary of phrases", root_dic_phrase)
    
    dic_phrase = get_dic(root_dic_phrase)
    print("%i entries"%len(dic_phrase))
    

    if args.interactive:
        print("Enter sentence to translate (type 0 to exit):")
        while True:
            in_sent = input()
            if in_sent == '0':
                sys.exit()
            print(translate(in_sent, dic_verb, dic_noun, dic_phrase) + '\n')

    elif root_dataset and root_translate and not iscsv:
        print("Translate text")
        with open(root_dataset, 'r', encoding="utf-8") as f_in, open(root_translate, 'w') as f_out:
            translate_iter = f_in.readlines()
            with tqdm(total=len(translate_iter)) as pbar:
                for l in translate_iter:
                    f_out.write(translate(l, dic_verb, dic_noun, dic_phrase) + '\n')
                    pbar.update(1)

    elif root_dataset and root_translate and iscsv:
        df = pd.read_csv(root_dataset, sep='\t')
        translate_iter = df[CSV_SPANISH_TAG]
        lad_translations = []
        with tqdm(total=translate_iter) as pbar:
            for a in translate_iter:
                lad_translations.append(translate(a, dic_verb, dic_noun, dic_phrase))
                pbar.update(1)
        df[CSV_LADINO_TAG] = lad_translations
        df.to_csv(root_translate, sep='\t', index=False)
    else:
        print("ERROR: No sentence or dataset given.")

if __name__ == '__main__':
    main()
