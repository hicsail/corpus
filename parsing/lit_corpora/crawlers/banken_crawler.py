import csv
import argparse
import time

from selenium import webdriver

from parsing.utils import *


def get_urls(csv_file):
    """
    Read URL list from input CSV file.
    """

    urls = []

    with open(csv_file, 'r', encoding='utf-8') as csv_in:
        read_csv = csv.reader(csv_in, delimiter=',')

        for row in read_csv:
            urls.append(row[0])

    return urls


def csv_path(path_str):
    """
    Return path to Banken CSV file.
    """

    base_dir = '/'.join(path_str.split('/')[:-2])

    return "{}/data/csv/LB/lit_banken.csv".format(base_dir)


def parse_url(base_url):
    """
    Modify URL to reflect download link for volume.
    """

    parts = base_url.split("/")

    return "{0}//{1}/txt/epub/{2}_{3}.epub".format(parts[0], parts[2], parts[4], parts[6])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="output directory", action="store")

    try:
        args = parser.parse_args()
    except IOError:
        fail("IOError")

    build_out(args.o)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cdriver = '{}/chromedriver'.format(dir_path)

    chrome_opts = webdriver.ChromeOptions()
    prefs = {"download.default_directory": args.o}
    chrome_opts.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(cdriver, chrome_options=chrome_opts)

    path_to_csv = csv_path(dir_path)
    url_list = get_urls(path_to_csv)

    download_urls = []

    for url in url_list:
        download_urls.append(parse_url(url))

    for url in download_urls:
        driver.get(url)
        time.sleep(5)

