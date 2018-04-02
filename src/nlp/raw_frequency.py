import tqdm
import nltk

from src.results import *


class RawFrequency:
    """
    Iterates over a corpus and tracks either binary occurrence of a set of keywords
    or their frequency. Binary occurrence is particularly useful for small volumes
    (i.e. - snippet files outputted by build_sub_corpus() in corpus.py).
    """

    def __init__(self, name: str, in_dir: str, text_type: str,
                 keys: [list], binary: bool=False):

        self.name = name
        self.in_dir = in_dir
        self.text_type = text_type
        self.keys = build_keys(keys)
        self.binary = binary

        self.freq_dict = {}

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

    def _update_freq_dict(self, cur_key, json_data, n):
        """
        Take frequencies from a single volume within a file.
        """

        self.freq_dict[cur_key] = {}
        self.freq_dict[cur_key]['Date'] = int(json_data['Date'])
        self.freq_dict[cur_key]['Frequencies'] = {}

        if self.binary:
            text = set(nltk.ngrams(json_data[self.text_type], n))

            for keyword in self.keys:
                if keyword in text:
                    self.freq_dict[cur_key]['Frequencies'][' '.join(keyword)] = 1
                else:
                    self.freq_dict[cur_key]['Frequencies'][' '.join(keyword)] = 0

        else:
            text = list(nltk.ngrams(json_data[self.text_type], n))
            self.freq_dict[cur_key]['Text Length'] = len(text)

            fdist = nltk.FreqDist(text)

            for keyword in self.keys:
                self.freq_dict[cur_key]['Frequencies'][' '.join(keyword)] = fdist[keyword]

        return self

    def _take_frequencies(self, jsondoc):
        """
        Take frequencies from a collection of volumes within a file.
        """

        n = self.detect_n()

        with open(self.in_dir + '/' + jsondoc, 'r', encoding='utf8') as json_doc:

            try:

                json_data = json.load(json_doc)

                for k in list(json_data.keys()):

                    cur_key = "{0}_{1}".format(jsondoc, k)
                    self._update_freq_dict(cur_key, json_data[k], n)

            except json.decoder.JSONDecodeError:

                print("Error loading file {}".format(jsondoc))

    def take_frequencies(self):
        """
        Build raw frequency tables.
        """

        for subdir, dirs, files in os.walk(self.in_dir):
            for jsondoc in tqdm.tqdm(files):
                if jsondoc[0] != '.':
                    self._take_frequencies(jsondoc)

        return self





