import argparse

from corpus import corpus
from corpus.clusters.cluster import KMeansAuthorCluster, HierarchicalAuthorCluster


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-k", action="store", help="keywords")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Text")
    parser.add_argument("-y", action="store", help="year ranges")
    parser.add_argument("-n", action="store", help="number of docs to display")
    parser.add_argument("-d", action="store", help="publication date key name for volumes", default="Date")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    corp = corpus.Corpus(
        'corp',
        args.i
    )

    tfidf = corp.tf_idf(
        'tfidf',
        [int(y) for y in args.y.split(",")],
        args.t,
        date_key=args.d
    )

    results = [tfidf.top_n(k.lower(), int(args.n)) for k in args.k.split(",")]

    for r in results:
        r.display()
