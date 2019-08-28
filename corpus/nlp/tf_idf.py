import tqdm
import pickle

from gensim.models import TfidfModel
from gensim.corpora import Dictionary

from corpus.results import *
from corpus.clusters.cluster import *


class Tfidf:
    """
    Data structure for identifying documents and their corresponding TF-IDF
    scores, with respect to particular keywords and a list of year periods.
    """

    def __init__(
            self, name: str, in_dir: str, text_type: str, year_list: list,
            date_key: str, stop_words: [list, set, None] = None):

        self.name = name
        self.in_dir = in_dir
        self.text_type = text_type
        self.year_list = year_list
        self.date_key = date_key
        self.stop_words = self.setup_stop_words(stop_words)

        self.tf_idf_models = None
        self.word_to_id = None
        self.corpora = None
        self.author_dict = None

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

    @staticmethod
    def stop_words_from_json(file_path: str):
        """
        Set stop_words from Json file.
        """

        print("Loading stop words from JSON file at {}".format(file_path))

        with open(file_path, 'r', encoding='utf8') as in_file:

            json_data = json.load(in_file)
            stop_words = set(json_data['Words'])

            return stop_words

    def _update_dictionaries_and_corpora(self, k, json_data, word_to_id_results, corpora_results):
        """
        Add data from a single volume to dictionary and corpora dicts.
        """

        year = int(json_data[k][self.date_key])

        if self.year_list[0] <= year < self.year_list[-1]:
            text = json_data[k][self.text_type]

            for i in range(len(text) - 1, -1, -1):

                if text[i] in self.stop_words:
                    del text[i]

            target = determine_year(year, self.year_list)

            if len(text) > 0:
                word_to_id_results[target].add_documents([text])
                d2b = word_to_id_results[target].doc2bow(text)
                corpora_results[target].append(d2b)

    def build_dictionaries_and_corpora(self):
        """
        Construct word_to_id which store the word -> id mappings and the bag of words
        representations of the documents in the corpus. Used for building TF-IDF models
        and LDA / LSI topic models.
        """

        if self.word_to_id is not None:
            return

        word_to_id_results = gensim_dict(self.year_list)
        corpora_results = list_dict(self.year_list)

        print("Building word to ID mappings.\n")

        for subdir, dirs, files in os.walk(self.in_dir):
            for jsondoc in tqdm.tqdm(files):
                if jsondoc[0] != ".":

                    with open(self.in_dir + "/" + jsondoc, 'r', encoding='utf8') as in_file:

                        try:
                            json_data = json.load(in_file)
                            for k in json_data.keys():

                                self._update_dictionaries_and_corpora(k, json_data, word_to_id_results, corpora_results)
                        except json.decoder.JSONDecodeError:

                            print("Error loading file {}".format(jsondoc))

        self.word_to_id = word_to_id_results
        self.corpora = corpora_results

        return self

    def save_models(self, out_dir: str):
        """
        Write dictionaries and tf-idf models to file.
        """

        if self.word_to_id is None or self.corpora is None:
            self.build_dictionaries_and_corpora()

        if self.tf_idf_models is None:
            self.build_tf_idf_models()

        build_out(out_dir)
        os.mkdir("{0}/{1}".format(out_dir, 'tfidf'))
        os.mkdir("{0}/{1}".format(out_dir, 'dictionaries'))

        print("Saving TF-IDF models to {}".format(out_dir))

        for year in self.year_list:

            model = self.tf_idf_models[year]
            model.save("{0}/tfidf/{1}".format(out_dir, str(year)))

            dictionary = self.word_to_id[year]
            dictionary.save("{0}/dictionaries/{1}".format(out_dir, str(year)))

    def load_models(self, in_dir: str):
        """
        Load dictionaries and tf-idf models from file.
        """

        self.tf_idf_models = {}
        self.word_to_id = {}

        print("Loading TF-IDF models from {}".format(in_dir))

        for year in self.year_list:
            self.tf_idf_models[year] = TfidfModel.load("{0}/tfidf/{1}".format(in_dir, str(year)))
            self.word_to_id[year] = Dictionary.load("{0}/dictionaries/{1}".format(in_dir, str(year)))

        return self

    def build_tf_idf_models(self):
        """
        Combines the word_to_id and corpora dictionaries
        to construct TF-IDF models for each year period.
        """

        if self.word_to_id is None or self.corpora is None:
            self.build_dictionaries_and_corpora()

        results = num_dict(self.year_list)

        print("Building TF-IDF models.\n")

        for year in tqdm.tqdm(self.year_list):
            results[year] = TfidfModel(self.corpora[year], dictionary=self.word_to_id[year])

        self.tf_idf_models = results

        return self

    def _update_top_n(self, k, json_data, results, num_docs, keyword, jsondoc):
        """
        Update dictionary that stores the top <n> documents w/r/t a given
        keyword within a corpus.
        """

        year = int(json_data[k][self.date_key])

        if self.year_list[0] <= year < self.year_list[-1]:

            text = json_data[k][self.text_type]

            if keyword in set(text):

                target = determine_year(year, self.year_list)
                num_docs[target] += 1
                d2b = self.word_to_id[target].doc2bow(text)
                tfidf_doc = self.tf_idf_models[target][d2b]

                for t in tfidf_doc:

                    if self.word_to_id[target].get(t[0]) == keyword:
                        results[target].append((jsondoc, t[1], k))

    def _top_n(self, results, n):
        """
        Helper method, takes top results given a threshold from input top results data.
        """

        top_results = list_dict(self.year_list)

        for year in self.year_list:
            top = sorted(results[year], key=lambda x: x[1])
            top_results[year] = top[:n]

        return top_results

    def top_n(self, keyword: str, n: int = 10):
        """
        Iterates over the corpus and computes TF-IDF scores for each document,
        with respect to the precomputed TF-IDF models. Extracts results for a
        particular keyword and displays the <n> documents whose TF-IDF scores
        for that keyword are the highest.
        """

        if self.tf_idf_models is None:
            self.build_tf_idf_models()

        results = list_dict(self.year_list)
        num_docs = num_dict(self.year_list, nested=0)

        print("Calculating {0} files with top TF-IDF scores for \'{1}\'\n".format(n, keyword))

        for subdir, dirs, files in os.walk(self.in_dir):
            for jsondoc in tqdm.tqdm(files):
                if jsondoc[0] != ".":

                    with open(self.in_dir + "/" + jsondoc, 'r', encoding='utf8') as in_file:

                        try:
                            json_data = json.load(in_file)
                            for k in json_data.keys():

                                self._update_top_n(k, json_data, results, num_docs, keyword, jsondoc)

                        except json.decoder.JSONDecodeError:
                            print("Error loading file {}".format(jsondoc))

        top_results = self._top_n(results, n)

        return TfidfResults(top_results, num_docs, keyword, self.name)

    @staticmethod
    def _cleanup_author_dict(doc_to_bow_list):
        """
        Merge single list of d2b scores.
        """

        ret = {}

        for t in doc_to_bow_list:

            try:
                ret[t[0]] += t[1]

            except KeyError:
                ret[t[0]] = t[1]

        return [(k, ret[k]) for k in ret.keys()]

    def cleanup_author_dict(self, author_dict):
        """
        Iterate over author_dict and merge d2b scores.
        """

        for k in author_dict.keys():
            for kk in author_dict[k].keys():

                new_doc_to_bow = self._cleanup_author_dict(author_dict[k][kk])
                author_dict[k][kk] = new_doc_to_bow

        return author_dict

    def _partition_by_author(self, k, json_data, author_dict):
        """
        Helper method, update author_dict with a single document.
        """

        year = int(json_data[k][self.date_key])

        if self.year_list[0] <= year < self.year_list[-1]:

            text = json_data[k][self.text_type]
            author = re.sub(r'\W+', '_', json_data[k]["Author"]).lower()
            target = determine_year(year, self.year_list)

            d2b = self.word_to_id[target].doc2bow(text)

            try:
                author_dict[target][author].extend(d2b)

            except KeyError:
                author_dict[target][author] = d2b

    def partition_by_author(self):
        """
        Within each year period, partition corpus by each author.
        """

        if self.tf_idf_models is None:
            self.build_tf_idf_models()

        author_dict = simple_dict(self.year_list)

        print("Partitioning corpus by author.\n")

        for subdir, dirs, files in os.walk(self.in_dir):
            for jsondoc in tqdm.tqdm(files):
                if jsondoc[0] != ".":

                    with open(self.in_dir + "/" + jsondoc, 'r', encoding='utf8')  as infile:

                        try:
                            json_data = json.load(infile)
                            for k in json_data.keys():

                                self._partition_by_author(k, json_data, author_dict)

                        except json.decoder.JSONDecodeError:

                            print("Error loading file {}".format(jsondoc))

        self.author_dict = self.cleanup_author_dict(author_dict)

        return self

    def save_author_partition(self, out_dir):
        """
        Serialize author_dict to disk.
        """

        print("Saving author partition to {}/author_partition.p".format(out_dir))

        with open("{}/author_partition.p".format(out_dir), 'wb') as outfile:

            pickle.dump(self.author_dict, outfile)

    def load_author_partition(self, in_dir):
        """
        Load precomputed author_dict
        """

        print("Loading precomputed author partition from {}/author_partition.p".format(in_dir))

        with open("{}/author_partition.p".format(in_dir), 'rb') as infile:

            self.author_dict = pickle.load(infile)

        return self

    def setup_scores_dict(self, key_list):
        """
        For each year period & author, take TF-IDF scores for each keyword.
        """

        if self.word_to_id is None or self.corpora is None:
            self.build_dictionaries_and_corpora()

        if self.tf_idf_models is None:
            self.build_tf_idf_models()

        if self.author_dict is None:
            self.partition_by_author()

        ret = {"scores": {}, "metadata": {"KEYS": key_list, "YEARS": self.author_dict.keys()}}

        for y in self.author_dict.keys():
            ret["scores"][y] = []

            print("Building TF-IDF scores dictionary for period {}".format(str(y)))
            for a in tqdm.tqdm(sorted(self.author_dict[y].keys())):

                word_scores = {}
                tf_idf_doc = self.tf_idf_models[y][self.author_dict[y][a]]

                for t in tf_idf_doc:

                    id_to_word = self.word_to_id[y].get(t[0])

                    if id_to_word in key_list:
                        word_scores[id_to_word] = t[1]

                for k in key_list:
                    if k not in word_scores:
                        word_scores[k] = 0

                ret["scores"][y].append(word_scores)

        return ScoreMatResults(ret)

    def cluster_k_means(self, key_list):

        scores_dict = self.setup_scores_dict(key_list)

        return KMeansAuthorCluster(scores_dict)

    def cluster_hierarchical(self, key_list):

        scores_dict = self.setup_scores_dict(key_list)

        return HierarchicalAuthorCluster(scores_dict)