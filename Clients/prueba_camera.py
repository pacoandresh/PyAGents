from DARPy.Client.Cli_robot import Client_Robot, Scan
from DARPy.Robot.Creator import Robot
import time
import cv2
import numpy as np
import threading
import imutils

def Show(image):
    while True: 
        buff = np.frombuffer(image.image_data,np.uint8)
        frame =np.reshape(buff,(image.height,image.width,image.deep))
        #frame=imutils.resize(buff,image.height,image.width)
        cv2.imshow("CAM", frame)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit1
        time.sleep(0.01)
    cv2.destroyAllWindows()

#busca robots en linea
robots=Scan(True)

#muestra los topics e interfaces que soportan
#robots.Show("Norobot")

js=Robot("Mybot")
js.Add("Joystick","joystick.joystick::Joystick",Frec=0.01,
        Config={"model":""})
js.Start()

robots.Show("Mybot")
#conecta a uno seleccionando los topic e interface que desees
R=robots.Connect("Mybot",
          Subs={"Image":"Camera/Image","btn":"Joystick/Joy_Btn","axis":"Joystick/Joy_Axis"},
          Proxys={})

# si te es mas cómodo pasalos a variables de tu programa
time.sleep(2)
Image=R.Image
R.Start_Worker(Show,args=(Image,))

    
while True:
    #print(R.btn,R.axis)
    time.sleep(0.05)
cv2.destroyAllWindows()
R.Shutdown()
