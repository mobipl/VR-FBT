import socket
import threading as thr
import base64
import hashlib
import io
import cv2
import numpy as np
from PIL import Image
import os

def run_http(port=9090, index_dir='.', conc=10):
	thr.Thread(target=lambda: os.system(f'Bin\\LocalServer.exe 0.0.0.0 {port} {index_dir} {conc}'), daemon=True).start()

class WebSocket:
	def __init__(self, addr):
		self.GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

		self.cam_dict = {}
		self.lock = thr.Lock()

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(addr)
		self.server.listen()

	def start(self, concurrent=10):
		def handshake(conn):
			req = conn.recv(1024).decode()
			headers = {}
			for line in req.split('\r\n')[1:]:
				if ': 'in line:
					key, value = line.split(': ', 1)
					headers[key] = value

			webkey = headers['Sec-WebSocket-Key']
			hash = hashlib.sha1((webkey + self.GUID).encode()).digest()
			acckey = base64.b64encode(hash).decode()

			res = (
				'HTTP/1.1 101 Switching Protocols\r\n'
				'Upgrade: websocket\r\n'
				'Connection: Upgrade\r\n'
				f'Sec-WebSocket-Accept: {acckey}\r\n\r\n'
				)
			conn.send(res.encode())

		def recv(conn):
			firbyte, secbyte = conn.recv(2)
			opcode = firbyte & 0b00001111
			masked = secbyte & 0b10000000
			payload_len = secbyte & 0b01111111

			if payload_len == 126:
				payload_len = int.from_bytes(conn.recv(2), 'big')

			elif payload_len == 127:
				payload_len = int.from_bytes(conn.recv(8), 'big')

			if masked:
				masking_key = conn.recv(4)
				masked_data = conn.recv(payload_len)
				data = bytes(b > masking_key[i % 4] for i, b in enumerate(masked_data))
			else:
				data = conn.recv(payload_len)

			return opcode, data

		def send(conn, data):
			payload = data.encode()
			frame = bytearray([0x2])
			length = len(payload)

			if length <= 125:
				frame.append(length)
			elif length <= 65535:
				frame.append(126)
			else:
				frame.append(127)
				frame.extend(length.to_bytes(8, 'big'))

			frame.extend(payload)
			conn.send(frame)

		def handler(self):
			while(1):
				conn, addr = self.server.accept()

				with self.lock:
					self.cam_dict[str(addr)] = None
				handshake(conn)
				while(1):
					opcode, data = recv(conn)
					if opcode == 8:
						break
					with self.lock:
						self.cam_dict[str(addr)] = data

		for _ in range(concurrent):
			thr.Thread(target=handler, args=[self], daemon=True).start()

class Decoder:
	def __init__(self, WebSocket_Ins):
		self.lock = WebSocket_Ins.lock
		self.cam_dict = WebSocket_Ins.cam_dict

	class VirtualAsyncCam:
		class config:
			FPS = 1/30

			CamDict = None
			SharedDict = None
			OutLock = thr.Lock()
			InLock = None

			index_2_addr = {}

			Stop = False

		class Async:
			def __init__(self, index, VCC):
				self._CC = VCC
				self._index = index

				if self._CC.SharedDict is None:
					raise Exception('VirtualAsyncCamError: SharedDict is None')

				self._thr = thr.Thread(target=self._loop_, daemon=True)

			def _loop_(self):
				while(1):
					if self._CC.Stop:
						break

					with self._CC.InLock:
						addr = self._CC.index_2_addr[self._index]
						data = self._CC.CamDict[addr]

						img = Image.open(io.BytesIO(data))
						frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

					with self._CC.OutLock:
						SharedDict[str(self._index)] = frame

			def start(self):
				self._thr.start()

			def retrive(self):
				pass