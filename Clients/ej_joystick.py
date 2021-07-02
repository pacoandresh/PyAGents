from DARPy.Client.Cli_robot import Client_Robot, Scan
import time

#busca robots en linea
robots=Scan(True)

#muestra los topics e interfaces que soportan
robots.Show("prueba")

#conecta a uno seleccionando los topic e interface que desees
R=robots.Connect("prueba",
          Subs={"axis":"Joystick/Joy_Axis","btn":"Joystick/Joy_Btn","pp":"Joystick/pp"},
          #Subs={"axis":"Joystick/Joy_Axis"},
          Proxys={})

# si te es mas cómodo pasalos a variables de tu programa

axis=R.axis
btn=R.btn

while True:
    print(R.axis)
    print(R.btn)
    print(R.pp)
    time.sleep(0.02)
R.Shutdown()
