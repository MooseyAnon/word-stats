


"""Basic heap implimentation to find most/least common ngrams"""

class BinaryHeap:
	def __init__(self):
		self.heaplist=[0]
		self.currentsize=0

	def _swapup(self,i):
		while i // 2 > 0:
			if self.heaplist[i]< self.heaplist[i//2]:
				t = self.heaplist[i//2]
				self.heaplist[i//2]=self.heaplist[i]
				self.heaplist[i]=t 
			i = i // 2

	def insert(self,i):
		self.heaplist.append(i)
		self.currentsize += 1 
		self._swapup(self.currentsize)

	def _swapdown(self,i):
		while i*2 <= self.currentsize:
			mc = self._min_child()
			if self.heaplist[i] > self.heaplist[mc]:
				t = self.heaplist[i]
				self.heaplist[i] = self.heaplist[mc]
				self.heaplist[mc]= t
			i = mc 

	def _min_child(self,i):
		if i*2 +1 > self.currentsize:
			return i*2	
		else:
			if self.heaplist[i*2]< self.heaplist[i*2+1]:
				return i * 2 
			else:
				return i * 2 + 1

	def delmin(self):
		r = self.heaplist[1]
		# make the root the current last item of the heap 
		self.heaplist[1]=self.heaplist[self.currentsize]
		self.currentsize -= 1 
		self.heaplist.pop()
		# swapdown new 1st index
		self._swapdown(1)
		return r 


	# buildheap from a given list
	def build_heap(self, alist):
		# make i the current middle value of heap becoz everything after half way is a leaf
		i = len(alist)//2 
		self.currentsize = len(alist)
		self.heaplist = [0]+alist[:]
		while i > 0:
			self._swapdown(i)
			i -= 1 