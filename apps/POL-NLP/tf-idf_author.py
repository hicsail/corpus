from corpus import corpus
import sys, csv
import argparse, re, os


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", action="store", help="path to author_dict.json file")
    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-o", action="store", help="output directory")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Filtered Text")

    parser.add_argument("-k", action="store", help="keywords")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    c = corpus.Corpus(
        'test',
        args.i
    )

    if args.o is not None:
        if not os.path.exists(args.o):
            os.mkdir(args.o)
        else:
            shutil.rmtree(args.o)
            os.mkdir(args.o)
    else:
        _fail("Please specify output directory.")

        

    model = c.tf_idf_author(
        'tfidf',
        args.o
    )
    """
       Build output directory, overwrite if it exists.
       """



    # check args if author_dict is given:
    if args.a is not None:
        model.get_author_dict_from_json(args.a)
    else:
        model.generating_author_dict(args.t)
        if args.o is not None:
            model.write_author_dict_to_file(args.t, args.o)

    model.build_tf_idf_author_model()
    model.get_all_word_scores()

    # danish:\
    # "Aftale voldgift forhandling Koalition samarbejde Fælles kompromis medvirkning samordning Overenskomst forlig ordning enstem enhed forbund forening fagforening"

    # british:\
    # "agreement arbitration bargaining coalition collaboration compromise cooperation coordination negotiation pact settlement unanimity unity"

    keylist = re.split(r'\W+', args.k.lower())

    score_mat = model.write_full_mat_csv(keylist)
    score_mat.write_csv('/Users/Even/Desktop/POL-NLP/british_score_mat.csv')

    # cluster_kmeans = model.cluster_kmeans(cooperation_list)
    # cluster_kmeans.write_authors_clustered('/Users/Even/Desktop/danish_authors.json', 'kmeans')




