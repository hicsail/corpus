from corpus import corpus, utils, results, graph
from corpus.nlp import tf_idf_author as tf
import pandas as pd
import sys, csv
import argparse, re, os
import matplotlib.pyplot as plt
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", action="store", help="path to author_dict.json file")

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Filtered Text")
    parser.add_argument("-s", action="store", help="yes[y] to save the author_dict.json", default="yes")
    parser.add_argument("-o", action="store", help="output directory where all the results will be saved")

    parser.add_argument("-k", action="store", help="keywords")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    # c = corpus.Corpus(
    #     'test',
    #     args.i
    # )
    #
    # out_dir = args.o
    # utils.build_out(out_dir)
    #
    # model = c.tf_idf_author(
    #     'tfidf',
    #     out_dir
    # )
    #
    # # check args if author_dict is given:
    # if args.a is not None:
    #     model.get_author_dict_from_json(args.a)
    # else:
    #     model.generating_author_dict(args.t)
    #     if (args.s.lower() != 'yes') & (args.s.lower() != 'y'):
    #         model.generating_author_dict(args.t, save=False)
    #     else:
    #         model.generating_author_dict(args.t, save=True)
    #
    # model.build_tf_idf_author_model()
    # model.get_all_word_scores()
    #
    # # danish:\
    # # "Aftale voldgift forhandling Koalition samarbejde Fælles kompromis medvirkning samordning Overenskomst forlig ordning enstem enhed forbund forening fagforening"
    #
    # # british:\
    # # "agreement arbitration bargaining coalition collaboration compromise cooperation coordination negotiation pact settlement unanimity unity"
    #
    # keylist = re.split(r'\W+', args.k.lower())
    #
    # score_mat = model.get_author_keywords_score_matrix(keylist)
    #
    # ans = prompt("Do you want to save the author tfidf scores on the keywords? ([y] for yes):   ")
    # if (ans.lower() == 'y') | (ans.lower() == 'yes'):
    #     full_mat_file = out_dir + '/author_keys_full_mat.csv'
    #     score_mat.write_full_mat(full_mat_file)
    #     print("Scores saved to file= author_keys_full_mat.csv")
    # else:
    #     print("Scores not saved")

    ######################## If score mat csv file available #############################
    out_dir = args.o
    full_mat_file = out_dir + '/author_keys_full_mat.csv'
    df = pd.read_csv(full_mat_file, index_col=0)
    score_mat = tf.AuthorKeywordsMat(df.values, [*df.index], [*df.columns])
    ######################################################################################

    see = prompt("Do you want to see the scatterplot using tSNE dimension reduction?  ([y] for yes):   ")
    if (see.lower() == 'y') | (see.lower() == 'yes'):
        score_mat.compute_tsne()
        graphTSNE = graph.GraphClusters(score_mat.tsne, title='Dimension Reduction using tSNE')
        graphTSNE.show_plot()

    while True:
        print('\n-------------- Start clustering ------------------- \nWhat clustering method would you like to use?')
        # TODO: could incorporate more
        cluster_method = prompt("[k] for k-means, [h] for hierarchical clustering, [exit] for exit the program:     ")

        if cluster_method == 'k':
            print("How many clusters are you expecting?")
            n = prompt("Input the number if you know it or any letter if you do not:    ")
            if n.isdigit():
                clabels = score_mat.cluster_kmeans(int(n))
            else:
                clabels = score_mat.cluster_kmeans()

            if score_mat.tsne is None:
                score_mat.compute_tsne()

            graphTSNE = graph.GraphClusters(score_mat.tsne, title='Clustering Result')
            graphTSNE.show_plot(cluster_labels=clabels)

            ans = prompt("Do you wan to save the result? ([y] for yes):   ")
            if (ans.lower() == 'y') | (ans.lower() == 'yes'):
                fname = 'result_kmeans_' + n
                result_file = out_dir + '/' + fname + '.txt'

                results.TfidfAuthorClusters(score_mat.nonzero_mat, score_mat.nonzero_authors, score_mat.col_index,
                                            clabels, score_mat.zauthors).\
                    write_authors_clustered(result_file, 'k means clustering')

                graph_result_file = out_dir + '/' + fname + '.png'
                graphTSNE.save(graph_result_file)
                print('Result saved to ' + fname)
                print("OUT", plt.get_fignums())
                graphTSNE.close()
            else:
                print("Result not saved")

        elif cluster_method == 'h':
            print("Please choose a linkage method from below for defining cluster distance. Default is 'ward'")
            dist_meth = prompt("single, complete, ward, average, weighted, centroid, median:    ")
            # TODO: what if user input is an invalid method?
            Z = score_mat.get_Z(dist_meth)
            out_fig = out_dir + '/' + 'dendrogram_' + dist_meth + '.png'
            score_mat.plot_dendrogram_and_save(Z, out_fig)

            cutoff = prompt("After you see the dendrogram, please check the bottom axis and pick a cutoff value:    ")
            # TODO: do I want to validate the input?

            clabels = score_mat.cluster_hcluster(Z, float(cutoff))

            if score_mat.tsne is None:
                score_mat.compute_tsne()

            graphTSNE = graph.GraphClusters(score_mat.tsne, title='Clustering Result')
            graphTSNE.show_plot(cluster_labels=clabels)

            ans = prompt("Do you wan to save the result? ([y] for yes):   ")
            if (ans.lower() == 'y') | (ans.lower() == 'yes'):
                fname = 'result_hcluster_' + dist_meth + '_' + cutoff
                result_file = out_dir + '/' + fname + '.txt'

                results.TfidfAuthorClusters(score_mat.nonzero_mat, score_mat.nonzero_authors, score_mat.col_index,
                                            clabels, score_mat.zauthors).\
                    write_authors_clustered(result_file, 'hierarchical clustering')

                graph_result_file = out_dir + '/' + fname + '.png'
                graphTSNE.save(graph_result_file)
                print("Result saved to " + fname)
                graphTSNE.close()

            else:
                print("Result not saved")

        elif cluster_method == 'exit':
            print("Bye.")
            break

        else:
            print("Command not recognized.\n")
            continue

