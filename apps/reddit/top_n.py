from src import corpus
import sys

if __name__ == '__main__':

    c = corpus.Corpus(
        'test',
        sys.argv[1]
    )

    #    def top_n(self, name, year_list, text_type, num_words: int=10, n_gram: int=1):

    e1 = c.top_n(
        'f1',
        [200500, 200600],
        'Filtered',
    )

    e1.display()