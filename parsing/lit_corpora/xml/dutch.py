from multiprocessing import Pool
from bs4 import BeautifulSoup

from parsing.utils import *
from parsing.parsed import Parsed

from pprint import pprint


class DutchParser:

    def __init__(self, input_dir, output_dir="/tmp/DM_parsed/"):

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.repeats = {}
        self.mapping = self.map_files()

    @staticmethod
    def set_csv():
        """
        Load CSV file with publication info mappings.
        """

        ret = []

        path = os.path.dirname(os.path.realpath(__file__))
        split = path.split('/')
        base = split[:-2]
        data_path = "{}/data/csv/DM/dutch.csv".format('/'.join(base))

        print("Loading CSV mapping from {}".format(data_path))

        data = open(data_path, 'r').read()

        for d in data.split('\n'):
            ret.append(d.split(','))

        return ret

    def add_repeat_rec(self, rec, current_mapping):

        doc_id = rec[0].replace('"', '')

        try:
            self.repeats[doc_id].append(rec[1:])
        except KeyError:
            self.repeats[doc_id] = []
            self.repeats[doc_id].append(rec[1:])

            cur_rec = current_mapping[doc_id]
            self.repeats[doc_id].append([cur_rec["author"], cur_rec["title"], cur_rec["pub_date"]])

        return self

    def map_files(self):
        """
        Populate dict with publication info.
        """

        ret = {}

        csv_data = self.set_csv()

        for f in csv_data:
            doc_id = f[0].strip("\"")
            if doc_id in ret:
                self.add_repeat_rec(f, ret)
            else:
                ret[doc_id] = {}

            ret[doc_id]["author"] = f[1]
            ret[doc_id]["title"] = f[2]
            ret[doc_id]["pub_date"] = f[3]

        return ret

    def log_repeats(self):

        if self.mapping is None:
            self.mapping = self.map_files()

        pprint(self.repeats)

    @staticmethod
    def get_text(tree, obj):
        """
        Grab text from an XML volume and add to Parsed object.
        """

        text = tree.find_all('text')

        for t in text:
            add_bs_xml_content(t.get_text(), obj, 'dutch')

    def _parse_files(self, doc, subdir):
        """
        Parse an individual XML volume.
        """

        try:
            f = open("{0}/{1}".format(self.input_dir, doc), 'r')
        except FileNotFoundError:
            f = open("{0}/{1}".format(subdir, doc), 'r')

        tree = BeautifulSoup(f.read(), 'xml')
        obj = Parsed()
        self.get_text(tree, obj)

        pub_info = self.mapping[doc[:-4]]

        obj.a = pub_info["author"]
        obj.t = pub_info["title"]
        obj.y = pub_info["pub_date"]

        with open("{0}/{1}.json".format(self.output_dir, doc[:-4]), 'w', encoding='utf-8') as out:
            out.write(build_json(obj))
            out.close()

        f.close()

    def parse_files(self):
        """
        Loop over a directory and parse all xml files.
        """

        os.makedirs(self.output_dir, exist_ok=True)

        for subdir, dirs, files in os.walk(self.input_dir):
            for xml_doc in files:
                if xml_doc[-3:] == 'xml':
                    if xml_doc[:-4] in self.mapping:
                        self._parse_files(xml_doc, subdir)

    def parse_files_threaded(self):
        """
        Same as above but multi-threaded.
        """

        os.makedirs(self.output_dir, exist_ok=True)
        thread_files = []

        for subdir, dirs, files in os.walk(self.input_dir):
            for xml_doc in files:
                if xml_doc[-3:] == 'xml':
                    if xml_doc[:-9] in self.mapping:
                        thread_files.append((xml_doc, subdir))

        pool = Pool()
        pool.starmap(self._parse_files, thread_files)
        pool.close()
        pool.join()
