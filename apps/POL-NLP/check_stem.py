import argparse

from nltk.stem.snowball import SnowballStemmer


def stem(words, language):

    stemmer = SnowballStemmer(language)

    return [stemmer.stem(word.lower()) for word in words.split(",")]


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-w", help="list of words to stem", action="store")
    parser.add_argument("-l", help="desired language", action="store")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()
    stems = stem(args.w, args.l)

    print(stems)
