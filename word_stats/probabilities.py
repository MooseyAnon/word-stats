from __future__ import division
import math
from functools import reduce
import operator 
from classes import *


# language modelling using the Markov Assumption
class NgramProbabilities(WordStats):
	def __init__(self):
		WordStats.__init__(self)

		self.pickle = PickleDoc()
		self.u_model = self.pickle.unpickle('unigram.pkl')
		logger.debug('unigram unpickled by NgramProbabilities!')
		self.b_model = self.pickle.unpickle('bigram.pkl')
		logger.debug('bigram unpickled by NgramProbabilities!')
		self.t_model = self.pickle.unpickle('trigram.pkl')
		logger.debug('trigram unpickled by NgramProbabilities!')



	def _standard_unigram_prob(self, alist):
		"""
		unsmoothed maximum likelihood estimate of the unigam for a given wi.

		P(wi) = c(wi)/N

		The mle of any given word is the count of that word in the model divided by the count of 

		total word tokens. 

		"""

		prob = []
		# results = []
		for word in alist:
			if word in self.u_model:
				wcount = self.u_model[word]
			else:
				wcount = 1

			x = -1*math.log(float(wcount)/float(len(self.u_model)), 2)
			prob.append(x)
			# results.append((word, x))

		return sum(prob) #, results

	def _laplace_smoothing_unigram_prob(self, alist):


		prob = []
		results = []
		for word in alist:
			if word in self.u_model:
				wcount = self.u_model[word]
			else:
				wcount = 1

			x = -1*math.log(float(wcount+1)/float(len(self.u_model)), 2) # due to the model holding all unique keys for the doc len(u_model) == V
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


	def _standard_bigram_prob(self, alist):

	
		results = []
		probs = []

		for bg in alist:
			if bg in self.b_model:
				bigram_count = self.b_model[bg]
			else:
				bigram_count = 1

			if bg[0] in self.u_model:
				w_minus_one_count = self.u_model[bg[0]]
			else:
				w_minus_one_count = 1
			# multiply by munis 1 to make answer postive because taking a base 10 leg of a number less than 1 == to a negative number
			x = -1*math.log(float(bigram_count)/float(w_minus_one_count), 2)
			# coud use this formula instead: float(bigram_count)/float(w_minus_one_count)
			results.append((('P: '+bg[1] +'|' +bg[0]), x))
			probs.append(x)

		return sum(probs)

	def _laplace_smoothing_bigram_prob(self, alist):

		
		results = []
		probs = []

		v = len(self.u_model) # v is the total vocab of the model, here this is equal to the total unigrams in this model

		for bg in alist:
			if bg in self.b_model:
				bigram_count = self.b_model[bg]
			else:
				bigram_count = 1

			if bg[0] in self.u_model:
				w_minus_one_count = self.u_model[bg[0]]
			else:
				w_minus_one_count = 1

			# multiply by munis 1 to make answer postive because taking a base 10 leg of a number less than 1 == to a negative number
			x = -1*math.log(float(bigram_count + 1)/float(w_minus_one_count + v), 2) # gettting the log of the probability allows us to sum rather than multiply the outcomes. However not nessessary
			# could use this formula instead: float(bigram_count + 1)/float(w_minus_one_count + v). however, this requires probabilties being multiplied not summed i.e. reduce(operator.mul, prob, 1)
			results.append((bg[1], x))
			probs.append(x)

		return results, sum(probs)


	def bigram_prob(self, astring, laplace=False):

		words = self.bigram(astring)

		if laplace == False:
			r = self._standard_bigram_prob(words)
		else:
			r = self._laplace_smoothing_bigram_prob(words)
			
		return r


	def _standard_trigram_proability(self, alist):

		

		results = []
		probs =[]
		for tr in alist:
			if tr in self.t_model:
				trigram_count = self.t_model[tr]
			else:
				trigram_count = 1

			bi = (tr[0], tr[1])

			if bi in self.b_model:
				bi_count = self.b_model[bi]
			else:
				bi_count = 1

			# multiply by munis 1 to make answer postive because taking a base 10 leg of a number less than 1 == to a negative number
			x = -1*math.log(float(trigram_count)/float(bi_count), 2)
			results.append((('P of -'+tr[2]+'- given '+ tr[0], tr[1]), x))
			probs.append(x)


		return sum(probs)


	def _laplace_smoothing_trigram_prob(self, alist):

		
		v = len(self.b_model)

		results = []
		probs =[]
		for tr in alist:
			if tr in self.t_model:
				trigram_count = self.t_model[tr]
			else:
				trigram_count = 1

			bi = (tr[0], tr[1])

			if bi in self.b_model:
				bi_count = self.b_model[bi]
			else:
				bi_count = 1

			x = -1*math.log(float(trigram_count+1)/float(bi_count+v), 2)
			results.append((('P of -'+tr[2]+'- given '+ tr[0], tr[1]), x))
			probs.append(x)

		return sum(probs)


	def trigram_prob(self, astring, laplace=False):

		words = self.trigram(astring)

		if laplace == False:
			r = self._standard_trigram_proability(words)
		else:
			r = self._laplace_smoothing_trigram_prob(words)
			
		return r

	def single_trigram_prob(self, tri):

		"""this method is useful for conducting linear interpolation on a string"""

		if tri in self.t_model:
			trigram_count = self.t_model[tri]
		else:
			trigram_count = 1

		bi = (tri[0], tri[1])

		if bi in self.b_model:
			bigram_count = self.b_model[bi]
		else:
			bigram_count = 1

		x = -1*math.log(trigram_count/bigram_count, 2)

		return x

	def single_bigram_prob(self, bi):
		"""this method is useful for conducting linear interpolation on a string"""

		if bi in self.b_model:
			bigram_count = self.b_model[bi]
		else:
			bigram_count = 1 

		if bi[0] in self.u_model:
			uni_count = self.u_model[bi[0]]
		else:
			uni_count = 1 

		x = -1*math.log(bigram_count/uni_count, 2)

		return x

	def single_unigram_prob(self, uni):
		"""this method is useful for conducting linear interpolation on a string"""

		if uni in self.u_model:
			uni_count = self.u_model[uni]
		else:
			uni_count = 1 

		x = -1*math.log(uni_count/len(self.u_model), 2)

		return x




class LMEvaluation(NgramProbabilities):
	def __init__(self):
		NgramProbabilities.__init__(self)

	def unigram_perplexity(self, astring):

		r = self.unigram_prob(astring)
		r2 = (1/len(self.u_model))

		p = 2**-r2
		
		r3 = r**-r2

		# p  = round(1/len(self.u_model), 12)

		return r, r2, p, r3
		# output fot st: (88.61551746431823, 0.0005592841163310962, 0.9996124089244686, 0.9974951407402597)
		

	def bigram_perplexity(self, astring):

		r = self.bigram_prob(astring) 

		r2 = (1/len(self.u_model))

		p = 2**-r2

		r3 = r**-r2

		return r, r2, p, r3
		# output for st: (29.444403643366805, 0.0005592841163310962, 0.9996124089244686, 0.998110007605239)

	def trigram_perplexity(self, astring):

		r = self.trigram_prob(astring)

		r2 = (1/len(self.u_model))

		p = 2**-r2

		r3 = r**-r2

		return r, r2, p, r3
		# output for st: (17.113213102571798, 0.0005592841163310962, 0.9996124089244686, 0.998412977175279)





class LinearInterpolation(NgramProbabilities):
	def __init__(self):
		NgramProbabilities.__init__(self)
		self.l = round(1/3, 4)

	def simple_lin_interpolation(self, astring):

		tris = self.trigram_prob(astring)
		bis = self.bigram_prob(astring)
		unis = self.unigram_prob(astring)

		sli = ((self.l * tris)+(self.l * bis)+(self.l * unis))
		return sli

	def simple_lin_interpolation2(self, astring):

		tris = self.trigram(astring)

		results = []

		for tri in tris:
			x = self.single_trigram_prob(tri)
			y= self.single_bigram_prob((tri[0], tri[1]))
			z = self.single_unigram_prob(tri[2])
			sli = ((self.l * x)+(self.l * y)+(self.l * z))
			results.append(sli)
		
		return sum(results)



st = "estimates of the city's loss in the $344,000 job have ranged as"

t2 = 'remedy this problem implementation of georgia\'s automobile'

t3 = 'hokus pokus hikory do'


t4 = 'judge durwood pye to investigate reports of possible irregularities in in'




t = LinearInterpolation()

print t.simple_lin_interpolation2(st)

print t.simple_lin_interpolation(st)



# t = NgramProbabilities()

# print t.unigram_prob(t4)

# 0.30257270693512306 unigram with laplace 
# 0.29697986577181207 unigram without laplace 



# print t.bigram_prob(t4)




# x = (1, 2, 3)

# print (x[1], x[2])


# print t.trigram_prob(st, laplace=True)

# t = LMEvaluation()

# print t.unigram_perplexity(st)


# x = math.log(1/5, 2)

# print x 

# y = 2**-x 

# print y 


# x = round(1/3, 4)

# a=b=c=x

# print a, b, c




		


























