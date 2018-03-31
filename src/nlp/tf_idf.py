import tqdm

from gensim.models import TfidfModel

from src.results import *


class Tfidf:
    """
    Data structure for identifying documents and their corresponding TF-IDF
    scores, with respect to particular keywords and a list of year periods.
    """

    def __init__(
            self, name: str, in_dir: str, text_type: str, year_list: list,
            stop_words: [list, set, None]=None):

        self.name = name
        self.in_dir = in_dir
        self.text_type = text_type
        self.year_list = year_list
        if stop_words is not None:
            self.stop_words = stop_words
        else:
            self.stop_words = {}

        self.tf_idf_models = None
        self.word_to_id = None
        self.corpora = None

    def _update_dictionaries_and_corpora(self, k, json_data, word_to_id_results, corpora_results):

        year = int(json_data[k]["Date"])

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
        Construct word_to_id that store the word -> id mappings and the bag of words
        representations of the documents in the corpus. Used for building TF-IDF models
        and LDA / LSI topic models.
        """

        if self.word_to_id is not None:
            return

        word_to_id_results = gensim_dict(self.year_list)
        corpora_results = list_dict(self.year_list)

        print("Building word to ID mappings.")

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

    def write_tfidf(self, out_dir: str):

        if self.tf_idf_models is None:
            self.build_tf_idf_models()

        build_out(out_dir)

        for year in self.year_list:

            model = self.tf_idf_models[year]
            model.save("{0}/{1}".format(out_dir, str(year)))

    def build_tf_idf_models(self):
        """
        Combines the word_to_id and corpora dictionaries
        to construct TF-IDF models for each year period.
        """

        if self.word_to_id is None or self.corpora is None:
            self.build_dictionaries_and_corpora()

        results = num_dict(self.year_list)

        for year in self.year_list:
            results[year] = TfidfModel(self.corpora[year], dictionary=self.word_to_id[year])

        self.tf_idf_models = results

        return self

    def _update_top_n(self, k, json_data, results, num_docs, keyword, jsondoc):
        """
        Update dictionary that stores the top <n> documents w/r/t a given
        keyword within a corpus.
        """

        year = int(json_data[k]["Date"])

        if self.year_list[0] <= year < self.year_list[-1]:

            text = json_data[k][self.text_type]

            if keyword in set(text):

                target = determine_year(year, self.year_list)
                num_docs[target] += 1
                d2b = self.word_to_id[target].doc2bow(text)
                tfidf_doc = self.tf_idf_models[target][d2b]

                for t in tfidf_doc:

                    if self.word_to_id[target].get(t[0]) == keyword:
                        results[target].append((jsondoc, t[1]))

    def _top_n(self, results, n):
        """
        Helper method, takes top results given a threshold from input top results data.
        """

        top_results = list_dict(self.year_list)

        for year in self.year_list:
            top = sorted(results[year], key=lambda x: x[1])
            top_results[year] = top[:n]

        return top_results

    def top_n(self, keyword: str, n: int=10, name: str='Top Files'):
        """
        Iterates over the corpus and computes TF-IDF scores for each document,
        with respect to the precomputed TF-IDF models. Extracts results for a
        particular keyword and displays the < n > documents whose TF-IDF scores
        for that keyword are the highest.
        """

        if self.tf_idf_models is None:
            self.build_tf_idf_models()

        results = list_dict(self.year_list)
        num_docs = num_dict(self.year_list, nested=0)

        print("Calculating {0} files with top TF-IDF scores for \'{1}\'".format(n, keyword))

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


