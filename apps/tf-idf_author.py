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

    model.get_author_dict_from_json('/Users/Even/Desktop/POL-NLP/british_author_dict.json')  # ~argv[2]
    # model.generating_author_dict('Filtered Text')
    # model.write_author_dict_to_file("Filtered Text", sys.argv[2])

    model.build_tf_idf_author_model()
    model.get_all_word_scores()
    # model.save_model(sys.argv[2])

    cooperation_words = "agreement arbitration bargaining coalition collaboration compromise cooperation coordination \
                        negotiation pact settlement unanimity unity"
    cooperation_list = cooperation_words.split()

    result = model.cluster_kmeans(cooperation_list)
    result.write_authors_clustered('/Users/Even/Desktop/temp.json', 'kmeans')

    # cooperation_list.insert(0, 'author_keywords')
    # # print(cooperation_list)
    #
    # # write the author-words tfidf score matrix to file
    # tfidf_result = '/Users/Even/Desktop/POL-NLP/tfidf_result.csv'
    # with open(tfidf_result, 'w') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerow(cooperation_list)
    #     for author, words in model.scores_author.items():
    #         row_author = [author]
    #         for w in cooperation_list[1:]:
    #             s = words.get(w)
    #             if s is None:
    #                 s = 0
    #             row_author.append(s)
    #         print(row_author)
    #         writer.writerow(row_author)
    #
    # csvFile.close()



