from corpus.results import *


class AuthorCluster:

    def __init__(self, scores_record: [str, ScoreMatResults]):

        if isinstance(scores_record, ScoreMatResults):
            self.scores_mat = scores_record.d["scores"]
            self.year_list = scores_record.y
            self.key_list = scores_record.k
        else:
            self.load_scores_from_file(scores_record)

    def load_scores_from_file(self, path):

        with open(path, 'r', encoding='utf8') as in_file:

            data = json.load(in_file)

            self.scores_mat = data["scores"]
            self.year_list = data["metadata"]["YEARS"]
            self.key_list = data["metadata"]["KEYS"]

        return self


class KMeansAuthorCluster(AuthorCluster):

    def __init__(self, scores_record):

        super(KMeansAuthorCluster, self).__init__(scores_record)


class HierarchicalAuthorCluster(AuthorCluster):

    def __init__(self, scores_record):

        super(HierarchicalAuthorCluster, self).__init__(scores_record)

