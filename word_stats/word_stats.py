import re, logging
"""
A simple set of functions that run some basic stats word documents. There are many in built python features that 

do that do similar tasks to these functions (e.g. collections) and external libraries that cover the rest (e.g. NLTK). 

Both are highly recommended, these are just to illustrate potenital implementations if you had to roll out your own solution.

All functions expect prior tokenisation. For some pre-built functions see 'https://github.com/MooseyAnon/word-tokenisation'
"""


# conifgure logging, because we love logs! 

# LOG_FORM output example = INFO 2017-10-26 21:58:20,336 - test message!
LOG_FORM = '%(levelname)s %(asctime)s - %(message)s'

logging.basicConfig(filename = 'word-stats.txt', 
					level = logging.DEBUG, 
					format = LOG_FORM,
					filemode='w') # get rid of this line to persist logs

logger = logging.getLogger()

# uncomment and run to test logger set up
# logger.info('test message!')


# for not this will act as stand alone, however could make use of file_to_word_split
def word_freq(afile):
	"""takes a document and returns a frequency distribution (dict) for each word"""

	f = open(afile).read().lower() 
	logger.debug('word_freq successfully opened and read {0}'.format(afile))

	word_list = [word for word in re.split('\s+', f)]

	freq_dict= {}

	for word in word_list:
		if word not in freq_dict:
			freq_dict[word]= 1
		else:
			freq_dict[word]+= 1

	return freq_dict



def freq_of_one_word(alist, word):
	"""expects a list and a word. returns the word and the number of occurences in the list"""

	# can easily be conerted to a doc that initially gets tokenised
	wrd_count=0
	for index, item in enumerate(alist):
		if item == word:
			wrd_count +=1 

	return word, wrd_count




def bigram(adoc):
	"""given a doc, returns a list of bigrams"""

	f = open(afile).read().lower()
	logger.debug('bigram successfully opened and read {0}'.format(afile))
	index=[w for w in re.split('\s+', f)]
	bigram_lst=[(index[w], index[w+1]) for w in range(0, len(index)-1)]
	return bigram_lst



def bigram_freq(afile):
	"""given a file, returns a frequency dist (dict) of bigrams"""

	local_bigram = bigram(astr)
	freq = {}
	for biram in local_bigram:
		if biram not in freq:
			freq[biram] = 1
		else: 
			freq[biram] += 1 	
	return freq



def n_gram(afile, n):
	"""takes a file and an int and returns a list of the int-grams"""

	f = open(afile).read().lower()
	logger.debug('n_gram successfully opened and read {0}'.format(afile))
	index=[w for w in re.split('\s+', f)]
	n_gram_lst=[]
	for w in range(len(index)-n+1):
		n_gram_lst.append(index[w:w+n])	
	return n_gram_lst


def n_gram_freq(afile, n):
	"""given a file and an int, returns a frequency dist (dict) of n-grams"""

	freq = {}
	local_ngram = n_gram(afile, n)

	for gram in local_ngram:
		if gram not in index:
			freq[gram] = 1 
		else:
			freq[gram] += 1 
	return freq



def stop_word_calculator(afile):
	"""works out the percentage of a document are stop words"""

	f = open(afile).read().lower() # allows us to calculate len of entire text
	logger.debug('stop_word_calculator successfully opened and read {0}'.format(afile))
	f_sw_free = stop_word_free_doc(afile) #find this function at https://github.com/MooseyAnon/word-tokenisation
	return len(f_sw_free)/ len(f)






