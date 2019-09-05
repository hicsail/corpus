from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn import manifold
from kneed import KneeLocator

import numpy as np
import matplotlib.pyplot as plt

from corpus.results import *


class AuthorCluster:
    """
    Base class for author-partitioned corpus clusters.
    """

    def __init__(self, scores_record: [str, ScoreMatResults]):

        if isinstance(scores_record, ScoreMatResults):
            self.scores_mat = scores_record.d["scores"]
            self.year_list = scores_record.y
            self.key_list = scores_record.k

        elif isinstance(scores_record, str):
            self.load_scores_from_file(scores_record)

        else:
            raise Exception("Must pass either ScoreMatResults object or filepath to ScoreMatResults JSON.\n")

        params = self.setup_vectors()

        self.nonzero_authors = params["NONZERO_AUTHORS"]
        self.nonzero_mat = params["NONZERO_MAT"]
        self.omitted_authors = params["OMITTED_AUTHORS"]

        self.tsne = self.compute_tsne()

    def load_scores_from_file(self, path):
        """
        Load dictionary that stores author matrices from JSON file.
        """

        with open(path, 'r', encoding='utf8') as in_file:

            data = json.load(in_file)

            self.scores_mat = data["scores"]
            self.year_list = data["metadata"]["YEARS"]
            self.key_list = data["metadata"]["KEYS"]

        return self

    @staticmethod
    def check_nonzero(word_scores):
        """
        Check whether all word scores for an entry are 0.
        """

        return sum([t[1] > 0 for t in word_scores.items()])

    @staticmethod
    def format_scores_entry(word_scores):
        """
        Transform dict of word scores to a list.
        """

        return [word_scores[k] for k in sorted(word_scores.keys())]

    def setup_vectors(self):
        """
        Set up vectors corresponding to authors with at least one positive score
        for all keywords, and omitted authors who have all scores == 0.
        """

        ret = {}

        nonzero_authors = {}
        nonzero_mat = {}
        omitted = {}

        for y in self.scores_mat.keys():

            ret[y] = {}
            omitted[y] = []

            for a in self.scores_mat[y].keys():

                if self.check_nonzero(self.scores_mat[y][a]):
                    ret[y][a] = self.format_scores_entry(self.scores_mat[y][a])

                else:
                    omitted[y].append(a)

            nonzero_authors[y] = sorted(ret[y].keys())
            nonzero_mat[y] = [ret[y][a] for a in nonzero_authors[y]]

        return {"NONZERO_AUTHORS": nonzero_authors, "NONZERO_MAT": nonzero_mat, "OMITTED_AUTHORS": omitted}

    def compute_tsne(self):
        """
        Compute TSNE for each year period.
        """

        ret = {}

        for y in self.nonzero_mat.keys():

            # filter out empty entries
            if len(self.nonzero_mat[y]) > 0:

                tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
                ret[y] = tsne.fit_transform(self.nonzero_mat[y])

        return ret

    def _dict_from_clusters_list(self, num_clusters_list: list):
        """
        Read number of clusters per year period from list.
        """

        ret = {}

        mat_keys = list(self.nonzero_mat.keys())

        for i in range(len(mat_keys) - 1):
            ret[mat_keys[i]] = num_clusters_list[i]

        return ret


class KMeansAuthorCluster(AuthorCluster):
    """
    K Means clustering for author-partitioned corpus clusters.
    """

    def __init__(self, scores_record):

        super(KMeansAuthorCluster, self).__init__(scores_record)

    def generate_num_clusters(self):
        """
        Generate ideal number of clusters for K Means.

        TODO: fill out empty entries in ret with an error message that can be
        interpreted when it's passed to graphing functions.
        """

        ret = {}

        for y in self.nonzero_mat.keys():
            max_ks = int(len(self.nonzero_mat[y]) / 4)

            # filter entries that are too small for clustering
            if max_ks > 4:

                all_ks = [i for i in range(1, max_ks)]
                errors = np.zeros(max_ks-1)

                for k in all_ks:

                    temp_kmeans = KMeans(init='k-means++', n_clusters=k, n_init=10)
                    temp_kmeans.fit_predict(self.nonzero_mat[y])
                    errors[k-1] = temp_kmeans.inertia_

                kn = KneeLocator(all_ks, errors, curve='convex', direction='decreasing')
                ret[y] = kn.knee

        return ret

    def _cluster(self, num_clusters_dict: dict):
        """
        Populate cluster labels dictionary for each year period.
        """

        ret = {}

        for y in num_clusters_dict.keys():

            c = KMeans(n_clusters=num_clusters_dict[y])
            c.fit(self.nonzero_mat[y])
            ret[y] = c.predict(self.nonzero_mat[y])

        return ret

    def fit_clusters(self, num_clusters: [list, None] = None):
        """
        Fit K Means cluster and return ClusterResults object.
        """

        if num_clusters is None:
            num_clusters_dict = self.generate_num_clusters()

        else:
            num_clusters_dict = self._dict_from_clusters_list(num_clusters)

        labels = self._cluster(num_clusters_dict)

        return ClusterResults(labels, self.tsne, self.nonzero_authors, self.omitted_authors, self.key_list)


class HierarchicalAuthorCluster(AuthorCluster):
    """
    Hierarchical clustering for author-partitioned corpus clusters.
    """

    def __init__(self, scores_record):

        super(HierarchicalAuthorCluster, self).__init__(scores_record)

        self.z = None

    def set_z(self, method: [str, None] = 'ward'):
        """
        Set Z values for each year period.
        """

        ret = {}

        for y in self.nonzero_mat.keys():

            # filter out empty entries
            if len(self.nonzero_mat[y]) > 0:

                nonzero_np = np.array([np.array(i) for i in self.nonzero_mat[y]])
                ret[y] = linkage(nonzero_np, method=method)

        self.z = ret

        return self

    def _cluster(self, cutoffs_dict):
        """
        Compute cluster labels for each year period.
        """

        ret = {}

        for y in self.nonzero_mat.keys():

            # filter out empty entries
            if len(self.nonzero_mat[y]) > 0:
                ret[y] = fcluster(self.z[y], cutoffs_dict[y], 'distance')

        return ret

    def fit_clusters(self, cutoffs_list: list):
        """
        Fit Hierarchical cluster and return ClusterResults object.
        """

        if self.z is None:
            self.set_z()

        num_clusters_dict = self._dict_from_clusters_list(cutoffs_list)
        labels = self._cluster(num_clusters_dict)

        return ClusterResults(labels, self.tsne, self.nonzero_authors, self.omitted_authors, self.key_list)

    def _generate_dendrograms(self, out_dir, y):
        """
        Generate dendrogram plot and save to file.
        """

        authors_np = [i for i in self.nonzero_authors[y]]

        figlen = len(self.nonzero_mat[y]) / 9
        fig = plt.figure(figsize=(15, figlen))

        # matplotlib is awful
        dn = dendrogram(self.z[y], orientation='left', labels=authors_np, leaf_font_size=9)

        plt.tight_layout()
        plt.savefig("{0}/{1}".format(out_dir, str(y)), dpi=200)

    def generate_dendrograms(self, out_dir):
        """
        Generate all dendrogram plots and save to directory.
        """

        build_out(out_dir)

        if self.z is None:
            self.set_z()

        for y in self.nonzero_mat.keys():

            # filter out empty entries
            if len(self.nonzero_mat[y]) > 0:
                self._generate_dendrograms(out_dir, y)
