#!/usr/bin/env python3
# ____________developed by paco andres_26/11/2020___________________


from PyAgent.libs_DDS.Ecal_Proxy import Client
import types
import time
import json


def_skel="""
def {0}{1}:
    try:
        params=[{2}]
        params=json.dumps(params).encode('utf-8')
        if self.Client.call_method("{0}",params):
            #print(self.Rets["{0}"])
            if self.Rets["{0}"]["ret_state"]==Status_OK:
                return self.Rets["{0}"]["return"]
            if self.Rets["{0}"]["ret_state"] in [Status_ERROR,Status_NotImplemented]:
                raise RuntimeError("PROXY: Remote method "+self.Rets["{0}"]["error_msg"])
    except:
        raise
"""

Status_OK=1
Status_ERROR=0
Status_NotImplemented=-2
Status_CONF=-1

class Proxy(object):
    def __init__(self,name_proxy, show=False,retrys=100):
        self.showerr=show
        self.name=name_proxy
        #print(self.name)
        self.connected=False
        self.Rets={}
        self.Configuration={}
        self.retrys=retrys
        self.Client=Client(self.name)
        self.connect()
        if self.connected:
            self.__create_hooks()
        
    def __Callback(self,service_info, response):
        response=json.loads(response.decode("utf-8"))
        call=service_info["method_name"]
        self.Rets[call]=None
        self.Rets[call]=service_info.copy()
        if self.Rets[call]["ret_state"]==Status_CONF:
            self.Configuration=response
            return True
        if self.Rets[call]["ret_state"] in [Status_ERROR,Status_NotImplemented]:
            self.Rets[call]["error_msg"]=response
            self.Rets[call]["return"]=None
            return True
        if self.Rets[call]["ret_state"]==Status_OK:
            self.Rets[call]["return"]=response
            return True

    def _close(self):
        self.Client.destroy()

    def connect(self):
        self.get_callback={}
        self.Client.add_response_callback(self.__Callback)
        ret=0
        status=False
        while not status and ret<self.retrys:
            status=self.Client.call_method(f"G_E_T_Configuration",''.encode('utf-8'))
            time.sleep(0.05)
            ret=ret+1
        self.connected=ret<self.retrys

    def __call__(self):
        if self.connected:
            return True
        else:
            self.connect()
            return self.connected

    def __str__(self):
        if self.connected:
            return f"Proxy {self.name}: ON LINE"
        else:
            return f"Proxy {self.name}: OFF LINE"

    def __create_hooks(self):
        hooks=[]
        for defs,params in self.Configuration.items():
            params_def=params[0]
            params_call=",".join(params[1])
            d=def_skel.format(defs,params_def,params_call)
            hooks.append((defs,d))
        for defs,fun in hooks:
            #print(defs,fun)
            exec(fun)
            self.__dict__[defs] = types.MethodType(eval(defs), self)
        self.functions=hooks
        return len(self.functions)>0

  