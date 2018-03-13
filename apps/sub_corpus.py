from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    s = c.build_sub_corpus(
        'sub',
        sys.argv[2],
        ['jonathan', 'lady'],
        'Filtered Text',
        40,
        [1700, 1800]
    )