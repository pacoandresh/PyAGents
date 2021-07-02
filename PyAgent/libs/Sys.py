#!/usr/bin/env python3
# ____________developed by paco andres_15/04/2019___________________


import time
import os
import threading
#from threading import Thread
from termcolor import colored
import importlib
from PyAgent.libs_Log.coloramadefs import C_Err, P_Log,P_Debug
from PyAgent.libs_Log.PyAgent_Log import Logging
from PyAgent.libs_DDS.Ecal_config import DDS_Initialize, DDS_Finalize, DDS_Ok
from PyAgent.libs_DDS.Proxy import Proxy
from PyAgent.libs_DDS.Publisher import TopicPublisher
from PyAgent.libs_DDS.Subscriber import TopicSubscriber
from PyAgent.libs_DDS.Interfaces import Create_Interface
from PyAgent.libs_DDS.Discovery import Discovery
import copy
import types
import json


sender_skel="""
def {0}_send(self,val=None):
    if val is None:
        return self._Agent_Topics['{0}'].send(self.{0}) 
    else:
        return self._Agent_Topics['{0}'].send(val)    
"""
subscriber_skel_proto="""
def _On_{0}_Rec(self,topic,msg,time):
    self.{0}.ParseFromString(msg)
"""
subscriber_skel_json="""
def _On_{0}_Rec(self,topic,msg,time):
    jso=json.loads(msg.decode())
    self.{0}.clear()
    if type(jso)==dict:
        for k in jso:
            self.{0}[k]=jso[k]
    else:
        for k in jso:
            self.{0}.append(k)
    #self.{0}=jso
"""
subscriber_skel_string="""
def _On_{0}_Rec(self,topic,msg,time):
    self.{0}=msg.decode()
"""
subscriber_skel_capnp="""
def _On_{0}_Rec(self,topic,msg,time):
    
    self.{0}=msg.decode()
"""


def Get_Cls(type,Environment,name):
    C_Err(type not in Environment,"Environment Error")
    match=[x for x in Environment[type] if x.endswith(name)]
    err=[k for x,k in Environment["Errors"].items() if x.endswith(name)]
    C_Err(len(err)>0,f"{err}")
    C_Err(len(match)==0,f"{name} not found")
    C_Err(len(match)>1,f"too many options for {name}, {match}")
    module,cls=match[0].split("::")
    mod=importlib.import_module(module)
    #P_Debug(module,cls)
    return getattr(mod,cls)

# Class control system agent
class Agent_Sys(Logging):
    def __init__(self,name,ENV,frec=0.1,Autostart=True,Loop=True,level_log=30):
        super().__init__(name,level_log)
        self._Agent_Name=name
        self._Agent_Pid=os.getpid()
        self._Agent_Frec=frec
        self._Agent_ENV=ENV
        self._Agent_LoopForEver=Loop
        self._Agent_Autostart=Autostart
        self._Agent_Worker_Run=True
        self._Agent_Workers=[]
        self._Agent_Topics={}
        self._Agent_Subscribers={}
        self._Agent_Interfaces=[]
        self._Resolv_Subcribers={}
        self._Resolv_Proxys={}
        DDS_Initialize(f"{self._Agent_Name}")
        
        self.Dns=Discovery()

    def __Configure__(self):
        #Injeting attributes from _Config
        self.L_info("[FG] Configuring Agent.")
        for atrib,value in self._Config.items():
            if atrib in self.__dict__:
                setattr(self,atrib,value)
                self.L_info(f"Changing attribute-->{atrib}-->{value}")
            else:
                self.L_warning(f"{atrib} not defined")
        delattr(self,"_Config")

        #Injecting Proxys
        self.Add_Proxys(**self._Proxys)
        delattr(self,"_Proxys")

        #Injecting Subscribers
        self.Add_Subscribers(**self._Subs)
        delattr(self,"_Subs")
        #Injecting workers
        for work in self._Agent_Workers:
            self.L_info(f"{work.name} Thread Initiated")
        #starting connectors
        self.L_info("[FG] Initiating Agent.")
        self.__Start_Interfaces()
        self.__Start_Subscribers()
        self.__Start_Proxys()
        
        if not self._Agent_Autostart:
            self.L_warning(f"Autostart not activate")
            
        #deleting discovery
        self.Dns.Close()
        delattr(self,"_Agent_ENV")
        delattr(self,"Dns")

    def __Start__(self):
        self.L_info("[FG] Starting Agent.")
        #time.sleep(2)
        self.Start_Workers()

    def __Close__(self):
        method_list = [func for func in dir(self) if callable(getattr(self, func))]
        if "Agent__Close" in method_list:
            self.Agent__Close()
            self.L_info(f"[FY] Agent_Close Method") 

    def Json_Topics(self,**topics):
        for topic,cls in locals()["topics"].items():
            #print(topic,cls, type(cls))
            C_Err(topic in self._Agent_Topics,f"Topic {topic} exist in definitions")
            top=cls
            setattr(self,topic,top)  
            self._Agent_Topics[topic]=TopicPublisher(f"{self._Agent_Name}/{topic}","json",desc=cls,type_=cls)
            _hook=sender_skel.format(topic)
            exec(_hook)
            #print(_hook)
            self.__dict__[f"{topic}_send"] = types.MethodType(eval(f"{topic}_send"), self)
            self.L_info(f"Topic Json [FC]{cls}[FW] as [FG]{topic}[FW] publicating")   
                   
    def Capnp_Topics(self,**topics):
        for topic,cls in locals()["topics"].items():
            pass
            #print(topic,cls)
            
            
    def String_Topics(self,**topics):
        for topic,cls in locals()["topics"].items():
            C_Err(type(cls) not in [int,float,str],f"type not supported for topic string")
            C_Err(topic in self._Agent_Topics,f"Topic {topic} exist in definitions")
            top=cls
            setattr(self,topic,top)  
            self._Agent_Topics[topic]=TopicPublisher(f"{self._Agent_Name}/{topic}","string",desc=cls,type_=cls)
            _hook=sender_skel.format(topic)
            exec(_hook)
            self.__dict__[f"{topic}_send"] = types.MethodType(eval(f"{topic}_send"), self)
            self.L_info(f"Topic String [FC]{cls}[FW] as [FG]{topic}[FW] publicating")   
            
    def Proto_Topics(self,**topics):
        for topic,cls in locals()["topics"].items():
            C_Err(topic in self._Agent_Topics,f"Topic {topic} exist in definitions")
            topiccls=Get_Cls("Protos",self._Agent_ENV,cls) #buscamos la clase en environment y si hay una que coincida la retornamos
            top=topiccls()
            setattr(self,topic,top)   
            C_Err(type(topiccls).__name__!='GeneratedProtocolMessageType',f"{topic} not is Proto class")
            self._Agent_Topics[topic]=TopicPublisher(f"{self._Agent_Name}/{topic}","proto",type_=topiccls)      
            _hook=sender_skel.format(topic)
            exec(_hook)
            #print(_hook)
            self.__dict__[f"{topic}_send"] = types.MethodType(eval(f"{topic}_send"), self)
            self.L_info(f"Topic Protobuf [FC]{topiccls}[FW] as [FG]{topic}[FW] publicating")   

    def Add_Subscribers(self,**subscribers):
        #print(locals()["subscribers"].items())
        self._Resolv_Subcribers.update(subscribers)
        
    def __Start_Subscribers(self):
        topics=self._Agent_Topics.values()
        subs=list(self._Resolv_Subcribers)
        while len(subs)>0:
            attr=subs[0]
            connector=self._Resolv_Subcribers[attr]
            #P_Debug(attr,connector)
            if connector not in topics:
                status,tipe,class_topic,skel=self.Dns.Get_Type_class_Topic(connector)
                #P_Debug(status,tipe,class_topic,attr,connector,skel)
                if status:
                    if tipe=="proto":
                        setattr(self,attr,class_topic())
                        eval(f"self.{attr}.Clear()")
                        _hook=subscriber_skel_proto.format(attr)
                        tdesc=f"{class_topic.__name__}"
                    if tipe=="json":
                        setattr(self,attr,skel)
                        _hook=subscriber_skel_json.format(attr)
                        tdesc=f"{skel}"
                    if tipe=="capnp":
                        setattr(self,attr,class_topic())
                        _hook=subscriber_skel_capnp.format(attr)
                        tdesc=f"{class_topic.__name__}"
                    if tipe =="string":
                        setattr(self,attr,skel)
                        _hook=subscriber_skel_string.format(attr)
                        tdesc=f"{class_topic}"
                    exec(_hook)
                    self.__dict__[f"_On_{attr}_Rec"] = types.MethodType(eval(f"_On_{attr}_Rec"), self)
                    sub_obj=TopicSubscriber(connector,tdesc,callback=eval(f"self._On_{attr}_Rec"))
                    self._Agent_Subscribers[attr]=sub_obj
                    time.sleep(0.2)
                    self.L_info(f"Subscriber: [FB]<{connector}> as[FG] {attr} [FW]connected")
                    subs.remove(attr)    
                else:
                    time.sleep(0.2)
                    self.L_warning(f"Subscriber: {attr} waiting for connect") 
            else:
                self.L_warning(f"Subscriber:{attr} located in same Agent, not connect") 
                subs.remove(attr)
        delattr(self,"_Resolv_Subcribers")

    def Add_Proxys(self,**Proxys):
        self._Resolv_Proxys.update(Proxys)

    def __Start_Proxys(self):
        myinterfaces=[x.name for x in self._Agent_Interfaces]
        proxys=list(self._Resolv_Proxys)
        while len(proxys)>0:
            attr=proxys[-1]
            if self._Resolv_Proxys[attr] not in myinterfaces:
                proxy=Proxy(self._Resolv_Proxys[attr])
                if proxy():
                    setattr(self,attr,proxy)
                    proxys.pop()
                    self.L_info(f"Proxy:{attr}-->{self._Resolv_Proxys[attr]} connected")
                else:
                    time.sleep(0.2)
                    self.L_warning(f"Proxy:{attr} waiting for connect")    
            else:
                self.L_warning(f"Proxy:{attr} located in same Agent, not connect") 
                proxys.pop()
        delattr(self,"_Resolv_Proxys")
 

    def Add_Interfaces(self,*interfaces):
        self._Interfaces.extend(interfaces)

    
    def __Start_Interfaces(self):
        starting=set(self._Interfaces)
        for inter in starting:
            inter=Get_Cls("Interfaces",self._Agent_ENV,inter)
            _inter=Create_Interface(inter,self)
            _inter.Start()
            for i in  _inter.Not_Implemented:
                self.L_warning(f"{i} not implemented in {inter}")
            self._Agent_Interfaces.append(_inter)
            self.L_info(f"Interface [FC]{inter}[FW] connected") 
        delattr(self,"_Interfaces")
        

    def Add_Workers(self, fn):
        if type(fn) not in (list, tuple):
            fn = (fn,)
        for func in fn:
            name=f"{self._Agent_Name}.{func.__name__}"
            t = threading.Thread(target=func,name=name, args=())
            t.setDaemon(True)
            self._Agent_Workers.append(t)


    def Start_Workers(self):
        for t in self._Agent_Workers:
            name=t.getName()
            if not t.is_alive(): # changed
                self.L_info(f"{name} worker Started")
                t.start()
                
    def Change_Subs_Callback(self,topic,callback):
        #print(self._Agent_Subscribers)
        if topic in self._Agent_Subscribers:
            self._Agent_Subscribers[topic].set_callback(callback)
            self.L_info(f"{topic} changing callback")
        else:
            self.L_warning(f"{topic} no is subscriber")
 
    def Shutdown(self):
        self._Agent_Worker_Run=False
        self.__Close__()
        self.L_info(f"[FY]Agent ShutDown") 
        return DDS_Finalize()

    def Ok(self):
        return DDS_Ok()

    def Set_Logging(self,level=20):
        self.Level_reconfigure(level)
        self.L_info(f"Logging level change. new level:{level}")
        
    def Hello(self):
        return "hi"

    def __LoopForEver__(self):
        self.L_info(f"Running Loop for ever")
        try:
            while self.Ok(): 
                time.sleep(5)
        except KeyboardInterrupt:
            self.Shutdown()
        