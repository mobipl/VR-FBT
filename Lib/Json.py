import json

class File:
	@staticmethod
	def load(path):
		with open(path, 'r') as file:
			out = json.load(file)
		return out

	@staticmethod	
	def save(path, data, indent=4):
		with open(path, 'w') as file:
			json.dump(data, file, indent=indent)

class String:
	@staticmethod
	def load(Str):
		return json.loads(Str)

	@staticmethod
	def toStr(data, indent=2):
		return json.dumps(data, indent=indent)