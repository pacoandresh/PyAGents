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

robots.Show("Mybot")
#conecta a uno seleccionando los topic e interface que desees
R=robots.Connect("Mybot",
          Subs={"y":"Camera/y","Image":"Camera/Image"},
          Proxys={})

# si te es mas cómodo pasalos a variables de tu programa
time.sleep(2)
#Image=R.Image
y=R.y
image=R.Image
R.Start_Worker(Show,args=(image,))

    
while True:
    print(id(y),"...",y)
    print(id(R.y),"PPP",R.y)
    time.sleep(0.05)
cv2.destroyAllWindows()
R.Shutdown()
