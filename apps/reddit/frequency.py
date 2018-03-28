from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    e1 = c.frequency(
        'f1',
        [200500, 200600],
        ['terrorist'],
        'Text'
    )

    e1.write_to_json('/Users/ben/Desktop/out')