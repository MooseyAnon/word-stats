import math
from functools import reduce
import operator 
from classes import *


class Probabilities(WordStats):
	def __init__(self):
		WordStats.__init__(self)
		self.pickle = PickleDoc()
		self.u_model = self.pickle.unpickle('unigram.pkl')
		logger.debug('unigram unpickled!')



	def _standard_unigram_prob(self, alist):
		"""
		unsmoothed maximum likelihood estimate of the unigam for a given wi.

		P(wi) = c(wi)/N

		The mle of any given word is the count of that word in the model divided by the count of 

		total word tokens. 

		"""

		prob = []
		results = []
		for word in alist:
			if word in self.u_model:
				wcount = self.u_model[word]
			else:
				wcount = 1

			x = float(wcount)/float(len(self.u_model))
			prob.append(x)
			results.append((word, x))

		return results, sum(prob)

	def _laplace_smoothing_unigram_prob(self, alist):


		prob = []
		results = []
		for word in alist:
			if word in self.u_model:
				wcount = self.u_model[word]
			else:
				wcount = 1

			x = float(wcount+1)/float(len(self.u_model)) # due to the model holding all unique keys for the doc len(u_model) == V
			prob.append(x)
			results.append((word, x))

		return results, sum(prob)

	def unigram_prob(self, astring, laplace=False):

		words = re.split('\s+', astring)

		if laplace == False:
			up = self._standard_unigram_prob(words)
			logger.debug('String prob with no laplace smoothing')
		else:
			up = self._laplace_smoothing_unigram_prob(words)
			logger.debug('String prob with laplace smoothing')

		return up


	def standard_bigram_prob(self, astring):

		bgs = self.bigram(astring)
		results = []
		probs = []

		for bg in bgs:
			if bg in self.b_model:
				bigram_count = self.b_model[bg]
			else:
				bigram_count = 1

			if bg[0] in self.u_model:
				w_minus_one_count = self.u_model[bg[0]]
			else:
				w_minus_one_count = 1

			x = float(bigram_count)/float(w_minus_one_count)
			results.append((bg[1], x))
			probs.append(x)

		return results, sum(probs)


# reduce(operator.mul, prob, 1)


st = "estimates of the city's loss in the $344,000 job have ranged as"

t2 = 'remedy this problem implementation of georgia\'s automobile'

t3 = 'hokus pokus hikory do'


t4 = 'judge durwood pye to investigate reports of possible irregularities in in'

# t = Probabilities()

# print t.unigram_prob(t4)

# 0.30257270693512306 unigram with laplace 
# 0.29697986577181207 unigram without laplace 























