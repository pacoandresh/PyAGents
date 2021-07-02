#!/usr/bin/env python3
# ____________developed by paco andres_26/11/2020___________________
import inspect
from PyAgent.libs_DDS.Ecal_Service  import Service
import json
import traceback

def get_func(cls):
    return [func for func in dir(cls) if callable(getattr(cls, func)) and
         not func.startswith("_")]

def check_functions(cls,cls1):
    return [x for x in get_func(cls) if  x not in get_func(cls1)]

def get_signature(fn):
    fun_param=str(inspect.signature(fn))
    params = inspect.signature(fn).parameters
    args = []
    for p in params.values():
        if p.name !="self":
            args.append(p.name)
    return fun_param,args

Status_OK=1
Status_ERROR=0
Status_NotImplemented=-2
Status_CONF=-1

class Base_Interface(object):
    pass



class Interface(object):
    def __init__(self,name):
        self.name=name
        self.__Server=Service(self.name)

    def Start(self):
        self.__Server.add_method("G_E_T_Configuration", "json", "json", self.__Callback)
        for link in self.Def_Interface:
            #print(f"starting {link}")
            self.__Server.add_method(link, "json", "json", self.__Callback)

    def G_E_T_Configuration(self):
        return self.Def_Interface

    def __Callback(self,method_name, req_type, resp_type, request):
        #print("executing: ",method_name)
        if method_name=="G_E_T_Configuration":
            returned=self.G_E_T_Configuration()
            #print(returned)
            return Status_CONF,json.dumps(returned).encode("utf-8")

        if method_name in self.Not_Implemented:
            error=f"{method_name} not Implemented"
            print(f"ERROR:{error}")
            returned=json.dumps(error).encode("utf-8")
            return Status_NotImplemented,returned
        try:
            params=json.loads(request.decode("utf-8"))
            #print(method_name,params)
            if isinstance(params,dict):           
                returned=getattr(self,method_name)(**params)
                return Status_OK,json.dumps(returned).encode("utf-8")
            if isinstance(params,(tuple,list)):
                returned=getattr(self,method_name)(*params)
                return Status_OK,json.dumps(returned).encode("utf-8")
        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print(''.join(tb1.format()))
            return Status_ERROR,json.dumps(str(e)).encode("utf-8")


class Create_Interface(object):
    def __new__(cls,service,component):
        Not_Implemented=check_functions(service,component)
        interface=Interface(f"{component._Agent_Name}/{service.__name__}")
        #print(Not_Implemented)
        #print(get_func(service))
        Def_Interface={}
        for x in get_func(service):
            Def_Interface[x]=get_signature(eval("service."+x))
            if x not in Not_Implemented:
                setattr(interface,x,eval("component."+x))
      
        setattr(interface,"Def_Interface",Def_Interface)
        setattr(interface,"Not_Implemented",Not_Implemented)

        return interface

    def __init__(self):
        pass

