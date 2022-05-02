import pandas as pd
from tqdm import tqdm
import argparse
import sys
import os
from util import translate, get_dic
import stanza


stanza.download(lang='es')

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_VERB_DICT = os.path.join(SCRIPT_DIR, "../resource/lista_verbos_ladino_conjugados.txt")
PATH_NOUN_DICT = os.path.join(SCRIPT_DIR, "../resource/lista_palabras_ladino.txt")
PATH_PHRASE_DICT = os.path.join("", "resource/dic_esp_lad_phr_v2.txt")


def get_dataset(url):
    with open(url, 'r', encoding="utf8", errors='ignore') as lines:
        value = [line.replace("\n","") for line in lines]
    return dict(zip(range(len(value)), value))


def find_all(name, path):
    result = []
    counter = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.find(name) != -1:
                text = get_dataset(path+file)
                counter = counter + len(text)
                result.append(os.path.join(root, name))
    return len(result), counter


def main():
    parser = argparse.ArgumentParser("translate Spanish <> Judeo-Spanish (Ladino)")
    parser.add_argument("-dv", "--lad_dic_verb", help="Dictionary of verbs.", 
        default=PATH_VERB_DICT, required=False)
    parser.add_argument("-dw", "--lad_dic_noun", help="Dictionary of words.", 
        default=PATH_NOUN_DICT, required=False)
    parser.add_argument("-dp", "--lad_dic_phrase", help="Dictionary of phrases.", 
        default=PATH_PHRASE_DICT, required=False)
    parser.add_argument("-s1", "--input_esp", help="Sentence segmented Spanish text file to translate",
                        default=None)
    parser.add_argument("-s2", "--input_2", help="Sentence segmented other language text file",
                        default=None)
    parser.add_argument("-n", "--language", help="second language name",
                        default=None)
    parser.add_argument("-o", "--output", help="Output path", default=None)
    args = parser.parse_args()


    root_dic_verb = args.lad_dic_verb
    root_dic_noun = args.lad_dic_noun
    root_dic_phrase = args.lad_dic_phrase
    root_dataset_1 = args.input_esp
    root_dataset_2 = args.input_2
    root_translate = args.output
    language = args.language

    if not os.path.exists(root_translate):
        print("Creating directory")
        os.makedirs(root_translate)
        
    print("Reading dictionary of verbs", root_dic_verb)
    
    dic_verb = get_dic(root_dic_verb)
    print("%i entries"%len(dic_verb))


    print("Reading dictionary of nouns", root_dic_noun)
    
    dic_noun = get_dic(root_dic_noun)
    print("%i entries"%len(dic_noun))

    print("Reading dictionary of phrases", root_dic_phrase)
    
    dic_phrase = get_dic(root_dic_phrase)
    print("%i entries"%len(dic_phrase))    
        

    outfilename = os.path.basename(root_dataset_1)
    files_n, counter = find_all(outfilename+"_", root_translate)
    outfilepath = os.path.join(root_translate, outfilename+"_"+str(files_n+1) + ".csv")
    print("Output to:", outfilepath)
    

    sentences_es = get_dataset(root_dataset_1)
    sentences_en = get_dataset(root_dataset_2)

    name = root_dataset_2.split("/")[-1]
    name = name.split(".")[0]

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
            if count > counter:
                es.append(sentences_es[a])
                en.append(sentences_en[b])
                la.append(translate(sentences_es[a], dic_verb, dic_noun, dic_phrase))
                s.append(name)
                flag = flag + 1
                if flag % 10 == 0:
                    p = {'Source': s, language: en, 'Spanish': es, 'Ladino': la}
                    df_1 = pd.DataFrame(p)
                    df_1.to_csv(outfilepath, sep='\t', index=False)
                    print("Save...")
            count = count + 1
            pbar.update(1)
        pbar.close()
    
    p = {'Source': s, language: en, 'Spanish': es, 'Ladino': la}
    df_1 = pd.DataFrame(p)
    df_1.to_csv(outfilepath, sep='\t', index=False)

    print("Finished...", outfilepath)

if __name__ == '__main__':
    main()
