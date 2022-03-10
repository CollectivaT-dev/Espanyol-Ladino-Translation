# Usage prepro.py

```
usage: translate Spanish <> Judeo-Spanish (Ladino) [-h] -d LAD_DIC [-i INPUT]
                                                   [-o OUTPUT] [-v] [-c]
required arguments:
  -d LAD_DIC, --lad_dic LAD_DIC
                        Dictionary root.

optional arguments:
  -h, --help            show help message and exit

  -s1 INPUT, --input_esp INPUT
                        Sentence segmented Spanish text file to translate
						
  -s2 INPUT, --input_2 INPUT
                        Sentence segmented other language text file

  -n INPUT, --language INPUT
                        second language name
			
  -c INPUT, --counter INPUT
                        Translates from the line counter

  -o OUTPUT, --output OUTPUT
                        Output path
```


## Translate from 2 sentence-segmented text file

This mode translates plain text file, line-by-line.

```
python src/prepro.py -d resource/dic_esp_lad_v3.txt -s1 resource/SciELO.en-es.es -s2 resource/Scielo.en-es.en -n English -o resource/ -c 0
```

