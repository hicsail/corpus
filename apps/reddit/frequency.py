from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    f = c.frequency(
        'f1',
        [200500, 200600, 200700],
        ['terrorist'],
        'Filtered'
    )

    f.frequency_from_file(sys.argv[2])

    e = f.take_freq()

    e.display()

    e.write_to_json('/Users/ben/Desktop/graph_data')