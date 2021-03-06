from selenium import webdriver
import time, argparse, csv, tqdm
from parsing.utils import *


def get_urls(csv_file):

    urls = []

    with open(csv_file, 'r', encoding='utf-8') as csv_in:
        read_csv = csv.reader(csv_in, delimiter=',')

        for row in read_csv:
            if row[0] != 'source':
                urls.append(row[0])

    return urls


def parse_url(base_url):

    split_url = base_url.split("/")
    parsed_url = []

    for elem in split_url:

        if elem != 'show':
            parsed_url.append(elem)
        else:
            parsed_url.append('download_xml')

    return "/".join(parsed_url)


def download_files(driver, urls):

    for url in tqdm.tqdm(urls):
        download_link = parse_url(url.strip())
        driver.get(url)
        link_list = driver.find_elements_by_tag_name("a")

        for link in link_list:
            if link.get_attribute('href') == download_link:
                link.click()
                time.sleep(5)

    driver.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-csv", metavar='in-directory', action="store", help="input directory argument")
    parser.add_argument("-o", help="output text file argument", action="store")

    try:
        args = parser.parse_args()
    except IOError:
        fail("IOError")

    build_out(args.o)
    chrome_opts = webdriver.ChromeOptions()

    prefs = {"download.default_directory": args.o}
    chrome_opts.add_experimental_option("prefs", prefs)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cdriver = '{}/chromedriver'.format(dir_path)

    driver = webdriver.Chrome(cdriver, chrome_options=chrome_opts)

    if args.csv is not None:
        urls = get_urls(args.csv)
        download_files(driver, urls)
    else:
        fail("Please specify csv file path.")


if __name__ == '__main__':
    main()