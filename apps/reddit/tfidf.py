import sys

from src import corpus


if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    f = c.tf_idf(
        'f1',
        [200500, 200600, 200700, 200800],
        'Filtered'
    )

    f.load_models('/Users/ben/Desktop/t_out/')

    f.top_n('people').display()


