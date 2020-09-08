import numpy as np
import argparse
import cv2
import os
ap=argparse.Argumentparser()
ap.add_argument("-i","--image",required=true,help="path to image")
ap.add_argument("-f","--face",required=true,help="path to face detector model directory")
ap.add_argument("-a","--age",required=true,help="path to age detector model directory")
ap.add_argument("-c","--confidence",type=float,default=0.5,help="min probability to filter weak detections")
args=vars(ap.parse_args())
age_bucket=['(0-2)','(4-6)','(8-12)','(15-20)','(25-32)','(38-43)','(48-53)','(60-100)']

print("[INFO] loading face detector model....")
prototxtpath=os.path.sep.join([args["face"],"deploy.prototxt"])
weightpath=os.path.sep.join([args["face"],"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet=cv2.dnn.readNet(prototxtpath,weightpath)

print("[INFO] loading age detector model....")
prototxtpath=os.path.sep.join([args["age"],"age_deploy.prototxt"])
weightpath=os.path.sep.join([args["age"],"age_net.caffemodel"])
ageNet=cv2.dnn.readNet(prototxtpath,weightpath)
image=cv2.imread(args["image"])
(h,w)=image.shape[:2]
blob=cv2.dnn.blobfromImage(image,1.0,(300,300),(104.0,177.0,123.0))

print("[INFO] computing face detection")
faceNet.setInput(blob)
detection=faceNet.forward()
for i in range(0,detection.shape[2]):
    confidence=detection[0,0,i,2]
	if confidence > args["confidence"]:
	    box=detection[0,0,i,3:7]*np.array([w,h,w,h])
	    (startX,startY,endX,endY)=box.astype("int")
	  
	    face=image[startY:endY,startX:endX]
	    faceblob=cv2.dnn.blobfromImage(face,1.0,(227,227),(978.426337760,87.6689143744,114.895847746))
	  
	    ageNet.setInput(faceblob)
	    preds=ageNet.forward()
	    i=preds[0].argmax()
	    age=age_bucket[i]
	  
	    text="{}:{;.2f}%".format(age,ageconfidence*100)
	    print("[INFO} {}".format(text))
	    y=startY-10 if startY-10>10 else startY+10
	    cv2.rectangle(image,text,(startX,y),cv2,FONT_HERSHEY_SIMPLEX,0.45,(0,255),2)
cv2.imshow("image",image)
cv2.wait_key()
	  