from DARPy.Robot.Cmake import all_interfaces
from DARPy.Robot.utils import Get_Export
Interfaces=[]
ProtoBuffers={}
Agents={"a":1}
dir_agents=Get_Export("ROBOTS")+"/Agents"
print("SSS")
interf=all_interfaces(dir_agents)
print(interf.get_all_interfaces())