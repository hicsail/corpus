from corpus import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    f = c.tf_idf(
        'freq',
        [1800, 1820, 1840],
        'Filtered Text',
    )

    tf_res = f.top_n('economy', 10)

    tf_res.display()



