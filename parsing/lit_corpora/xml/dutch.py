import xml.etree.ElementTree as ET

from parsing.utils import *
from parsing.parsed import Parsed

# TODO: ElementTree doesn't work with Dutch corpus, switch to BeautifulSoup


class DutchParser:

    def __init__(self, input_dir, output_dir="/tmp"):

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.mapping = self.map_files()

    @staticmethod
    def set_csv():

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

    def map_files(self):

        ret = {}

        csv_data = self.set_csv()

        for f in csv_data:
            ret[f[0].strip("\"")] = f[3]

        return ret

    def get_text(self, root, obj):

        for child in root:

            if "text" in child.tag:

                print("found some shit")

            else:

                self.get_text(child, obj)

    def _parse_files(self, doc, subdir):
        """
        doc = xml_doc[:-9] # to get mapping
        need to check if this doc exists in csv map

        xml seems to start volume body with '<text>'
        """
        try:
            tree = ET.parse("{0}/{1}".format(self.input_dir, doc))
        except FileNotFoundError:
            tree = ET.parse("{0}/{1}".format(subdir, doc))
        root = tree.getroot()
        obj = Parsed()
        self.get_text(root, obj)

        return

    def parse_files(self):

        for subdir, dirs, files in os.walk(self.input_dir):
            for xml_doc in files:
                if xml_doc[-3:] == 'xml':
                    self._parse_files(xml_doc, subdir)


