from parsing.lit_corpora.xml_parsers import dutch

parser = dutch.DutchParser('/Users/ben/Desktop/work/DM/')

parser.identify_missing_volumes()