import argparse

from corpus import corpus


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-o", action="store", help="output file path")
    parser.add_argument("-k", action="store", help="keywords")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Text")
    parser.add_argument("-y", action="store", help="year ranges")
    parser.add_argument("-n", action="store", help="frequency record name")
    parser.add_argument("-d", action="store", help="publication date key name for volumes", default="Year Published")
    parser.add_argument("-b", action="store_true", help="track binary word occurrence")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    corp = corpus.Corpus(
        'corp',
        args.i
    )

    rf = corp.raw_frequency(args.n, args.t, args.b)
    rf.take_freq(args.k.split(","), args.n)