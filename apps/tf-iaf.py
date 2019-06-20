import json, tqdm, sys
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from nltk.corpus import stopwords

from corpus.results import *


# read files
print("reformatting files.\n")
in_dir = sys.arg[1]
stop_words = set(stopwords.words("en"))
for subdir, dirs, files in os.walk(in_dir):
    for jsondoc in tqdm.tqdm(files):
        if jsondoc[0] != ".":
            with open(in_dir + "/" + jsondoc, 'r', encoding='utf8') as in_file:

                try:
                    json_data = json.load(in_file)
                    for k in json_data.keys():
                        author_raw = (json_data[k]["Author"]).lower()
                        target = re.sub('\W+', '_', author_raw)
                        text = json_data[k]["Filtered Text"]
                        for i in range(len(text) - 1, -1, -1):
                            if text[i] in stop_words:
                                del text[i]


                except json.decoder.JSONDecodeError:
                    print("Error loading file {}".format(jsondoc))


