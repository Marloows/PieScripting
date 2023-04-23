"""
	search the pythonpath to find the module by name and opens it

	Flags:
		-n, -notepad                             notepad
		-code, -c                                vscode
		-cat, -type                              type
		-npp, -n++, -notepad++                   notepad++
		-default                                 system default
		-x, -location, -file                     Opens at location

"""

import sys
import os

from importlib.util import find_spec


def cmd_format(cmd_format):
	"""
			return a function that expect arg to be passed on to the cmd_command
	"""
	def wrapper(*args):
		args = ' '.join(f'"{a}"' for a in args)
		os.system(f'{cmd_format} {args}')

	return wrapper


def one_at_a_time(f):
	def wrapper(*args):
		if len(args):
			for a in args:
				f(a)
		else:
			f()
	return wrapper


def gen_single_sys_calls(cmd_command):  # V0
	"""
			return a function tha is 
	"""
	@one_at_a_time
	def sys_call(a):
		cmd_format(cmd_command)(a)

	return one_at_a_time(sys_call)


def open_at_location(*args):
	"""
			open the file explorer at the location of the file
			when given multiple file it opens multiple windows
	"""
	gen_single_sys_calls('explorer /select,')(*args)


def open_with_sys_default(*args):
	"""
			open the file explorer at the location of the file
			when given multiple file it opens multiple windows
	"""
	gen_single_sys_calls('explorer')(*args)


class Singleton(type):  # Allows only one instant of a child class

	def __init__(self, *args, **kwargs):  # initialize the class
		self.__instance = None
		super().__init__(*args, **kwargs)

	def __call__(self, *args, **kwargs):  # called whenever the class constructed is called
		if self.__instance is None:
			self.__instance = super().__call__(*args, **kwargs)
			return self.__instance
		return self.__instance


class ConfigEditor(metaclass=Singleton):

	def __init__(self):
		self.EDITOR = dict()
		self.DEFAULT_EDITOR = self.config()
		self.sys_call = self.EDITOR[self.DEFAULT_EDITOR]

	def config(self):
		"""
				configure the known editor and returns the default one
		"""

		# basics
		# WINDOWS
		self.add_editor('type', 'cat', gen_single_sys_calls(
			'type'))        # TODO # Support for multiple file
		self.add_editor('notepad', 'n', gen_single_sys_calls(
			'notepad'))        # TODO # Support for multiple file

		# Default
		self.add_editor('code', 'c')

		# open with the system default        # ON WINDOWS
		self.add_editor('explorer', 'system-default',
						'default', 'sys', f=open_with_sys_default)

		self.add_editor('vim', 'v')
		self.add_editor('notepad++', 'npp', 'n++')

		# open at location
		self.add_editor('x', 'location', 'file', f=open_at_location)

		# return the default editor
		# in my case it's the system default
		return 'default'

	def __getitem__(self, key):
		if key in self.EDITOR.keys():
			return self.EDITOR[key]
		return self.DEFAULT_EDITOR

	def __call__(self, *args, **kwargs):
		self.sys_call(*args, **kwargs)

	def extend_known_editor(self, flags, f):
		self.EDITOR.update(dict.fromkeys(flags, f))

	def add_editor(self, cmd_command, *flag, f=None):
		"""
				Append the known editors/programs
				the command name is always included
				add other flags to configure the EDITOR dictionary
		"""
		self.extend_known_editor(
			[cmd_command, *flag], f if f else cmd_format(cmd_command))

	def parse_flag(self, f):
		# str.strip only removes at start and the end
		if f.strip('-') in self.EDITOR:
			self.sys_call = self.EDITOR[f]


def open_in(*files, editor=ConfigEditor()):
	"""
			Just passes the *files argument to the "editor/program"
	"""
	# Everything "should" be a string
	# leave the processing to each function
	editor.sys_call(*files)


def find_lib(*lib):
	"""
			return a list of path if the module are found
	"""

	# locate_lib
	def loc(l): return find_spec(l)  # return None if l no t found

	lib = [l.origin for l in map(loc, lib) if l]

	return lib if len(lib) else ['']


def parse_argv():

	# initialize with the default value
	# if no flag was found revert to default
	editor = ConfigEditor()

	lib = list()        # in case there is multiple files

	for arg in sys.argv[1:]:
		if '-' in arg:
			# if there is a flag found try to overwrite the editor
			# only works if the program is known
			editor.parse_flag(arg.strip('-'))
		else:
			lib.append(arg)

	lib = find_lib(*lib)  # return a list with module paths

	return lib, editor


def main():

	if len(sys.argv) < 2:
		print(__doc__)
		print("\n***\tInput a module name\t***\n")
		return

	lib, editor = parse_argv()

	open_in(*lib, editor=editor)


if __name__ == "__main__":
	main()
