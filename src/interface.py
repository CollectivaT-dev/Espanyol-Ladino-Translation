import os
import stanza
from .util import translate as ladino_translate
from .util import get_dic
from app.settings import MODELS_ROOT_DIR

stanza.download(lang='es', model_dir=MODELS_ROOT_DIR)
path_verb_dic = os.path.join(os.path.dirname(__file__), '../resource/lista_verbos_ladino_conjugados.txt')
path_noun_dic = os.path.join(os.path.dirname(__file__), '../resource/lista_palabras_ladino.txt')
path_phrase_dic = os.path.join(os.path.dirname(__file__), '../resource/dic_esp_lad_phr_v2.txt')

dic_verb = get_dic(path_verb_dic)
print("Read verb dictionary: %i entries"%len(dic_verb))

dic_noun = get_dic(path_noun_dic)
print("Read noun dictionary: %i entries"%len(dic_noun))

dic_phrase = get_dic(path_phrase_dic)
print("Read post phrase dictionary: %i entries"%len(dic_phrase))

def translate(string):
	return ladino_translate(string, dic_verb, dic_noun, dic_phrase, stanza_cachedir=MODELS_ROOT_DIR)