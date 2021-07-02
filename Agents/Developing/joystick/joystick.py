#!/usr/bin/env python3
# ____________developed by paco andres_26/11/2020___________________
import time
import sys

import PyAgent.libs.Cmake as CM
from PyAgent.libs.Sys import Agent_Sys
from PyAgent.libs.Server import Create_Agent, Create_Agent_From_Json
from evdev import InputDevice, categorize, ecodes,list_devices
from evdev.events import AbsEvent
import evdev



class Joystick(Agent_Sys):
    def __init__(self):
        # this method only for assing topic and attributes 
        self.Json_Topics(Joy_Btn=[])
        self.Json_Topics(Joy_Axis={})
        #self.Capnp_Topics(pepe="capnp.joystick::Ejes")
        
        self.model="No model"
        self.Add_Workers(self.worker)
        
    def Agent__Start(self):
        #here configures before start all
        self.Get_Device(self.model,show=False)
        #self.ejes={"ABS_Z":None,"ABS_Y":None,"ABS_X":None}
        self.Act_Keys=[]
        self.Act_Keys_codes=[]
        self.CAPS={v:k for k,v in self.joystick.capabilities(verbose=True)[('EV_KEY', 1)]}

    def worker(self):
        keys=[]
        while self._Agent_Worker_Run:
            for event in self.joystick.read_loop():
                if event.type==ecodes.EV_ABS:
                    absevent=categorize(event)
                    self.Joy_Axis[ecodes.bytype[absevent.event.type][absevent.event.code]]=absevent.event.value
                    self.Joy_Axis_send()
                if event.type == evdev.ecodes.EV_KEY: 
                    self.Joy_Btn=[]              
                    KEYS=[self.CAPS[x] for x in self.joystick.active_keys(verbose=False)]
                    for k in KEYS:
                        if type(k)==list:
                            self.Joy_Btn.extend(k)
                        if type(k)==str:
                            self.Joy_Btn.append(k)
                    if len(KEYS)==0:
                        self.Joy_Btn=[]      
                    self.Joy_Btn_send()
            time.sleep(self._Agent_Frec)
                


    def Get_Device(self,model,show=False):
        devices = [InputDevice(path) for path in list_devices()]
        if show:
            #print(devices)
            print("Available Devices:")
            for device in devices:
                print(device.path, device.name, device.phys)
        for dev in devices:
            if model=="":
                self.joystick=InputDevice(dev.path)
                self.L_info(f"Joystick {self.joystick} connected")
                return self.joystick
            if dev.name==model:
                try:
                    self.joystick=InputDevice(dev.path)
                    self.L_info(f"Joystick {self.joystick} connected")
                    return self.joystick
                except:
                    self.joystick=None
                    self.L_error(f"Joystick {self.joystick} error connecting")
                    self.Shutdown()
        self.L_error(f"Joystick {model} not found")
        self.joystick=None
        
    

        
    def Agent__Close(self):
        # here if you want save anything before stop agent
        pass
            

if __name__ == "__main__":
    
    # si hay 3 parámetros en la llamada decodificamos y arrancamos. llamada externa
    if len(sys.argv)==3:
        Create_Agent_From_Json(Json=sys.argv[2],Environment=CM.Environment)
    else:    
        #print(CM.Environment)
        CM.Show_Errors()
        # sino llamada local de prueba.
        name="Logitech Logitech Attack 3"
        #name="Sony PLAYSTATION(R)3 Controller"
        Agent=Create_Agent("prueba/Joystick",Joystick,CM.Environment,0.01,
                            Autostart=True,
                            Loop=True,
                            Interfaces=[],
                            Config={"model":name},
                            Subs={},
                            Proxys={})

 
 