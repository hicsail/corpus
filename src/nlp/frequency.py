import tqdm
import nltk
import math

from src.results import *


class Frequency:
    """
    Data structure for calculating word frequencies with respect
    to a list of year periods and (optionally) key words. Keywords
    can be either individual words or n-grams for any n, but must
    use a consistent value of n within a particular list.
    """

    def __init__(self, name: str, in_dir: str, text_type: str, year_list: list,
                 keys: [list, None]=None, stop_words: [list, set, str, None] = None):

        self.name = name
        self.in_dir = in_dir
        self.text_type = text_type
        self.year_list = year_list
        if keys is not None:
            self.keys = build_keys(keys)
        else:
            self.keys = None
        if stop_words is not None:
            if isinstance(stop_words, str):
                self.stop_words_from_json(stop_words)
            elif isinstance(stop_words, list):
                self.stop_words = set(stop_words)
            else:
                self.stop_words = stop_words
        else:
            self.stop_words = {}

        self.frequency_record = None
        self.global_freq = None
        self.avg_freq = None
        self.variance = None
        self.num_docs = None

    def stop_words_from_json(self, file_path: str):
        """
        Set stop_words from Json file.
        """

        with open(file_path, 'r', encoding='utf8') as in_file:

            json_data = json.load(in_file)
            self.stop_words = set(json_data['Words'])

    def detect_n(self):
        """
        Detect value of n for n-grams.
        """

        if self.keys is None:
            return 1

        lengths = set()
        for k in self.keys:
            lengths.add(len(k))

        assert(len(lengths) == 1)

        return lengths.pop()

    def _update_frequency_lists(self, frequency_lists, json_data, n: int):
        """
        Update frequency lists with text from a volume.
        """

        year = int(json_data["Date"])

        if self.year_list[0] <= year < self.year_list[-1]:

            text = list(nltk.ngrams(json_data[self.text_type], n))

            for i in range(len(text) - 1, -1, -1):

                if text[i] in self.stop_words:
                    del text[i]

            target = determine_year(year, self.year_list)

            fdist = nltk.FreqDist(text)

            if frequency_lists[target] == 0:
                frequency_lists[target] = {}
                frequency_lists[target]['FDIST'] = fdist
                frequency_lists[target]['NUM_DOCS'] = 1
                frequency_lists[target]['TOTAL_WORDS'] = len(text)
            else:
                frequency_lists[target]['FDIST'] |= fdist
                frequency_lists[target]['NUM_DOCS'] += 1
                frequency_lists[target]['TOTAL_WORDS'] += len(text)

        return self

    def set_frequency_record(self):

        freq_rec = num_dict(self.year_list)

        print("Calculating frequency records.\n")

        if self.keys is None:
            n = 1
        else:
            n = self.detect_n()

        for subdir, dirs, files in os.walk(self.in_dir):
            for json_doc in tqdm.tqdm(files):
                if json_doc[0] != ".":

                    with open(self.in_dir + "/" + json_doc, 'r', encoding='utf8') as in_file:

                        try:

                            json_data = json.load(in_file)
                            for k in list(json_data.keys()):
                                self._update_frequency_lists(freq_rec, json_data[k], n)

                        except json.decoder.JSONDecodeError:

                            print("Error loading file {}".format(json_doc))

        self.frequency_record = freq_rec

    def take_freq(self):
        """
        Reduce leaf entries in frequency dicts to obtain
        average frequencies (as a percentage of total words)
        for each period / keyword pair.
        """

        if self.frequency_record is None:
            self.set_frequency_record()

        num_docs = num_dict(self.year_list)
        freq = self.frequency_record
        results = num_dict(self.year_list, self.keys, 1)

        for year in self.year_list[:-1]:

            if freq[year]['TOTAL_WORDS'] > 0:

                total = 0

                for k in self.keys:

                    total += freq[year]['FDIST'][k]
                    results[year][k] = freq[year]['FDIST'][k] / freq[year]['TOTAL_WORDS']

                    num_docs[year] = freq[year]['NUM_DOCS']

                results[year]['TOTAL'] = total / freq[year]['TOTAL_WORDS']

        return FrequencyResults(results, num_docs, 'Global frequency (%)', self.name)

    def _take_average_freq(self):

        num_docs = num_dict(self.year_list)
        freq = self.frequency_record
        results = num_dict(self.year_list, self.keys, 1)

        for year in self.year_list[:-1]:

            if freq[year]['TOTAL_WORDS'] > 0:

                total = 0

                for k in self.keys:

                    total += freq[year]['FDIST'][k]
                    results[year][k] = freq[year]['FDIST'][k] / freq[year]['NUM_DOCS']

                    num_docs[year] = freq[year]['NUM_DOCS']

                results[year]['TOTAL'] = total / freq[year]['NUM_DOCS']

        return results, num_docs

    def take_average_freq(self):
        """
        Reduce leaf entries in frequency dicts to obtain
        average occurrence per document for each period / keyword pair.
        """

        if self.frequency_record is None:
            self.set_frequency_record()

        results, num_docs = self._take_average_freq()

        return FrequencyResults(results, num_docs, 'Average frequency', self.name)

    @staticmethod
    def _top_n(fdist: nltk.FreqDist, num: int, total_words: dict):
        """
        Helper to top_n. Returns a list of lists, with each
        list representing the top n words for a given period.
        """

        keys = []
        top = fdist.most_common(num)

        for tup in top:
            keys.append((tup[0], round((tup[1] / total_words) * 100, 4)))

        return keys

    def _update_top(self, json_data, num_docs, num_words, fdists, n):
        """
        Update dictionaries storing top words with contents of a volume.
        """

        year = int(json_data["Date"])

        if self.year_list[0] <= year < self.year_list[-1]:

            text = list(nltk.ngrams(json_data[self.text_type], n))
            target = determine_year(year, self.year_list)
            num_docs[target] += 1

            total_words = len(list(text))
            num_words[target] += total_words
            fdist = nltk.FreqDist(text)

            if fdists[target] == 0:
                fdists[target] = fdist
            else:
                fdists[target] |= fdist

    def top_n(self, num: int, n: int=1):
        """
        Construct a dictionary that stores the top
        <num> words per period across a corpus.
        """

        fdists = num_dict(self.year_list)
        num_words = num_dict(self.year_list)
        n_words = list_dict(self.year_list)
        num_docs = num_dict(self.year_list, nested=0)

        print("Calculating top {0} words per period".format(str(num)))

        for subdir, dirs, files in os.walk(self.in_dir):
            for json_doc in tqdm.tqdm(files):
                if json_doc[0] != ".":

                    with open(self.in_dir + "/" + json_doc, 'r', encoding='utf8') as in_file:

                        try:

                            json_data = json.load(in_file)

                            for k in list(json_data.keys()):

                                self._update_top(json_data[k], num_docs, num_words, fdists, n)

                        except json.decoder.JSONDecodeError:

                            print("Error loading file {}".format(json_doc))

        for year in self.year_list[:-1]:

            if len(fdists[year]) >= num:
                n_words[year].extend(self._top_n(fdists[year], num, num_words[year]))
            else:
                n_words[year].extend(self._top_n(fdists[year], len(fdists[year]), num_words[year]))

        return TopResults(n_words, num_docs, self.name)
