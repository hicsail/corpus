from corpus import corpus
import sys, pandas

if __name__ == '__main__':

    author_dict = corpus.doc2author(sys.argv[1], sys.argv[2], "Filtered Text")

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    model = c.tf_idf_author(
        'tfidf',
        author_dict,
    )

    model.build_tf_idf_author_model()

    result = dict()
    # word = "agreement"
    # result[word] = model.get_word_score(word)

    cooperation_words = "agreement arbitration bargaining coalition collaboration compromise cooperation coordination negotiation pact settlement unanimity unity"
    cooperation_list = cooperation_words.split()

    for w in cooperation_list:
        result[w] = model.get_word_score(w)

    df = pandas.DataFrame(result, index=list(author_dict.keys()))

    tfidf_result = sys.argv[2] + '/tfidf_result.csv'

    df.to_csv(tfidf_result, encoding='utf-8')

