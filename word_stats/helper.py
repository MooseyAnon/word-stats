from classes import *


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


	def _extend_pickled_list(self, obj, extendfile):

		if os.path.exists(extendfile):
			with open(extendfile, 'r') as ef:
				p1 = pickle.load(ef)
				logger.debug('1. unpickled {0}'.format(ef))
				p2 = p1 + obj
				logger.debug('1.5 appended')
				# return p1, type(p2)
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

		else:
			return 'file does not exist'

				
	def extend_pickled_dict(self, obj, extendfile):

		if os.path.exists(extendfile):
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

		else:
			return 'file does not exist'





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




# t = PickleDoc()

# y = ['k-yaaa','lovvve','k-hello2','version2']
# t.pickle(y, '12345.pkl')

# d = ['next','add','is','here']

# print t.extend_pickled(d, '12345.pkl')

# print t.unpickle('12345.pkl')


# t = CSVSaver()

# d = {'k-yaaa':'lovvve','k-hello2':'version2' }

# t.csv_write(d, 'test.csv')




# print y + d

d = {1:2, 2:3, 3:4}

p = {5:6, 6:7, 8:9, 2:4, 4:[1,2,3]}

# for k in d.keys():
for i, j in p.items():
	if i not in d.keys():
		d[i] = j
	else:
		pass

print d

# p[4] = 3
# p4 = p[4].append(4)
# print type(p[4]) == list

# print p[4]

# t = PickleDoc()

# t.pickle(d, 'testing.pkl')

# print t.extend_pickled_dict(p, 'testing.pkl')

# output: {1: 2, 2: 3, 3: 4, 4: [1, 2, 3], 5: 6, 6: 7, 8: 9}



