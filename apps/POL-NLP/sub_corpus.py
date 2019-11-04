import argparse

from corpus import corpus

"""
TODO: specify time period
"""


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-o", action="store", help="output directory")
    parser.add_argument("-k", action="store", help="keywords")
    parser.add_argument("-l", action="store", help="number of words to extract per snippet")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Filtered")
    parser.add_argument("-d", action="store", help="publication date key name for volumes", default="Year Published")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    corp = corpus.Corpus(
        "corp",
        args.i
    )

    sub = corp.build_sub_corpus(
        'sub',
        args.o,
        args.k.split(','),
        args.t,
        args.d,
        int(args.l)
    )
