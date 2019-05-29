from src import corpus, graph
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    e1 = c.frequency(
        'f1',
        [1800, 1820, 1840],
        'Filtered Text'
    )

    freq1 = e1.take_freq(['state'], 'f1')
    freq1.write_to_json('/Users/ben/Desktop/out.json')

    freq2 = e1.take_freq(['education'], 'f2')

    g = graph.GraphFrequency(['/Users/ben/Desktop/out.json', freq2], colors=['black', 'orange']).create_plot().show()

