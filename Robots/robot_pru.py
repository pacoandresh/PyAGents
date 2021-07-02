import os
import sys
from DARPy.Robot.Creator import Robot


Mybot=Robot("Mybot",
            Frec=0.001)

Mybot.Add("GPS","gps.gps_comp::Gps_Agent",
            Interfaces=[])
Mybot.Add("Joystick","joystick.joystick::Joystick",Frec=0.01,
        Config={"model":""})

Mybot.Add("Camera","camera.usbcamera::UsbCamera",          Frec=0.01)

Mybot.Start()


