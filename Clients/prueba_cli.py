from DARPy.Client.Cli_robot import Client_Robot, Scan
from DARPy.Robot.Creator import Robot
import time
import json

def On_micall_Rec(topic,msg,time):
    print(msg)



# necesitamos el joystick para controlar el robot y lo lanzamos si no está
# "model":"Sony PLAYSTATION(R)3 Controller"
# "model":"Logitech Logitech Attack 3"
Mybot=Robot("Mybot")
Mybot.Add("Joystick","joystick.joystick::Joystick",Frec=0.1,
        Config={"model":""})
Mybot.Start()
time.sleep(2)

#busca robots en linea
robots=Scan(True)
#muestra los topics e interfaces que soportan
robots.Show("Mybot")
#conecta a uno seleccionando los topic e interface que desees
R=robots.Connect("Mybot",
          Subs={"Gps":"GPS/Gps","Image":"Camera/Image",
                "btn":"Joystick/Joy_Btn",
                "axis":"Joystick/Joy_Axis",
                "pp":"Joystick/pp"},
          Proxys={"cal":"GPS/calculator","sys":"GPS/Sys_C"})


#R.Change_Subs_Callback("Gps",On_micall_Rec)

# si te es mas cómodo pasalos a variables de tu programa

cal=R.cal

for t in range(10000):
    time.sleep(0.05)
    print(R.Gps,"::",R.axis,"::",R.btn,"::",R.pp)
    print(cal.suma(R.axis["ABS_X"],R.axis["ABS_Y"]))
    print(R.sys.Hello())
R.Shutdown()
