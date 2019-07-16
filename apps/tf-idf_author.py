from corpus import corpus
import sys, csv

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    model = c.tf_idf_author(
        'tfidf',
    )

    model.get_author_dict_from_json('/Users/Even/Desktop/POL-NLP/danish_author_dict.json')  # ~argv[2]
    # model.generating_author_dict('Filtered Text')
    # model.write_author_dict_to_file("Filtered Text", sys.argv[2])

    model.build_tf_idf_author_model()
    model.get_all_word_scores()
    # model.save_model(sys.argv[2])

    cooperation_words = "Aftale voldgift forhandling Koalition samarbejde Fælles kompromis medvirkning samordning  \
    Overenskomst forlig ordning enstem enhed forbund forening fagforening"

    # "agreement arbitration bargaining coalition collaboration compromise cooperation coordination negotiation pact settlement unanimity unity"

    cooperation_list = cooperation_words.lower().split()

    score_mat = model.write_full_mat_csv(cooperation_list)
    score_mat.write_csv('/Users/Even/Desktop/danish_score_mat.csv')

    # cluster_kmeans = model.cluster_kmeans(cooperation_list)
    # cluster_kmeans.write_authors_clustered('/Users/Even/Desktop/danish_authors.json', 'kmeans')




