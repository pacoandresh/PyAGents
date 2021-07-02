#!/usr/bin/env python3
# ____________developed by paco andres_15/04/2021
# ___________________
import json
import importlib



def Get_Cls(name):
    module,cls=name.split("::")
    mod=importlib.import_module(module)
    return getattr(mod,cls)

def Loader_Config(clss, *args,**kwargs):
    """ Decorator for load configuration into component
        init superclass control, configure and start agent 
    """
    original_init = clss.__init__

    def init(self):
        method_list = [func for func in dir(self) if callable(getattr(self, func))]
        #print(args)
        for k, v in kwargs.items():
            #print(k,"-->",v)
            setattr(self, k, v)
        self._Agent_Status="Init"    
        super(clss, self).__init__(*args)
        self._Agent_Status="Configuring"
        original_init(self) 
        super(clss,self).__Configure__()
        if "Agent__Start" in method_list:
            self.Agent__Start()
        if args[3]:
            super(clss,self).__Start__()
            self._Agent_Status="OK"
        if self._Agent_Status=="OK" and args[4]:
            super(clss,self).__LoopForEver__()

    clss.__init__ = init
    return clss

def Create_Agent(name_Agent,
                Specific_Class_Agent,
                ENV,
                Frec=None,
                Autostart=True,
                Loop=True,
                Agent_Interface=True,
                Config={},
                Interfaces=[],
                Subs={},
                Proxys={}):
   
    if Agent_Interface:
        Interfaces.append("PyAgent.libs.Sys_Control::Sys_C")
        ENV["Interfaces"].append("PyAgent.libs.Sys_Control::Sys_C")
    
    if type(Specific_Class_Agent)==str:
        Specific_Class_Agent=Get_Cls(Specific_Class_Agent)
    if Frec is None:
        Frec=0.1    
    Agent=Loader_Config(Specific_Class_Agent,
                        name_Agent,
                        ENV,
                        Frec,
                        Autostart,
                        Loop,
                        _Config=Config,
                        _Interfaces=Interfaces,
                        _Subs=Subs,
                        _Proxys=Proxys)
    #P_Log(f"[FY]Creating Agent: {name_Agent}")
    return Agent()


def Create_Agent_From_Json(Json,Environment):
    Robot=json.loads(Json)
    #print(Robot)
    Agent=Create_Agent(Robot["Name"],Robot["Agent"],Environment,Robot["Frec"],
                        Autostart=Robot["Autostart"],
                        Agent_Interface=True,
                        Loop=True,
                        Interfaces=Robot["Interfaces"],
                        Config=Robot["Config"],
                        Subs=Robot["Subs"],
                        Proxys=Robot["Proxys"])
    return Agent

