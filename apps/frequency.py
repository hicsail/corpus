from corpus import corpus, graph
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    e1 = c.frequency(
        'f1',
        [1800, 1820, 1830, 1860, 1880, 1900],
        'Filtered Text',
        'Year Published'
    )

    freq1 = e1.take_freq(['state', 'king'], 'f1')
    freq1.write_to_json(sys.argv[2])

    freq2 = e1.take_freq(['education', 'bills'], 'f2')

    g = graph.GraphFrequency([sys.argv[2], freq2], colors=["green"]).create_plot(total_only=True).show()

