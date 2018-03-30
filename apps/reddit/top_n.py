from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    e1 = c.top_n(
        'f1',
        [200600, 200700],
        'Filtered',
    )

    e1.display()