# Espanyol-Ladino Translation

This is an example of translation going from modern Spanish to Ladino rule-based.

# Installation

In order to clone this repository:
```
git clone https://github.com/CollectivaT-dev/Espanyol-Ladino-Translation
```

After create a virtualenvironment and install all the requirements
```
python -m venv venv
source venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

# Translate

To run the translator, use it in the following way:

```
python main.py -d <dictionary_ladino_root> -i <dataset_to_translate_root> -o <output_file_root>
```

Example:

```
python main.py -d "resource/dic_esp_lad_v3.txt" -i "resource/dataset.csv" -o "dataset_translate.csv"
```

## Results

(Espanyol -> Ladino)

Input | Output
 --- | ---
Me gusta leer . | Me plaze meldar .
Estuve comprando una casa . | Yo estuve merkando una kaza . 
Hoy es tu cumpleaños . | Oy es tu aniversario .
Me tengo que ir al trabajo . | Me tenjo ke ir a el echo .
