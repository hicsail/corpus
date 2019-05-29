from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    t = c.lda_model(
        'lda',
        [1800, 1820, 1840],
        'Filtered Text',
        30
    )

    t.write(sys.argv[2], 30)
