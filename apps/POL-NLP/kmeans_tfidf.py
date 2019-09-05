import argparse

from corpus import corpus


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-k", action="store", help="keywords")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Text")
    parser.add_argument("-y", action="store", help="year ranges")
    parser.add_argument("-o", action="store", help="output directory")
    parser.add_argument("-d", action="store", help="publication date key name for volumes", default="Year Published")

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

    ck = tfidf.cluster_k_means(["hi", "cat", "mat", "__www__"])
    clusters = ck.fit_clusters()
    clusters.save_results('/Users/ben/Desktop/kmeans_results/')

    print("Done with kmeans_tfidf.py")
