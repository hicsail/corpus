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

    f.top_n('people').display()

    f.write_tfidf(sys.argv[2])