from numba import njit
from numba.typed import List
import math 

#____Obj____
class keypoint:
	def __init__(self, pos, vis):
		self.pos = List(pos)
		self.vis = vis

		self.his = List()

	def append_history(self):
		self.his.append(self.pos)

#____wrappers____
def get_Joint_Map(name, Json_lib):
	return Json_lib.File.load(f'Content/Joint-Maps/{name}.json')

#____Optimized-Math____
@njit
def midpoint(p1, p2):
	mid = List()
	mid.append((p1.pos[0]+p2.pos[0])/2)
	mid.append((p1.pos[1]+p2.pos[1])/2)
	mid.append((p1.pos[2]+p2.pos[2])/2)
	return mid

@njit
def legendre_lowpass_o2(x, cutoff, fs):
	omega = math.tan(math.pi * cutoff / fs)
	c = omega**2

	norm = 1 + 1.618*omega + c
	a0 = c / norm
	a1 = 2*c / norm
	b1 = 2*(c-1) / norm
	b2 = (1 - 1.618*omega + c) / norm

	out = List([0.0]*len(x))
	for i in range(len(x)):
		if i == 0:
			out[i] = a0*x[i]
		elif i == 1:
			out[i] = a0*x[i] + a1*x[i-1] - b1*out[i-1]
		else:
			out[i] = (a0*x[i] + a1*x[i-1] - a0*x[i-2] - b1*out[i-1] - b2*out[i-2])

@njit
def legendre_highpass_o2(x, cutoff, fs):
	omega = math.tan(math.pi * cutoff / fs)
	c = omega**2

	norm = 1 + 1.618*omega + c
	a0 = 1 / norm
	a1 = -2 / norm
	b1 = 2*(c-1) / norm
	b2 = (1 - 1.618*omega + c) / norm

	out = List([0.0]*len(x))
	for i in range(len(x)):
		if i == 0:
			out[i] = a0*x[i]
		elif i == 1:
			out[i] = a0*x[i] + a1*x[i-1] - b1*out[i-1]
		else:
			out[i] = (a0*x[i] + a1*x[i-1] - a0*x[i-2] - b1*out[i-1] - b2*out[i-2])