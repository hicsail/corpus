from corpus import corpus, utils, results, graph
from corpus.nlp import tf_idf_author as tf
import pandas as pd
import sys, csv
import argparse, re, os
import matplotlib.pyplot as plt
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Filtered Text")
    parser.add_argument("-o", action="store", help="output directory where author_dict.json file will be saved")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    c = corpus.Corpus(
        'corp',
        args.i
    )

    model = c.tf_idf_author(
        'tfidf_author',
        out_dir=args.o,
        text_type=args.t
    )

    model.generating_author_dict()
