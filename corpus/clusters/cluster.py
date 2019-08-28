from sklearn.cluster import KMeans

from corpus.results import *


class AuthorCluster:

    def __init__(self, scores_record: [str, ScoreMatResults]):

        if isinstance(scores_record, ScoreMatResults):
            self.scores_mat = scores_record.d["scores"]
            self.year_list = scores_record.y
            self.key_list = scores_record.k
        elif isinstance(scores_record, str):
            self.load_scores_from_file(scores_record)
        else:
            print("Must pass either ScoreMatResults object or filepath to ScoreMatResults JSON.\n")
            # TODO: exit

        params = self.setup_vectors()

        self.nonzero_authors = params["NONZERO_AUTHORS"]
        self.nonzero_mats = params["NONZERO_MATS"]
        self.omitted_authors = params["OMITTED_AUTHORS"]

    def load_scores_from_file(self, path):

        with open(path, 'r', encoding='utf8') as in_file:

            data = json.load(in_file)

            self.scores_mat = data["scores"]
            self.year_list = data["metadata"]["YEARS"]
            self.key_list = data["metadata"]["KEYS"]

        return self

    @staticmethod
    def check_nonzero(word_scores):

        return sum([t[1] > 0 for t in word_scores.items()])

    @staticmethod
    def format_scores_entry(word_scores):

        return [word_scores[k] for k in sorted(word_scores.keys())]

    def setup_vectors(self):

        ret = {}

        nonzero_authors = {}
        nonzero_mats = {}
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
            nonzero_mats[y] = [ret[y][a] for a in nonzero_authors[y]]

        return {"NONZERO_AUTHORS": nonzero_authors, "NONZERO_MATS": nonzero_mats, "OMITTED_AUTHORS": omitted}


class KMeansAuthorCluster(AuthorCluster):

    def __init__(self, scores_record):

        super(KMeansAuthorCluster, self).__init__(scores_record)


class HierarchicalAuthorCluster(AuthorCluster):

    def __init__(self, scores_record):

        super(HierarchicalAuthorCluster, self).__init__(scores_record)

