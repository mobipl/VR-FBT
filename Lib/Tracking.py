#Fuck Tensorflow and its outdated converters
import os

print('Loading PyTorch')

import torch
import torchvision.transforms as T
from Model.blazepose_landmark import BlazePoseLandmark

os.system('cls')

class Pose:
	def __init__(self):
		self.model = BlazePoseLandmark()
		det_checkpoint = torch.load('Model/blazepose_landmark.pth')
		self.model.load_state_dict(det_checkpoint)
		self.model.eval()

	def preprocess(self, img):
		transform = T.Compose([T.ToTensor(), T.Resize((256,256)), T.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])])

		return transform(img).insqueeze(0)

	def process(self, tensor):
		with torch.no_grad():
			landmarks = model(tensor)
			print(landmarks)

		return landmarks