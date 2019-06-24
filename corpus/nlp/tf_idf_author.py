import numpy as np

from gensim.models import TfidfModel
from gensim.corpora import Dictionary

from corpus.results import *

class TfidfAuthor:
    """
    Data structure for identifying authors(instead of documents) and their corresponding TF-IDF
    scores, with respect to particular keywords
    """

    def __init__(
            self, name: str, author_dict: dict, stop_words: [list, set, None] = None):

        self.name = name
        self.author_dict = author_dict
        self.stop_words = self.setup_stop_words(stop_words)

        self.tf_idf_model = None
        self.word_to_id = None
        self.corpora = None

    def setup_stop_words(self, stop_words):

        if stop_words is not None:
            if isinstance(stop_words, str):
                return self._stop_words_from_json(stop_words)
            elif isinstance(stop_words, list):
                return set(stop_words)
            else:
                return stop_words
        else:
            return {}

    def _stop_words_from_json(self, file_path: str):
        """
        Set stop_words from Json file.
        """

        print("Loading stop words from JSON file at {}".format(file_path))

        with open(file_path, 'r', encoding='utf8') as in_file:

            json_data = json.load(in_file)
            stop_words = set(json_data['Words'])

            return stop_words

    def build_dictionaries_and_corpora(self):
        """
        Construct word_to_id which store the word -> id mappings and the bag of words
        representations of the documents in the corpus. Used for building TF-IDF models
        and LDA / LSI topic models.
        """

        if self.word_to_id is not None:
            return

        word_to_id = corpora.Dictionary()
        corpora_results = []

        print("Building word to ID mappings.\n")

        for author, text in self.author_dict.items():

            # for i in range(len(text) - 1, -1, -1):
            #     if text[i] in self.stop_words:
            #         del text[i]
            if len(text) > 0:
                word_to_id.add_documents([text])
                d2b = word_to_id.doc2bow(text)
                corpora_results.append(d2b)

        self.word_to_id = word_to_id
        self.corpora = corpora_results

        return self

    def save_model(self, out_dir: str):
        """
        Write dictionaries and tf-idf_author models to file.
        """

        if self.word_to_id is None or self.corpora is None:
            self.build_dictionaries_and_corpora()

        if self.tf_idf_model is None:
            self.build_tf_idf_author_models()

        build_out(out_dir)
        os.mkdir("{0}/{1}".format(out_dir, 'tfidf_author'))
        os.mkdir("{0}/{1}".format(out_dir, 'dictionaries'))

        model = self.tf_idf_model
        model.save("{0}/tfidf_authors".format(out_dir))

        dictionary = self.word_to_id
        dictionary.save("{0}/dictionaries".format(out_dir))

    def load_model(self, in_dir: str):
        """
        Load dictionaries and tf-idf_author models from file.
        """

        self.tf_idf_model = TfidfModel.load("{0}/tfidf_authors".format(in_dir))
        self.word_to_id = Dictionary.load("{0}/dictionaries".format(in_dir))

        return self

    def build_tf_idf_author_model(self):
        """
        Combines the word_to_id and corpora dictionaries
        to construct TF-IDF models for each author.
        """

        if self.word_to_id is None or self.corpora is None:
            self.build_dictionaries_and_corpora()

        print("Building TF-IDF author models.\n")

        self.tf_idf_model = TfidfModel(self.corpora, dictionary=self.word_to_id, smartirs='ntc')

        return self

    def get_word_score(self, word: str):

        word_score_author = []
        word_id = self.word_to_id.token2id.get(word)

        if word_id is None:
            print("\nATTENTION: word {0} not used by any author".format(word))

        else:
            # Show the TF-IDF weights
            for doc in self.corpora:
                used = False
                tfidf = self.tf_idf_model[doc]
                for wid, s in tfidf:
                    if wid == word_id:
                        used = True
                        word_score_author.append(s)
                if used == False:
                    word_score_author.append(0)
        return word_score_author
