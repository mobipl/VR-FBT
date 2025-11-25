import toml

class File:
	@staticmethod
	def load(path):
		with open(path, 'r') as file:
			out = toml.load(file)
		return out

	@staticmethod	
	def save(path, data):
		with open(path, 'w') as file:
			toml.dump(data, file)

class String:
	@staticmethod
	def load(Str):
		return toml.loads(Str)

	@staticmethod
	def toStr(data):
		return toml.dumps(data)