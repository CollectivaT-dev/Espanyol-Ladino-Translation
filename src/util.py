
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
    if phrase.find("r se") != -1:
        phrase = phrase.replace("r se", "rse")
    if phrase.find("r la") != -1:
        phrase = phrase.replace("r la", "rla")
    if phrase.find("r las") != -1:
        phrase = phrase.replace("r las", "rlas")
    if phrase.find("r lo") != -1:
        phrase = phrase.replace("r lo", "rlo")
    if phrase.find("r los") != -1:
        phrase = phrase.replace("r las", "rlos")
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