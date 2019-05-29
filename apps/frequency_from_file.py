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
        ['economy'],
        'Filtered Text'
    )
    e1.write_freq('/Users/ben/Desktop/brit_freq.json')

    c2 = corpus.Corpus(
        'test2',
        sys.argv[1]
    )
    e2 = c2.frequency(
        'f2',
        [1800, 1820, 1840],
        ['education', 'book'],
        'Filtered Text'
    )
    e2.frequency_from_file('/Users/ben/Desktop/brit_freq.json')

    freq1 = e1.take_freq()
    freq2 = e2.take_freq()

    g = graph.GraphFrequency([freq1, freq2], colors=['black', 'orange', 'blue'])\
        .create_plot()\
        .show()

