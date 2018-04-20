from selenium import webdriver
import csv


def get_urls(csv_file):

    urls = []

    with open(csv_file, 'r', encoding='utf-8') as csv_in:
        read_csv = csv.reader(csv_in, delimiter=',')

        for row in read_csv:
            urls.append(row[0])

    return urls