from corpus import corpus, graph
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    c.debug_corpus_keys()

