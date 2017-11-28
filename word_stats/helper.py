

"""Unfinished helper classes for wrtiting, reading and extending csv and pickled files"""

class PickleDoc:
	# def __init__(self):
		

	def pickle(self, obj, writefile=None):

		if writefile:
			with open(writefile, 'w') as ad:
				pckled = pickle.dump(obj, ad)
				logger.debug('pickled object at {0}'.format(writefile))
				# return pckled
		else:
			with open('default.plk', 'w') as df:
				pckled = pickle.dump(obj, df)
				logger.debug('pickled object at default file')
				# return pckled


	def unpickle(self, readfile):
		logger.debug('unpickling {0}'.format(readfile))

		try:
			with open(readfile, 'r') as rf:
				p = pickle.load(rf)
				logger.debug('unpickled {0}'.format(readfile))
				return p
		except IOError:
			logger.debug('issue unpickling {0}'.format(readfile))


	def extend_pickled(self, obj, extendfile):

		if os.path.exists(extendfile):
			# with open(extendfile, 'r') as ef:
			# 	p1 = pickle.load(ef)
			# 	logger.debug('1. unpickled {0}'.format(ef))
			# 	# p2 = pickle.dump(obj, p1)
			# 	# r = pickle.load(p2)
			# 	# return p1 
			# 	ef.close()

			with open(extendfile, 'a+b') as ew:
				logger.debug('2. about to pickle object at {0}'.format(ew))
				pickle.dump(obj, ew)
				logger.debug('3. pickled object at {0}'.format(ew))
				ew.close()
				logger.debug('3.5 closed object at ')

			with open(extendfile, 'r') as e:
				logger.debug('4. reading object {0}'.format(e))
				r = pickle.load(e)
				logger.debug('5. read object {0}'.format(e))

			return r

		else:
			return 'file does not exist'

				
			# return r



class CSVSaver:

	def csv_write(self, adict, writefile=None):

		if writefile:
			with open(writefile, 'wb') as wf:
				w = csv.writer(wf)
				w.writerow(adict.items())
				# w.writerow(adict.values())
		else:
			with open('default.csv', 'wb') as wf:
				w = csv.writer(sys.stderr)
    			w.writerow(adict.keys())
    			w.writerow(adict.values())