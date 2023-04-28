"""
	initializer

		Turns a python function into a generator

		The function is meant to represent a mathematical sequence

		Which will be turned into an infinite sequence!

"""

from functools import wraps	# just for wrapping

def initialize(n0:int = 0, *a_, h:int = 1):
	"""
		Initialize a mathematical sequence with starting values and turns it into a infinite sequence! 

			- The sequence must return a single value #the-value-of-the-sequence-at-that-index

			- The sequence must accept at least one parameter n #an-index

			- The sequence can have as many "RELATIVE" recursive dependencies as needed or none at all

		Returns an wrapper, which turns a sequence into an infinite yielder!

		The generator returns a tuple of the sequence value with the corresponding index

			(n, a_n)	#index-value-pair

		parameter:
			- n0   stating index                                  Default 0
			- a_   starting value of the relative dependencies
			- h    each time n will be shifted be step.           Default 1

		The generator has internal state, which will be changed
		Each time #next is called upon the generator:

			n += h
			a = f(n, *a_)	# where *a_ previous terms

		The sequence can be written as a function of (n, *a_) #a_ are previous-terms
		The previous terms can also be written as a parameter
		
			For k previous dependency:
				f(n, a_{n-k}, a_{n-k-1}, a_{n-k-2}.... , a_{n-1})

			f(n, a0, a1, a2)

		The order is important!

		Unfortunately f must be depended on n!

	"""
	def wrapper(f):
		@wraps(f)
		def yielder():
			def shift_dependencies(a):	# update dependencies
				nonlocal a_
				a_ = [*a_[1:], a]		# by adding the last value and dropping the first
			push = shift_dependencies if len(a_) else lambda a: None
			n = n0
			while True:		# infinite yielder!!!
				a = f(n, *a_)
				yield n, a
				push(a)		# shifts the dependency stack
				n += h
		return yielder
	return wrapper

# -----------------------------

####################
#### Formatting ####
####################

def line_formatter(Format:str = "a({}) : {}"):
	"""
		returns a function that prints a that it received according to a specific Format
	"""
	return lambda *args: print(Format.format(*args))

def loop(A, n:int = 10):
	"""
		loops over an infinite sequence n times
	"""
	while (n := n - 1) > 0:
		yield next(A)


def show(A, n:int = 10, Format:str = "a({}) : {}"):
	f = line_formatter(Format)
	for na in loop(A(), n):
		f(*na)

## ------------------------------------ ##

################
##### Main #####
################

def main():
	print(__doc__)

if __name__ == '__main__':
	main()

