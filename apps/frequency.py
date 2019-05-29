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
        ['state'],
        'Filtered Text'
    )

    freq1 = e1.take_freq()
    freq1.write_to_json('/Users/ben/Desktop/out.json')

    e2 = c.frequency(
        'f2',
        [1800, 1820, 1840],
        ['education'],
        'Filtered Text'
    )

    freq2 = e2.take_freq()

    g = graph.GraphFrequency(['/Users/ben/Desktop/out.json', freq2], colors=['black', 'orange']).create_plot().show()

