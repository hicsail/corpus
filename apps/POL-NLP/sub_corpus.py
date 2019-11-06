import argparse
import sys

from corpus import corpus


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-o", action="store", help="output directory")
    parser.add_argument("-k", action="store", help="keywords")
    parser.add_argument("-l", action="store", help="number of words to extract per snippet")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Filtered")
    parser.add_argument("-d", action="store", help="publication date key name for volumes", default="Year Published")
    parser.add_argument("-y", action="store", help="year range")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    if args.y:
        r = args.y.split(",")
        y_min = int(r[0])
        y_max = int(r[1])

    else:
        y_min = -1*sys.maxsize
        y_max = sys.maxsize

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
        int(args.l),
        [y_min, y_max]
    )
