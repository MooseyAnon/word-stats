from classes import *


"""Unfinished helper classes for wrtiting, reading and extending csv and pickled files"""

class PickleDoc:
		

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


	def _extend_pickled_list(self, obj, extendfile):
		"""extends a pickled list object from a given file"""

		with open(extendfile, 'r') as ef:
			p1 = pickle.load(ef)
			logger.debug('1. unpickled {0}'.format(ef))
			p2 = p1 + obj
			logger.debug('1.75 appended {0}'.format(type(p2)))


		with open(extendfile, 'w') as ew:
			logger.debug('2. about to pickle object at {0}'.format(ew))
			pickle.dump(p2, ew)
			logger.debug('3. pickled object at {0}'.format(ew))
			ew.close()
			logger.debug('3.5 closed object at ')

		with open(extendfile, 'r') as e:
			logger.debug('4. reading object {0}'.format(e))
			r = pickle.load(e)
			logger.debug('5. read object {0}'.format(e))

		return r


				
	def _extend_pickled_dict(self, obj, extendfile):
		"""extends a pickled dict object from a given file"""

		with open(extendfile, 'r') as efr:
			p1 = pickle.load(efr)

			for k, v in obj.items():
				if k not in p1.keys():
					p1[k] = v
				elif type(p1[k]) == list:
					p1[k] = p1[k].append(v)
				else:
					pass

		with open(extendfile, 'w') as efw:
			pickle.dump(p1, efw)

		with open(extendfile, 'r') as er:
			r = pickle.load(er)

		return r



	def extend_file(self, obj, extendfile):


		if os.path.exists(extendfile):
			if type(obj) == dict:
				ex_file = self._extend_pickled_dict(obj, extendfile)
			elif type(obj) == list:
				ex_file = self._extend_pickled_list(obj, extendfile)
			else:
				logger.debug('Object type is not extensable')

		else: 
			logger.debug('file does not exists')






class CSVSaver:

	def csv_write(self, adict, writefile=None):

		if writefile:
			with open(writefile, 'wb') as wf:
				w = csv.writer(wf)
				for key, value in adict.items():
						w.writerow([key, value])
			
		else:
			with open('default.csv', 'wb') as wf:
				w = csv.writer(wf)
    			for key, value in adict.items():
						w.writerow([key, value])


	def csv_read(self, readfile):

		try:
			with open(readfile, 'rb') as rf:
				reader = csv.reader(rf)
				d = dict(reader)
				return d
		except IOError:
			logger.debug('Had problems reading {0}'.format(readfile))






