from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    t = c.lda_model(
        'lda',
        [1700, 1720, 1740],
        'Filtered Text'
    ).write(
        sys.argv[2]
    )
