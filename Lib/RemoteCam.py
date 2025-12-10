import socket
import threading as thr

class server:
	HTTP_Mimick = None
	WS_Mimick = None

	index = '<html><body><p>test</p></body></html>'
	add = None


	def __init__(self, port=9080):
		self.addr = ('localhost',port)

		self.running = True

		if self.HTTP_Mimick is None:
			self.HTTP_Mimick = self.Basic_HTTP_Mimick

		# if self.WS_Mimick is None:
		# 	self.WS_Mimick = self.Basic_WS_Mimick

		self.HTTP_Mimick()

	def Basic_HTTP_Mimick(self, concurrent=5):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind(self.addr)
		server.listen()

		def Handler(self, server):
			while(1):
				conn, addr = server.accept()

				req = conn.recv(1024).decode()
				
				print(req)

				req_line = req.splitlines()[0]
				method, _, _ = req_line.split()

				headers = {}
				for line in req.splitlines()[1:]:
					if line.strip() == "":
						break
					if ":" in line:
						key, value = line.split(':', 1)
						headers[key.strip()] = value.strip()

				if not 'Referer' in headers:
					headers['Referer'] = ''

				match headers['Referer'].split('/')[-1]:
					case '':
						res_body = self.index
					case 'add':
						res_body = self.add

					case _:
						res_body = '<p>404</p>'

				res_header = (
						'HTTP/1.1 200 OK\r\n'
						f'Content-Length: {len(res_body)}\r\n'
						'Content-Type: text/html\r\n'
						'\r\n'
					)


				res = res_header + res_body

				conn.sendall(res.encode())
				conn.close()

		for _ in range(concurrent):
			thr.Thread(target=Handler, args=[self, server], daemon=True).start()