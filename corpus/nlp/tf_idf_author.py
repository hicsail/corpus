import tqdm, re

from gensim.models import TfidfModel
from gensim.corpora import Dictionary

from corpus.results import *


class TfidfAuthor:
    """
    Data structure for identifying authors(instead of documents) and their corresponding TF-IDF
    scores, with respect to particular keywords and a list of year periods.
    """

    def __init__(
            self, name: str, in_dir: str, text_type: str, author_key: str,
            stop_words: [list, set, None] = None):

        self.name = name
        self.in_dir = in_dir
        self.text_type = text_type
        self.author_key = author_key
        self.stop_words = self.setup_stop_words(stop_words)

        self.author_list = None
        self.tf_idf_author_models = None
        self.word_to_id = None
        self.corpora = None

    def setup_stop_words(self, stop_words):

        if stop_words is not None:
            if isinstance(stop_words, str):
                return self.stop_words_from_json(stop_words)
            elif isinstance(stop_words, list):
                return set(stop_words)
            else:
                return stop_words
        else:
            return {}

    def stop_words_from_json(self, file_path: str):
        """
        Set stop_words from Json file.
        """

        print("Loading stop words from JSON file at {}".format(file_path))

        with open(file_path, 'r', encoding='utf8') as in_file:

            json_data = json.load(in_file)
            stop_words = set(json_data['Words'])

            return stop_words

    ################################################
    def _generate_author_list(self):
        if self.author_list is not None:
            return

        print("Generating author list.\n")
        author_list = []
        for subdir, dirs, files in os.walk(self.in_dir):
            for jsondoc in tqdm.tqdm(files):
                if jsondoc[0] != ".":
                    with open(self.in_dir + "/" + jsondoc, 'r', encoding='utf8') as in_file:
                        try:
                            json_data = json.load(in_file)
                            for k in json_data.keys():
                                author_raw = (json_data[k][self.author_key]).lower()
                                author = re.sub('\W+', '_', author_raw)
                                author_list.append(author)
                        except json.decoder.JSONDecodeError:
                            print("Error loading file {}".format(jsondoc))

        self.author_list = set(author_list)

    def build_dictionaries_and_corpora(self):
        """
        Construct word_to_id which store the word -> id mappings and the bag of words
        representations of the documents in the corpus. Used for building TF-IDF models
        and LDA / LSI topic models.
        """

        if self.word_to_id is not None:
            return

        self._generate_author_list()
        word_to_id_results = gensim_dict(self.author_list)
        corpora_results = list_dict(self.author_list)

        print("Building word to ID mappings.\n")

        for subdir, dirs, files in os.walk(self.in_dir):
            for jsondoc in tqdm.tqdm(files):
                if jsondoc[0] != ".":
                    with open(self.in_dir + "/" + jsondoc, 'r', encoding='utf8') as in_file:

                        try:
                            json_data = json.load(in_file)
                            for k in json_data.keys():
                                author_raw = (json_data[k][self.author_key]).lower()
                                target = re.sub('\W+', '_', author_raw)
                                text = json_data[k][self.text_type]
                                for i in range(len(text) - 1, -1, -1):
                                    if text[i] in self.stop_words:
                                        del text[i]
                                if len(text) > 0:
                                    word_to_id_results[target].add_documents([text])
                                    d2b = word_to_id_results[target].doc2bow(text)
                                    corpora_results[target].append(d2b)

                        except json.decoder.JSONDecodeError:

                            print("Error loading file {}".format(jsondoc))

        self.word_to_id = word_to_id_results
        self.corpora = corpora_results

        return self

    def save_models(self, out_dir: str):
        """
        Write dictionaries and tf-idf_author models to file.
        """

        if self.word_to_id is None or self.corpora is None:
            self.build_dictionaries_and_corpora()

        if self.tf_idf_author_models is None:
            self.build_tf_idf_author_models()

        build_out(out_dir)
        os.mkdir("{0}/{1}".format(out_dir, 'tfidf_author'))
        os.mkdir("{0}/{1}".format(out_dir, 'dictionaries'))

        for author in self.author_list:

            model = self.tf_idf_author_models[author]
            model.save("{0}/tfidf_author/{1}".format(out_dir, author))

            dictionary = self.word_to_id[author]
            dictionary.save("{0}/dictionaries/{1}".format(out_dir, author))

    def load_models(self, in_dir: str):
        """
        Load dictionaries and tf-idf_author models from file.
        """

        self.tf_idf_author_models = {}
        self.word_to_id = {}

        for author in self.author_list:
            self.tf_idf_author_models[author] = TfidfModel.load("{0}/tfidf_author/{1}".format(in_dir, author))
            self.word_to_id[author] = Dictionary.load("{0}/dictionaries/{1}".format(in_dir, author))

        return self

    def build_tf_idf_author_models(self):
        """
        Combines the word_to_id and corpora dictionaries
        to construct TF-IDF models for each author.
        """

        if self.word_to_id is None or self.corpora is None:
            self.build_dictionaries_and_corpora()

        results = num_dict(self.author_list)

        print("Building TF-IDF author models.\n")

        for author in tqdm.tqdm(self.author_list):
            results[author] = TfidfModel(self.corpora[author], dictionary=self.word_to_id[author], smartirs='ntc')

        self.tf_idf_author_models = results

        return self




