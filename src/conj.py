import stanza
import unidecode
import util

import mlconjug3


def main():
    default_conjugator = mlconjug3.Conjugator(language='es')
    v = default_conjugator.conjugate("comprar")
    print(v.iterate())

if __name__ == '__main__':
    main()
