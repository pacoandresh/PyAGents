from DARPy.Robot.Creator import Robot


Mybot=Robot("Mybot")

Mybot.Add("GPS","gps.gps_comp::Gps_Agent",
            Frec=0.001,
            Interfaces=["interfaces.calculator::calculator"])

Mybot.Add("Camera","camera.usbcamera::UsbCamera",
          Frec=0.01,
          Config={"width":800,"height":600})





#Mybot.Save_Model("models/modelo1.json")

Mybot.Start()


