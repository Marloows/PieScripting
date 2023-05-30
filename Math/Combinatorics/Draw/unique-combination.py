"""
	All Unique Combination of a n-Set of element from a given Set

	- Each element can be arbitrary number of duplicates
		Or you can think as drawing a number out an urn and the putting it back

	- The combination of the elements is what makes a particular configuration unique not the order!
"""

def choose_of(n:int, N:int) -> list:
	"""
	Return Numeric Combination of:
		n choices out of R
	"""
	if n < 1:
		return [tuple()]

	append = lambda x, A: [(x, *a) for a in A]

	sub_combination = lambda i: append(N-i, choose_of(n-1, N-i))

	return sum(map(sub_combination, range(N)), [])	# sum of lists is concatenation

# - - - - - - - - - - - - - - - - - - -

def choose(n:int, G:list | tuple) -> list:
	"""
		choose n out R
	"""
	L = len(G)
	fetch = lambda *I: tuple(G[L-i] for i in I)
	return [fetch(*I) for I in choose_of(n, L)]

# - - - - - - - - - - -

def show(n:int , G:list | tuple) -> None:
	"""
		Just for show
	"""
	print(f"\n\tGroup: {G}\n")
	print(f"Combinations of {n}:\n")
	for i, k in enumerate(choose(n, G), 1):
		print(f"i: {i:<3}, {k}")
	print("\n")

def show_numeric(n:int , K:int) -> None:
	"""
		Just to show numerical combinations
	"""
	show(n, [*range(K+1)])


# - - - - - - - - - - -

show(3, [11, 3, 2, 7, 37])

