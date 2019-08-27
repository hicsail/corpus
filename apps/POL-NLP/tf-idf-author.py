import argparse


def setup_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", action="store", help="path to *_author_dict.json file")
    parser.add_argument("-i", action="store", help="input directory")
    parser.add_argument("-t", action="store", help="text field to analyze", default="Filtered Text")
    parser.add_argument("-o", action="store", help="output directory where all the results will be saved")
    parser.add_argument("-k", action="store", help="keywords")

    return parser.parse_args()


if __name__ == '__main__':

    args = setup_parser()

    if args.a:
        print("Hi")
    else:
        print("Hey")