import rich
from rich.progress import Progress as RichProgress

import getpass
import win32ui
import win32api

import os, sys
import threading as thr

class CLIBaseClass:
	name = 'CLI-Kit'
	ver = '0.1.1'

	handler = None

	rich = rich

	def __init__(self):
		self.cmd_dict = {}
		for name in dir(self):
			if name.startswith('cmd_'):
				ref = getattr(self, name)
				if callable(ref):
					c_name = name[4:]
					self.cmd_dict[c_name] = ref

		if self.handler is None:
			self.handler = self._Internal_DefaultHandler_

		self.running = True

		self.setup()
		thr.Thread(target=self.handler).start()


	def _Internal_DefaultHandler_(self, *args, **kwargs):
		while(self.running):
			msg = input(' >>> ').strip()
			try:
				if msg in self.cmd_dict:
					self.cmd_dict[msg]()
				else:
					rich.print(f'[red]No Command: "{msg}"')
			except:
				rich.print('[red]Error During Execution')

	def setup(self):
		pass 

	def cmd_help(self, *args, **kwargs):
		"""Shows this message."""
		for cmd in self.cmd_dict:
			print(f'{cmd} - {self.cmd_dict[cmd].__doc__ or 'No tip provided'}')

	def cmd_exit(self, *args, **kwargs):
		"""Exits the program."""
		self.running = False


class CLITools:
	class ProgressBar:
		def __init__(self, label, total=100):
			self.instance = RichProgress()

			self.task = self.instance.add_task(label, total=total)

		def start(self):
			self.instance.start()

		def add_progress(self, amount):
			self.instance.update(self.task, advance=amount)

		def is_finished(self):
			return self.instance.finished

		def end(self):
			self.instance.stop()

	class Table:
		def __init__(self, title):
			self.console = rich.console.Console()
			self.table = rich.table.Table(title=title)

		def add_column(self, name, **kwargs):
			self.table.add_column(name, **kwargs)

		def add_row(self, *values):
			self.table.add_row(*values)

		def print(self):
			self.console.print(self.table)

	class WriteOver:
		def __init__(self, msg, do_clear=True, clear_len=25):
			sys.stdout.write('\x1b[1A')
			sys.stdout.write('\r')
			sys.stdout.flush()

			if do_clear:
				print(' '*clear_len, end='\r')

			rich.print(msg)

	class GetSecret:
		def __init__(self, prompt='Secret >>> '):
			self.sec = getpass.getpass(prompt=prompt)

		def get(self):
			return self.sec

class GUITools:
	FD_SAFE = 0
	FD_OPEN = 1
	FD_FILEMUSTEXIST = 0x00001000
	FD_PATHMUSTEXIST = 0x00000800
	FD_MULTISELECT = 0x00000200
	FD_OVERWRITEPROMPT = 0x00000002
	FD_FILTER_ALL = 'All Files (*.*)|*.*'
	FD_FILTER_TXT = 'Text Files (*.txt)|*.txt'
	FD_FILTER_IMG = 'Image Files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp'

	MB_TYPE_OK = 0x00000000
	MB_TYPE_OKCANCLE = 0x00000001
	MB_TYPE_ABORTRETRYIGNORE = 0x00000002
	MB_TYPE_YESNOCANCLE = 0x00000003
	MB_TYPE_YESNO = 0x00000004
	MB_TYPE_RETRYCANCLE = 0x00000005
	MB_ICON_HAND = 0x00000010
	MB_ICON_QUESTION = 0x00000020
	MB_ICON_EXCLAMATION = 0x00000030
	MB_ANS_OK = 1
	MB_ANS_CANCLE = 2
	MB_ANS_ABORT = 3
	MB_ANS_RETRY = 4
	MB_ANS_IGNORE = 5
	MB_ANS_YES = 6
	MB_ANS_NO = 7

	class FileDialog:
		def __init__(self, mode=1, default_ext=None, init_filename=None, init_dir=None, flags=None, filter='All Files (*.*)|*.*'):
			self.dlg = None
			SelectedFlags = 0x00080000
			if flags is not None:
				SelectedFlags |= flags
				


			dlg = win32ui.CreateFileDialog(mode, default_ext, init_filename, SelectedFlags, filter)

			if init_dir is not None:
				dlg.SetOfInitialDir(init_dir)

			output = dlg.DoModal()
			if output == 1:
				self.dlg = dlg

		def get(self, multi=False):
			if self.dlg is not None:
				if multi:
					return self.dlg.GetPathNames()
				else:
					return self.dlg.GetPathName()

			else: 
				return False

	class MsgBox:
		def __init__(self, hwnd=0, text='Msg', title='MsgBox', type=0x00000000|0x00000040):
			self.res = win32api.MessageBox(hwnd, text, title, type)


		def get(self):
			return self.res


