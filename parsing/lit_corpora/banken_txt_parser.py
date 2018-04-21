import csv
import argparse
import tqdm

from parsing.utils import *
from parsing.parsed import Parsed


def csv_path(path_str):
    """
    Return path to Banken CSV file.
    """

    base_dir = '/'.join(path_str.split('/')[:-1])

    return "{}/data/csv/LB/lit_banken.csv".format(base_dir)


def parse_url(base_url):
    """
    Modify URL to reflect download link for volume.
    """

    parts = base_url.split("/")

    return "{0}_{1}".format(parts[4], parts[6])


def parse_csv(csv_in):
    """
    Build volume mappings from input CSV file.
    """

    ids = {}
    with open(csv_in, 'r', encoding='utf-8') as csv_in:
        read_csv = csv.reader(csv_in, delimiter=',')
        for row in read_csv:
            src = row[0]
            id_str = parse_url(src)
            ids[id_str] = {}
            ids[id_str]["PUBDATE"] = row[1]
            ids[id_str]["TITLE"] = row[2]
            ids[id_str]["AUTHOR"] = row[3]

    return ids

def parse_txt(in_dir, ids, out_dir):
    """
    Iterate over directory of Banken text files, parse each volume to a JSON object.
    """

    for subdir, dirs, files in os.walk(in_dir):
        for txt_f in tqdm.tqdm(files):

            if txt_f[0] != ".":
                reading = False
                obj = Parsed()

                with open(in_dir + txt_f, 'r', encoding='utf-8') as txt_in:
                    for line in txt_in:
                        add_content(line, obj, 'german')

                with open(out_dir + txt_f[:-4] + '.json', 'w', encoding='utf-8') as out:
                    out.write(build_json(obj))
                    out.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="output directory", action="store")

    try:
        args = parser.parse_args()
    except IOError:
        fail("IOError")

    build_out(args.o)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    mappings = parse_csv(csv_path(dir_path))


