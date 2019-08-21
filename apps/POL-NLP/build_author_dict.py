import argparse

from corpus import corpus


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Filtered Text")
    parser.add_argument("-o", action="store", help="output directory where author_dict.json file will be saved")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    c = corpus.Corpus(
        'corp',
        args.i
    )

    model = c.tf_idf_author(
        'tfidf_author',
        out_dir=args.o,
        text_type=args.t
    )

    model.generating_author_dict()
