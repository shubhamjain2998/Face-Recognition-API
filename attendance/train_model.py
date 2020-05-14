from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import pickle
import cv2
import os
import numpy as np
import imutils
from imutils import paths

embedding_path = os.getcwd() + os.path.sep + "output/embeddings_dataset.pickle"
# recognizer_path = os.getcwd() + os.path.sep + "output/recognizer.pickle"
# recognizer_path = os.getcwd() + os.path.sep + "output/RFC/lassifier.pickle"
recognizer_path = os.getcwd() + os.path.sep + "output/XGBClassifier.pickle"
le_path = os.getcwd() + os.path.sep + "output/le.pickle"

# load the face embeddings
print("[INFO] loading face embeddings...")
data = pickle.loads(open(embedding_path, "rb").read())
print(data["names"][0])

# encode the labels
print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] training model...")
# recognizer = SVC(C=1.0, kernel="linear", probability=True)
# recognizer = RandomForestClassifier()
recognizer = XGBClassifier()
recognizer.fit(np.array(data["embeddings"]), labels)

# write the actual face recognition model to disk
f = open(recognizer_path, "wb")
f.write(pickle.dumps(recognizer))
f.close()

# write the label encoder to disk
f = open(le_path, "wb")
f.write(pickle.dumps(le))
f.close()