PRIMES = (

#	1   2   3   4   5   6   7   8   9   10
	2,  3,  5,  7,  11, 13, 17, 19, 23, 29,   #  +0
	31, 37, 41, 43, 47, 53, 59, 61, 67, 71,  #  +10
	73, 79, 83, 89, 97                       #  +20

)

def nonzero(A):
	return tuple(a for a in A if a != 0)

def sieve_of_eratosthenes(bis):
	N = list(range(3, bis+1 if bis%2 else bis, 2))
	
	p, index = 3, 0
	
	while not ((index := p*p) > bis):
		step = 2*p
		while not index > bis:
			N[(index-3)//2] = 0
			index += step
		
		p += 2
		while (N[(p-3)//2]) == 0:
			p += 2

	# return tuple((2, *(n for n in N if n != 0)))
	return (2, *(n for n in N if n != 0), )

def extend_sieve_of_eratosthenes(bis, P):
	
	von = P[-1] + 2

	N = list(range(von, bis+1 if bis%2 else bis, 2))

	foothold = lambda p: (r + 1 + r%2)*p if (von - p*(r := von//p)) != 0 else r*p

	foothold_of = map(foothold, P)

	nfoothold = lambda: next(foothold_of)

	nfoothold()		# starts at three

	index = 0

	for p in P[1:]:
		if p*p > bis:
			break
		step = 2*p

		index = nfoothold()

		while not index > bis:
			N[(index-von)//2] = 0
			index += step
	else:
		p += 2
		while (N[(p-von)//2]) == 0:
			p += 2
		
		while not ((index := p*p) > bis):
			step = 2*p
			while not index > bis:
				N[(index-von)//2] = 0
				index += step
			
			p += 2
			while (N[(p-von)//2]) == 0:
				p += 2

	return (*P, *(n for n in N if n != 0))


# Alias/Shell for the main methode to find Prime
def primes(bis = 1000):
	return sieve_of_eratosthenes(bis)

def extend_primes(bis = 10**3, P = PRIMES):
	return extend_sieve_of_eratosthenes(bis, P)


