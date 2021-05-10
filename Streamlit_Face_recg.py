import face_recognition as fr
import os
import cv2
import numpy as np
import pickle
import streamlit as st 
import datetime
import csv

def authenticate():

 def classify_face(img):
    faces = pickle.loads(open('9save','rb').read())

    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img,face_locations)
    face_names = []
    date_time_list=[]

    for face_encodings in unknown_face_encodings:
        matches = fr.compare_faces(faces["faces_encoded"],face_encodings)
        name = "Unknown"
        face_distances = fr.face_distance(faces["faces_encoded"],face_encodings)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = faces["known_face_names"][best_match_index]
        face_names.append(name)

        now=datetime.datetime.now()
        dtString=now.strftime('%A,%d %B %Y (IST)  %H:%M:%S')
        date_time_list.append(dtString)

        
        
        for (top,right,bottom,left),name in zip(face_locations,face_names):
            cv2.rectangle(img, (left-20, top -20),(right+20,bottom+20), (255,0,0),2)
            cv2.rectangle(img,(left-20,bottom-15),(right+20,bottom+20),(255,0,0),cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img,name,(left-20,bottom+15),font,1.0, (255,255,255),2)
    return img,face_names,date_time_list

 def csvdata(x,y):
    rows=[[x,y]]
    f=open('Employee_Details.csv','a')
    with f:
        csvwriter=csv.writer(f)
        csvwriter.writerows(rows)

        
 cap = cv2.VideoCapture(0)
#1 for External Webcam
 while True: 
        ret,img = cap.read()
        img,face_names,date_time_list=classify_face(img)
        cv2.imshow('Face_Recognition',img)
        if face_names!=[]:
          for i in face_names:
             if i=="Unknown":
               print(i)
               print(date_time_list)
               st.text(i)
               st.text(date_time_list)
               csvdata(i,date_time_list)
             else:
               print("{} You are Authorized Person to Enter".format(i))
               print(date_time_list)
               st.text(i+" You are Authorized Person to Enter")
               st.text(date_time_list)
               csvdata(i,date_time_list)
        if cv2.waitKey(1) & 0xFF == ord('p'):
           break
 cap.release()    
 cv2.destroyAllWindows()

 
def main():
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Employee Authentication WebApp</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    st.text("\n")
    col1, col2, col3,col4,col5 = st.beta_columns(5)
    if col3.button("start"):
        st.text("Results")
        authenticate()
        
if __name__=='__main__':
    main()
