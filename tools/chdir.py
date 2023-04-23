import os

from functools import wraps

class Chdir:

	def __init__(self, cwd_tmp):
		self.URZUSTAND = os.getcwd()
		self.cwd = self.URZUSTAND
		self.cwd_tmp = cwd_tmp

	def switch(self):
		self.cwd, self.cwd_tmp = self.cwd_tmp, self.cwd
		os.chdir(self.cwd)
	
	def __enter__(self):
		self.switch()
		return self
	
	def __exit__(self, *args):
		self.reset()
	
	def __call__(self, *args):

		if len(args) == 0:
			self.switch()
			return
		
		return self.__deco__(*args)
	
	def __deco__(self, func):
		
		@wraps(func)	# to keep the original funcs info
		def wrapper(*args, **kwargs):
			with self:
				re = func(*args, **kwargs)
			return re
		
		return wrapper

	def reset(self):
		if self.URZUSTAND != self.cwd:
			self.switch()

	def __del__(self):
		self.reset()

