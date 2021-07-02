#!/usr/bin/env python3
# ____________developed by paco andres_26/11/2020___________________
import time
import sys

import PyAgent.libs.Cmake as CM
from PyAgent.libs.Sys import Agent_Sys
from PyAgent.libs.Server import Create_Agent, Create_Agent_From_Json
import cv2


class PiCamera_Agent(Agent_Sys):
    def __init__(self):
        self.Proto_Topics(Image="proto.Image_pb2::Image")
        self.Image.width=self._Config["width"]
        self.Image.height=self._Config["height"]
        self.Add_Workers(self.worker)
        

    def worker(self):
        while self._Agent_Worker_Run:
            
            self.Image.frame=self.Image.frame+1
            self.Image_send()
            time.sleep(self._Agent_Frec)
            



if __name__ == "__main__":
    CM.Show_Errors()
    # si hay 3 parámetros en la llamada decodificamos y arrancamos. llamada externa
    if len(sys.argv)==3:
        Create_Agent_From_Json(Json=sys.argv[2],Environment=CM.Environment)
    else:    
        # sino llamada local de prueba.
        Agent=Create_Agent("Norobot/Camera",PiCamera_Agent,CM.Environment,0.04,
                            Autostart=True,
                            Loop=True,
                            Interfaces=[],
                            Config={"width":640,"height":480},
                            Subs={},
                            Proxys={})

 
 