from corpus import corpus
import sys, csv, pandas

if __name__ == '__main__':

    # author_dict = corpus.doc2author(sys.argv[1], sys.argv[2], "Filtered Text")

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    model = c.tf_idf_author(
        'tfidf',
        author_dict,
    )

    model.build_tf_idf_author_model()

    model.get_all_word_scores()
    # model.save_model(sys.argv[2])

    # result = dict()
    # result[word] = model.get_word_score(word)

    cooperation_words = "agreement arbitration bargaining coalition collaboration compromise cooperation coordination negotiation pact settlement unanimity unity"
    cooperation_list = cooperation_words.split()
    cooperation_list.insert(0, 'author_keywords')
    #print(cooperation_list)

    tfidf_result = sys.argv[2] + '/tfidf_result.csv'
    with open(tfidf_result, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(cooperation_list)
        for author, words in model.scores_author.items():
            row_author = [author]
            for w in cooperation_list[1:]:
                s = words.get(w)
                if s is None:
                    s = 0
                row_author.append(s)
            print(row_author)
            writer.writerow(row_author)

    csvFile.close()



