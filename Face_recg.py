import face_recognition as fr
import os
import cv2
import numpy as np
import pickle

def classify_face(img):
    faces = pickle.loads(open('9save','rb').read())

    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img,face_locations)
    face_names = []

    for face_encodings in unknown_face_encodings:
        matches = fr.compare_faces(faces["faces_encoded"],face_encodings)
        name = "Unknown"
        face_distances = fr.face_distance(faces["faces_encoded"],face_encodings)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = faces["known_face_names"][best_match_index]
        face_names.append(name)
        
        for (top,right,bottom,left),name in zip(face_locations,face_names):
            cv2.rectangle(img, (left-20, top -20),(right+20,bottom+20), (255,0,0),2)
            cv2.rectangle(img,(left-20,bottom-15),(right+20,bottom+20),(255,0,0),cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img,name,(left-20,bottom+15),font,1.0, (255,255,255),2)
    return img,face_names

cap = cv2.VideoCapture(0) 
while True: 
        ret,img = cap.read()
        img,face_names=classify_face(img)
        cv2.imshow('Face_Recognition',img)
        print(face_names)
        if cv2.waitKey(1) & 0xFF == ord('p'):
           break
cap.release()    
cv2.destroyAllWindows()
