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

                    tmp_filt = json_data["0"]["Filtered Text"]
                    del json_data["0"]["Filtered Text"]
                    json_data["0"]["Filtered"] = tmp_filt

                    tmp_filt_stemmed = json_data["0"]["Filtered Text Stemmed"]
                    del json_data["0"]["Filtered Text Stemmed"]
                    json_data["0"]["Filtered Stemmed"] = tmp_filt_stemmed

                    tmp_full = json_data["0"]["Full Text"]
                    del json_data["0"]["Full Text"]
                    json_data["0"]["Text"] = tmp_full

                    tmp_stem = json_data["0"]["Full Text Stemmed"]
                    del json_data["0"]["Full Text Stemmed"]
                    json_data["0"]["Stemmed"] = tmp_stem

                    tmp_pub = json_data["0"]["Year Published"]
                    del json_data["0"]["Year Published"]
                    json_data["0"]["Date"] = tmp_pub

                    with open(out_dir + "/" + json_doc, 'w', encoding='utf8') as out_file:
                        out_file.write(json.dumps(json_data, indent=4))