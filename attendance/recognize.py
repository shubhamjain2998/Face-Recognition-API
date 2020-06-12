import numpy as np
import imutils
import pickle
import cv2
import os
from xgboost import XGBClassifier

def predict_face(image_to_predict):
	detector = os.path.dirname(os.path.abspath(__file__)) + "/" + "face_detection_model"
	embeddingModel = os.path.dirname(os.path.abspath(__file__)) + "/" + "openface_nn4.small2.v1.t7"
	recognizer_path = os.path.dirname(os.path.abspath(__file__)) + "/" + "output" + "/" + "XGBClassifier.pickle"
	# recognizer_path = os.getcwd() + os.path.sep + "output/XGBClassifier.pickle"
	# recognizer_path = "/home/jatin/Documents/AAA Govt Project/Face-Recognition-API/attendance/output/XGBClassifier.pickle"
	label_encoder = os.path.dirname(os.path.abspath(__file__)) + "/" + "output" + "/" + "le.pickle"
	
	protoPath = os.path.sep.join([detector, "deploy.prototxt"])
	modelPath = os.path.sep.join([detector,
		"res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

	# load our serialized face embedding model from disk
	embedder = cv2.dnn.readNetFromTorch(embeddingModel)
	
	# load the actual face recognition model along with the label encoder
	
	recognizer = pickle.loads(open(recognizer_path, "rb").read())
	le = pickle.loads(open(label_encoder, "rb").read())


	# load the image, resize it to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image dimensions
	image = image_to_predict
	image = imutils.resize(image, width=600)
	(h, w) = image.shape[:2]

	# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(image, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)

	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
	detector.setInput(imageBlob)
	detections = detector.forward()
	
	result = {}
	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]

		# print("confidence : ", confidence)
		# filter out weak detections
		if confidence > 0.8:
			# compute the (x, y)-coordinates of the bounding box for the
			# face
			flag = 1
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# extract the face ROI
			face = image[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]

			# ensure the face width and height are sufficiently large
			if fW < 20 or fH < 20:
				continue

			# construct a blob for the face ROI, then pass the blob
			# through our face embedding model to obtain the 128-d
			# quantification of the face
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
				(0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()
			# print("yeh vector hai :",vec)

			# perform classification to recognize the face
			preds = recognizer.predict_proba(vec)[0]
			# print(preds)
			j = np.argmax(preds)
			proba = preds[j]
			name = le.classes_[j]

			result = {"name": name, "accuracy":round(proba*100,2), "error" : ""}
			break
		
		else:
			flag=0
			continue
	if flag==0:
		result = {"name": "", "accuracy": "", "error" : "No faces were found !!!"}
	return result