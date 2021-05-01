import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import pickle

def get_encoded_faces():
    encoded = {}
    for dirpath, dnames, fnames in os.walk("./dataset"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png")  or f.endswith(".jpeg"):
                face = fr.load_image_file("dataset/"+f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    return encoded
faces=get_encoded_faces()
faces_encoded = list(faces.values())
known_face_names = list(faces.keys())
enco={"faces_encoded":faces_encoded,"known_face_names":known_face_names}

f=open('9save',"wb")
f.write(pickle.dumps(enco))
f.close()

#uncomment and run this only for the first time for creating csv file with 2 fields(name and date)
"""import csv
fields=['Name','Date and Time']
f=open('Employee_Details.csv','w')
with f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(fields)"""
