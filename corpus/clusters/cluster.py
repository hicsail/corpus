from corpus.results import *


class AuthorCluster:

    def __init__(self, scores_record: [str, ScoreMatResults]):

        if isinstance(scores_record, ScoreMatResults):
            self.scores_mat = scores_record.d
            self.year_list = scores_record.y
            self.key_list = scores_record.key_list
        else:
            pass


class KMeansAuthorCluster(AuthorCluster):

    def __init__(self, scores_record):

        super(KMeansAuthorCluster, self).__init__(scores_record)


class HierarchicalAuthorCluster(AuthorCluster):

    def __init__(self, scores_record):

        super(HierarchicalAuthorCluster, self).__init__(scores_record)

