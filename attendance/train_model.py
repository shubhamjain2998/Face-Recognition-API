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
            
def create_dataset(id,image):
    embedding_path = os.getcwd() + os.path.sep + "output/embeddings_dataset.pickle"
    data = pickle.loads(open(embedding_path, "rb").read())
    # recognizer_path = os.getcwd() + os.path.sep + "output/recognizer.pickle"
    # recognizer_path = os.getcwd() + os.path.sep + "output/RFC/lassifier.pickle"
    # recognizer_path = os.getcwd() + os.path.sep + "output/XGBClassifier.pickle"
    # le_path = os.getcwd() + os.path.sep + "output/le.pickle"

    # data = pickle.loads(open(embedding_path, "rb").read())
    # le = LabelEncoder()
    # labels = le.fit_transform(data["names"])

    detector_path = os.getcwd() + os.path.sep + "face_detection_model"
    protoPath = detector_path + os.path.sep + 'deploy.prototxt'
    modelPath = detector_path + os.path.sep + 'res10_300x300_ssd_iter_140000.caffemodel'
    detector = cv2.dnn.readNetFromCaffe(protoPath,modelPath)

    embedder_path = os.getcwd() + os.path.sep + "openface_nn4.small2.v1.t7"
    embedder = cv2.dnn.readNetFromTorch(embedder_path)

    image = imutils.resize(image,width=600)
    (h,w) = image.shape[:2]
    
    #construct a blob from the image
    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 
        1.0, 
        (300, 300),
        (104.0, 177.0, 123.0), 
        swapRB=False, 
        crop=False
    )

    detector.setInput(imageBlob)
    detections = detector.forward()

    if len(detections)>0:
        # we're making the assumption that each image has only ONE
        # face, so find the bounding box with the largest probability
        
        i = np.argmax(detections[0,0,:,2])
        confidence = detections[0,0,i,2]
        min_confidence = 0.5
    
        # ensure that the detection with the largest probability also
        # means our minimum probability test (thus helping filter out
        # weak detections)
        if confidence > min_confidence:
            
            # compute the (x, y)-coordinates of the bounding box for the face
            box = detections[0,0,i,3:7] * np.array([w,h,w,h])
            (startX,startY,endX,endY) = box.astype(int)
            
            # extract the face ROI and grab the ROI dimensions
            face = image[startY:endY, startX:endX]
            (fH,fW) = face.shape[:2]
                
            
            # construct a blob for the face ROI, then pass the blob
            # through our face embedding model to obtain the 128-d
            # quantification of the face
            faceBlob = cv2.dnn.blobFromImage(
                face, 
                1.0 / 255,
                (96, 96), 
                (0, 0, 0), 
                swapRB=True, 
                crop=False
            )
            embedder.setInput(faceBlob)
            vec = embedder.forward()
        
            # add the name of the person + corresponding face
            # embedding to their respective lists
            data['name'].append(id)
            data['embeddings'].append(vec.flatten())





def create_model():            
    embedding_path = os.getcwd() + os.path.sep + "attendance/output/embeddings_dataset.pickle"
    # recognizer_path = os.getcwd() + os.path.sep + "output/recognizer.pickle"
    # recognizer_path = os.getcwd() + os.path.sep + "output/RFC/lassifier.pickle"
    recognizer_path = os.getcwd() + os.path.sep + "attendance/output/XGBClassifier.pickle"
    le_path = os.getcwd() + os.path.sep + "attendance/output/le.pickle"

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