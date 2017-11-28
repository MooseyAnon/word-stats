import re, logging, csv, os, sys 
import matplotlib.pyplot as plt
import cPickle as pickle

# conifgure logging, because we love logs! 

# LOG_FORM output example = INFO 2017-10-26 21:58:20,336 - test message!
LOG_FORM = '%(levelname)s %(asctime)s - %(message)s'

logging.basicConfig(filename = 'classdotpy-logs.txt', 
					level = logging.DEBUG, 
					format = LOG_FORM,
					filemode='w') # get rid of this line to persist logs

logger = logging.getLogger()

# uncomment and run to test logger set up
# logger.info('test message!')


class OpenInput:
	def __init__(self, someinput=None):
		self.output = None
		if someinput:
			print self.open_file(someinput)

	def _open_standard(self, someinput):

		try:
			with open(someinput, 'r') as af:
				self.output = af.read() 
				return self.output
		except IOError:
			logger.debug('open_standard could not open this {0}'.format(someinput))


	def _open_csv(self, someinput):
		try:
			with open(someinput, 'r') as af:
				self.output = af.read() 
				return self.output
		except IOError:
			logger.debug('open_csv could not open this {0}'.format(someinput))

	def _check_file_type(self, someinput):
		"""check file type (using the file format) and open using right function"""

		pdf = re.compile('[A-Za-z0-9]+\.pdf$')
		csv = re.compile('[A-Za-z0-9]+\.csv$')
		txt = re.compile('[A-Za-z0-9]+\.txt$')
		pkl = re.compile('[A-Za-z0-9]+\.pkl$') # for pickled models

		if bool(pdf.search(someinput)) == True:
			# opened_pdf=open_pdf(afile) # needs to be done after finding the right 3rd party libraries
			pass
			# opened_pdf

		elif bool(csv.search(someinput)) == True:
			opened_csv = self._open_csv(someinput) 
			logger.debug('check_file_type opened a csv file named {0}'.format(someinput))
			return opened_csv
		
		elif bool(txt.search(someinput)) == True:
			opened_reg_file = self._open_standard(someinput)
			logger.debug('check_file_type opened a txt file named {0}'.format(someinput))
			return opened_reg_file  

		elif bool(pkl.search(someinput)) == True:
			unpickled_file = self._open_standard(someinput)
			logger.debug('check_file_type unpickled a file named {0}'.format(someinput))
			return unpickled_file

		else:
			f = someinput
			logger.debug('check_file_type cannot open this file format. But it has returned {0}'.format(type(someinput)))
			return f


	def open_file(self, someinput):
		"""simple open file function to act as interface to more thorough file checking functions.
			Returns a checked and read file"""

		f = self._check_file_type(someinput)
		logger.debug('open_file successfully opened {0}'.format(someinput))
		return f

# t = OpenInput('smalltext.txt')




class TextTokeniser(OpenInput):
	"""
	class for tokenising both strings and documents. 

	"""

	def __init__(self, someinput=None):
		OpenInput.__init__(self)
		self.output = []
		self.stopwords = []
		if someinput:
			print self.default_tokens(someinput)

	def  default_tokens(self, someinput):

		f = self.open_file(someinput)
		logger.debug('default_tokens successfully opned and read {0} file'.format(someinput))
		self.output=[word for word in re.split('\s+', f)]
		return self.output

	def punct_free_tokens(self, someinput):

		f = self.open_file(someinput)
		logger.debug('punct_free_tokens successfully opned and read {0} file'.format(someinput))
		self.output = [word for word in re.split('\s+', f.translate(None, '_+-.,!@#$%^&*();\/|<>"'))] # replaces given input them with "" wherever found in doc 
		return self.output

	def document_vocab(self, someinput):
			
		f = self.self.punct_free_tokens(someinput)
		logger.debug('document_vocab successfully opned and read {0} file'.format(someinput))
		self.output = set(f)
		return self.output 

	def capital_tokens(self, someinput):

		f = self.open_file(someinput)
		logger.debug('capital_tokens successfully opned and read {0} file'.format(someinput))
		self.output = [word for word in re.findall('[A-Z]\w+', f)]
		return self.output

	def split_newline_chars(self, someinput):
	
		f = self.open_file(someinput)
		logger.debug('split_newline_chars successfully opned and read {0} file'.format(someinput))
		self.output = [line for line in re.split('\n+', f)]
		return self.output



	def remove_stop_words(self, readfile, swf=None):

		if swf:
			try:
				self.stopwords = default_tokens(swf)
			except IOError as err:
				logger.debug('remove_stop_words could not open your stopword file reverting to default. Error Raised: {0}'.format(err))
		else:
			self.stopwords = self.default_tokens('stopwords.txt') # come from list of most common english words

		
		rf = self.open_file(readfile)
		logger.debug('remove_stop_words successfully opned and read {0} file'.format(readfile))

		self.output = [word for word in rf if word not in self.stopwords]
		return  self.output




class CSVTokeniser(OpenInput):
	def __init__(self):
		OpenInput.__init__(self)
		self.output= []

	def csv_lines(self, someinput):

		f = self.open_file(someinput)
		reader = csv.reader(f)
		logger.debug('csv_lines successfully opned and read {0}'.format(someinput))
		self.output = [row for row in reader]
		return self.output 

	def csv_tokens(self, someinput):

		f = self.open_file(someinput)
		reader = csv.reader(f, delimiter=' ')
		logger.debug('csv_tokens successfully opned and read {0}'.format(someinput)) 
		self.output = [word for row in reader for word in row] 
		return self.output


	def punct_free_lines(self, someinput):
		f = self.open_file(someinput)
		self.output = []
		for line in f:
			data = line.translate(None, '_+-.,!@#$%^&*();\/|<>"')
			self.output.append([data])
		return self.output

	def csv_vocab(self, someinput):
		self.output = set(self.csv_tokens(someinput))
		return self.output

	def csv_capitals(self, someinput):
		"""returns capital letter words in each line of file"""
		f = self.open_file(someinput)
		self.output = []
		for line in f:
			data= re.findall('[A-Z]\w+', line)
			self.output.append(data)
		return self.output



class WordStats(TextTokeniser):
	def __init__(self):
		TextTokeniser.__init__(self)
		self.index = {}
		self.list=[]

	def delindex(self):
		return self.index.clear()

	def dellist(self):
		del self.list[:]
		return self.list

	def token_freq(self, someinput):
		self.delindex()
		logger.debug('cleared index before running token_freq')
		t = self.punct_free_tokens(someinput)
		for word in t:
			if word not in self.index:
				self.index[word] = 1
			else:
				self.index[word] += 1 

		return self.index

	def one_token_freq(self, token, readfile):
		otf = self.punct_free_tokens(readfile)
		token_count = 0
		for index, item in enumerate(otf):
			if item == token:
				token_count += 1 

		return token, token_count

	def bigram(self, someinput):
		self.dellist()
		logger.debug('cleared list before running bigram')
		b = self.punct_free_tokens(someinput)
		bigram_lst=[(b[w-1], b[w]) for w in range(0, len(b)-1)]
		bigram_lst.append((b[-2], b[-1])) # get the last bigram of the list
		return bigram_lst

	def bigram_freq(self, someinput):
		self.delindex()
		logger.debug('cleared index before running bigram_freq')
		bfs = self.bigram(someinput)
		for bf in bfs:
			if bf not in self.index:
				self.index[bf] = 1
			else:
				self.index[bf] += 1
		return self.index

	def trigram(self, someinput):
		self.dellist()
		logger.debug('cleared list before running trigram')
		tg = self.punct_free_tokens(someinput)
		self.list=[(tg[t-2], tg[t-1], tg[t]) for t in range(0, len(tg)-3)]
		self.list.append((tg[t-3], tg[t-2], tg[t-1])) # lat 3 items
		return self.list

	def trigram_freq(self, someinput):
		self.delindex()
		logger.debug('cleared index before running trigram_freq')
		tgf = self.trigram(someinput)
		for t in tgf:
			if t not in self.index:
				self.index[t] = 1
			else:
				self.index[t] += 1
		return self.index

	def n_gram(self, someinput, n):
		self.dellist()
		logger.debug('cleared list before running n_gram')
		ng = self.punct_free_tokens(someinput)
		for g in range(len(ng)- n+1):
			self.list.append(tuple(ng[g:g+n]))
		self.list.append(tuple(ng[g-n]))
		return self.list

	def n_gram_freq(self, someinput, n):
		self.delindex()
		logger.debug('cleared index before running n_gram_freq')
		ngf = self.n_gram(someinput, n)
		for ng in ngf:
			if ng not in self.index:
				self.index[ng] = 1
			else:
				self.index[ng] += 1

		return self.index

	def stopword_calculator(self, someinput):
		f = self.default_tokens(someinput)
		swf = self.remove_stop_words(someinput)
		return round(float(len(swf))/float(len(f)), 5)



class WordGraph(WordStats):
	def __init__(self):
		WordStats.__init__(self)

	def token_freq_graph(self, someinput):
		f = self.token_freq(someinput)
		logger.debug('token_freq_graph successfully opened, read and created a freq dist for {0}'.format(someinput))
		plt.title('Term Frequency Graph')
		plt.xlabel('Terms')
		plt.ylabel('Frequency')
		x = range(0,len(f.keys()))
		my_xticks = f.keys()
		plt.xticks(x, my_xticks, rotation=90)
		y = f.values()
		plt.plot(x,y,'ro')
		logger.debug('token_freq_vizgraph successfully created a line graph for {0}'.format(someinput))
		plt.show()

	def bigram_freq_graph(self, someinput):
		"""takes file and visualises the biram freq dist"""

		f = self.bigram_freq(someinput)
		logger.debug('bigram_freq_graph successfully opened, read and created a freq dist for {0}'.format(someinput))
		plt.title('Bigram Frequency Graph')
		plt.xlabel('Bigram')
		plt.ylabel('Frequency')
		x = range(0,len(f.keys()))
		my_xticks = f.keys()
		plt.xticks(x, my_xticks, rotation=90)
		y = f.values()
		plt.plot(x,y)
		logger.debug('bigram_freq_graph successfully created a line graph for {0}'.format(someinput))
		plt.show()


	def trigram_freq_graph(self, someinput):
		"""takes file and visualises the triram freq dist"""

		f = self.trigram_freq(someinput)
		logger.debug('trigram_freq_graph successfully opened, read and created a freq dist for {0}'.format(someinput))
		plt.title('Bigram Frequency Graph')
		plt.xlabel('Bigram')
		plt.ylabel('Frequency')
		x = range(0,len(f.keys()))
		my_xticks = f.keys()
		plt.xticks(x, my_xticks, rotation=90)
		y = f.values()
		plt.plot(x,y)
		logger.debug('bigram_freq_graph successfully created a line graph for {0}'.format(someinput))
		plt.show()


	def n_gram_freq_graph(someinput, n):
		"""takes a file, an int and visualises that int-grams freq dist"""

		f = self.n_gram_freq(someinput, n)
		logger.debug('n_gram_freq_graph successfully opened, read and created a freq dist for {0}'.format(someinput))
		plt.title('N-gram Frequency Graph')
		plt.xlabel('N-grams')
		plt.ylabel('Frequency')
		x = range(0,len(f.keys()))
		my_xticks = f.keys()
		plt.xticks(x, my_xticks, rotation=90)
		y = f.values()
		plt.plot(x,y)
		logger.debug('n_gram_freq_graph successfully created a line graph for {0}'.format(someinput))
		plt.show()


class BuildModel(WordStats):
	def __init__(self):
		WordStats.__init__(self)
		self.pickle = PickleDoc()

	def unigram_model(self, someinput, writefile=None):
		f = self.token_freq(someinput)
		if writefile:
			wf = writefile
			logger.debug('unigram_model found a writefile param: {0}'.format(writefile))	
		else:
			wf = None
			logger.debug('unigram_model found no writefile param')
		self.pickle.pickle(f, wf)
			

	def bigram_model(self, someinput, writefile=None):
		f = self.bigram_freq(someinput)
		if writefile:
			wf = writefile
		else:
			wf = None
		self.pickle.pickle(f, wf)

	def trigam_model(self, someinput, writefile=None):
		f = self.trigram_freq(someinput)
		if writefile:
			wf = writefile
		else:
			wf = None
		self.pickle.pickle(f, wf)

	def n_gram_model(self, someinput, n, writefile=None):
		f = self.n_gram(someinput, n)
		if writefile:
			wf = writefile
		else:
			wf = None
		self.pickle.pickle(f, wf)




# print 

# x = os.listdir('/Users/ahmedmahdi/Documents/testcrawl/crawl/brown')


# print x







d = {1:2, 2:3, 4:1, 5:1, 6:4, 8:3, 9:4}

# def reverse_dict(di):
# 	d1={}

# 	for k, v in di.items():
# 		if v not in d1:
# 			d1[v] = []
# 			d1[v].append(k)
# 		else:
# 			d1[v].append(k)
# 	return d1

# print d
# print 
# print reverse_dict(d)





























