import json
import re
import os
import shutil

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from parsing.parsed import Parsed, RedditComment


def fail(msg: str):
    """
    Print error and exit program.
    """

    print(msg)
    os._exit(1)


def build_out(out_dir: str):
    """
    Build output directory, overwrite if it exists.
    """

    if out_dir is not None:
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        else:
            shutil.rmtree(out_dir)
            os.mkdir(out_dir)
    else:
        fail("Please specify output directory.")


def build_json(file: Parsed):
    """
    Construct JSON object which represents a volume in a corpus.
    """

    if file.t is None:
        file.t = "No title listed"
    if file.a is None:
        file.a = "No author listed"
    if file.p is None:
        file.p = "No publisher listed"
    if file.i == '':
        file.i = "No ISBN listed"
    if file.d is None:
        file.d = "No document type"
    if file.h is None:
        file.h = "No HTID for this file"

    file.t = file.t.replace("\n", " ")
    file.a = file.a.replace("\n", " ")
    file.p = file.p.replace("\n", " ")
    file.d = file.d.replace("\n", " ")
    file.ch = filter_chapters(file.ch)

    jfile = json.dumps({'Title': file.t, 'Author': file.a, 'Publisher': file.p, 'Date': file.y,
                        'ISBN': file.i, 'Document Type': file.d, 'List of chapters': file.ch, 'HTID': file.h,
                        'Text': file.c, 'Stemmed': file.cstem, 'Filtered': file.tx,
                        'Filtered Stemmed': file.txstem, 'Full Sentences': file.c_sent,
                        'Filtered Sentences': file.tx_sent, 'Stemmed Sentences': file.cstem_sent,
                        'Filtered Stemmed Sentences': file.txstem_sent, 'URL': file.url},
                       sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    return jfile


def build_reddit_json(file: RedditComment):

    entry = \
        {
            'Author': file.author,
            'Date': file.date,
            'Sub ID': file.sub_id,
            'Subreddit':file.subreddit,
            'Score': file.score,
            'Upvotes': file.upvotes,
            'Controversy': file.controversy,
            'Text': file.text,
            'Filtered': file.filtered,
            'Stemmed': file.stemmed,
            'Filtered Stemmed': file.f_stemmed,
            'ID': file.comment_id
        }

    return entry


def filter_chapters(chapters: str):
    """
    Delete 'None' and empty chapter entries.
    """

    ch = chapters.split(",")

    for i in range(len(ch) - 1, -1, -1):
        if ch[i].strip() == "" or ch[i] is None:
            del ch[i]
    ch_string = ", ".join(ch)

    return ch_string


def add_content(text: str, file: Parsed, language: str):
    """
    Transforms text into raw/filtered/stemmed forms and adds it to a file object.
    """

    sentences = re.split('(?<=[.!?]) +', text)

    for sentence in sentences:
        sentence = clean_text(sentence)

        if len(sentence) > 1:
            file.add_content_sent(" ".join(sentence))
            sentence_stemmed = stem_text(sentence, language)
            file.add_stemmed_sent(" ".join(sentence_stemmed))
            sentence_filtered = filter_text(sentence, language)

            if len(sentence_filtered) > 1:
                file.add_filtered_sent(" ".join(sentence_filtered))
                sentence_filtered_stemmed = stem_text(sentence_filtered, language)
                file.add_filtered_stemmed_sent(" ".join(sentence_filtered_stemmed))

    text_list = clean_text(text)

    # full text
    file.add_content(text_list)

    # stem the full text
    stemmed = stem_text(text_list, language)
    file.add_stemmed(stemmed)

    # filter the unstemmed full text
    filtered = filter_text(text_list, language)
    file.add_filtered(filtered)

    # stem the filtered text
    filtered_stemmed = stem_text(filtered, language)
    file.add_filtered_stemmed(filtered_stemmed)


def add_reddit_content(text: str, file: RedditComment):
    """
    Add content to Reddit volume.
    """

    text_list = clean_text(text)

    # full text
    file.add_content(text_list)

    # stem the full text
    stemmed = stem_text(text_list, "english")
    file.add_stemmed(stemmed)

    # filter the unstemmed full text
    filtered = filter_text(text_list, "english")
    file.add_filtered(filtered)

    # stem the filtered text
    filtered_stemmed = stem_text(filtered, "english")
    file.add_filtered_stemmed(filtered_stemmed)


def add_xml_content(root, file: Parsed, language: str):
    """
    Transforms text from xml file into raw/filtered/stemmed forms and adds it to a file object.
    """

    text = ''
    if str(root.text) != 'None':
        text += root.text

    if str(root.tail) != 'None':
        text += ' ' + root.tail

    if text != '':
        sentences = re.split('(?<=[.!?]) +', text)

        for sentence in sentences:
            sentence = clean_text(sentence)

            if len(sentence) > 1:
                file.add_content_sent(" ".join(sentence))
                sentence_stemmed = stem_text(sentence, language)
                file.add_stemmed_sent(" ".join(sentence_stemmed))
                sentence_filtered = filter_text(sentence, language)

                if len(sentence_filtered) > 1:
                    file.add_filtered_sent(" ".join(sentence_filtered))
                    sentence_filtered_stemmed = stem_text(sentence_filtered, language)
                    file.add_filtered_stemmed_sent(" ".join(sentence_filtered_stemmed))

        text_list = clean_text(text)

        # full text
        file.add_content(text_list)

        # stem the full text
        stemmed = stem_text(text_list, language)
        file.add_stemmed(stemmed)

        # filter the unstemmed full text
        filtered = filter_text(text_list, language)
        file.add_filtered(filtered)

        # stem the filtered text
        filtered_stemmed = stem_text(filtered, language)
        file.add_filtered_stemmed(filtered_stemmed)


def add_bs_xml_content(text: str, f: Parsed, lang: str):
    """
    Add content to Parsed object from BeautifulSoup XML parser output.
    """

    sentences = re.split("[.!?]", text)

    for sentence in sentences:

        s = clean_text(sentence)

        if len(s) > 1:

            f.add_content_sent(" ".join(s))
            s_stem = stem_text(s, lang)
            f.add_stemmed_sent(" ".join(s_stem))
            s_filt = filter_text(s, lang)

            if len(s_filt) > 1:

                f.add_filtered_sent(" ".join(s_filt))
                s_filt_stem = stem_text(s_filt, lang)
                f.add_filtered_stemmed_sent(" ".join(s_filt_stem))

    text_list = clean_text(text)
    f.add_content(text_list)

    stem = stem_text(text_list, lang)
    f.add_stemmed(stem)

    filt = filter_text(text_list, lang)
    f.add_filtered(filt)

    filt_stem = stem_text(filt, lang)
    f.add_filtered_stemmed(filt_stem)


def clean_text(text: str):
    """
    Convert all letters to lowercase, remove non-alphabetic characters, remove empty strings
    """

    # strip each word of non-alphabetic characters
    text_list = re.split('\W[0-9]*', text)

    for i in range(len(text_list) - 1, -1, -1):

        # delete empty strings
        if text_list[i] == "" or text_list[i] == "None":
            del text_list[i]
        else:
            text_list[i] = text_list[i].lower()

    return text_list


def filter_text(text: list, language: str):
    """
    Remove stop words from text
    """

    filtered_words = set(stopwords.words(language))

    for i in range(len(text) - 1, -1, -1):

        if text[i] in filtered_words:
            del text[i]

    return text


def stem_text(text: list, language: str):
    """
    Stem words in a list of text.
    """

    stemmer = SnowballStemmer(language)
    stemmed = []

    for word in text:
        stemmed.append(stemmer.stem(word))

    return stemmed
