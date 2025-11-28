import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

print('Loading Tensorflow...')

import tensorflow as tf
import cv2

os.system('cls')

def check_GPU():
	return tf.config.list_physical_devices('GPU')

class BlazePose:
	def __init__(self):
		if not os.path.exists('Model/blazepose'):
			import tensorflow_hub as hub
			#Fuck This BS
			tf.saved_model.save(self.model, 'Model/blazepose')
			del hub

		else:
			self.model = tf.saved_model.load('Model/blazepose')

	def preprocess(self, img):
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		in_tensor = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 256,256)
		in_tensor = tf.cast(in_tensor, dtype=tf.float32)
		return in_tensor

	def process(self, in_tensor):
		return self.model(in_tensor)['output_0'].numpy()
