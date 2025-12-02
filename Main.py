from Lib import *
import os
import threading as thr

#____Err____
class Err:
	class ProfileError(Exception):
		def __init__(self, msg='Invalid Profile Data'):
			super().__init__(msg)

#____wrappers____
def get_profile(name):
	data = Toml.File.load(f'Content/Profiles/{name}.toml')
	return data

def get_settings():
	data = Json.File.load('Content/settings.json')
	return data

#____Startup____
def startup_cam(indices, fps):
	CamConfig = AsyncCam.Camera.Config()
	CamConfig.SharedDict = {}
	CamConfig.FPS = 1/fps

	CamDict = {}
	for index in indices:
		CamDict[index] = AsyncCam.Camera.Async(index, CamConfig)
		CamDict[index].start()

	return CamDict, CamConfig

def startup_BlazePose():
	return Tracking.Pose()

def startup_profile(name):
	data = get_profile(name)
	return data

def startup_Map(name):
	JMap = Data.get_Joint_Map(name, Json)
	Map = Data.Map(JMap)
	return Map

class FBT_loop:
	def __init__(self, CamDict, CamCon, BlazePose, Map, profile, settings):
		self.CamDict = CamDict
		self.CamCon = CamCon
		self.Pose = BlazePose
		self.Map = Map
		self.profile = profile
		self.settings = settings

		self.running = True

		thr.Thread(target=self._loop_, daemon=True).start()

	def _loop_(self):
		if self.profile['tracking']['mode'].upper() == 'SINGLE':
			cam = self.CamDict[0]
			try:
				cam.retrive()
			except AsyncCam.AsyncCamError as e:
				print(e)
				self.running = False

			while(self.running):
				delta = 0
				with Clock.delta.precClock() as d:
					delta = d
					cam.retrive()

					img = cam._CC.SharedDict[str(cam._index)]

					tensor = self.Pose.preprocess(img)
					score, landmarks, heatmap = self.Pose.process(tensor)

					landmark_list = landmarks.squeeze(0).detach().cpu().tolist()

					self.Map.Update(landmark_list)

				Clock.sleep(1/self.settings['fps'], delta)


		elif self.profile['tracking']['mode'].upper() == 'MULTI':
			pass

		else:
			raise Err.ProfileError()



#____Shutdown____
def shutdown_cam(CamDict, CamConfig):
	CamConfig.Stop = True
	Clock.time.sleep(0.1)
	del CamDict
	del CamConfig

def shutdown_BlazePose(BlazePose):
	del BlazePose

#____CLI____
with open('Content/ASCII/Logo.txt', encoding='utf-8') as file:
	logo = file.read()

def custom_handler(ins):
	while(ins.running):
			print()
			msg = input(' >>> ')
			cmd = msg.split(' ')[0]
			try:
				if cmd in ins.cmd_dict:
					ins.cmd_dict[cmd](msg)

				else:
					ins.rich.print(f'[red]No Command: [#808080]"{msg}"')
			except Exception as e:
				ins.rich.print(f'[red]Error During Execution: [{type(e).__name__}] {e}')

CLIKit.CLIBaseClass.handler = custom_handler

class CLI(CLIKit.CLIBaseClass):
	def setup(self):
		self.name = 'VR-FBT'
		self.ver = '0.0.1'

		self.settings = get_settings()

		self.CurrentProfile = self.settings['default_profile']

		self.rich.print(f'[red]{logo}\n\n[green]Type "help" for help | [WIP]')

	def cmd_version(self, msg):
		"""Returns the current version."""
		self.rich.print(f'[yellow]{self.name}_{self.ver}')

	def cmd_reload(self, msg):
		"""Reloads the program."""
		os.system('cls')
		self.setup()
		self.rich.print('[yellow]Program Reloaded')

	def cmd_profile(self, msg):
		"""Selects a profile.
		profile <Profile-Name>"""
		_, name = msg.upper().split(' ')

		if os.path.exists(f'Content/Profiles/{name}.toml'):
			self.CurrentProfile = name
			self.rich.print(f'[green]Profile {name} Selected')
		else:
			self.rich.print(f'[red]No Profile {name}')

	def cmd_start(self, msg):
		"""Starts the full body tracking."""
		self.rich.print('[yellow]Full-Body-Tracking Startup...')
		profile_data = startup_profile(self.CurrentProfile)

		self.rich.print(f'[#808080]Running profile: {self.CurrentProfile}\nMode: {profile_data['tracking']['mode']}\nFPS: {self.settings['fps']}')

		CamDict, CamCon = startup_cam(profile_data['camera']['cam-index'], self.settings['fps'])
		BlazePose = startup_BlazePose()

		Map = startup_Map(profile_data['tracking']['joint-map'])

		Loop = FBT_loop(CamDict, CamCon, BlazePose, Map, profile_data, self.settings)

		Clock.time.sleep(0.2)
		if Loop.running:
			input('\nTo stop press "Enter"')
		else:
			self.rich.print('[red]\nFalied to start')

		self.rich.print('\n[yellow]Full-Body-Tracking Shutdown...')

		Loop.running = False
		Clock.time.sleep(0.1)

		del Loop

		shutdown_cam(CamDict, CamCon)
		shutdown_BlazePose(BlazePose)

		del profile_data


c = CLI()
while(c.running):
	Clock.time.sleep(1)