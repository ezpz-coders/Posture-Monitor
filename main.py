import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
import time
from tkinter import *
from sys import exit
from pynotifier import Notification

file = open('Output.txt', 'r')
for each in file:
    strictness , t1=map(float,each.split())

    

def popupError(s):
    popupRoot = Tk()
    popupRoot.after(2000, exit)
    popupButton = Button(popupRoot, text = s, font = ("Verdana", 12), bg = "yellow", command = exit)
    popupButton.pack()
    popupRoot.geometry('400x50+700+500')
    popupRoot.mainloop()

class Posture:
    def __init__(self):
        self.rshold = None
        self.lshold = None
        self.nose = None
        self.isCap = True


def checkPose(currPos,toComp):
    x1= currPos[0]
    x2=toComp[0]
    y1= currPos[1]
    y2=toComp[1]
    
    x = (x2 - x1)**2 
    y = (y2 - y1)**2
    
    dis = (x+y)**0.5
    
    return dis


stop = time.time() + t1


def mainCheck(nose,ls,rs,toComp):
   
        
    global stop
    global strictness
    ndist = checkPose(nose, toComp.nose)
    lsdist = checkPose(ls, toComp.lshold)
    rsdist = checkPose(rs, toComp.rshold)
    #print(ndist,lsdist,rsdist)
    print(time.time(),stop)
    currposture=None
    if ndist > 200/strictness or lsdist/strictness > 75 or rsdist/strictness > 75:
        currposture = "bad"
    elif ndist/strictness > 100 or lsdist/strictness > 50 or rsdist/strictness > 50:
        currposture = "alert"
        stop += 0.25
    else:
        currposture = "good"
        stop = time.time()+t1
        
    if stop > time.time()+t1:
        stop = time.time()+t1
        # print("exceed")
    
    print(currposture)
    
    if time.time() >= stop:
        print("BAD")
        Notification(
        	title='Check Your Posture',
        	description='It seems like you are sitting recklessly.',
        	icon_path='path/to/image/file/icon.png', # On Windows .ico is required, on Linux - .png
        	duration=2,                              # Duration in seconds
        	urgency='normal'
        ).send()
        stop = time.time() + t1
    
    
    




def webWin():
  
    cap = cv2.VideoCapture(0)
    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
        
      cposture = Posture()
      while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue
    
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = holistic.process(image)
        image_height, image_width, _ = image.shape
    
        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        '''
        mp_drawing.draw_landmarks(
            image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        '''
      
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        cv2.imshow('MediaPipe Holistic', image)
        #print("LEFT SHOULDER","RIGHT SHOULDER","NOSE")
        if results.pose_landmarks:
            cnose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width,results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_width
            
            crshold = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * image_width,results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_width
            
            clshold = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_width
            
            #print(clshold,crshold,cnose)
       
        
        key = cv2.waitKey(1)
        #print(cposture.lshold,cposture.rshold,cposture.nose)
        if key == ord('c') and cposture.isCap:
            cposture.isCap = False
            cposture.rshold = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * image_width,results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * image_width
            cposture.lshold = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * image_width
            cposture.nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width,results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_width
        
        try:
            
            mainCheck(cnose,clshold,crshold,cposture)
            
        except:
            pass
        
        if key == ord('q'):
             break
         
        if key == ord('p'):
            cv2.waitKey(-1)
        
    cap.release()
    
webWin()