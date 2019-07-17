# corpus

Calculate and display NLP metrics on large corpora over time. 

### Requirements

Python 3.5+, mostly due to type annotations.

### Purpose

This library provides a simple interface to compute various NLP metrics on large corpora. It was originally
developed in collaboration with Professor Cathie Jo Martin for her research into historical trends in word
use across a large corpus of British and Danish literature. 

### Data Format

The functions in this library assume a particular schema for input data. In particular, a _corpus_ is expected
to be of the form:

```
<root_directory>/
    <volume1.json>
    <volume2.json>
    ...
    ...
    <volumeN.json>
```

And each JSON file is expected to be structured as follows:

```
{
    "0": {
        'Title': <string>,
        'Author': <string>,
        'Year Published': <string>,
        'Text': <list of string tokens>
        }
    "1": {
        'Title': <string>,
        'Author': <string>,
        'Year Published': <string>,
        'Text': <list of string tokens>
        }
    ...
    ...
    "<n>": {
        'Title': <string>,
        'Author': <string>,
        'Year Published': <string>,
        'Text': <list of string tokens>
        }
}

```

Each JSON file is assumed to hold multiple voluems (`0, 1, ... <n>`) so as to save space when dealing
with large corpora of small volumes (reddit comments, tweets, etc.).

### Data

Several parsing scripts are provided at `parsing/` that can be used to build datasets from
several sources. Right now, however, only parsing for the Reddit dataset (at `parsing/reddit`) 
is up to date.


### Basic Usage

Begin by instantiating a **corpus** as follows:

```
    MyCorpus = corpus.Corpus(
        'MyCorpus',
        '<path_to_corpus>'
    )
```

To build a record of word frequencies over the periods 1800-1820 & 1820-1840:
```
    MyFrequency = MyCorpus.frequency(
        'MyFrequency',
        [1800, 1820, 1840],
        ['<word1', '<word2>', ... '<wordN>']
    )
    
    MyFrequency.take_freq()
```

The results can be displayed to terminal, or written to a JSON file for later use: 

```
    MyFrequency.display()
    
    MyFrequency.write_to_json('<output_path1>')
```

When working with a very large corpus, it is useful to amortize the cost of calculating
word frequencies by writing the frequency records to file:

```
    MyFrequency.write_freq('<output_path2>,json')
```

Those records can then be loaded in the future and applied to further queries as follows:

```
    MyCorpus = corpus.Corpus(
        'MyCorpus',
        '<path_to_corpus>'
    )
    
    MyFrequency = MyCorpus.frequency(
        'MyFrequency',
        [1800, 1820, 1840],
        ['<word1', '<word2>', ... '<wordN>']
    )
    
    MyFrequency.frequency_from_file('<path_from_2>.json')
    
    MyFrequency.take_freq()
```


### Graphing Results

Frequency results can be graphed:

```    
    MyGraph = graph.GraphFrequency([MyFrequency]).create_plot()
    
    MyGraph.show()
```

Multiple corpora can also be graphed alongside one another:
```    
    CorpusTwo = corpus.Corpus(
        'CorpTwo',
        '<path_to_corpus_two>'
    )
    
    FreqTwo = CorpusTwo.frequency(
        'freq_two',
        [1800, 1820, 1840],
        ['<new_word1>', '<new_word2>', ... , '<new_wordN>']
    )
    
    FreqTwo.take_freq()
    
    MyGraphTwo = graph.GraphFrequency([MyFrequency, FreqTwo]).create_plot()
    
    MyGraphTwo.show()
```

Output JSON files can also be passed to a graph alongside Frequency objects:

```
    FreqTwo.write_to_json('<output_path>')

    MyGraph = graph.GraphFrequency([FreqOne, '<path_from_1>.json']).create_plot().show()
```

### Other Functions

This library also provides TF-IDF scoring, LDA / LSI Topic Modeling, and Difference in Proportions functions that can
be applied to corpora in ways similar to the above. 

### TF-IDF-Authors

This class is to treat all documents written by the same author as one document and calculate their scores on a list of words chosen.
It then provides clustering methods for exploration and visualization.

#### To Use
```angular2html


```