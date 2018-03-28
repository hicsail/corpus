

class Parsed:
    """
    Main volume object for lit_corpora. Stores text along with title, publication date, and author.
    """
    def __init__(self, title='', author='', pub_info='', years="2000 ",
                 isbn='', doc_type='', chapters='', htid='', url=''):
        self.t = title
        self.a = author
        self.p = pub_info
        self.y = years
        self.i = isbn
        self.d = doc_type
        self.ch = chapters
        self.h = htid
        self.c = []
        self.url = url
        self.cstem = []
        self.tx = []
        self.txstem = []
        self.c_sent = []
        self.tx_sent = []
        self.cstem_sent = []
        self.txstem_sent = []

    def add_content_sent(self, text):
        self.c_sent.append(text)

    def add_filtered_sent(self, text):
        self.tx_sent.append(text)

    def add_stemmed_sent(self, text):
        self.cstem_sent.append(text)

    def add_filtered_stemmed_sent(self, text):
        self.txstem_sent.append(text)

    def add_content(self, text):
        self.c.extend(text)

    def add_filtered(self, text):
        self.tx.extend(text)

    def add_stemmed(self, text):
        self.cstem.extend(text)

    def add_filtered_stemmed(self, text):
        self.txstem.extend(text)

    def add_chapter(self, chapter):
        self.ch += chapter + ", "


class RedditComment:
    """
    Volume object for a Reddit corpus. Stores text along with subreddit ID, author, and MM-YYYY of comment.
    """
    def __init__(
            self,
            sub_id='',
            author='',
            date='',
            score=0,
            upvotes=0,
            controversy=0,
            comment_id=''):

        self.sub_id = sub_id
        self.author = author
        self.date = date
        self.score = score
        self.upvotes = upvotes
        self.controversy = controversy
        self.comment_id = comment_id

        self.text = []
        self.filtered = []
        self.stemmed = []
        self.f_stemmed = []

    def add_content(self, text):
        self.text.extend(text)

    def add_filtered(self, text):
        self.filtered.extend(text)

    def add_stemmed(self, text):
        self.stemmed.extend(text)

    def add_filtered_stemmed(self, text):
        self.f_stemmed.extend(text)

