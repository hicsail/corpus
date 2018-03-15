import matplotlib.pyplot as plt
import numpy as np
import json


class GraphFrequency:
    """
    Visualize NLP results. Takes an input list of FrequencyResults
    objects and produces a graph of them together.
    """

    def __init__(self, corpora: list, title: str='Frequency Graph', colors: [list, None]=None):

        self.corpora = corpora
        self.title = title
        self.colors = colors

        self.graph_dict = {}
        self.num_docs = {}
        self.year_list = []
        self.g_max = 0
        self.plt = None

    def check_names(self):
        """
        Ensure that there are no name repeats in the corpora list.
        """

        names = set()

        for corpus in self.corpora:

            if isinstance(corpus, str):
                with open(corpus, 'r', encoding='utf8') as in_file:
                    jsondata = json.load(in_file)
                    names.add(jsondata['Name'])
            else:
                names.add(corpus.name)

        assert len(names) == len(self.corpora)

    def check_colors(self):
        """
        If a list of colors is passed, ensure that it is of the same length as the corpora list.
        """

        if self.colors is not None:
            assert len(self.colors) == len(self.corpora)

    def results_type(self):
        """
        Determine the type of data being plotted.
        """

        f_types = set()

        for corpus in self.corpora:

            if isinstance(corpus, str):
                with open(corpus, 'r', encoding='utf8') as in_file:
                    jsondata = json.load(in_file)
                    f_types.add(jsondata['Frequency Type'])
            else:
                f_types.add(corpus.f_type)

        if len(f_types) != 1:
            print("Warning: mismatched frequency types across corpora.\n")

        return f_types.pop()

    def check_year_lists(self):
        """
        Verify that all input corpora share a common year list.
        """

        year_lists = set()

        for corpus in self.corpora:

            if isinstance(corpus, str):
                with open(corpus, 'r', encoding='utf8') as in_file:
                    jsondata = json.load(in_file)
                    year_lists.add(tuple(jsondata['Years']))
            else:
                year_lists.add(tuple(corpus.years))

        if len(year_lists) != 1:
            print("Warning: malformed year list inputs.\n")

        self.year_list = list(year_lists.pop())

        return self

    def _build_graph_list(self, k, d):
        """
        Build a list of values to be graphed for a given keyword.
        """

        a = [0] * len(self.year_list)

        for i in range(len(self.year_list)):
            a[i] = d[self.year_list[i]][k]

        return a

    def _build_graph_list_from_json(self, k, d):
        """
        Build a list of values to be graphed for a given keyword from a JSON file.
        """

        a = [0] * len(self.year_list)

        for i in range(len(self.year_list)):
            a[i] = d[str(self.year_list[i])][k]

        return a

    def build_graph_dict(self):
        """
        Traverse each corpus' frequency dictionaries and populate
        dictionary of keyword / value mappings to be graphed.
        """

        for corpus in self.corpora:

            if isinstance(corpus, str):
                with open(corpus, 'r', encoding='utf8') as in_file:
                    jsondata = json.load(in_file)

                    c_res = jsondata['d']
                    c_keys = [k[0] for k in c_res[str(self.year_list[0])].items()]

                    name = jsondata['Name']
                    self.graph_dict[name] = {}

                    for k in c_keys:
                        self.graph_dict[name][k] = self._build_graph_list_from_json(k, c_res)
            else:
                c_res = corpus.d
                c_keys = [k[0] for k in c_res[self.year_list[0]].items()]

                self.graph_dict[corpus.name] = {}

                for k in c_keys:
                    self.graph_dict[corpus.name][k] = self._build_graph_list(k, c_res)

        return self

    def build_num_docs(self):
        """
        Build dictionary that records number of documents per period.
        """

        num_docs = {}

        for corpus in self.corpora:

            if isinstance(corpus, str):
                with open(corpus, 'r', encoding='utf8') as in_file:
                    jsondata = json.load(in_file)
                    values = jsondata['n'].values()

                    name = jsondata['Name']
                    num_docs[name] = values
            else:
                values = list(corpus.n.values())
                num_docs[corpus.name] = values

        self.num_docs = num_docs

        return self

    def find_max(self):
        """
        Traverse dict of frequency values and return min/max.
        """

        for c in self.graph_dict:
            for k in self.graph_dict[c]:
                for i in range(len(self.graph_dict[c][k])):
                    if self.graph_dict[c][k][i] > self.g_max:
                        self.g_max = self.graph_dict[c][k][i] * 1.1

        return self

    def _generate_labels(self):
        """
        Generate labels for x-axis.
        """

        labels = []
        for i in range(len(self.year_list) - 1):
            start = str(self.year_list[i])
            end = str(self.year_list[i + 1])
            labels.append("{0}-{1}".format(start, end))

        return labels

    def create_plot(self, x_label: str='Period', y_label: [str, None]=None,
                    title: [str, None]=None, bar: bool=True, bar_width: int=5,
                    leg_size: int=10, include_total=False):
        """
        Generate graph of input data.
        """

        self.check_year_lists()
        self.check_colors()

        self.build_graph_dict()
        self.build_num_docs()
        self.find_max()

        ax1 = plt.subplot2grid((1, 1), (0, 0))

        plt.xlabel(x_label)

        if y_label is None:
            y_label = self.results_type()
            plt.ylabel(y_label)
        else:
            plt.ylabel(y_label)

        if title is None:
            plt.title(self.title)
        else:
            plt.title(title)

        index = np.array(sorted(self.year_list))
        plt.xticks(index, self._generate_labels())

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(-25)
            label.set_size(7)

        if bar:
            i = 0
            colors_idx = 0
            for f in self.graph_dict:
                for k in self.graph_dict[f]:
                    if k == 'TOTAL' and not include_total:
                        pass
                    else:
                        x_coord = index + (5 * i) + bar_width

                        if self.colors is None:
                            rects = ax1.bar(
                                x_coord, self.graph_dict[f][k],
                                bar_width, alpha=.8,  color=np.random.rand(1, 3),
                                label="{0}: {1}".format(f, ' '.join(k) if isinstance(k, tuple) else k)
                            )
                        else:
                            rects = ax1.bar(
                                x_coord, self.graph_dict[f][k],
                                bar_width, alpha=.8,  color=self.colors[colors_idx],
                                label="{0}: {1}".format(f, ' '.join(k) if isinstance(k, tuple) else k)
                            )
                            colors_idx += 1

                        num_docs_record = list(self.num_docs[f])

                        for j in range(len(rects)):
                            h = rects[j].get_height()
                            ax1.text(rects[j].get_x() + rects[j].get_width()/2., 1.05*h, num_docs_record[j],
                                     ha='center', va='bottom')

                        i += 1

            ax1.axis(
                [self.year_list[0], self.year_list[len(self.year_list) - 1], float(0), float(self.g_max)]
            )

        else:
            for f in self.graph_dict:
                for k in self.graph_dict[f]:

                    ax1.plot(index, self.graph_dict[f][k],
                             label="{0}: {1}".format(f, ' '.join(k) if isinstance(k, tuple) else k)
                             )

            ax1.axis(
                [self.year_list[0], self.year_list[len(self.year_list) - 2], float(0), float(self.g_max)]
            )

        leg = ax1.legend(prop={'size': leg_size})
        leg.get_frame().set_alpha(0.1)

        self.plt = plt

        return self

    def show(self):
        """
        Display generated graph.
        """

        self.plt.show()

    def save(self, out_path: str):
        """
        Save graph to file
        """

        try:
            self.plt.savefig(out_path)
        except ValueError:
            print("Unsupported file format. \n"
                  "Please use one of the following: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz")


