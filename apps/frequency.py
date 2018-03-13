from src import corpus, graph
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    e1 = c.frequency(
        'f1',
        [1800, 1820, 1840],
        ['lady'],
        'Filtered Text'
    )

    e2 = c.frequency(
        'f2',
        [1800, 1820, 1840],
        ['miss'],
        'Filtered Text'
    )

    g = graph.GraphFrequency([e1, e2], colors=['black', 'grey']).create_plot().show()
