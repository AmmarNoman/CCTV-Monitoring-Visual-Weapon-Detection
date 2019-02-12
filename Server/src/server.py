#TODO

from threading import Thread
from collections import deque
import socket as s
import tensorflow as tf
import cv2
import numpy as np
import _pickle as pickle
import sys
import zmq
import base64 as b64
import tensorflow as tf

class Receiver(Thread):
	def __init__(self, addr):
		Thread.__init__(self)

		context = zmq.Context()
		self.socket = context.socket(zmq.REP)
		self.socket.bind(addr)

		print("Listening on", addr)

	def run(self):
		model = tf.keras.models.load_model("../../Models/model-current.h5")
		model.summary()

		while True:
			received = self.socket.recv_string()
			jpegStr = b64.b64decode(received)
			jpeg = np.fromstring(jpegStr, dtype=np.uint8)
			frame = cv2.imdecode(jpeg, 1)

			frame = cv2.resize(frame, (100,100)) #work it so it can use process size of (256, 144)
			frameArr = np.asarray(frame)
			frameArr = np.expand_dims(frameArr, axis=0)
			result = str(model.predict(frameArr)[0][0])

			#encoded = b64.b64encode(result)
			self.socket.send_string(result)



if __name__ == '__main__':
	responseQueues = {}
	receiver = Receiver('tcp://0.0.0.0:5000')
	receiver.start()