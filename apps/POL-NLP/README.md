***
###check_stem.py

purpose:

	check how certain words stem 

arguments:

	-w : list of words to stem 
	-l : language

usage:

	python3 check_stem.py -w "runs,walks,crawls" -l "english"

output:

	list of stemmed words

	ex.

	["run", "walk", "crawl"]


***
###debug_corpus.py

purpose:

	check which fields exist in the files for a given corpus. sometimes i forget what the text fields are called and the files are too large to inspect manually so this is handy sometimes.

arguments:

	-i : path to corpus directory

usage:

	python3 debug_corpus.py -i "/Users/ben/Desktop/corpus/"

output:

	list of field keys

	ex.

	Date
	Filtered
	Stemmed Sentences
	Author
	Filtered Stemmed Sentences
	Document Type
	List of chapters
	Publisher
	Text
	Stemmed
	ISBN
	Full Sentences
	Title
	Filtered Stemmed


***
###frequency.py

purpose:

	take word frequencies over a corpus for some set of words and write output to a file

arguments:

	-i : path to corpus directory
	-o : output json file path
	-k : list of keywords, separate each keyword by a comma
	-t : text field to analyze (defaults to text)
		- note : if you're running this script on an entire corpus, other text fields you might be interested in are the following -- 
			Filtered, Stemmed, Filtered Stemmed
	-y : list of year periods
	-n : name of this frequency record (will be displayed when graphed)

usage:

	python3 frequency.py -i "/Users/ben/Desktop/corpus/" -o "/Users/ben/Desktop/out.json" -k "cat,mat,hat" -t "Filtered Stemmed" -y "1800,1830,1870" -n "my favorite words"

output:

	writes JSON file output that stores frequencies of all words passed


***
###graph.py

purpose:

	graph word frequencies

arguments:

	-i : input directory. the script will graph the data associated with all files in this directory
	-t : display total frequencies (instead of those from individual words)
	-tite : graph title
	-bar_width : width of graph bars, default is 5

usage:

	python3 graph.py -i "/Users/ben/Desktop/frequency_files/" -t -title "My Favorite Words" -bar_width "4"

output:

	a graph


***
###sub_corpus.py

purpose:

	build a directory of "snippet" files based on input keywords

arguments:

	-i : path to input corpus directory
	-o : path to output corpus directory
	-k : list of keywords, separate each keyword by a comma
	-l : number of words to extract per snippet
	-t : text field to analyze (defaults to text)
		- note : if you're running this script on an entire corpus, other text fields you might be interested in are the following -- 
			Filtered, Stemmed, Filtered Stemmed

usage:

	python3 sub_corpus.py -i "/Users/ben/Desktop/corpus/" -o "/Users/ben/Desktop/sub_corpus/" -k "cat,mat,hat" -l "30" -t "Filtered Stemmed"


***
###topic_model.py

purpose:

	create LDA topic models over a corpus of text

arguments:

	-i : path to input corpus directory
	-o : output text file path
	-t : text field to analyze
	-y : list of year periods
	-l : language (defaults to english)
	-num_topics : number of topics for the algorithm to look for (default is 10)
	-passes : number of passes the algorithm makes. more passes takes more time, but yields better results (roughly)
	-stop : path to stopwords file. useful if you want the algorithm to ignore certain words when building topics

usage:

	python3 topic_model.py -i "/Users/ben/Desktop/corpus/" -o "/Users/ben/Desktop/out.txt" -t "Filtered" -y "1800,1830,1880,1900" -l "danish" -num_topics "20" -passes "10" -stop "/Users/ben/Desktop/danish_stopwords.json"















