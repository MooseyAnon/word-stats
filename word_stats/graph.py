import matplotlib.pyplot as plt


from word_stats import *


"""
some simple visualisations of the word stats. They're not very attractive but are aimed to get you up and running 

as quickly as possible. They each show a good over view of what is happening in the doc.
"""

def term_freq_graph(afile):
	"""takes file and visualises the term freq dist"""

	f = word_freq(afile)
	logger.debug('term_freq_graph successfully opened, read and created a freq dist for {0}'.format(afile))
	plt.title('Term Frequency Graph')
	plt.xlabel('Terms')
	plt.ylabel('Frequency')
	x = range(0,len(f.keys()))
	my_xticks = f.keys()
	plt.xticks(x, my_xticks, rotation=90)
	y = f.values()
	plt.plot(x,y,'ro')
	logger.debug('term_freq_graph successfully created a line graph for {0}'.format(afile))
	plt.show()



def bigram_freq_graph(afile):
	"""takes file and visualises the biram freq dist"""

	f = bigram_freq(afile)
	logger.debug('bigram_freq_graph successfully opened, read and created a freq dist for {0}'.format(afile))
	plt.title('Bigram Frequency Graph')
	plt.xlabel('Bigram')
	plt.ylabel('Frequency')
	x = range(0,len(f.keys()))
	my_xticks = f.keys()
	plt.xticks(x, my_xticks, rotation=90)
	y = f.values()
	plt.plot(x,y)
	logger.debug('bigram_freq_graph successfully created a line graph for {0}'.format(afile))
	plt.show()


def n_gram_freq_graph(afile, n):
	"""takes a file, an int and visualises that int-grams freq dist"""

	f = n_gram_freq(afile, n)
	logger.debug('n_gram_freq_graph successfully opened, read and created a freq dist for {0}'.format(afile))
	plt.title('N-gram Frequency Graph')
	plt.xlabel('N-grams')
	plt.ylabel('Frequency')
	x = range(0,len(f.keys()))
	my_xticks = f.keys()
	plt.xticks(x, my_xticks, rotation=90)
	y = f.values()
	plt.plot(x,y)
	logger.debug('n_gram_freq_graph successfully created a line graph for {0}'.format(afile))
	plt.show()

