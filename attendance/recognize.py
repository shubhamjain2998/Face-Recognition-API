# import the necessary packages
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
	print("path = ",recognizer_path)
	# recognizer_path = os.getcwd() + os.path.sep + "output/XGBClassifier.pickle"
	# recognizer_path = "/home/jatin/Documents/AAA Govt Project/Face-Recognition-API/attendance/output/XGBClassifier.pickle"
	label_encoder = os.path.dirname(os.path.abspath(__file__)) + "/" + "output" + "/" + "le.pickle"

	print(recognizer_path)
	print(label_encoder)
	print("[INFO] loading face detector...")
	protoPath = os.path.sep.join([detector, "deploy.prototxt"])
	print("loaded protopath")
	modelPath = os.path.sep.join([detector,
		"res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
	print(detector)

	# load our serialized face embedding model from disk
	# print("[INFO] loading face recognizer...")
	embedder = cv2.dnn.readNetFromTorch(embeddingModel)
	print("loaded embedding model")
	
	# load the actual face recognition model along with the label encoder
	# print(pickle.loads(open(recognizer_path, "rb").read()))
	
	recognizer = pickle.loads(open(recognizer_path, "rb").read())
	print(recognizer)
	le = pickle.loads(open(label_encoder, "rb").read())
	print(le)


	# load the image, resize it to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image dimensions
	print("image le rahe hain")
	image = image_to_predict
	print(image.shape)
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

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections
		if confidence > 0.8:
			# compute the (x, y)-coordinates of the bounding box for the
			# face
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
			print("yeh vector hai :",vec)

			# perform classification to recognize the face
			preds = recognizer.predict_proba(vec)[0]
			print(preds)
			j = np.argmax(preds)
			print("j =",j)
			proba = preds[j]
			print(proba)
			name = le.classes_[j]

			print(name)

			# # draw the bounding box of the face along with the associated
			# # probability
			# text = "{}: {:.2f}%".format(name, proba * 100)
			# y = startY - 10 if startY - 10 > 10 else startY + 10
			# cv2.rectangle(image, (startX, startY), (endX, endY),
			# 	(0, 0, 255), 2)
			# cv2.putText(image, text, (startX, y),
			# 	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

			# cv2.imshow(image)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
			result = {"name": name, "accuracy":round(proba*100,2)}
			print(result)

	return result
