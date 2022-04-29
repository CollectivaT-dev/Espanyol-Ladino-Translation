import stanza
import unidecode
import util
import argparse
import pandas as pd
import sys
from tqdm import tqdm
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_VERB_DICT = os.path.join(SCRIPT_DIR, "../resource/lista_verbos_ladino_conjugados.txt")
PATH_NOUN_DICT = os.path.join(SCRIPT_DIR, "../resource/lista_palabras_ladino.txt")
PATH_PHRASE_DICT = os.path.join("", "resource/dic_esp_lad_phr_v2.txt")

stanza.download('es')
nlp = stanza.Pipeline('es')

CSV_SPANISH_TAG = "Spanish"
CSV_LADINO_TAG = "Ladino"


def translate(phrase, verb_dic, noun_dic, phrase_dic):
    up = 0
    if phrase[0].isupper() == True:
        up = 1
    phrase = phrase[0].lower() + phrase[1:]
    doc = nlp(phrase)
    jud_phrase = ""
    w = ""
    aux = 0
    pers = ""
    index = -1
    perf_veb = ["he","has","ha","hemos","habéis","han"]
    pro_next_verb = ["se","me"]
    pro_verb = 0
    verb = 0
    for sent in doc.sentences:
        for word in sent.words:
            flag1 = 0
            flag2 = 0
            w = ""
            word_esp = word.text
            if word_esp.isupper() or any(ele.isupper() for ele in word_esp[1:]):
                w = word_esp
                flag1 = 1
                flag2 = 0
            mixed_case = not word_esp.islower() and not word_esp.isupper()
            if mixed_case:
                flagd2 = 1
            if  word.upos in ["PRON"] and  word_esp.lower() in pro_next_verb:
                w = word.text
                pro_verb = 1
                flag1 = 1
            if word.upos in ["VERB","AUX"] and flag1 == 0:
                #TODO: Make this work with verb_dic.get(word_esp.lower())
                for d in verb_dic:
                    if word_esp.lower() == d or word_esp.lower() == util.elimina_tildes(d):
                        word_lad = verb_dic[d]
                        if word_esp.lower() in perf_veb and word.upos in ["AUX"]:
                            index = perf_veb.index(word_esp.lower())
                            pers = word_esp.lower()
                            w = ""
                            aux = 1
                        elif word_esp.lower() in ["había","habías","había","habíamos","habíais","habían","habré","habrás","habrá","habremos","habréis","habrán","habría","habrías","habría","habríamos","habríais","habrían","haya","hayas","haya","hayamos","hayáis","hayan","hubiera","hubiese","hubieras","hubieses","hubiéramos","hubiésemos","hubierais","hubieseis","hubieran","hubieses"] and word.upos in ["AUX"]:    
                            w = verb_dic[d]
                            aux = 2
                        elif aux == 1:
                            w = verb_dic[d].split("/")[index]
                            aux = 0
                        elif aux == 2:
                            w = verb_dic[d].split("/")[6]
                            aux = 0
                        else:
                            w = word_lad
                        verb = 1
                        flag1 = 1
                        pro_verb = 0
                        break #TODO: Check if it breaks anything
            elif flag1 == 0:
                #TODO: Make this work with noun_dic.get(word_esp.lower())
                for d in noun_dic:
                    if word_esp.lower() == d or word_esp.lower() == util.elimina_tildes(d):
                        word_lad = noun_dic[d]
                        w = word_lad
                        flag1 = 1
                        verb = 0
                        break #TODO: Check if it breaks anything
            if word.upos in ["VERB","AUX"] and (word.lemma)[-2:] not in ["ar","er","ir"] and flag1 == 0:
                w = util.judeo_parse(word.text)
                flag1 = 1
                flag2 = 0
                verb = 1
                pro_verb = 0
            if flag1 == 0:
                if word.upos in ["VERB","AUX"]: 
                    #TODO: Make this work with verb_dic.get(word_esp.lower())
                    for d in verb_dic:
                        if word.lemma == d or word.lemma == util.elimina_tildes(d):
                            word_lad = verb_dic[d]
                            w = util.conj_verb(word, word_lad,aux, pers)
                            aux = 0
                            flag1 = 1
                            verb = 1
                            pro_verb = 0
                            break
                    if flag1 == 0:
                        w = util.conj_verb(word, word.lemma,aux, pers)
                        w = util.judeo_parse(w)
                        aux = 0
                        flag1 = 1
                        verb = 1
                        pro_verb = 0
                else: 
                    #TODO: Make this work with noun_dic.get(word_esp.lower())
                    for d in noun_dic:
                        if word.lemma == d or word.lemma == util.elimina_tildes(d):
                            word_lad = noun_dic[d]
                            if word.lemma == word_lad or word_esp.lower() == word_lad:
                                w = word_esp
                            elif word.upos in ["NOUN", "ADJ"]:
                                w = util.conj_adj_noun(word, word_lad)
                            elif word.upos == "DET":
                                w = word_esp
                            else:
                                w = word_lad
                            flag1 = 1
                            verb = 0
                            break           
            if flag1 == 0:
                if word.upos == "PROPN" or word.upos == "DET":
                    w = util.judeo_parse(word.text)
                    verb = 0
                else:
                    w = util.judeo_parse(word_esp)
                    verb = 0
            if flag2 == 1:
                jud_phrase += w.capitalize() + " "
            else:
                if pro_verb == 1 and verb == 1:
                    jud_phrase = jud_phrase[:-1] + w + " "
                    pro_verb = 0
                else:
                    jud_phrase += w + " "
    jud_phrase = unidecode.unidecode(util.fix_phrase(jud_phrase, phrase_dic))
    if up == 1:
        jud_phrase = jud_phrase[0].capitalize()+ jud_phrase[1:]
    return jud_phrase


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

    if not args.lad_dic_verb:
        print("ERROR: No dictionary given.")
        sys.exit()
        
    if not args.lad_dic_noun:
        print("ERROR: No dictionary given.")
        sys.exit()   
        

    print("Reading dictionary of verbs", root_dic_verb)
    
    dic_verb = util.get_dic(root_dic_verb)
    print("%i entries"%len(dic_verb))


    print("Reading dictionary of nouns", root_dic_noun)
    
    dic_noun = util.get_dic(root_dic_noun)
    print("%i entries"%len(dic_noun))

    print("Reading dictionary of phrases", root_dic_phrase)
    
    dic_phrase = util.get_dic(root_dic_phrase)
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
