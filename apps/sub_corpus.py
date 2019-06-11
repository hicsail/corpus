from corpus import corpus, graph
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1],
    )

    s = c.build_sub_corpus(
        'sub',
        sys.argv[2],
        ['economy', 'education'],
        'Filtered Text',
        30,
        [1800, 1900]
    )

    freq = s.frequency('f', [1800, 1820, 1840], ['book'], 'Text').take_freq()

    g = graph.GraphFrequency([freq], colors=['orange']).create_plot().show()
