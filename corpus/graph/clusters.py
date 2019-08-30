import matplotlib.pyplot as plt
import matplotlib.colors as c
import numpy as np


class GraphClusters:
    """
    Visualize clustering results.
    """

    def __init__(self, data: np.ndarray, cluster_labels: list, title: str):

        self.data = data
        self.title = title
        self.cluster_labels = cluster_labels

        self.fig = None
        self.plt = None

    def create_plot(self):
        """
        Generate plot.
        """

        # setup the plot
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))

        n = len(set(self.cluster_labels))
        cmap = plt.get_cmap('jet', n)
        # define the bins and normalize

        bounds = np.linspace(0, n, n + 1)
        norm = c.BoundaryNorm(bounds, cmap.N)

        # the plot
        scat = ax.scatter(self.data[:, 0], self.data[:, 1], c=self.cluster_labels, cmap=cmap, norm=norm)

        # the colorbar
        cb = plt.colorbar(scat, drawedges=True)
        cb.set_label('Group Number')
        tick_locs = bounds + 0.5
        cb.set_ticks(tick_locs)
        cb.set_ticklabels([('#' + str(int(b))) for b in bounds + 1])

        scat.axes.get_xaxis().set_visible(False)
        scat.axes.get_yaxis().set_visible(False)
        ax.set_title(self.title)

        self.plt = plt

    def save(self, out_path: str):
        """
        Save graph to file
        """

        try:
            self.plt.savefig(out_path)
        except ValueError:
            print("Unsupported file format. \n"
                  "Please use one of the following: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz")
