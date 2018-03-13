from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    f = c.tf_idf(
        'freq',
        [1700, 1720, 1740],
        'jonathan',
        10,
        'Filtered Text'
    )

    f.display()

