import argparse

from corpus import corpus


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-o", action="store", help="output text file path")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Text")
    parser.add_argument("-y", action="store", help="year ranges")
    parser.add_argument("-l", action="store", help="language", default="english")
    parser.add_argument("-num_topics", action="store", help="number of topics", default=10),
    parser.add_argument("-passes", action="store", help="number of passes", default=1)
    parser.add_argument("-stop", action="store", help="path to stopwords file", default=None)
    parser.add_argument("-d", action="store", help="publication date key name for volumes", default="Year Published")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    corp = corpus.Corpus(
        "corp",
        args.i
    )

    lda = corp.lda_model(
        'lda',
        [int(y) for y in args.y.split(",")],
        args.t,
        num_topics=int(args.num_topics),
        passes=args.passes,
        stop_words=args.stop,
        date_key=args.d
    )

    lda.write(args.o, args.num_topics)
