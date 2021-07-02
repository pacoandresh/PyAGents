#!/usr/bin/env python3
# ____________developed by paco andres_26/11/2020___________________
import time
import sys

import PyAgent.libs.Cmake as CM
from PyAgent.libs.Sys import Agent_Sys

from PyAgent.libs.Server import Create_Agent, Create_Agent_From_Json

from functools import reduce



class Gps_Agent(Agent_Sys):
    def __init__(self):
        self.Json_Topics(Gps={"X":1,"Y":1,"Z":1})
        self.midato=2
        self.Add_Workers(self.worker)
        #print(self.__dict__)
          
    def worker(self):
        while self._Agent_Worker_Run:
            self.Gps["X"]=self.Gps["X"]+1
            self.Gps["Y"]=self.Gps["Y"]-1
            self.Gps["Z"]=self.Gps["Z"]+0.5
            self.Gps_send()
            time.sleep(self._Agent_Frec)
    
    def Agent__Start(self):
        #here configures before start all
        pass
        
    def Agent__Close(self):
        # here if you want save anything before stop agent
        pass
            
    
    def suma(self,a,b):
        print(f"sumando {a}+{b}")
        return a+b

    def suma_list(self,lista):
        return reduce(lambda a,b:a+b,lista)


if __name__ == "__main__":
    CM.Show_Errors()
    # si hay 3 parámetros en la llamada decodificamos y arrancamos. llamada externa
    if len(sys.argv)==3:
        #print(sys.argv)
        Create_Agent_From_Json(Json=sys.argv[2],Environment=CM.Environment)
    else:    
        #iniciamos el dns para poder resolver datos del robot
        robot="Prueba"
        Agent=Create_Agent(f"{robot}/comp1",Gps_Agent,CM.Environment,
                            Autostart=True,
                            Loop=True,
                            Interfaces=["interfaces.calculator::calculator"],
                            Config={"midato":0},
                            Subs={},
                            Proxys={})
 
 