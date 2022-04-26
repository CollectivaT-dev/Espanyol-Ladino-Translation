
from ftfy import fix_encoding
import mlconjug3
import unicodedata

default_conjugator = mlconjug3.Conjugator(language='es')

def judeo_parse(word):
    word = word.lower()
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



def conj_aux(aux_esp, aux_lad):
    text_aux = aux_esp.text
    text_aux = text_aux.lower()
    inf_aux = aux_esp.lemma

    suffix = get_suffix(text_aux, inf_aux)

    if "Number=Sing|Person=3|Tense=Imp" in aux_esp.feats:
        aux_lad = aux_lad[:len(aux_lad) - 1] + suffix
    elif "|Number=Sing|Person=3|Tense=Pres|" in aux_esp.feats or \
            "|Number=Sing|Person=1|Tense=Pres|" in aux_esp.feats or \
            "|Number=Plur|Person=3|Tense=Pres|" in aux_esp.feats:
        aux_lad = aux_lad[:len(aux_lad) - 2] + suffix
    return aux_lad


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
    return default_conjugator.conjugate(word).conjug_info['Gerundio']['Gerundio Gerondio']['']


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
    tipo = 0
    flag = 0
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
                esp_verb_conj = default_conjugator.conjugate(inf_esp_verb).conjug_info['Condicional'][t][p]
            elif t == "Subjuntivo presente" or t == "Subjuntivo pretérito imperfecto 1":
                esp_verb_conj = default_conjugator.conjugate(inf_esp_verb).conjug_info['Subjuntivo'][t][p]
            else:
                esp_verb_conj = default_conjugator.conjugate(inf_esp_verb).conjug_info['Indicativo'][t][p]
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
                elif inf_lad_verb[-2:].replace("\n","") == "er":
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
                elif inf_lad_verb[-2:].replace("\n","") == "ir":
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