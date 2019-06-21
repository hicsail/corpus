import os
import shutil
import json
import tqdm
import re

from nltk.stem.snowball import SnowballStemmer
from gensim import corpora


def _fail(msg: str):
    """
    Generic fail method for debugging.
    """

    print(msg)
    os._exit(1)


def build_keys(keys: list):
    """
    Build list of keyword tuples.
    """

    return [tuple(k.split()) for k in keys]


def num_dict(alist: list, keywords: [list, None]=None, nested: [int, None]=0):
    """
    Build empty dictionary with integers at leaf entries.
    alist: year_list or author_list
    """

    results = {}

    for item in alist:

        if nested == 0:
            results[item] = 0

        elif nested == 1:
            results[item] = {}
            results[item]['TOTAL'] = 0
            for keyword in keywords:
                results[item][keyword] = 0

        else:
            _fail('Shouldn\'t be able to get here.')

    return results


def list_dict(alist: list, keywords: [list, None]=None, nested: [None, int]=0):
    """
    Build empty dictionary with lists at leaf entries.
    alist: year_list or author_list
    """

    results = {}

    for item in alist:

        if nested == 0:
            results[item] = []

        elif nested == 1:
            results[item] = {}
            for keyword in keywords:
                results[item]['TOTAL'] = []
                results[item][keyword] = []

        else:
            _fail('Shouldn\'t be able to get here.')

    return results


def gensim_dict(alist: list):
    """
    Build empty dictionary with gensim Dictionary objects at leaf entries.
    alist: year_list or author_list
    """

    results = {}

    for item in alist:
        results[item] = corpora.Dictionary()

    return results


def determine_year(year: int, year_list: list):
    """
    Given a year and list of year periods,
    return which period that year falls into.
    """

    for i in (range(len(year_list[:-1]))):

        if year_list[i] <= year < year_list[i + 1]:
            return year_list[i]

    _fail("{} is not in range".format(year))


def stem(word: str, language: [str, None] = 'english'):
    """
    Returns input word and its stem.
    """

    try:
        s = SnowballStemmer(language.lower())
    except ValueError:
        _fail("{} is not supported, please enter a valid language.".format(language))

    stemmed = s.stem(word.lower())

    return '{0}: {1}'.format(word, stemmed)


# TODO: ask user if they want to overwrite directory or add to it, if it exists
def build_out(out_dir: str):
    """
    Build output directory, overwrite if it exists.
    """

    if out_dir is not None:
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        else:
            shutil.rmtree(out_dir)
            os.mkdir(out_dir)
    else:
        _fail("Please specify output directory.")


def doc2author(in_dir: str, out_dir: str, text_type: str):
    """
    create a dictionary <key=author, value=text>
    """
    print("\nGenerating author dictionary.\n")
    author_dict = dict()
    outfile = out_dir + "/british_small_author_dict.json"
    exists = os.path.isfile(outfile)
    if exists:
        with open(outfile, 'r') as fp:
            author_dict = json.load(fp)
    else:
        for subdir, dirs, files in os.walk(in_dir):
            for jsondoc in tqdm.tqdm(files):
                if jsondoc[0] != ".":
                    with open(in_dir + "/" + jsondoc, 'r', encoding='utf8') as infile:
                        try:
                            json_data = json.load(infile)
                            for k in json_data.keys():
                                author_raw = (json_data[k]["Author"]).lower()
                                author = re.sub(r'\W+', '_', author_raw)
                                text = json_data[k][text_type]
                                # stopwords are not excluded, since we are working on tf-idf
                                author_dict[author] = []
                                author_dict[author].extend(text)
                                # if author in author_dict:
                                #     author_dict[author].extend(text)
                                # else:
                                #     author_dict[author] = text
                        except json.decoder.JSONDecodeError:
                            print("Error loading file {}".format(jsondoc))
        with open(outfile, 'w') as fp:
            json.dump(author_dict, fp, sort_keys=True, indent=4)

    return author_dict





