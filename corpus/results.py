import numpy as np
import json
import re

from collections import defaultdict, OrderedDict

from corpus.utils import *
from corpus.graph import GraphClusters


class Results:
    """
    Base class for all Results objects.
    """

    def __init__(self, d: [dict, str], n: dict):

        self.d = d
        self.n = n


class FrequencyResults(Results):
    """
    Stores word frequency results over a list of keywords.
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

        print("Writing results to file.")
        with open(out_path, 'w') as t:

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
    Stores top word frequencies across a corpus.
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

        print("Writing results to file.")
        with open(out_path, 'w') as t:

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

        print("Writing results to file.")
        with open(out_path, 'w') as t:

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

        print("Writing results to file.")
        with open(out_path, 'w') as t:

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


class DiffPropResults(Results):
    """
    Stores difference in proportions metrics between two corpora.

    # TODO: fill out num_docs (n) parameter
    """

    def __init__(self, d: dict, year_list: list, name: str):

        super(DiffPropResults, self).__init__(d, {})
        self.name = name
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

        print("Writing results to file.")
        with open(out_path, 'w') as t:

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


class ScoreMatResults(Results):
    """
    Stores data that gets fed to clustering classes.

    # TODO: fill out num_docs (n) parameter
    """

    def __init__(self, d):

        super(ScoreMatResults, self).__init__(d, {})

        self.y = self.d["metadata"]["YEARS"]
        self.k = self.d["metadata"]["KEYS"]

    def debug_key_list(self):

        print("Key list: {}".format(", ".join(k for k in self.k)))

    def debug_year_list(self):

        print("Year list: {}".format(", ".join(self.y)))

    def write_to_json(self, out_path):
        """
        Write TF-IDF scores data to file.
        """

        with open(out_path, 'w', encoding='utf8') as out_file:
            out_file.write(json.dumps(self.d, indent=4, ensure_ascii=False))


class ClusterResults:
    """
    Encapsulates graphed cluster objects.
    """

    def __init__(self, l, t, a, o, k):

        self.labels = l
        self.tsne = t
        self.authors_dict = a
        self.omitted = o
        self.key_list = k

        self.graphs = None
        self.authors_grouped = None

    def graph_results(self):
        """
        Initialize GraphClusters objects for each year period.
        """

        ret = {}

        for y in self.tsne.keys():

            ret[y] = GraphClusters(self.tsne[y], self.labels[y], title="Clustering Result for period: {}".format(y))

        self.graphs = ret

        return self

    def group_authors(self):
        """
        Group authors into their respective cluster groups per year period.
        """

        ret = {}

        for y in self.authors_dict.keys():

            author_group = self.authors_dict[y]

            if len(author_group) > 0:

                ret[y] = {}

                for i in range(len(author_group)):

                    label = self.labels[y][i] + 1
                    author = author_group[i]

                    try:
                        ret[y][label].append(author)

                    except KeyError:
                        ret[y][label] = [author]

        self.authors_grouped = ret

        return self

    def write_cluster_groups(self, out_path):
        """
        Write authors grouped by cluster ID to file.
        """

        if self.authors_grouped is None:
            self.group_authors()

        with open(out_path, 'w') as t:

            for y in self.authors_grouped.keys():

                t.write("\nYear Period beginning: {}\n".format(str(y)))

                for a in sorted(self.authors_grouped[y].keys()):
                    t.write("\n\tCluster: {}\n\n".format(str(a)))

                    for aa in self.authors_grouped[y][a]:
                        t.write("\t\t{}\n".format(aa))

    def save_results(self, out_dir):
        """
        Save cluster figures to a directory.
        """

        if self.graphs is None:
            self.graph_results()

        build_out(out_dir)

        for y in self.graphs.keys():

            # have to create & save bc subsequent plots will overwrite past plots
            self.graphs[y].create_plot()
            self.graphs[y].save("{0}/{1}.png".format(out_dir, str(y)))
