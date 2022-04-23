from spanishconjugator import Conjugator
from ftfy import fix_encoding

def judeo_parse(word):
    if word.find("h") != -1:
        indices = [i for i, x in enumerate(word) if x == "h"]
        for h in indices:
            string_list = list(word)
            if h != 0:
                if word[h - 2] != "c":
                    string_list[h] = ""
            else:
                string_list[0] = ""
        word = "".join(string_list)
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


def conj_verb(verb_esp, verb_lad):
    text_verb = verb_esp.text
    text_verb = text_verb.lower()
    inf_verb = verb_esp.lemma

    if text_verb[-2] in ["ar", "er", "ir"] or "VerbForm=Inf" in verb_esp.feats:
        verb_lad = verb_lad
    else:
        suffix = get_suffix(text_verb, inf_verb)
        if len(suffix) == 0:
            verb_lad = text_verb
        elif "Number=Sing|Person=1|Tense=Past" in verb_esp.feats or \
                "Number=Sing|Person=3|Tense=Past" in verb_esp.feats or \
                "Number=Sing|Person=1|Tense=Pres" in verb_esp.feats:
            root_lad = verb_lad[:len(verb_lad) - 2]
            if len(root_lad) == 0:
                verb_lad = text_verb
            elif root_lad[-1] == suffix[:1]:
                verb_lad = verb_lad[:len(verb_lad) - 3] + suffix
            else:
                verb_lad = verb_lad[:len(verb_lad) - 2] + suffix
        elif "Number=Sing|Person=3|Tense=Fut" in verb_esp.feats or \
                "Number=Sing|Person=1|Tense=Fut" in verb_esp.feats or \
                "Number=Plur|Person=3|Tense=Fut" in verb_esp.feats or \
                "Number=Plur|Person=3|Tense=Past" in verb_esp.feats or \
                "Number=Plur|Person=1|Tense=Fut" in verb_esp.feats:
            verb_lad = verb_lad + suffix
        elif "Number=Sing|Person=2|Tense=Pres" in verb_esp.feats or \
                "Number=Plur|Person=3|Tense=Pres" in verb_esp.feats or \
                "Number=Plur|Person=1|Tense=Pres" in verb_esp.feats or \
                "|Number=Plur|Person=3|Tense=Imp|" in verb_esp.feats:
            verb_lad = verb_lad[:len(verb_lad) - 1] + suffix
    return verb_lad


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


def fix_phrase(phrase):
    file = open('resource/dic_esp_lad_phr_v2.txt', 'r', encoding="utf-8")
    lines = file.readlines()
    for line in lines:
        if phrase.find(line.split(";")[0]) != -1:
            phrase = phrase.replace(line.split(";")[0], line.split(";")[1].replace("\n", ""))
    if phrase.find("del komida") != -1:
        phrase = phrase.replace("del komida", "de la komida")
    phrase = phrase.replace(" .", ".").replace(" ?", "?")\
        .replace(" !", "!").replace(" ,", ",").replace("de el", "del")\
        .replace('" ', '"').replace(" ;", ";").replace("¿ ", "")\
        .replace("¡ ", "").strip()
    phrase = " ".join(phrase.split())
    return phrase


def get_dic(root):
    file = open(root, 'r', encoding="utf-8")
    lines = file.readlines()
    dic = []
    for line in lines:
        p = {"src": line.split(";")[0], "target": line.split(";")[1]}
        dic.append(p)
    return dic


def get_gerundio(word):
    if word[-2:].replace("\n","") == "ar":
        word = word[:-2]+"ando"
    elif word[-2:].replace("\n","") in ["er","ir"]:
        if len(word) > 2:
            if word[-3] in ["ñ","ll"]:
                word = word[:-2]+"endo"
            else:
                word = word[:-2]+"iendo"
        else:
            word = word[:-2]+"iendo"
    return word


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
    if per == "yo":
        per_num = 0
    elif per == "tu":
        per_num = 1
    elif per == "usted":
        per_num = 2
    elif per == "nosotros":
        per_num = 3
    elif per == "vosotros":
        per_num = 4
    elif per == "ustedes":
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
    

def conj_verb(verb_esp, inf_lad_verb, aux, pers):
    tipo = 0
    flag = 0
    tempo = ["present","imperfect","preterite","future","simple_conditional"]
    person = ["yo","tu","usted","nosotros","vosotros","ustedes"]
    data = ["o","as","a","amos","ash","an"]
    pers = change_aux_number(pers)
    esp_verb = verb_esp.text
    esp_verb = esp_verb.lower()
    inf_esp_verb = verb_esp.lemma
    if verb_esp == inf_lad_verb:
        inf_lad_verb = judeo_parse(inf_esp_verb)
    for t in tempo:
        for p in person:
            esp_verb_conj = ""
            if t == "simple_conditional":
                esp_verb_conj = Conjugator().conjugate(inf_esp_verb,t,"conditional",p)
            else:
                esp_verb_conj = Conjugator().conjugate(inf_esp_verb,t,"indicative",p)
            esp_verb_conj = str(esp_verb_conj)
            if str(esp_verb_conj) != "None":
                esp_verb_conj = fix_encoding(esp_verb_conj)
            if tipo == 0:
                if inf_lad_verb[-2:].replace("\n","") == "ar":
                    if t == "present":
                        data = ["o","as","a","amos","ash","an"]
                    elif t == "imperfect":
                        data = ["ava","avas","ava","avamos","avash","avan"]
                    elif t == "preterite":
                        data = ["i","ates","o","imos","atesh","aron"]
                    elif t == "future":
                        data = ["va","vas a","va","vamos a","vash a","van a"]
                    elif t == "conditional_simple":
                        data = ["aria","arias","aria","ariamos","ariash","arian"]
                elif inf_lad_verb[-2:] == "er":
                    if t == "present":
                        data = ["o","es","e","emos","esh","en"]
                    elif t == "imperfect":
                        data = ["ia","ias","ia","iamos","iash","ian"]
                    elif t == "preterite":
                        data = ["i","ites","yo","imos","itesh","yeron"]
                    elif t == "future":
                        data = ["va","vas a","va","vamos a","vash a","van a"]
                    elif t == "conditional_simple":
                        data = ["eria","erias","eria","eriamos","eriash","erian"]    
                elif inf_lad_verb[-2:] == "ir":
                    if t == "present":
                        data = ["o","es","e","imos","ish","en"]
                    elif t == "imperfect":
                        data = ["ia","ias","ia","iamos","iash","ian"]
                    elif t == "preterite":
                        data = ["i","ites","yo","imos","itesh","yeron"]
                    elif t == "future":
                        data = ["va","vas a","va","vamos a","vash a","van a"]
                    elif t == "conditional_simple":
                        data = ["iria","irias","iria","iriamos","iriash","irian"]
            
            per = change_person_number(p)
            if t == "preterite" and aux == 1 and per == pers:
                inf_lad_verb = inf_lad_verb[:-2]+data[per]
                flag = 1
                break
            if esp_verb_conj == esp_verb:
                if t == "future":
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
                return inf_lad_verb