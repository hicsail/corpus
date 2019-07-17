from corpus import corpus
import sys, csv
import argparse, re, os


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", action="store", help="path to author_dict.json file")

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Filtered Text")
    parser.add_argument("-s", action="store", help="yes[y] to save the author_dict.json")
    parser.add_argument("-o", action="store", help="output directory for all the results")

    parser.add_argument("-k", action="store", help="keywords")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    c = corpus.Corpus(
        'test',
        args.i
    )

    #TODO: checkout the build_out in utils(?)
    # out_dir = build_out(args.o)
    out_dir = args.o

    model = c.tf_idf_author(
        'tfidf',
        out_dir
    )

    # check args if author_dict is given:
    if args.a is not None:
        model.get_author_dict_from_json(args.a)
    else:
        model.generating_author_dict(args.t)
        if (args.s.lower() == 'yes') | (args.s.lower() == 'y'):
            model.generating_author_dict(args.t, save=True)
        else:
            model.generating_author_dict(args.t, save=False)

    model.build_tf_idf_author_model()
    model.get_all_word_scores()

    # danish:\
    # "Aftale voldgift forhandling Koalition samarbejde Fælles kompromis medvirkning samordning Overenskomst forlig ordning enstem enhed forbund forening fagforening"

    # british:\
    # "agreement arbitration bargaining coalition collaboration compromise cooperation coordination negotiation pact settlement unanimity unity"

    keylist = re.split(r'\W+', args.k.lower())

    score_mat = model.get_author_keywords_score_matrix(keylist)

    full_mat_file = out_dir + '/author_keys_full_mat.csv'
    score_mat.write_full_mat(full_mat_file)  # TODO: how to make this optional?

    #TODO: maybe a while(1) loop instead of exit?
    # result_kmeans = score_mat.cluster_kmeans()
    # result_kmeans_file = out_dir + '/result_kmeans'
    # result_kmeans.write_authors_clustered(result_kmeans_file, 'kmeans')

    score_mat.plot_dendrogram('ward')
    # result_hcluster = score_mat.cluster_hcluster(0.05)
    # result_hcluster_file = out_dir + '/result_kmeans'
    # result_hcluster.write_authors_clustered(result_hcluster_file, 'kmeans')


