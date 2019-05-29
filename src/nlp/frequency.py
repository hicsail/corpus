import tqdm
import nltk

from src.results import *


class Frequency:
    """
    Data structure for calculating word frequencies with respect
    to a list of year periods and (optionally) key words. Keywords
    can be either individual words or n-grams for any n, but must
    use a consistent value of n within a particular list.
    """

    def __init__(self, name: str, in_dir: str, text_type: str,
                 year_list: list, stop_words: [list, set, str, None] = None):

        self.name = name
        self.in_dir = in_dir
        self.text_type = text_type
        self.year_list = year_list
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

    def stop_words_from_json(self, file_path: str):
        """
        Set stop_words from Json file.
        """

        with open(file_path, 'r', encoding='utf8') as in_file:

            json_data = json.load(in_file)
            self.stop_words = set(json_data['Words'])

    def frequency_from_file(self, file_path: str):
        """
        Load a precomputed frequency distribution record from a json file.
        """

        with open(file_path, 'r', encoding='utf8') as in_file:

            json_data = json.load(in_file)

            freq_dict = {}

            for year in json_data.keys():

                freq_dict[int(year)] = {}
                freq_dict[int(year)]['NUM_DOCS'] = json_data[year]['NUM_DOCS']
                freq_dict[int(year)]['TOTAL_WORDS'] = json_data[year]['TOTAL_WORDS']
                freq_dict[int(year)]['FDIST'] = json_data[year]['FDIST']

            self.frequency_record = freq_dict

        return self

    def write_freq(self, out_path: str):
        """
        Write this object's frequency records to file for later use.
        """

        if self.frequency_record is None:
            self.set_frequency_record()

        j_file = json.dumps(
            self.frequency_record,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
            ensure_ascii=False
        )

        with open(out_path, 'w', encoding='utf8') as out_file:
            out_file.write(j_file)

    def _clean_records(self, freq_rec):
        """
        Convert keys in frequency record from tuples to strings.
        """

        freq_dict = {}

        for year in self.year_list[:-1]:

            freq_dict[year] = {}
            freq_dict[year]['NUM_DOCS'] = freq_rec[year]['NUM_DOCS']
            freq_dict[year]['TOTAL_WORDS'] = freq_rec[year]['TOTAL_WORDS']
            freq_dict[year]['FDIST'] = {}

            for k in freq_rec[year]['FDIST'].keys():
                freq_dict[year]['FDIST'][' '.join(k)] = freq_rec[year]['FDIST'][k]

        return freq_dict

    def detect_n(self, keys):
        """
        Detect value of n for n-grams.
        """

        if keys is None:
            return 1

        lengths = set()
        for k in keys:
            lengths.add(len(k.split()))

        assert(len(lengths) == 1)

        return lengths.pop()

    def _update_frequency_lists(self, frequency_lists: dict, json_data, n: int):
        """
        Update frequency lists with text from a volume.
        """

        try:
            year = int(json_data["Date"])
        except KeyError:
            year = int(json_data["Year Published"])

        if self.year_list[0] <= year < self.year_list[-1]:

            text = list(nltk.ngrams(json_data[self.text_type], n))

            for i in range(len(text) - 1, -1, -1):
                if text[i] in self.stop_words:
                    del text[i]

            target = determine_year(year, self.year_list)
            fdist = nltk.FreqDist(text)

            if frequency_lists[target] == 0:

                frequency_lists[target] = {}
                for kw in fdist:
                    frequency_lists[target]['FDIST'] = {}
                    frequency_lists[target]['FDIST'][kw] = fdist[kw]
                frequency_lists[target]['NUM_DOCS'] = 1
                frequency_lists[target]['TOTAL_WORDS'] = len(text)

            else:

                for kw in fdist:
                    try:
                        frequency_lists[target]['FDIST'][kw] += fdist[kw]
                    except KeyError:
                        frequency_lists[target]['FDIST'][kw] = fdist[kw]
                frequency_lists[target]['NUM_DOCS'] += 1
                frequency_lists[target]['TOTAL_WORDS'] += len(text)

        return self

    def set_frequency_record(self, keys):
        """
        Calculate frequency distributions per period.
        """

        frequency_lists = num_dict(self.year_list)

        print("Calculating frequency records.\n")

        n = self.detect_n(keys)

        for subdir, dirs, files in os.walk(self.in_dir):
            for json_doc in tqdm.tqdm(files):
                if json_doc[0] != ".":

                    with open(self.in_dir + "/" + json_doc, 'r', encoding='utf8') as in_file:

                        try:

                            json_data = json.load(in_file)
                            for k in list(json_data.keys()):

                                self._update_frequency_lists(frequency_lists, json_data[k], n)

                        except json.decoder.JSONDecodeError:

                            print("Error loading file {}".format(json_doc))

        self.frequency_record = self._clean_records(frequency_lists)

    def take_freq(self, keys, name):
        """
        Calculate keyword frequencies for each period from frequency records
        """

        if self.frequency_record is None:
            self.set_frequency_record(keys)

        num_docs = num_dict(self.year_list)
        freq = self.frequency_record
        results = num_dict(self.year_list, keys, 1)

        for year in self.year_list[:-1]:

            if freq[year]['TOTAL_WORDS'] > 0:

                total = 0
                for k in keys:
                    try:
                        total += freq[year]['FDIST'][k]
                        results[year][k] = freq[year]['FDIST'][k] / freq[year]['TOTAL_WORDS']
                    except KeyError:
                        pass

                num_docs[year] = freq[year]['NUM_DOCS']
                results[year]['TOTAL'] = total / freq[year]['TOTAL_WORDS']

        return FrequencyResults(results, num_docs, 'Global frequency (%)', name)

    def _take_average_freq(self, keys):
        """
        Calculate average keyword frequency per document from frequency records.
        """

        num_docs = num_dict(self.year_list)
        freq = self.frequency_record
        results = num_dict(self.year_list, keys, 1)

        for year in self.year_list[:-1]:

            if freq[year]['TOTAL_WORDS'] > 0:

                total = 0

                for k in keys:

                    total += freq[year]['FDIST'][k]
                    results[year][k] = freq[year]['FDIST'][k] / freq[year]['NUM_DOCS']
                    num_docs[year] = freq[year]['NUM_DOCS']

                results[year]['TOTAL'] = total / freq[year]['NUM_DOCS']

        return results, num_docs

    def take_average_freq(self, keys):
        """
        Calculate average keyword frequency per document from frequency records.
        """

        if self.frequency_record is None:
            self.set_frequency_record(keys)

        results, num_docs = self._take_average_freq(keys)

        return FrequencyResults(results, num_docs, 'Average frequency', self.name)

    @staticmethod
    def _top_n(fdist, num: int, total_words: int):
        """
        Helper to top_n. Returns a list of lists, with each
        list representing the top n words for a given period.
        """

        keys = []

        s = [(k, fdist[k]) for k in sorted(fdist, key=fdist.get, reverse=True)]
        top = s[:num]

        for tup in top:
            keys.append((tup[0], round((tup[1] / total_words) * 100, 4)))

        return keys

    def top_n(self, num: int = 10):
        """
        Construct a dictionary that stores the top
        <num> words per period across a corpus.
        """

        if self.frequency_record is None:
            self.set_frequency_record()

        num_docs = num_dict(self.year_list)
        n_words = list_dict(self.year_list)
        freq = self.frequency_record

        print("Calculating top {0} words per period".format(str(num)))

        for year in self.year_list[:-1]:

            num_docs[year] = freq[year]['NUM_DOCS']

            if freq[year]['NUM_DOCS'] > num:
                n_words[year].extend(
                    self._top_n(freq[year]['FDIST'], num, freq[year]['TOTAL_WORDS'])
                )
            else:
                n_words[year].extend(
                    self._top_n(freq[year]['FDIST'], freq[year]['NUM_DOCS'], freq[year]['TOTAL_WORDS'])
                )

        return TopResults(n_words, num_docs, self.name)
