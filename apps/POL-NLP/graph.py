import argparse
import os

from corpus.graph.frequencies import GraphFrequency

"""
TODO: line graphing
TODO: look into mean, var, avg
TODO: configurable numbers above bars
TODO: black & white graphing
TODO: .tiff output
"""


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-t", action="store_true", help="display total only")
    parser.add_argument("-title", action="store", help="graph title")
    parser.add_argument("-bar_width", action="store", help="bar width", default=5)

    return parser.parse_args()


def setup_filepaths(input_dir):

    for subdir, dirs, files in os.walk(input_dir):
        return ["{0}/{1}".format(input_dir, file) for file in files if file[0] != "."]


if __name__ == '__main__':

    args = setup_parser()

    paths = setup_filepaths(args.i)

    g = GraphFrequency(paths)\
        .create_plot(total_only=args.t, title=args.title, bar_width=int(args.bar_width))\
        .show()
