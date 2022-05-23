<p align="center"><img src="https://raw.githubusercontent.com/CollectivaT-dev/Espanyol-Ladino-Translation/master/img/ab-tr.jpg"></p>

# Spanish to Judeo-Spanish converter

This is an simple dictionary-based script to convert a Spanish sentences to [Judeo-Spanish](https://en.wikipedia.org/wiki/Judaeo-Spanish). 

# Installation

In order to clone this repository:
```
git clone https://github.com/CollectivaT-dev/Espanyol-Ladino-Translation
```

After, create a virtualenvironment and install all the requirements
```
python -m venv venv
source venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

# Usage

```
usage: translate Spanish <> Judeo-Spanish (Ladino) [-h] -d LAD_DIC [-i INPUT]
                                                   [-o OUTPUT] [-v] [-c]
required arguments:
  -dv LAD_DIC_VERB, --lad_dic_verb LAD_DIC_VERB
                        Dictionary of verbs.
  -dw LAD_DIC_NOUN, --lad_dic_noun LAD_DIC_NOUN
                        Dictionary of nouns.

optional arguments:
  -h, --help            show help message and exit

  -i INPUT, --input INPUT
                        Sentence segmented text file to translate
  -o OUTPUT, --output OUTPUT
                        Output path
  -v, --interactive     Interactive translator
  -c, --csv             Translate dataset CSV with EN, ES columns
```

## Interactive mode

This mode opens an interactive panel where given sentence is translated. 

```
python src/main.py -dv resource/lista_verbos_ladino_conjugados.txt -dw resource/lista_palabras_ladino.txt -v
```

## Translate sentence-segmented text file

This mode translates plain text file, line-by-line.

```
python src/main.py -dv resource/lista_verbos_ladino_conjugados.txt -dw resource/lista_palabras_ladino.txt -i samples/sentences.txt -o translated_sentences.txt
```

## Translate TSV

This mode reads a tab-separated file, translates sentences under column "Spanish" and adds it as a new "Ladino" column. You need to use the option `-c` or `--csv`.

```
python src/main.py -dv resource/lista_verbos_ladino_conjugados.txt -dw resource/lista_palabras_ladino.txt -i samples/sentences.csv -o translated_sentences.csv -c
```

# Examples

Input | Output
 --- | ---
Estoy aprendiendo el judeoespañol. | Esto ambezando el Judeo-Espanyol.
Me levanto a las siete cada día. | Me alevanto a las siete kada dia.
Me gusta leer. | Me plaze meldar.
Bebo café turco después del almuerzo. | Bevo kafe turko despues del komida de midi.
Tengo dos niños; una hija y un hijo. | Tengo dos kriaturas; una ija y un ijo.
Estoy muy cansada. | Esto muy kansada.
Mi padre es médico. | Mi padre es doktor.
Tengo sed; dame un caso de agua por favor. | Tengo ser; dame un kavzo de agua por favor.
El teléfono está sonando. | El telefon esta sonando.
¡No comas mucho pan! | No komas muncho pan!

# Citation

```
Alp Öktem, Rodolfo Zevallos, Yasmin Moslem, Güneş Öztürk, Karen Şarhon. 
Preparing an endangered language for the digital age: The Case of Judeo-Spanish. 
Workshop on Resources and Technologies for Indigenous, Endangered and Lesser-resourced Languages in Eurasia (EURALI) @  LREC 2022. Marseille, France. 20 June 2022
```

---

This repo is developed as part of project "Judeo-Spanish: Connecting the two ends of the Mediterranean" carried out by Col·lectivaT and Sephardic Center of Istanbul within the framework of the “Grant Scheme for Common Cultural Heritage: Preservation and Dialogue between Turkey and the EU–II (CCH-II)” implemented by the Ministry of Culture and Tourism of the Republic of Turkey with the financial support of the European Union. The content of this website is the sole responsibility of Col·lectivaT and does not necessarily reflect the views of the European Union. 
