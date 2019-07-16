import re
import json
import csv
import pandas as pd
import numpy as np
from collections import defaultdict, OrderedDict
from corpus.utils import *


class Results:
    """
    Base class for all Results objects.
    """

    def __init__(self, d: dict, n: dict):

        self.d = d
        self.n = n


class FrequencyResults(Results):
    """
    Data structure that stores word frequency results over a list of keywords.
    """

    def __init__(self, d: dict, n: dict, f_type: str, name: str):

        super(FrequencyResults, self).__init__(d, n)

        self.name = name
        self.f_type = f_type
        self.years = [y[0] for y in self.d.items()]

    def debug_str(self):
        """
        Identify results object name and frequency type.
        """

        print("FrequencyResults object: \n\t - name: {0} \n\t - stores: {1}"
              .format(self.name, self.f_type)
              )

    def clean_keys(self):
        """
        Iterate over frequency results dictionary & convert tuples to strings.
        """

        d = self.d

        for f in d:
            for k in d[f]:
                if isinstance(k, tuple):
                    d[f][' '.join(k)] = d[f].pop(k)

        return d

    @staticmethod
    def _build_json(d: dict):
        """
        Transform results dictionary to JSON object.
        """

        jfile = json.dumps(d, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

        return jfile

    def write_to_json(self, out_path: str):
        """
        Write results to JSON file to use for later analysis.
        """

        d = self.clean_keys()

        jf = dict()
        jf['Years'] = self.years
        jf['Frequency Type'] = self.f_type
        jf['Name'] = self.name
        jf['n'] = self.n
        jf['d'] = d

        with open(out_path, 'w', encoding='utf-8') as j:
            j.write(self._build_json(jf))

    def write(self, out_path: str):
        """
        Write contents of FrequencyResults object to file.
        """

        with open(out_path + '.txt', 'w') as t:
            print("Writing results to text file.")

            for i in range(len(self.years) - 1):
                t.write(
                    "________________\n"
                    "Period: {0} - {1}\n"
                    .format(str(self.years[i]), str(self.years[i+1]))
                )
                t.write(
                    "Number of documents for this period: {}\n"
                    .format(str(self.n[self.years[i]]))
                )
                for k in self.d[self.years[i]].items():
                    if k[0] == 'TOTAL':
                        t.write(
                            "{0} of all keywords taken together for this period: {1}\n"
                            .format(self.f_type, str(k[1]))
                        )
                    else:
                        t.write(
                            "{0} of \"{1}\" for this period: {2}\n"
                            .format(self.f_type, " ".join(k[0]), str(k[1]))
                        )

    def display(self, keys: [None, list]=None):
        """
        Display FrequencyResults in console.
        """

        if keys is not None:
            keys = build_keys(keys)
        else:
            keys = ['TOTAL']

        for i in range(len(self.years) - 1):
            print(
                "________________\n"
                "Period: {0} - {1}\n"
                .format(str(self.years[i]), str(self.years[i+1]))
            )
            print(
                "Number of documents for this period: {}\n"
                .format(str(self.n[self.years[i]]))
            )
            for k in keys:
                if k == 'TOTAL':
                    print(
                        "{0} of all keywords taken together for this period: {1}"
                        .format(self.f_type, str(self.d[self.years[i]]['TOTAL']))
                        + "\n"
                    )
                else:
                    print(
                        "{0} of \"{1}\" for this period: {2}\n"
                        .format(self.f_type, " ".join(k), str(self.d[self.years[i]][k]))
                    )


class TopResults(Results):
    """
    Data structure that stores top word frequencies across a corpus.
    """

    def __init__(self, d: dict, n: dict, name: str):

        super(TopResults, self).__init__(d, n)

        self.name = name
        self.years = [y[0] for y in self.d.items()]

    def debug_str(self):
        """
        Identify TopResults object and name.
        """

        print("TopResults object: \n\t - name: {0}"
              .format(self.name)
              )

    def write(self, out_path: str):
        """
        Write contents of Frequency object to file.
        """

        with open(out_path + '.txt', 'w') as t:
            print("Writing results to text file.")

            for i in range(len(self.years) - 1):
                t.write(
                    "________________\n"
                    "Period: {0} - {1}\n"
                    .format(str(self.years[i]), str(self.years[i+1]))
                )
                t.write(
                    "Number of documents for this period: {}\n"
                    .format(str(self.n[self.years[i]]))
                )
                t.write("Top words for this period: \n")
                for k in self.d[self.years[i]]:
                    t.write(
                        "\"{0}\": {1}%\n"
                        .format(k[0], str(k[1]))
                    )

    def display(self):
        """
        Display TopResults in console.
        """

        for i in range(len(self.years) - 1):
            print(
                "________________\n"
                "Period: {0} - {1}\n"
                .format(str(self.years[i]), str(self.years[i+1]))
            )
            print(
                "Number of documents for this period: {}\n"
                .format(str(self.n[self.years[i]]))
            )
            print("Top words for this period:")
            for k in self.d[self.years[i]]:
                print(
                    "\"{0}\": {1}%"
                    .format(k[0], str(k[1]))
                )


class TfidfResults(Results):
    """
    Data structure that stores documents ranked by TF-IDF score for a keyword per period.
    """

    def __init__(self, d: dict, n: dict, keyword: str, name: str):

        super(TfidfResults, self).__init__(d, n)

        self.keyword = keyword
        self.name = name
        self.years = [y[0] for y in self.d.items()]

    def debug_str(self):
        """
        Identify TfidfResults object, name, and keyword.
        """

        print("TfidfResults object: \n\t - name: {0} \n\t - keyword: {1}"
              .format(self.name, self.keyword)
              )

    def write(self, out_path: str):
        """
        Write contents of Tfidf object to file.
        """

        with open(out_path + '.txt', 'w') as t:
            print("Writing results to text file.")

            for i in range(len(self.years) - 1):
                t.write(
                    "________________\n"
                    "Period: {0} - {1}\n"
                    .format(str(self.years[i]), str(self.years[i+1]))
                )
                t.write(
                    "Number of documents for this period: {}\n"
                    .format(str(self.n[self.years[i]]))
                )
                t.write(
                    "Documents with the highest TF-IDF score for \'{0}\' in this period: \n"
                    .format(self.keyword)
                )
                for k in self.d[self.years[i]]:
                    t.write(
                        "\"{0}[{1}]\": {2}%\n"
                        .format(k[0], k[2], str(k[1]))
                    )

    def display(self):
        """
        Display Tfidf results in console.
        """

        for i in range(len(self.years) - 1):
            print(
                "________________\n"
                "Period: {0} - {1}\n"
                .format(str(self.years[i]), str(self.years[i+1]))
            )
            print(
                "Number of documents for this period: {}\n"
                .format(str(self.n[self.years[i]]))
            )
            print("Documents with the highest TF-IDF score for \'{0}\' in this period: \n"
                  .format(self.keyword))
            for k in self.d[self.years[i]]:
                print(
                    "\"{0}[{1}]\": {2}%\n"
                    .format(k[0], k[2], str(k[1]))
                )


class TopicResults(Results):
    """
    Stores topic modeling results.
    """

    def __init__(self, d: dict, n: dict, name: str):

        super(TopicResults, self).__init__(d, n)

        self.name = name
        self.years = [y[0] for y in self.d.items()]

    def debug_str(self):
        """
        Identfiy TopicResults object and name.
        """

        print("Topic Model object: \n\t - {0}"
              .format(self.name)
              )

    @staticmethod
    def _filter_topic(t: str):
        """
        Filter confusing characters from returned topic string.
        """

        filtered = re.split('\W[0-9]*', str(t))

        for k in range(len(filtered) - 1, -1, -1):
            if filtered[k] == "" or filtered[k] == "None":
                del filtered[k]
            else:
                filtered[k] = filtered[k].lower()

        return ", ".join(filtered)

    @staticmethod
    def _filter_topic_weights(t: str):
        """
        Filter out weight values from returned topic string.
        """

        filtered = str(t[1]).split('+')

        for k in range(len(filtered) - 1, -1, -1):
            if filtered[k] == "" or filtered[k] == "None":
                del filtered[k]
            else:
                filtered[k] = filtered[k].split('*')

        res = []
        for k in filtered:
            res.append(
                "{0} ({1})".format(k[1].strip(), k[0].strip())
            )

        return ", ".join(res)

    def write(self, out_path: str, num_topics: int = 10,
              num_words: int=10, weights: bool = False):
        """
        Write contents of LdaResults object to file.
        """

        with open(out_path, 'w') as t:
            print("Writing results to file.")

            for i in range(len(self.years) - 1):
                t.write(
                    "________________\n"
                    "Period: {0} - {1}\n"
                    .format(str(self.years[i]), str(self.years[i+1]))
                )
                t.write(
                    "Number of documents for this period: {}\n"
                    .format(str(self.n[self.years[i]]))
                )
                topics = self.d[self.years[i]]\
                    .show_topics(num_topics=num_topics, num_words=num_words)
                idx = 0
                for topic in topics:
                    if not weights:
                        top = self._filter_topic(topic)
                        t.write("Topic {0}: {1}\n"
                                .format(str(idx), top)
                                )
                        idx += 1
                    else:
                        top = self._filter_topic_weights(topic)
                        t.write("Topic {0}: {1}\n"
                                .format(str(idx), top))
                        idx += 1


class DiffPropResults:
    """
    Stores difference in proportions metrics between two corpora.
    """

    def __init__(self, d: dict, year_list: list, name: str):

        self.name = name
        self.d = d
        self.years = year_list

    def display(self):
        """
        Display difference in proportions results in console.
        """

        for i in range(len(self.years) - 1):
            print(
                "________________\n"
                "Period: {0} - {1}\n"
                .format(str(self.years[i]), str(self.years[i+1]))
            )
            print(
                "Z-score: {0}\n"
                .format(str(self.d[self.years[i]][0]))
            )
            print(
                "P values: {0}\n"
                .format(str(self.d[self.years[i]][1]))
            )
            print(
                "Significance: {0}\n"
                .format(str(self.d[self.years[i]][2]))
            )
            print(
                "Critical: {0}\n"
                .format(str(self.d['Critical']))
            )

    def write(self, out_path: str):
        """
        Write difference in proportions results to file.
        """

        with open(out_path + '.txt', 'w') as t:
            print("Writing results to text file.")

            for i in range(len(self.years) - 1):
                t.write(
                    "________________\n"
                    "Period: {0} - {1}\n"
                    .format(str(self.years[i]), str(self.years[i+1]))
                )
                t.write(
                    "Z-score: {0}\n"
                    .format(str(self.d[self.years[i]][0]))
                )
                t.write(
                    "P values: {0}\n"
                    .format(str(self.d[self.years[i]][1]))
                )
                t.write(
                    "Significance: {0}\n"
                    .format(str(self.d[self.years[i]][2]))
                )
                t.write(
                    "Critical: {0}\n"
                    .format(str(self.d['Critical']))
                )


class TfidfAuthorResultMat:
    """
    the score matrix, either full mat or non_zero mat
    """
    def __init__(self, authors: list, author_keywords_score_mat: np.ndarray, keywords: list):
        self.authors = authors
        self.author_keywords_score_mat = author_keywords_score_mat
        self.keywords = keywords

        assert len(authors) == len(author_keywords_score_mat)
        assert len(keywords) == len(author_keywords_score_mat[0])

    def write_csv(self, out_path: str):
        df = pd.DataFrame(data=self.author_keywords_score_mat, columns=self.keywords, index=self.authors)
        df.to_csv(out_path)


class TfidfAuthorClusters(TfidfAuthorResultMat):
    """
    clustering results
    """
    def __init__(self, authors: list, author_keywords_score_mat: np.ndarray, cluster_labels: list, zero_authors: list):
        super(TfidfAuthorClusters, self).__init__(authors, author_keywords_score_mat)
        self.cluster_labels = cluster_labels
        self.zero_authors = zero_authors

        assert len(authors) == len(cluster_labels)

    def _cluster_authors(self):
        clustered_authors_dict = defaultdict(list)
        for k, v in zip(self.cluster_labels, self.authors):
            clustered_authors_dict[k].append(v)
        return clustered_authors_dict

    #TODO: may add some stats later
    def write_authors_clustered(self, out_path: str, name: str):
        """
        :param out_path: the output file
        :param name: name of the clustering method
        """
        # n_clusters = set(self.cluster_labels)
        # clustered_authors_list = sorted(self._cluster_authors().items()) # returns a list of tuples
        clustered_authors_dict = OrderedDict(sorted(self._cluster_authors().items()))

        with open(out_path + '.txt', 'w') as t:
            print("Writing results to text file.")
            t.write("Clustered by {0}\n".format(name))
            t.write("Authors not used any key words:\n\t{0}\n".format(self.zero_authors))
            for key, val in clustered_authors_dict.items():
                t.write("Group {0}:\n\t{1}\n".format(key, val))
