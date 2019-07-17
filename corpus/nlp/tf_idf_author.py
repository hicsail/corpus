import numpy as np

from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from sklearn import manifold
from sklearn.cluster import KMeans

from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
import pandas as pd

from kneed import KneeLocator

from corpus.results import *


class TfidfAuthor:
    """
    Data structure for identifying authors(instead of documents) and their corresponding TF-IDF
    scores, with respect to particular keywords
    """

    def __init__(
            self, name: str, in_dir: str, out_dir: str, stop_words: [list, set, None] = None):

        self.name = name
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.stop_words = self.setup_stop_words(stop_words)

        self.author_dict = None
        self.tf_idf_model = None
        self.word_to_id = None
        self.corpora = None

        self.author_word_score_dict = None

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

    def get_author_dict_from_json(self, file_path: str):
        """
        Set author_dict from Json file.
        """

        print("Loading author_dict from JSON file at {}\n".format(file_path))
        exists = os.path.isfile(file_path)
        if exists:
            with open(file_path, 'r', encoding='utf8') as fp:
                self.author_dict = json.load(fp)
        else:
            print("\nAuthor dict not found, please use 'generating_author_dict' to generate author_dict, \
            \nor use 'write_author_dict_to_file' if you want ot save it")

        return self

    def generating_author_dict(self, text_type: str, save: bool=True):
        author_dict = dict()
        for subdir, dirs, files in os.walk(self.in_dir):
            for jsondoc in tqdm.tqdm(files):
                if jsondoc[0] != ".":
                    with open(self.in_dir + "/" + jsondoc, 'r', encoding='utf8') as infile:
                        try:
                            json_data = json.load(infile)
                            for k in json_data.keys():
                                author_raw = (json_data[k]["Author"]).lower()
                                author = re.sub(r'\W+', '_', author_raw)
                                text = json_data[k][text_type]
                                author_dict[author] = []
                                author_dict[author].extend(text)

                        except json.decoder.JSONDecodeError:
                            print("Error loading file {}".format(jsondoc))

        self.author_dict = author_dict

        if save:
            print("\nWriting author_dict to csv file... might take a while...\n")
            outfile = self.out_dir + "/author_dict.json"
            with open(outfile, 'w') as fp:
                json.dump(self.author_dict, fp, sort_keys=True, indent=4)

        return self

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

        # corpora_results = [word_to_id.doc2bow(text) for _, text in self.author_dict.items()]

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
            self.build_tf_idf_author_model()

        build_out(out_dir)
        os.mkdir("{0}/{1}".format(out_dir, 'tfidf_authors'))
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

        self.tf_idf_model = TfidfModel(self.corpora, dictionary=self.word_to_id, smartirs='ltc')

        return self

    def get_all_word_scores(self):
        """

        :return: a dictionary
            {
                "author1": { "w1": <score>, "w2": <score>, ... },
                "author2": { "w1": <score>, "w2": <score>, ... },
                ...
             }
        """

        author_word_score_dict = dict()

        for author, text in self.author_dict.items():

            author_word_score_dict[author] = dict()

            d2b = self.word_to_id.doc2bow(text)
            tfidf = self.tf_idf_model[d2b]
            for wid, s in tfidf:
                word = self.word_to_id.get(wid)
                author_word_score_dict[author][word] = s

        self.author_word_score_dict = author_word_score_dict
        return self

    def get_author_keywords_score_matrix(self, keywords: list):
        """
        :param keywords: a list of key words
        :return: a 2D array, each row is a author and each column is a word
        """
        full_mat = []
        for a, words in self.author_word_score_dict.items():
            scores_per_author = []
            for w in keywords:
                s = words.get(w)
                if s is None:
                    s = 0
                scores_per_author.append(s)
            full_mat.append(scores_per_author)

        return AuthorKeywordsMat(full_mat, [*self.author_dict], keywords)


class AuthorKeywordsMat:
    """
    takes in the full matrix of author-keywords tfidf scores
    """

    def __init__(self, mat, row_index: list, col_index: list):
        """

        :param mat:
        :param row_index: authors
        :param col_index: the keywords list
        """

        assert len(row_index) == len(mat)
        assert len(col_index) == len(mat[0])

        self.mat = mat
        self.row_index = row_index  # authors
        self.col_index = col_index  # keywords

        self.nonzero_mat = None
        self.nonzero_authors = None  # only for authors who used at least one keyword
        self._get_nonzero_mat()

        self.tsne = None
        # self.kmeans = None
        # self.hclustering = None


    def write_full_mat(self, outfile: str):
        df = pd.DataFrame(data=self.mat, columns=self.col_index, index=self.row_index)
        df.to_csv(outfile)

    def _get_nonzero_mat(self):

        nonzero_index = [i for i in range(len(self.mat)) if np.count_nonzero(self.mat[i]) != 0]
        self.nonzero_authors = [self.row_index[i] for i in nonzero_index]
        self.nonzero_mat = [self.mat[i] for i in nonzero_index]

        return self

    def _get_zero_authors(self):

        zero_authors = list(set(self.row_index) - set(self.nonzero_authors))
        assert len(zero_authors) + len(self.nonzero_authors) == len(self.row_index)

        return zero_authors

    ##################################################################################################
    #        t-SNE
    #        authors not using any keywords are excluded
    ##################################################################################################

    def compute_tsne(self):

        print("Computing t-SNE embedding on NON-zero authors")
        tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
        mat_tsne = tsne.fit_transform(self.nonzero_mat)

        self.tsne = mat_tsne
        # TODO: plot?
        return self

    ##################################################################################################
    #        Clustering Methods
    #        authors not using any keywords are excluded
    ##################################################################################################
    #        K-Means
    ##################################################################################################

    def cluster_kmeans(self, n: [int, None]=None):

        if n is None:
            print("You did not specify a cluster number.\nLet me try to find one for you.")
            maxK = int(len(self.nonzero_mat) / 4)
            Ks = [i for i in range(1, maxK)]
            errors = np.zeros(maxK-1)
            for k in tqdm.tqdm(Ks):
                temp_kmeans = KMeans(init='k-means++', n_clusters=k, n_init=10)
                temp_kmeans.fit_predict(self.nonzero_mat)
                errors[k - 1] = temp_kmeans.inertia_

            kn = KneeLocator(Ks, errors, curve='convex', direction='decreasing')
            n = kn.knee

        print("Kmeans Clustering on K = ", n)
        kmeans = KMeans(n_clusters=n)
        kmeans.fit(self.nonzero_mat)

        cluster_labels = kmeans.predict(self.nonzero_mat)
        zauthors = self._get_zero_authors()

        # return authors, mat, labels and authors_not_using_keywords
        return TfidfAuthorClusters(self.nonzero_mat, self.nonzero_authors, self.col_index, cluster_labels, zauthors)

    ##################################################################################################
    #        Hierarchical Clustering
    ##################################################################################################

    def plot_dendrogram(self, method: [str, None]=None):

        if method is None:
            method = 'ward'
        Z = linkage(self.nonzero_mat, method=method)
        fig = plt.figure(figsize=(15, 50))
        dn = dendrogram(Z, orientation='left', labels=self.nonzero_authors, leaf_font_size=11,
                        color_threshold=max(Z[:, 2]))
        # plt.show()
        plt.savefig('hahaha.png')

    def cluster_hcluster(self, cutoff):

        cluster_labels = fcluster(Z, cutoff, 'distance')
        zauthors = self._get_zero_authors()
        return TfidfAuthorClusters(self.nonzero_authors, self.nonzero_mat, cluster_labels, zauthors)
