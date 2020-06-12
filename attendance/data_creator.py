import pickle
import cv2
import os
import numpy as np
import imutils
from imutils import paths
            
def create_dataset(name,image):

    # embedding_path = os.getcwd() + os.path.sep + "output/empty_embeddings_dataset.pickle"
    embedding_path = os.getcwd() + os.path.sep + '/attendance/output/embeddings_dataset.pickle'
    data = pickle.loads(open(embedding_path, "rb").read())

    detector_path = os.getcwd() + os.path.sep + "attendance/face_detection_model"
    protoPath = detector_path + os.path.sep + 'deploy.prototxt'
    modelPath = detector_path + os.path.sep + 'res10_300x300_ssd_iter_140000.caffemodel'
    detector = cv2.dnn.readNetFromCaffe(protoPath,modelPath)

    embedder_path = os.getcwd() + os.path.sep + "attendance/openface_nn4.small2.v1.t7"
    embedder = cv2.dnn.readNetFromTorch(embedder_path)

    image = imutils.resize(image,width=600)
    (h,w) = image.shape[:2]
    
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
            data['names'].append(name)
            data['embeddings'].append(vec.flatten())

    file = open(embedding_path, "wb")
    file.write(pickle.dumps(data))
    file.close()