"""
   initializer

      Turns a python function into a generator

      The function is meant to represent a mathematical sequence

      Which will be turned into an infinite sequence!

"""

from collections import defaultdict
from typing import Iterable, Iterator, Callable, Generator
from functools import wraps

## ------------------------------------ ##

#############################################
################ FORMATTING #################
#############################################

def line_separator(
      repeat_line_pattern:int    = 12,
      line_pattern:str           = '-',
      line_patter_sep: str       = ' ',
      padding_top:str            = '\n',
      padding_bottom:str         = 2*'\n'
   ):
   """
      Just for printing a horizontal line

      - - - - - - - - - - - - - - - - -
   """
   print(padding_top, end='')
   print(*(repeat_line_pattern*line_pattern),sep=line_patter_sep, end=padding_bottom)

# --------------

##########################
#### Table Formatting ####
##########################

def solidify(f: Callable):
   @wraps(f)
   def wrapper(S, *args, **kwargs):
      return f(tuple(S), *args, **kwargs)
   return wrapper

@solidify
def table(A:Iterable, cell_formatting:str = '{}') -> tuple:
   """
      Formatted Table

      A must be a "Matrix" of str!
   """

   def fetch_max_colum_width(Matrix:Iterable) -> dict:
      column_width = defaultdict(lambda: 0)   # in case incomplete rows

      def compare(x:int, at:int) -> None:
         # change the value if a max is found otherwise keep len_max[at] as is
         column_width[at] = x if x > column_width[at] else column_width[at]

      for row in Matrix:
         for i, x in enumerate(row):
            compare(len(x), i)

      return column_width

   def generate_cell_format(padding:int, alignment:str = '^') -> str:
      return cell_formatting.format("{" + f":{alignment}{padding}" + "}")

   cell_format = tuple(map(generate_cell_format, fetch_max_colum_width(A).values()))

   def format_cell(i:int, word:str, cell_format=cell_format):
      return cell_format[i].format(word)

   def format_line(line:Iterable, padding:str = ''):
      fIW = lambda IW: format_cell(IW[0], IW[1])      # just index, word
      return *map(fIW, enumerate(line)),

   S = tuple(map(format_line, A))

   return S

def fetch_header(n:int, var:tuple = ('n', 'a'), gen_dy_dt: Callable = lambda y: (lambda n:f"{y}({'n' if not n else '+'+str(n)})")):
   t, y = var
   dy_dt = gen_dy_dt(y)
   return t, y, *map(dy_dt, range(n-2))

def find_max_column_num(A:Iterable):
   return max(map(len, A))      # map the len function on each row of A

def join(A:Iterable, cell_format:str, line_format:str = "{}", cell_binding:str = '', line_binding:str = '\n') -> str:
   join_cells = lambda W: cell_binding.join(cell_format.format(w) for w in W)

   join_lines = lambda L: line_binding.join(line_format.format(l) for l in L)

   return join_lines(map(join_cells, A))

@solidify
def table_view(A:Iterable, cell:str = "   {}   ", verbose:bool = True, fetch_header:Callable = fetch_header) -> str:

   S = [fetch_header(find_max_column_num(A)), tuple(), *A]

   S = join(table(S), cell)

   if verbose:
      print(S)

   return S

# -----------------

## Markdown Format

def markdown_padding_line(widths:tuple) -> tuple:
   """
      Only supports :-:
   """
   def fetch_padding(width:int):
      return ((width-2)*'-').join(2*':') if width > 2 else ":-:"

   return *map(fetch_padding, widths),

@solidify
def markdown_table(A:Iterable, verbose:bool = True, fetch_header:Callable = fetch_header) -> str:

   columns_num = find_max_column_num(A)

   S = [fetch_header(columns_num), *A]

   S = table(S, cell_formatting = " {} ")

   widths = *map(len, S[0]),

   S = [S[0], markdown_padding_line(widths), *S[1:]]

   S = join(S, cell_format="{}", line_format = "|{}|", cell_binding = '|')

   if verbose:
      print(S)

   return S


# ------------------

## Show

def loop(A:Iterator, n: int = 10) -> Generator:
   """
      loops over an infinite sequence n times
   """
   while (n := n - 1) > 0:      # countdown
      yield next(A)

def show(A:Callable, n: int = 10, pre_process:Callable = lambda x: x, fetch_header:Callable = fetch_header) -> None:

   pre_processed = lambda Row: tuple(map(lambda x: f"{pre_process(x)}", Row))   # row-wise

   S = map(pre_processed, loop(A(), n))

   markdown_table(S, verbose=True, fetch_header=fetch_header)

def show_rounded(A:Callable, n: int = 10, rounded2:int = 6) -> None:

   show(A, n, pre_process=lambda x: round(x, rounded2), fetch_header=fetch_header)

## ------------------------------------ ##

###############################################
################ Initializing #################
###############################################

def independent_yielder(f:Callable, n0, h) -> Generator:
   @wraps(f)
   def yielder(n = n0, h = h):
      while True:		# infinite yielder!!!
         yield n, f(n)
         n += h
   return yielder()

def depended_yielder(f:Callable, n0, *a_, h) -> Generator:
   @wraps(f)
   def yielder(n = n0, a_ = a_, h = h):
      while True:		# infinite yielder!!!
         a = f(n, *a_)
         yield n, a
         a_ = [*a_[1:], a]		# update dependencies
         n += h
   return yielder()

def post_process(processor:Callable):
   def decorator(f:Callable):
      @wraps(f)
      def wrapper(*args, **kwargs):
         r = f(*args, **kwargs)
         return processor(r)
      return wrapper
   return decorator

def show_sequence(verbose:bool, *args, **kwargs) -> Callable:
   if not verbose:
      return post_process(lambda x: x)
   def print_first(X):
      show(X, *args, **kwargs)
      return X
   return post_process(print_first)

def initialize(
         n0 = 0, *a_, h = 1, 
         verbose: bool = True, loop: int = 10) -> Callable:
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
   def generator_factory(n0, *a_, h) -> Callable:
      @show_sequence(verbose, loop)
      def wrapper(f:Callable):
         @wraps(f)
         def yielder():
            if len(a_):
               return depended_yielder(f, n0, *a_, h = h)
            return independent_yielder(f, n0, h)
         return yielder
      return wrapper
   return generator_factory(n0, *a_, h=h)

#############################################
################# Main ######################
#############################################

def main():
   print(__doc__)

if __name__ == '__main__':
   main()

