from parsing.misc import xcel_to_csv

import sys

converter = xcel_to_csv.XcelToCsv(sys.argv[1])
converter.convert_and_write()