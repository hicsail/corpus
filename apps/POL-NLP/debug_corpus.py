import argparse

from corpus import corpus


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    corp = corpus.Corpus(
        'corp',
        args.i
    )

    corp.debug_corpus_keys()

