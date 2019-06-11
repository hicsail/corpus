from corpus import corpus
from corpus.diff_prop import DiffProportions
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    # name: str, text_type: str, key_list: list, binary: bool=False
    rf = c.raw_frequency('test', ['miss', 'upon'], binary=True)

    rf2 = c.raw_frequency('test2', ['swift', 'govern'], binary=True)

    dp = DiffProportions('dp', [rf, rf2], [200500, 200600, 200700, 200800]).take_difference().display()
