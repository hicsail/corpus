from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    f = c.frequency(
        'f1',
        [200500, 200600, 200700, 200800],
        ['terrorist'],
        'Filtered'
    )

    f.frequency_from_file(sys.argv[2])

    f.take_freq().display()

    f.take_average_freq().display()

    f.top_n().display()