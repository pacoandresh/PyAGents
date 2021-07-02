#!/usr/bin/env python3
# ____________developed by paco andres_26/11/2020___________________
import time
import sys

import PyAgent.libs.Cmake as CM
from PyAgent.libs.Sys import Agent_Sys
from PyAgent.libs.Server import Create_Agent, Create_Agent_From_Json

import cv2
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import imutils 
import queue


class UsbCamera(Agent_Sys):
    def __init__(self):
        self.Proto_Topics(Image="proto.Image_pb2::Image")
        self.String_Topics(y=1)
        
        self.width=640
        self.height=480
        self.framerate=24
        self.codec='H264'
        self.idcam=0
        self.video= VideoStream(src=self.idcam,resolution=(self.height,self.width),framerate=self.framerate).start()
        self.Image.Clear()
        self.Image.width=self.width
        self.Image.height=self.height
        self.Image.codec=self.codec
        self.Image.deep=3
        self.Q=queue.Queue()
        self.frame=[np.zeros((self.width,self.height)),np.zeros((self.width,self.height))]
        self.write=0
        self.send=1

    def Agent__Start(self):
        #here configures before start all
        self.Add_Workers(self.worker_read)
        time.sleep(0.2)
        self.Add_Workers(self.worker_send)
        
        
    def Agent__Close(self):
        # here if you want save anything before stop agent
        pass    

    def worker_read(self):
        while self._Agent_Worker_Run:
            frame = self.video.read()
            frame=imutils.resize(frame,height=self.height,width=self.width)
            self.Q.put(frame)
            time.sleep(self._Agent_Frec)
    
    def worker_send(self):
        while self._Agent_Worker_Run:
            if not self.Q.empty():
                frame=self.Q.get()
                #print(self.Q.qsize())
                shape=frame.shape
                #print(shape)
                self.Image.height=shape[0]
                self.Image.width=shape[1]
                self.Image.deep =shape[-1]
                #salida = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV)
                self.Image.image_data=np.ndarray.tobytes(frame)
                self.Image_send()
                self.y=self.y+1
                self.y_send()
            time.sleep(self._Agent_Frec)
            



if __name__ == "__main__":
    CM.Show_Errors()
    # si hay 3 parámetros en la llamada decodificamos y arrancamos. llamada externa
    if len(sys.argv)==3:
        Create_Agent_From_Json(Json=sys.argv[2],Environment=CM.Environment)
    else:    
        # sino llamada local de prueba.
        Agent=Create_Agent("Mybot/Camera",UsbCamera,CM.Environment,0.001,
                        Autostart=True,
                        Loop=True,
                        Interfaces=[],
                        Config={"width":800,"height":600},
                        Subs={},
                        Proxys={})
    

    

 
 