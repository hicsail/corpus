

class AuthorCluster:

    def __init__(self, tf_idf_model, keywords):

        self.tf_idf_model = tf_idf_model
        self.keywords = keywords


class KMeansAuthorCluster(AuthorCluster):

    def __init__(self, tf_idf_model, keywords):

        super(KMeansAuthorCluster, self).__init__(tf_idf_model, keywords)


class HierarchicalAuthorCluster(AuthorCluster):

    def __init__(self, tf_idf_model, keywords):

        super(HierarchicalAuthorCluster, self).__init__(tf_idf_model, keywords)

