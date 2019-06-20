from corpus import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    model = c.tf_idf_author(
        'tfidf',
        'Filtered Sentences',
    )

    model.build_dictionaries_and_corpora()
    model.save_models("/Users/Even/Desktop/tfidf_author_out")

    res = model.build_tf_idf_author_models()

    cooperation_words = "agreement arbitration bargaining coalition collaboration compromise cooperation coordination negotiation pact settlement unanimity unity"
    cooperation_list = cooperation_words.split()

    for w in cooperation_list:
        #TODO: map words to id?
        for author in model.author_list:
            model.word_to_id[author].token2id

