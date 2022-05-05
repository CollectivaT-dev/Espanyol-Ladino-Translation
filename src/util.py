from ftfy import fix_encoding
import mlconjug3
import unicodedata
import unidecode
import stanza
import json

default_conjugator = mlconjug3.Conjugator(language='es')
nlp = None
perf_veb = ["he","has","ha","hemos","habéis","han"]
pro_next_verb = ["se","me","le","lo"]
pref_verb_chaing = ["había","habías","había","habíamos","habíais","habían","habré","habrás","habrá","habremos","habréis","habrán","habría","habrías","habría","habríamos","habríais","habrían","haya","hayas","haya","hayamos","hayáis","hayan","hubiera","hubiese","hubieras","hubieses","hubiéramos","hubiésemos","hubierais","hubieseis","hubieran","hubieses"]

def load_stanza_nlp(cachedir=None):
    global nlp
    if cachedir:
        nlp = stanza.Pipeline(lang='es', dir=cachedir)
    else:
        nlp = stanza.Pipeline(lang='es')

def translate(phrase, verb_dic, noun_dic, phrase_dic, stanza_cachedir=None):
    if phrase == "" or str(phrase) == "None":
        return ""
        
    if not nlp:
        load_stanza_nlp(stanza_cachedir)
    
    aux, index, pro_verb, verb, up = 0, -1, 0, 0, 0
    if phrase[0].isupper() == True:
        up = 1
    phrase = phrase[0].lower() + phrase[1:]
    doc = nlp(phrase)
    jud_phrase, pers = "", ""
    for sent in doc.sentences:
        for word in sent.words:
            flag1, flag2, flag3 = 0, 0, 0
            w = ""
            word_esp = word.text
            if word_esp.isupper() or any(ele.isupper() for ele in word_esp[1:]):
                w = word_esp
                flag1, flag2, flag3= 1, 0, 1
            if word_esp[0].isupper() and flag3 == 0:
                flag2 = 1
            mixed_case = not word_esp.islower() and not word_esp.isupper()
            if mixed_case:
                flagd2 = 1
            if  word.upos in ["PRON"] and  word_esp.lower() in pro_next_verb:
                w = word.text
                pro_verb, flag1 = 1, 1
            if word.upos in ["VERB","AUX"] and flag1 == 0:
                #TODO: Make this work with verb_dic.get(word_esp.lower())
                if str(verb_dic.get(word_esp.lower())) != "None":
                    word_lad = str(verb_dic.get(word_esp.lower()))
                    if word_esp.lower() in perf_veb and word.upos in ["AUX"]:
                        index = perf_veb.index(word_esp.lower())
                        pers = word_esp.lower()
                        w = ""
                        aux = 1
                    elif word_esp.lower() in pref_verb_chaing and word.upos in ["AUX"]:    
                        w = word_lad
                        aux = 2
                    elif aux == 1:
                        if word_lad.find("/") != -1:
                            w = word_lad.split("/")[index]                            
                        else:
                            w = word_lad
                        aux = 0
                    elif aux == 2:
                        if word_lad.find("/") != -1:
                            w = word_lad.split("/")[6]
                        else:
                            w = word_lad
                        aux = 0
                    else:
                        w = word_lad
                    verb, flag1, pro_verb= 1, 1, 0
                '''
                for d in verb_dic:
                    if word_esp.lower() == d or word_esp.lower() == elimina_tildes(d):
                        word_lad = verb_dic[d]
                        if word_esp.lower() in perf_veb and word.upos in ["AUX"]:
                            index = perf_veb.index(word_esp.lower())
                            pers = word_esp.lower()
                            w = ""
                            aux = 1
                        elif word_esp.lower() in pref_verb_chaing and word.upos in ["AUX"]:    
                            w = verb_dic[d]
                            aux = 2
                        elif aux == 1:
                            if verb_dic[d].find("/") != -1:
                                w = verb_dic[d].split("/")[index]                            
                            else:
                                w = verb_dic[d]
                            aux = 0
                        elif aux == 2:
                            if verb_dic[d].find("/") != -1:
                                w = verb_dic[d].split("/")[6]
                            else:
                                w = verb_dic[d]
                            aux = 0
                        else:
                            w = word_lad
                        verb, flag1, pro_verb= 1, 1, 0
                        break #TODO: Check if it breaks anything
                 '''
            elif flag1 == 0:
                #TODO: Make this work with noun_dic.get(word_esp.lower())
                if str(noun_dic.get(word_esp.lower())) != "None":
                        w = str(noun_dic.get(word_esp.lower()))
                        flag1, verb = 1, 0
                '''
                for d in noun_dic:
                    if word_esp.lower() == d or word_esp.lower() == elimina_tildes(d):
                        word_lad = noun_dic[d]
                        w = word_lad
                        flag1, verb = 1, 0
                        break #TODO: Check if it breaks anything
                '''
            if word.upos in ["VERB","AUX"] and (word.lemma)[-2:] not in ["ar","er","ir","ír"] and flag1 == 0:
                w = judeo_parse(word.text)
                flag1, flag2, verb, pro_verb= 1, 0, 1, 0
            if flag1 == 0:
                if word.upos in ["VERB","AUX"]: 
                    #TODO: Make this work with verb_dic.get(word_esp.lower())
                    if str(verb_dic.get(word.lemma)) != "None":
                        word_lad = str(verb_dic.get(word.lemma))
                        w = conj_verb(word, word_lad,aux, pers)
                        aux, flag1, verb, pro_verb = 0, 1, 1, 0
                    if flag1 == 0:
                        w = conj_verb(word, word.lemma,aux, pers)
                        w = judeo_parse(w)
                        aux, flag1, verb, pro_verb = 0, 1, 1, 0
                    '''
                    for d in verb_dic:
                        if word.lemma == d or word.lemma == elimina_tildes(d):
                            word_lad = verb_dic[d]
                            w = conj_verb(word, word_lad,aux, pers)
                            aux, flag1, verb, pro_verb = 0, 1, 1, 0
                            break
                    if flag1 == 0:
                        w = conj_verb(word, word.lemma,aux, pers)
                        w = judeo_parse(w)
                        aux, flag1, verb, pro_verb = 0, 1, 1, 0
                    '''
                else: 
                    #TODO: Make this work with noun_dic.get(word_esp.lower())
                    if str(noun_dic.get(word.lemma)) != "None":
                        word_lad = str(noun_dic.get(word.lemma))
                        if word.lemma == word_lad or word_esp.lower() == word_lad:
                            w = word_esp
                        elif word.upos in ["NOUN", "ADJ"]:
                            w = conj_adj_noun(word, word_lad)
                        elif word.upos == "DET":
                            w = word_esp
                        else:
                            w = word_lad
                        flag1, verb = 1, 0
                    '''
                    for d in noun_dic:
                        if word.lemma == d or word.lemma == elimina_tildes(d):
                            word_lad = noun_dic[d]
                            if word.lemma == word_lad or word_esp.lower() == word_lad:
                                w = word_esp
                            elif word.upos in ["NOUN", "ADJ"]:
                                w = conj_adj_noun(word, word_lad)
                            elif word.upos == "DET":
                                w = word_esp
                            else:
                                w = word_lad
                            flag1, verb = 1, 0
                            break
                    '''
            if flag1 == 0:
                if word.upos == "PROPN" or word.upos == "DET":
                    w = judeo_parse(word.text)
                    verb = 0
                else:
                    w = judeo_parse(word_esp)
                    verb = 0
            if flag2 == 1:
                jud_phrase += w.capitalize() + " "
            else:
                if pro_verb == 1 and verb == 1:
                    jud_phrase = "".join([jud_phrase[:-1], w, " "]) 
                    pro_verb = 0
                else:
                    jud_phrase += w + " "
    jud_phrase = unidecode.unidecode(fix_phrase(jud_phrase, phrase_dic))
    if up == 1:
        jud_phrase = "".join([jud_phrase[0].capitalize(), jud_phrase[1:]]) 
    return jud_phrase


def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])


def judeo_parse(word):
    word = word.lower()
    if word.find("h") != -1:
        indices = [pos for pos, char in enumerate(word) if char == "h"]
        for h in indices:
            if h == 0:
                word = replace_str_index(word,h,"*")
            if h > 1 and word[h-1] not in ["c","s"]:
                word = replace_str_index(word,h,"*")
        word = word.replace("*","")
    if word.find("ca") != -1:
        word = word.replace("ca", "ka")
    if word.find("co") != -1:
        word = word.replace("co", "ko")
    if word.find("cu") != -1:
        word = word.replace("cu", "ku") 
    if word.find("ñ") != -1:
        word = word.replace("ñ", "ny")
    if word.find("qu") != -1:
        word = word.replace("qu", "k")
    if word.find("rd") != -1:
        word = word.replace("rd", "dr")
    if word.find("cr") != -1:
        word = word.replace("cr", "kr")
    if word.find("ll") != -1:
        word = word.replace("ll", "y")
    if word.find("ge") != -1:
        word = word.replace("ge", "dje")
    if word.find("gi") != -1:
        word = word.replace("gi", "dji")
    if word.find("cir") != -1:
        word = word.replace("cir", "zir")
    if word.find("ción") != -1:
        word = word.replace("ción", "sion")
    if word.find("ce") != -1:
        word = word.replace("ce", "se")
    if word.find("ci") != -1:
        word = word.replace("ci", "si")
    if word.find("gu") != -1:
        word = word.replace("gu", "g")
    if word.find("sc") != -1:
        word = word.replace("sc", "s")
    if word.find("zar") != -1:
        word = word.replace("zar", "sar")
    if word.find("ct") != -1:
        word = word.replace("ct", "kt")
    if word.find("x") != -1:
        word = word.replace("x", "ks")
    if word.find("ee") != -1:
        word = word.replace("ee", "ye")
    if word.find("yy") != -1:
        word = word.replace("yy", "y")
    return word


def complete_word(word_1, word_2):
    for f in range(len(word_1) - len(word_2)):
        word_2 = word_2 + " "
    return word_2


def get_suffix(real_verb, inf_verb):
    flag_1 = 0
    flag_2 = 99
    word_1 = ""
    word_2 = ""
    words = [real_verb, inf_verb]

    for word in words:
        if len(word) > flag_1:
            word_1 = word
            flag_1 = len(word)
        if len(word) < flag_2:
            word_2 = word
            flag_2 = len(word)

    word_2 = complete_word(word_1, word_2)

    suffix_vec = []
    for x, y in zip(word_1, word_2):
        if x != y:
            suffix_vec.append(x)

    suffix = ''.join([str(elem) for elem in suffix_vec])
    return suffix


def conj_adj_noun(word_esp, word_lad):
    text_esp = word_esp.text
    if str(word_esp.feats) != "None":
        if "Sing" in word_esp.feats:
            word_lad = word_lad
        elif "Plur" in word_esp.feats:
            if (text_esp[-2:].find("a") != -1 and word_lad[-2:].find("a") != -1) or \
                    (text_esp[-2:].find("o") != -1 and word_lad[-2:].find("o") != -1):
                suffix_esp = text_esp[len(text_esp) - 2:]
                root_lad = word_lad[:len(word_lad) - 1]
                word_lad = root_lad + suffix_esp
            elif word_esp.text[-1].find("s") != -1:
                if word_esp.text[-2:] == "es" and word_lad[-1] != "e":
                    word_lad = word_lad + "es"
                elif word_esp.text[-3:] == "ses" or word_esp.text[-2:] == "es":
                    word_lad = word_lad[:len(word_lad) - 1] + "es"
                else:
                    word_lad = word_lad + "s"
            else:
                word_lad = word_lad + "s"
    return word_lad


def fix_phrase(phrase, phrase_dict):
    phrase = " "+phrase+" "
    if phrase.find(" ay ke ") != -1:
        phrase = phrase.replace(" ay ke "," kale ")
    if phrase.find(" tengo ke ") != -1:
        phrase = phrase.replace(" tengo ke "," devo de ")
    if phrase.find(" tyenes ke ") != -1:
        phrase = phrase.replace(" tyenes ke "," deves de ")
    if phrase.find(" tyene ke ") != -1:
        phrase = phrase.replace(" tyene ke "," deve de ")
    if phrase.find(" tenemos ke ") != -1:
        phrase = phrase.replace(" tenemos ke "," devemos de ")
    if phrase.find(" tenesh ke ") != -1:
        phrase = phrase.replace(" tenesh ke "," devesh de ")
    if phrase.find(" tyenen ke ") != -1:
        phrase = phrase.replace(" tyenen ke "," deven de ")
    phrase = phrase.replace(" .", ".").replace(" ?", "?")\
        .replace(" !", "!").replace(" ,", ",")\
        .replace('" ', '"').replace(" ;", ";").replace("¿ ", "")\
        .replace("¡ ", "").replace("Qué ","Ke ").replace("Cuánto ","Kuanto ")
    for key in phrase_dict:
        if phrase.find(" "+key+" ") != -1:
            phrase = phrase.replace(" "+key+" "," "+phrase_dict[key]+" ")
            break
    phrase = " ".join(phrase.split())
    return phrase


def get_dic(root):
    with open(root, 'r', encoding="utf-8") as lines:
            key, value = zip(*[(line.split(";")[0],line.split(";")[1].replace("\n","")) for line in lines])
    return dict(zip(key, value))


def get_gerundio(word):
    try:
        return default_conjugator.conjugate(word).conjug_info['Gerundio']['Gerundio Gerondio']['']
    except:
    	return get_gerundio_esp(word)


def get_gerundio_esp(word):
    pl = " "
    if len(word.split(" ")) > 1:
        word = word.split(" ")[0]
        f = 0
        for i in word.split(" "):
            if f != 0: 
                pl = pl + i + " "
            f = f + 1
    if word[-2:].replace("\n","") == "ar":
        word = word[:-2]+"ando"
    elif word[-2:].replace("\n","") in ["er","ir"]:
        word = word[:-2]+"iendo"
    return word+pl.rstrip()


def get_gerundio_lad(word):
    pl = " "
    if len(word.split(" ")) > 1:
        word = word.split(" ")[0]
        f = 0
        for i in word.split(" "):
            if f != 0: 
                pl = pl + i + " "
            f = f + 1
    if word[-2:].replace("\n","") == "ar":
        word = word[:-2]+"ando"
    elif word[-2:].replace("\n","") in ["er","ir"]:
        word = word[:-2]+"yendo"
    return word+pl.rstrip()
    
    
def get_conj_noun(word, word_lad):
    word_esp = word_esp.text
    word_lad = judeo_parse(word_esp)
    return word_lad

def get_participio(word):
    if word[-2:] == "ar":
        word = word[:-2]+"ado"
    elif word[-2:] in ["er","ir"]:
        word = word[:-2]+"ido"
    return word


def change_person_number(per):
    per_num = 0
    if per == "1s":
        per_num = 0
    elif per == "2s":
        per_num = 1
    elif per == "3s":
        per_num = 2
    elif per == "1p":
        per_num = 3
    elif per == "2p":
        per_num = 4
    elif per == "3p":
        per_num = 5
    return per_num


def change_aux_number(aux):
    aux = str(aux)
    per_num = 0
    if aux == "he":
        per_num = 0
    elif aux == "has":
        per_num = 1
    elif aux == "ha":
        per_num = 2
    elif aux == "hemos":
        per_num = 3
    elif aux == "habéis":
        per_num = 4
    elif aux == "han":
        per_num = 5
    return per_num
    

def elimina_tildes(word):
    word = str(word)
    word = word.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    return word


def conj_verb(verb_esp, inf_lad_verb, aux, pers):
    tipo, flag = 0, 0
    tempo = ["Indicativo presente", "Indicativo pretérito imperfecto","Indicativo pretérito perfecto simple","Indicativo futuro","Condicional Condicional","Subjuntivo presente","Subjuntivo pretérito imperfecto 1"]
    person = ["1s","2s","3s","1p","2p","3p"]
    data = ["o","as","a","amos","ash","an"]
    pers = change_aux_number(pers)
    esp_verb = verb_esp.text
    esp_verb = esp_verb.lower()
    inf_esp_verb = verb_esp.lemma
    for t in tempo:
        for p in person:
            esp_verb_conj = ""
            if t == "Condicional Condicional":
                try:
                    esp_verb_conj = default_conjugator.conjugate(inf_esp_verb).conjug_info['Condicional'][t][p]
                except:
                    esp_verb_conj = inf_esp_verb
            elif t == "Subjuntivo presente" or t == "Subjuntivo pretérito imperfecto 1":
                try:
                    esp_verb_conj = default_conjugator.conjugate(inf_esp_verb).conjug_info['Subjuntivo'][t][p]
                except:
                    esp_verb_conj = inf_esp_verb
            else:
                try:
                    esp_verb_conj = default_conjugator.conjugate(inf_esp_verb).conjug_info['Indicativo'][t][p]
                except:
                    esp_verb_conj = inf_esp_verb
            esp_verb_conj = str(esp_verb_conj)
            if str(esp_verb_conj) != "None":
                esp_verb_conj = fix_encoding(esp_verb_conj)
            if tipo == 0:
                if inf_lad_verb[-2:].replace("\n","") == "ar":
                    if t == "Indicativo presente":
                        data = ["o","as","a","amos","ash","an"]
                    elif t == "Indicativo pretérito imperfecto":
                        data = ["ava","avas","ava","avamos","avash","avan"]
                    elif t == "Indicativo pretérito perfecto simple":
                        data = ["i","ates","o","imos","atesh","aron"]
                    elif t == "Indicativo futuro":
                        data = ["va","vas a","va","vamos a","vash a","van a"]
                    elif t == "Condicional Condicional":
                        data = ["aria","arias","aria","ariamos","ariash","arian"]
                    elif t == "Subjuntivo presente":
                        data = ["e","es","e","emos","esh","en"]
                    elif t == "Subjuntivo pretérito imperfecto 1":
                        data = ["ara","aras","ara","aramos","arash","aran"]
                elif inf_lad_verb[-2:].replace("\n","") in ["er","ér"]:
                    if t == "Indicativo presente":
                        data = ["o","es","e","emos","esh","en"]
                    elif t == "Indicativo pretérito imperfecto":
                        data = ["ia","ias","ia","iamos","iash","ian"]
                    elif t == "Indicativo pretérito perfecto simple":
                        data = ["i","ites","yo","imos","itesh","yeron"]
                    elif t == "Indicativo futuro":
                        data = ["va","vas a","va","vamos a","vash a","van a"]
                    elif t == "Condicional Condicional":
                        data = ["eria","erias","eria","eriamos","eriash","erian"]
                    elif t == "Subjuntivo presente":
                        data = ["a","as","a","amos","ash","an"]
                    elif t == "Subjuntivo pretérito imperfecto 1":
                        data = ["yera","yeras","yera","yeramos","yerash","yeran"]
                elif inf_lad_verb[-2:].replace("\n","") in ["ir","ír"]:
                    if t == "Indicativo presente":
                        data = ["o","es","e","imos","ish","en"]
                    elif t == "Indicativo pretérito imperfecto":
                        data = ["ia","ias","ia","iamos","iash","ian"]
                    elif t == "Indicativo pretérito perfecto simple":
                        data = ["i","ites","yo","imos","itesh","yeron"]
                    elif t == "Indicativo futuro":
                        data = ["va","vas a","va","vamos a","vash a","van a"]
                    elif t == "Condicional Condicional":
                        data = ["iria","irias","iria","iriamos","iriash","irian"]
                    elif t == "Subjuntivo presente":
                        data = ["a","as","a","amos","ash","an"]
                    elif t == "Subjuntivo pretérito imperfecto 1":
                        data = ["yera","yeras","yera","yeramos","yerash","yeran"]
            per = change_person_number(p)
            if t == "Indicativo pretérito perfecto simple" and aux == 1 and per == pers:
                inf_lad_verb = inf_lad_verb[:-2]+data[per]
                flag = 1
                break
            if esp_verb_conj == esp_verb:
                if t == "Indicativo futuro":
                    inf_lad_verb = data[per]+" "+inf_lad_verb
                else:
                    inf_lad_verb = inf_lad_verb[:-2]+data[per]
                flag = 1
                break
        if flag == 1:
            break
    if flag == 1:
        return inf_lad_verb
    else:
        ger_esp_verb = get_gerundio(inf_esp_verb)
        if esp_verb == ger_esp_verb:
            ger_lad_verb = get_gerundio_lad(inf_lad_verb)
            return ger_lad_verb
        else:
            participio_esp_verb = get_participio(inf_esp_verb)
            if esp_verb == participio_esp_verb:
                part_lad_verb = get_participio(inf_lad_verb)
                return part_lad_verb
            else:
                return esp_verb