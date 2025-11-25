import threading as thr
import cv2
import time

class AsyncCamError(Exception):
	def __init__(self, msg='Unknown Camera Error'):
		super().__init__(msg)



class Camera:
	class Config:
		FPS = 1/30

		SharedDict = None
		Lock = thr.Lock()

		Stop = False

	class Async:
		_RC = 0

		def __init__(self, index, CC):
			self._CC = CC
			self._index = index

			if self._CC.SharedDict is None:
				raise AsyncCamError(msg='SharedDict is None')

			self._thr = thr.Thread(target=self._loop_, daemon=True)

		def _loop_(self):
			while(1):
				try:
					if self._CC.Stop:
						break

					self.cap.grab()

					self._RC = 0

					time.sleep(self._CC.FPS)

				except cv2.error:
					self.cap = cv2.VideoCapture(self._index, cv2.CAP_DSHOW)
					self._RC += 1

					if self._RC > 3:
						raise AsyncCamError(f'Camera disconnected at index {self._index}')

		def start(self):
			self.cap = cv2.VideoCapture(self._index, cv2.CAP_DSHOW)
			self._thr.start()

		def retrive(self):
			with self._CC.Lock:
				_, frame = self.cap.retrieve()
				self._CC.SharedDict[str(self._index)] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


class Scale:
	@staticmethod
	def down(img, size):
		return cv2.resize(img, size, interpolation=cv2.INTER_AREA)

	@staticmethod
	def up(img, size):
		return cv2.resize(img, size, interpolation=cv2.INTER_LINEAR)