"""
	Contains:

		- Indexer Class.
"""

class Indexer():
	"""
		Objects are Variable with internal State and Interactive Behaviour!

		An Indexer is an object that remembers how often it was used.

		By "calling" the state of the variable the index will shift by step.

		Defaults:

		Starting index of 0 and a step of 1
			==> the first index will be 1
			==> index() -> i0 +1

		The first index will always be start+step!

	"""

	# slots makes the attribute number fixed!
	__slots__ = '_index', '_start', '_step'
	# double __ attributes names makes them unaccessible from a derivative class

	def __init__(self, start:int = 0, step:int = 1):
		self._index = start		# first index is actually start+step
		self._step = step		# index backwards for step < 0
		self._start = start		# used to reset

	def __call__(self)->int:
		"""
			shift index.

			Should be the 
		"""
		self._index += self._step
		return self._index

	@property
	def index(self)->int:
		"""
			A property is callable just by asking for the attribute value!

			obj.index <==> getattr(obj, index) #Function-Call
		"""
		return self()

	# state-value no increment/decrement
	@property
	def count(self)->int:
		return self._index

	###############################
	######### Looped-Over #########
	###############################

	def __iter__(self):
		"""
			INFINITE YIELDER!!!

			Possible Usage is to be zipped with a finite Sequence
		"""
		while True:		# !!!
			yield self()

	#################################
	############ casting ############
	#################################

	# Casting <==> Index-Shift

	def __int__(self) -> int:	# make it an int
		"""
			called by int(self)
		"""
		# basically calls self.__call__()
		return self()

	# also works with str
	def __repr__(self) -> str:	# 2-> string
		return str(self.index)

	###############################################
	############ Arithmetic-Operations ############
	###############################################

	# DOESN'T CHANGE INTERNAL STATE!

	### Addition ###
	# to be used with an external start

	# add other to self		self + other
	def __add__(self, other):
		# let the other guy do the heavy lifting
		return other.__add__(int(self))		# calling int shift the index

	# add self to other		other + self
	def __radd__(self, other):
		return self.__add__(other)

	### Multiplication ###
	# to be used with  an external step

	def __mul__(self, other):
		# the behavior is defined by the other!
		return other.__mul__(int(self))

	def __rmul__(self, other):
		# oder shouldn't matter
		return self.__mul__(other)

	##################################
	##### Modify-Internal-State ######
	##################################

	def reset(self):
		self._index = self._start

