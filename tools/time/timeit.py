"""
	My First Python Tool Created :)

	#Legacy-Code
	#TODO #NOT-Maintain-Able

"""

import time

from functools import wraps

class Timer:
	"""
		Timer-Object can be used:
			- as a timer by initialize it, calling script, and calling it again at the end
			- as logger by calling it multiple times
			- as context manager		*in with-statement
			- as a decorator
	"""

	# time_keeper = time.perf_counter_ns

	time_keeper = time.perf_counter

	cls_instances = 0

	@classmethod
	def get_cls_index(cls):
		cls.cls_instances += 1
		return cls.cls_instances

	# Class default values

	precision = 3   # significant figures to display the timer time

	msg = "\nTimer:\t{} seconds elapsed . . .\n"     # message to be displayed for single call

	msg_mark = "\nMark_{}\t{} seconds elapsed since last mark.\n"   # message to be displayed for repeated call

	msg_mark_no_index = '{1} seconds elapsed....'

	def __init__(
		self, msg = msg,
		msg_mark = msg_mark,
		precision = precision, no_index = True
	):

		# Properties
		self.index = 0                  # the index of timer call
		self.time = float()             # last measured cycle
		self.msg = msg                  # formatted message to be displayed     # When the timer is used once
		self.msg_mark = msg_mark        # formatted message to be displayed with index
		self.precision = precision      # How many significant figures to be displayed
		if no_index:
			self.msg_mark = self.__class__.msg_mark_no_index

		# Timer
		self.marks = [self.time_keeper()]
		
		self.cls_instance = T = self.get_cls_index()



	# calling the T-Object has two effect
		
		# with no arguments it’s a timer click

		# with argument it returns a decorator
			# a decorator is a function that takes a function as an input and returns a function “a wrapper” as 
	def __call__(self, *args):
		if len(args) != 0:
			return self.__deco__(*args)
		self.show_timer_mark()
		return self.time


	# list-like behaviour

	# returns the value stored in self.marks
	def __getitem__(self, index):
		if index < 0:
			return self.marks[-((-index)%(len(self.marks)+1))]
		return self.marks[index%len(self.marks)]    # fail-safe     # idiot-proof

	# length of the T-Object is the length self.marks
	def __len__(self):
		return len(self.marks)

	# iteration behaviour
	def __iter__(self):
		for t in self.marks:
			yield t



	# Contextmanager 
	# to be called in with-statement for example

	def __enter__(self):
		self.mark()
		return self

	def __exit__(self, *args):
		# args: exc_type, exc_value, traceback
		self.mark()
		self.show_timer()


	# Methods


	def mark(self, index = -2):
		"adds the time to T-Object and rest the clock for the next cycle"

		self.index += 1
		self.marks.append(self.time_keeper())
		self.time = round(self.marks[-1] - self.marks[index], self.precision)



	def reset (self):
		"reset the timer and re-initialize its values"

		self.marks.clear()
		self.mark()
		self.index = 0



	# functionality

	# Decorator

	def __deco__(self, func):
		"To be use when the T-Object is called to be a decorator"

		@wraps(func)
		def wrapper(*args, **kwargs):
			self.__enter__()
			revalue = func(*args, **kwargs)
			self.__exit__()
			return revalue
		return wrapper



	# Print/Display

	
	def show_timer(self):
		"displays the time elapsed since last call according to formatted message"

		print(self.show_timer_cls(self.msg, self.time))

	# to be also used when exported
	@staticmethod
	def show_timer_cls(msg, time):
		return msg.format(time)



	def show_timer_mark(self):
		"marks time and displays the time elapsed since last call"

		self.mark()
		print(self.show_timer_mark_cls(self.msg_mark, self.index, self.time))
		

	# to be also used when exported
	@staticmethod
	def show_timer_mark_cls(msg, index, time):
		return msg.format(index, time)


	# Summary/Export

	# message to be displayed for single call
	msg_summary = "Marks_{} occurred after\t{} seconds"

	# message to be displayed for repeated call
	msg_mark_summary = "Marks_{} occurred after\t{} seconds"


	def get_time(self):
		"return a list with time between the timer calls"

		return *(round(self.marks[n] - self.marks[n-1], self.precision) for n in range(1, len(self.marks))),


	def data(self):
		"returns a dictionary with important values"

		summ = dict()
		summ['marks'] = *(mark for mark in self.marks),
		summ['time'] = self.get_time()
		return summ


	def summary(self):
		"returns timer summary as str"

		summ = self.data()

		a = self.show_timer_mark_cls   # alias

		text = 'Timer Information\n\nTime between calls:\n'
		msg = Timer.msg_summary
		for index, t in enumerate(summ['time']):
			text += '\n\n' + a(msg, index, t)
		
		text += '\n\n\n\nMarks occurred n seconds since python session have started:\n'
		msg = Timer.msg_mark_summary
		for index, m in enumerate(summ['marks']):
			text += '\n\n' +  a(msg, index, m)
		text += 2*'\n'
		return text


	# export timer summary to txt file
	def export(self, out_file = 'timer_summary.txt', mode = 'w'):
		"exports timer summary to txt file"

		text = self.summary()
		
		with open(out_file, mode) as file:
			file.write(text)

		print('Timer summary has been exported as', out_file)

		return text

		# giving out_file as a full path can change the location where the file is saved
		# otherwise it's going be saved in current working directory

	def __del__(self):
		if self.cls_instance == 1:
			print('\n\nTime Spent in Total')
			self.mark(0)
			self.show_timer()



