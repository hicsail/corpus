# corpus

Calculate and display NLP metrics on large corpora over time. 

### Purpose

This library provides a simple interface to compute various NLP metrics on large corpora. It was originally
developed in collaboration with Professor Cathie Jo Martin for her research into historical trends in word
use across a large corpus of British and Danish literature. 

### Assumptions

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

### Tutorial

Begin by instantiating a **corpus** as follows:

```
    MyCorpus = corpus.Corpus(
        'MyCorpus',
        <path_to_corpus>
    )
```

To build a record of word frequencies over the periods 1800-1820 & 1820-1840:

```$xslt
    MyFrequency = MyCorpus.frequency(
        'MyFrequency',
        [1800, 1820, 1840],
        ['<word1', '<word2>', ... '<wordN>']
    )
```

Finally, the results can be displayed to terminal or written to file:

```$xslt
    MyFrequency.display()
    MyFrequency.write()
```