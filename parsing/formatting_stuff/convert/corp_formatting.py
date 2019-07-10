import sys
import tqdm

from parsing.utils import *


if __name__ == '__main__':

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    build_out(out_dir)

    for subdir, dirs, files in os.walk(in_dir):
        for json_doc in tqdm.tqdm(files):
            if json_doc[0] != ".":

                with open(in_dir + "/" + json_doc, 'r', encoding='utf8') as in_file:

                    json_data = json.load(in_file)
                    new_json = {"0": json_data}

                    with open(out_dir + "/" + json_doc, 'w', encoding='utf8') as out_file:

                        out_file.write(json.dumps(new_json, indent=4))
