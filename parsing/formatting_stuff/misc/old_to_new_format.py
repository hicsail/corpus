import sys
import json
import os
import tqdm

"""
A lot of old corpora isn't in the right format, this just converts 
them to a JSON structure that the library can understand
"""

os.mkdir(sys.argv[2])

for subdir, dirs, files in os.walk(sys.argv[1]):
    for json_doc in tqdm.tqdm(files):
        if json_doc[0] != ".":

            with open(sys.argv[1] + "/" + json_doc, 'r', encoding='utf8') as in_file:

                json_data = json.load(in_file)
                new_format = {"0": json_data}
                out_f = open(sys.argv[2] + "/" + json_doc, 'w', encoding='utf8')
                out_f.write(json.dumps(new_format, indent=4))
