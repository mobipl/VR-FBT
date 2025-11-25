from pythonosc.udp_client import SimpleUDPClient

class Const:
	BasePath = '/tracking/trackers/'

	class Type:
		Position = 'position'
		Rotation = 'rotation'

class Pharse:
	@staticmethod
	def list(OSCList):
		return ( OSCList[0]+OSCList[1]+'/'+OSCList[2], OSCList[3] )

	@staticmethod
	def dict(OSCDict):
		return (OSCDict['BasePath']+OSCDict['TrackerID']+'/'+OSCDict['Type'], OSCDict['Data'])

	@staticmethod
	def str(OSCStr): # '{BasePath}{TrackerID}/{Type}|{Data}'
		msg = OSCStr.split('|')
		return (msg[0], eval(msg[1]))

	@staticmethod
	def direct(BasePath, TrackerID, Type, Data):
		return (BasePath+TrackerID+'/'+Type, Data)

	@staticmethod
	def debug(Name, Data):
		return ('Debug/'+Name, Data)

class Server:
	def __init__(self, ip, port=9000):
		self.client = SimpleUDPClient(ip, port)

	def Send(self, msg):
		self.client.send_message(msg[0], msg[1])



