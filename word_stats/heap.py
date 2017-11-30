


class MaxHeap:

	def __init__(self):
		self.heap = []
		self.currentsize = 0
	
	def get_heap(self):
		return self.heap

	def heap_size(self):
		return self.currentsize

	def get_max(self):
		return self.heap[0]

	def get_parent_index(self, childindex):
		return (childindex-1)/2

	def get_left_child_index(self, parentindex):
		return (parentindex * 2) + 1

	def get_right_child_index(self, parentindex):
		return (parentindex * 2) + 2
		
	def has_parent(self, index):
		return self.get_parent_index(index) >= 0

	def has_left_child(self, parent):
		return self.get_left_child_index(parent) < self.currentsize

	def has_right_child(self, parent):
		return self.get_right_child_index(parent) < self.currentsize

	def has_children(self, parent):
		i = self.currentsize
		if self.get_left_child_index(parent) < i and self.get_right_child_index(parent) < i:
			return True
		else:
			return False

	def get_parent(self, child):
		if child == 0:
			None
		else:
			return self.heap[self.get_parent_index(child)]

	def get_left_child(self, parent):
		if self.has_left_child(parent) == False:
			return None 
		else:
			return self.heap[self.get_left_child_index(parent)]

	def get_right_child(self, parent):
		if self.has_right_child(parent) == False:
			return None 
		else:
			return self.heap[self.get_right_child_index(parent)]

	def add(self, item):
		self.heap.append(item)
		self._heapifyup()
		self.currentsize += 1

	def delmax(self):
		self.heap[0] = self.heap[-1]
		del self.heap[-1]
		self._heapifydown()
		self.currentsize -= 1

	def _max_child(self, parent):
		if self.has_children(parent) == True:
			i = self.get_left_child(parent)
			j = self.get_right_child(parent)
			if i > j:
				return i
			else:
				return j
		# there can be a left child without right but there can never be a right withough left
		elif self.has_left_child(parent) == True: 
			return self.get_left_child(parent)
		else:
			return None

	def _heapifyup(self):
		i = self.currentsize 
		print 'eye ---- is --- ', i
		while self.has_parent(i) == True and self.get_parent(i) < self.heap[i]:
			print 'heap i is', self.heap[i], 'at index ', i 
			t = self.get_parent(i) 
			self.heap[self.get_parent_index(i)] = self.heap[i] # hold 
			self.heap[i] = t

			i = self.get_parent_index(i)
			print 'new eye ---- is ----', self.heap[i], 'at index', i


	def _heapifydown(self):
		i = 0 
		while self.has_left_child(i):
			print self.has_left_child(i)
			mc = self._max_child(i)
			print 'mc is ----', mc, self.heap.index(mc)
			if mc is not None:
				print self.heap[i]
				if self.heap[i] < mc:
					t = self.heap[i]
					print 't is ----', t
					t2 = self.heap.index(mc)
					print 't2 is -----', t2
					self.heap[i] = self.heap[self.heap.index(mc)]
					print 'self eye ======', self.heap[i]
					
					self.heap[t2] = t
					print 't is now at index {0} with value {1}'.format(t, self.heap[t2])

					i = self.heap[t2]
					print 'new eye is -----', i 
				else:
					break
			else:
				break


	def build_heap(self, alist):
		"""not a great way to do it but will work for now"""
		for c in alist:
			self.add(c)

		return self.heap








































