# corpus

Calculate and display NLP metrics on large corpora over time. 

### Purpose

This library provides a simple interface to compute various NLP metrics on large corpora. It was originally
developed in collaboration with Professor Cathie Jo Martin for her research into historical trends in word
use across a large corpus of British and Danish literature. 

### Data Format

The functions in this library assume a particular schema for input data. In particular, a _corpus_ is expected
to be of the form:

```$xslt
<root_directory>/
    <volume1.json>
    <volume2.json>
    ...
    ...
    <volumeN.json>
```

And each JSON file is expected to be structured as follows:

```$xslt
'Title': <string>,
'Author': <string>,
'Year Published': <string>,
'Full Text': <list of string tokens>
```

### Data

Several parsing scripts are provided at `parsing/scripts` that can be used to build datasets from
several sources. 

TODO: Explain the different data sources, provide URLs

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
```

Finally, the results can be displayed to terminal, or written to a JSON file for later use: 

```
    MyFrequency.display()
    
    MyFrequency.write_to_json('<output_path>')
```


### Graphing Results

One or more corpora can be graphed alongside one another as follows:

```
    CorpusOne = corpus.Corpus(
        'CorpOne',
        '<path_to_corpus_one>'
    )
    
    FreqOne = CorpusOne.frequency(
        'freq_one',
        [1800, 1820, 1840],
        ['<word1>', '<word2>', ... , '<wordN>']
    )
    
    CorpusTwo = corpus.Corpus(
        'CorpTwo',
        '<path_to_corpus_two>'
    )
    
    FreqTwo = CorpusTwo.frequency(
        'freq_two',
        [1800, 1820, 1840],
        ['<new_word1>', '<new_word2>', ... , '<new_wordN>']
    )
    
    MyGraph = graph.GraphFrequency([FreqOne, FreqTwo]).create_plot()
    
    MyGraph.show()
```

Output JSON files can also be passed to a graph alongside Frequency objects:

```
    FreqTwo.write_to_json('<output_path>')

    MyGraph = graph.GraphFrequency([FreqOne, '<output_path>']).create_plot().show()
```

### Other Functions

This library also provides TF-IDF scoring, LDA / LSI Topic Modeling, and Difference in Proportions functions that can
be applied to corpora in ways similar to the above (documentation coming). 