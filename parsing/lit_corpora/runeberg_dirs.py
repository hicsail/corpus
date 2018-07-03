import csv
import argparse
import tqdm

from parsing.utils import *
from parsing.parsed import Parsed


def csv_path(path_str):
    """
    Return path to Runeberg CSV file.
    """

    base_dir = '/'.join(path_str.split('/')[:-1])

    return "{}/data/csv/RB/runeberg.csv".format(base_dir)


def parse_csv(csv_in):
    """
    Build volume mappings from input CSV file.
    """

    ids = {}
    with open(csv_in, 'r', encoding='utf-8') as csv_in:
        read_csv = csv.reader(csv_in, delimiter=',')
        for row in read_csv:
            src = row[2]
            ids[src] = {}
            ids[src]["PUBDATE"] = row[1]
            ids[src]["TITLE"] = row[2]
            ids[src]["AUTHOR"] = row[3]

    return ids


def parse_txt(in_dir, mappings, out_dir):
    """
    Iterate over directory of Runeberg text files, parse each volume to a JSON object.
    """

    for subdir, dirs, files in os.walk(in_dir):
        for vol in tqdm.tqdm(dirs):

            if vol[0] != "." and vol != "":

                obj = Parsed()

                try:
                    with open("{}/{}/title".format(in_dir, vol), 'r') as title_str:
                        id_str = title_str.read()
                    maps = mappings[id_str]
                    valid = True
                except KeyError:
                    valid = False

                if valid:

                    obj.a = maps["AUTHOR"]
                    obj.t = maps["TITLE"]
                    obj.y = maps["PUBDATE"]

                    for subdir, dirs, files in os.walk("{}/{}/Pages/".format(in_dir, vol)):
                        for text_f in files:
                            if text_f != "whole-page-ok.lst" and text_f[0] != ".":
                                with open("{}/{}/Pages/{}".format(in_dir, vol, text_f), 'r') as txt_in:
                                    for line in txt_in:
                                        add_content(line, obj, 'swedish')

                    with open(out_dir + vol[:-4] + '.json', 'w', encoding='utf-8') as out:
                        out.write(build_json(obj))
                        out.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input directory", action="store")
    parser.add_argument("-o", help="output directory", action="store")

    try:
        args = parser.parse_args()
    except IOError:
        fail("IOError")

    build_out(args.o)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    mappings = parse_csv(csv_path(dir_path))

    parse_txt(args.i, mappings, args.o)