from PyAgent.libs_Log.coloramadefs import P_Log
import os
import sys
from pyparsing import *
import importlib



def Get_cls(name):
    #print(name)
    module,cls=name.split("::")
    mod=importlib.import_module(module)
    return getattr(mod,cls)

def Get_Packages_Errors(base,f):
    pack = Word(srange("[a-zA-Z_]"), srange("[a-zA-Z0-9_.]"))
    #subpack = Word(srange("[a-zA-Z_]*"), srange("[a-zA-Z0-9_,]"))
    package_import = Suppress("import ")+pack
    package_from = Suppress("from ")+pack
    packages=[]
    with open(f,"r") as file:
        lines=file.readlines()
    for l in lines: 
        try:
            m=package_import.parseString(l) 
            packages.extend(m)
            #print("package",m)
        except:
            pass
        try:
            m=package_from.parseString(l) 
            packages.extend(m)
            #print("package_from",m)
        except:
            pass

    packages=list(set(packages))
    errors=[]
    for p in packages:
        try:
            m=importlib.import_module(p)
        except:
            errors.append(f"Please Run pip3 install {p}")    
    return errors


def get_Clases_cls(base,f):
    name=Word(srange("[a-zA-Z_]"), srange("[a-zA-Z0-9_]"))
    Interface_class=Suppress("class ")+name+Suppress("(Base_Interface):")
    Agent_class=Suppress("class ")+name+Suppress("(Agent_Sys):")
    #Proto_class=name+Suppress(" = _reflection.GeneratedProtocolMessageType")
    Proto_match=" = _reflection.GeneratedProtocolMessageType"
    Interface=[]
    Proto=[]
    Agent=[]
    if base in sys.path:
        module=f.replace(base+"/","").replace("/",".").replace(".py","")
        #print(base,f, module)
    else:
        module=f.replace(base+"/","").replace("/",".").replace(".py","")
    with open(f,"r") as file:
        lines=file.readlines()

        for l in lines:
            try: 
                m=Interface_class.parseString(l)
                Interface.extend([module+"::"+c for c in m])
            except:
                pass
        for l in lines: 
            try:
                m=Agent_class.parseString(l)
                Agent.extend([module+"::"+c for c in m])  
            except:
                pass
        for l in lines: 
            pos=l.find(Proto_match)
            if pos!=-1:
                c=l[0:pos]
                Proto.append(module+"::"+c)  
        
    errors=check_module(module)
    Ret_Interfaces={k:errors for k in Interface}
    Ret_Agents={k:errors for k in Agent}
    Ret_Proto={k:errors for k in Proto}

    return Ret_Agents,Ret_Interfaces,Ret_Proto

def check_module(module):
    errors=[]
    try:
        m=importlib.import_module(module)
    except Exception as e:
        errors.append(module+"-->"+str(e))
    return errors

def CMake():
    if "AGENTS" in os.environ:
        #print("using $AGENTS")
        dir_agents=os.environ["AGENTS"]
        if dir_agents not in sys.path:
            sys.path.append(dir_agents)
    else:
        dir_agents=os.getcwd()

    Allfiles=[]
    
    ERRORS={}
    INTERFACES={}
    AGENTS={}
    PROTOS={}
    for path, dirs, files in os.walk(dir_agents):
        if "__" not in path:
            for f in files:
                if "__" not in f and ".py" in f:
                    Allfiles.append(path+"/"+f)
    for f in Allfiles:
        pack_errors=Get_Packages_Errors(dir_agents,f)
        ERRORS.update({f:pack_errors})
        agents,interfaces,protos=get_Clases_cls(dir_agents,f)
        INTERFACES.update(interfaces)
        AGENTS.update(agents)
        PROTOS.update(protos)

    ERRORS.update({k:e for k,e in PROTOS.items() if len(e)>0})
    ERRORS.update({k:e for k,e in  AGENTS.items() if  len(e)>0})
    ERRORS.update({k:e for k,e in  INTERFACES.items() if  len(e)>0})
    
    
    PROTOS=[p for p,e in PROTOS.items() if len(e)==0 ]
    INTERFACES=[i for i,e in INTERFACES.items() if len(e)==0 ]
    AGENTS=[a for a,e in AGENTS.items() if len(e)==0 ]            
    return {"Protos":PROTOS,"Interfaces":INTERFACES,"Agents":AGENTS,"Errors":ERRORS,"Dir_Agents":dir_agents}



Environment=CMake()

def Show_Errors():
    if len(Environment["Errors"])>0:
        P_Log("[FY] CMake is cheking errors in Agents...")
    for package,errors in Environment["Errors"].items():
        for error in errors:
            P_Log("\t[FW] {}".format(error))


if __name__ == '__main__':  
    pass
    
