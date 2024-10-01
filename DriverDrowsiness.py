import cv2 as cv
import mediapipe as mp
import time
from scipy.spatial import distance as dis
import numpy as np



cap=cv.VideoCapture(0)

mpface=mp.solutions.face_mesh
face=mpface.FaceMesh()
mpdraw=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles


ptime=0
frame_count=0
min_frame=20
min_tolerance=5.0


while True:
    istrue,frame= cap.read()

    rgb=cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    results=face.process(rgb)
    lmlist=[]
    face_2d=[]
    face_3d=[]
    if results.multi_face_landmarks:
        for facelm in results.multi_face_landmarks:
            #mpdraw.draw_landmarks(frame,facelm,mpface.FACEMESH_CONTOURS)
            for id,lm in enumerate(facelm.landmark):
                h,w,_=frame.shape
                x,y=int(lm.x*w),int(lm.y*h)
                lmlist.append([id,x,y])

                if id==33 or id==263 or id==1 or id==61 or id==291 or id==199:
                    if id==1:
                        nose_2d=(lm.x*w,lm.y*h)
                        nose_3d=(lm.x*w,lm.y*h,lm.z*3000)

                x,y=int(lm.x*w),int(lm.y*h)

                face_2d.append([x,y])
                face_3d.append([x,y,lm.z])

            face_2d=np.array(face_2d,dtype=np.float64)

            face_3d=np.array(face_3d,dtype=np.float64)

            focal_length=1*w

            cam_matrix=np.array([[focal_length,0,h/2],[0,focal_length,w/2],[0,0,1]])

            dist_matrix=np.zeros((4,1),dtype=np.float64)

            success,rot_vec,trans_vec=cv.solvePnP(face_3d,face_2d,cam_matrix,dist_matrix)

            rmat,jac=cv.Rodrigues(rot_vec)

            angles,mtxR,mtxQ,Qx,Qy,Qz=cv.RQDecomp3x3(rmat)

            x=angles[0]*360
            y=angles[1]*360
            z=angles[2]*360
            
            
            
            if x<-10:
                downcount+=1
                
            elif x>10:
                upcount+=1
            else:
                upcount=0
                downcount=0

            nose_3d_projection,jacobian=cv.projectPoints(nose_3d,rot_vec,trans_vec,cam_matrix,dist_matrix)

            if (upcount!=0 and upcount<150) or (downcount!=0 and downcount<150):
                cv.putText(frame,"Driver Distracted",(20,50),cv.FONT_HERSHEY_COMPLEX,1.0,(0,0,255),2)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    if len(lmlist)!=0:

        h,w,_=frame.shape

        #lefteye
        x1,y1=int(lmlist[159][1]*w),int(lmlist[159][2]*h)
        x2,y2=int(lmlist[145][1]*w),int(lmlist[145][2]*h)
        
        x5,y5=int(lmlist[133][1]*w),int(lmlist[133][2]*h)
        x6,y6=int(lmlist[33][1]*w),int(lmlist[33][2]*h)

        ldistancet2b=dis.euclidean((x1,y1),(x2,y2))
        ldistancel2r=dis.euclidean((x5,y5),(x6,y6))

        ratiolefteye=ldistancel2r/ldistancet2b
        
        #right eye
        x7,y7=int(lmlist[386][1]*w),int(lmlist[386][2]*h)
        x8,y8=int(lmlist[374][1]*w),int(lmlist[374][2]*h)
        
        x9,y9=int(lmlist[263][1]*w),int(lmlist[263][2]*h)
        x10,y10=int(lmlist[362][1]*w),int(lmlist[362][2]*h)

        rdistancet2b=dis.euclidean((x7,y7),(x8,y8))
    
        rdistancel2r=dis.euclidean((x9,y9),(x10,y10))

        ratiorighteye=rdistancel2r/rdistancet2b
        
        #lips
        x11,y11=int(lmlist[13][1]*w),int(lmlist[13][2]*h)
        x12,y12=int(lmlist[14][1]*w),int(lmlist[14][2]*h)
        x13,y13=int(lmlist[78][1]*w),int(lmlist[78][2]*h)
        x14,y14=int(lmlist[308][1]*w),int(lmlist[308][2]*h)


        lipdistancet2b=dis.euclidean((x11,y11),(x12,y12))
        lipdistancel2r=dis.euclidean((x13,y13),(x14,y14))

        ratiolips=lipdistancel2r/lipdistancet2b

        ratio=(ratiolefteye+ratiorighteye)/2

        if ratio>min_tolerance:
            frame_count+=1
        else:
            frame_count=0

        if frame_count>min_frame or downcount>150:

            cv.putText(frame,"Driver Sleepy",(40,80),cv.FONT_HERSHEY_COMPLEX,1.0,(0,0,255),3)

        if ratiolips<3:
            cv.putText(frame,"Driver Yawning",(70,110),cv.FONT_HERSHEY_COMPLEX,1.0,(0,0,255),3)

    cv.putText(frame,str(int(fps)),(20,70),cv.FONT_HERSHEY_PLAIN,1.0,(255,0,0),1)
    cv.imshow("video",frame)

    if cv.waitKey(1) & 0xFF==27:
        break
cap.release()
cv.destroyAllWindows()