from Lib import *

#____wrappers____
def get_profile(name):
	data = Toml.File.load(f'Content/Profiles/{name}.toml')
	return data

def get_settings():
	data = Json.File.load('Content/settings.json')
	return data


#____CLI____
with open('Content/ASCII/Logo.txt', encoding='utf-8') as file:
	logo = file.read()

def custom_handler(ins):
	while(ins.running):
			msg = input(' >>> ')
			cmd = msg.split(' ')[0]
			try:
				if cmd in ins.cmd_dict:
					ins.cmd_dict[msg](msg)

				else:
					ins.rich.print(f'[red]No Command: [#808080]"{msg}"')
			except Exception as e:
				ins.rich.print(f'[red]Error During Execution: [{type(e).__name__}] {e}')

CLIKit.CLIBaseClass.handler = custom_handler

class CLI(CLIKit.CLIBaseClass):
	def setup(self):
		self.name = 'VR-FBT'
		self.ver = '0.0.1'

		self.rich.print(f'[red]{logo}\n\n[green]Type "help" for help | WIP')

	def cmd_version(self, msg):
		"""Returns the current version."""
		self.rich.print(f'[yellow]{self.name}_{self.ver}')


c = CLI()
while(c.running):
	Clock.time.sleep(1)