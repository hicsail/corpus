import argparse

from corpus import corpus

"""
TODO: avg / variance
"""


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-o", action="store", help="output file path")
    parser.add_argument("-k", action="store", help="keywords")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Text")
    parser.add_argument("-y", action="store", help="year ranges")
    parser.add_argument("-n", action="store", help="frequency record name")
    parser.add_argument("-d", action="store", help="publication date key name for volumes", default="Year Published")
    parser.add_argument("-txt", action="store", help="output text filepath")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    corp = corpus.Corpus(
        'corp',
        args.i
    )

    freq = corp.frequency(
        'freq',
        [int(y) for y in args.y.split(",")],
        args.t,
        args.d
    )

    freq1 = freq.take_freq(args.k.split(","), args.n)
    freq1.write_to_json("{}_global.json".format(args.o))
    freq1.write("{}_global.txt".format(args.txt))

    avg = freq.take_average_freq(args.k.split(","), args.n)
    avg.write_to_json("{}_avg.json".format(args.o))
    avg.write("{}_avg.txt".format(args.txt))

    var = freq.take_variance(args.k.split(","), args.n)
    var.write_to_json("{}_var.json".format(args.o))
    var.write("{}_var.txt".format(args.txt))
