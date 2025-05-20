from ultralytics import YOLO
from pyniryo import *
from shared import SharedData
import numpy as np
import time
import cv2
import os
import json

import distance

def vision(ned2, share):
    MODEL_PATH = os.path.join('..','runs','detect','yoloworld-v1','weights','last.pt')
    # MODEL_PATH = os.path.join('..','runs','detect','orientationv2','weights','last.pt')
    model = YOLO(MODEL_PATH)

    colors = [(255,0,0),(0,0,255),(0, 155, 255),(255,0,255)]
    HEIGHT = 480
    WIDTH = 640

    MID_X = WIDTH//2
    MID_Y = HEIGHT//2
    

    
    coords = {"xm":0,"ym":0,"update":0}
    data = {}


    mtx,dist = ned2.get_camera_intrinsics()

    while True:
        try:

            if share.getUpdate() == 1:
                continue

            compressed_image = ned2.get_img_compressed()

            image = cv2.imdecode(np.frombuffer(compressed_image, np.uint8), cv2.IMREAD_COLOR)
            image = undistort_image(image,mtx,dist)
        

            results = model(image)[0]

            if results != None:
                xm,ym = distance.find_shortest(results.boxes.data.tolist(),share)

                
                
                cv2.line(image,(MID_X,MID_Y), (int(xm),int(ym)),(0,0,0),3)

                coords = {"xm":xm,"ym":ym,"update":1}

                # coords['xm'] = xm
                # coords['ym'] = ym
                # coords['update'] = 1

                

                for result in results.boxes.data.tolist():  
                    x1, y1, x2, y2, score, classid = result  
                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), colors[0], 1)

                    label = results.names[int(classid)].upper()  # Get class name
                    score = int(score*100)
                    cv2.putText(image, '{lab} {score}'.format(lab = label, score = classid), (int(x1), int(y1 - 5)), cv2.FONT_HERSHEY_PLAIN, 0.75, colors[0], 1, cv2.LINE_AA)
                    cv2.putText(image, '{xm},{ym}'.format(xm = (int((x1+x2))/2), ym = (int((y1+y2))/2)), (int(x1-10), int(y2 + 5)), cv2.FONT_HERSHEY_PLAIN, 0.75, colors[0], 1, cv2.LINE_AA)
                    

                    if share.getUpdate() == 0:
                        share.dump(coords)
                        share.setDist(distance.dist_from_center(xm,ym))

                        share.setX1(x1)
                        share.setX2(x2)
                        
                        share.setY1(y1)
                        share.setY2(y2)

                        print(share.getDist())
                        share.setUpdate(1)


        except Exception as e:
            print(e)
            continue
            



        cv2.imshow("img",image)
        if cv2.waitKey(1) == ord('q'):
            break

    # closing all open windows
    cv2.destroyAllWindows()