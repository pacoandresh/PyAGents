import ecal.core.core as libEcal
import time
import threading
import json
from ecal.proto.helper import get_type_from_descriptor

Retrys=50

class Discovery(object):
    
    def __init__(self,stime=0.05):
        self.data={}
        self.status=1
        self.stime=stime
        self.run=True
        libEcal.mon_initialize()
        thread =threading.Thread(target=self.worker,name="PyAgent_monitor")
        thread.setDaemon(True)
        thread.start()
        while self.status>0:
            time.sleep(0.05)

    def Get_data(self):      
        self.status,self.data=libEcal.mon_monitoring()
        #print("estado:",self.status)
        #pprint.pprint(self.data)

    def worker(self):
        while self.run:
            self.Get_data()
            time.sleep(self.stime)

    def Get_Type_class_Topic(self,topic_name):
        status,data=self.Get_Topic(topic_name)
        if status:
            tipe,cls=data[topic_name]["ttype"].split(":")
            if tipe in ["proto","capnp"]:
                clas=get_type_from_descriptor(cls,data[topic_name]["tdesc"])
                skel=None
            if tipe=="json":
                desc=json.loads(data[topic_name]["tdesc"].decode())
                clas=type(desc)
                skel=desc
            if tipe=="string":
                desc=data[topic_name]["tdesc"].decode()
                clas=type(desc)
                skel=desc
            return status,tipe,clas,skel
        else:
            return status,None,None,None

    def Get_Topic(self,topic_name):
        #data=self.topics(filters={"tname":topic_name,"direction":"publisher"})
        data=self.Get_Topics(topic_name)
        #print(data)
        if len(data)>0:
            return True,data
        else:
            return False,None
        
    def Get_Topics(self,starwith,columns=["hname","ttype","tdesc","direction","dfreq"]):
        if "topics" in self.data:
            topics=self.data["topics"]
        else:
            topics=[]
        if len(columns)==0:          
            topics={x["tname"]:{k:v for k,v in x.items()} for x in topics if x["tname"].startswith(starwith) and x["direction"]=="publisher"}
        else:
            topics={x["tname"]:{k:v for k,v in x.items() if k in columns} for x in topics if x["tname"].startswith(starwith) and x["direction"]=="publisher"}
        return topics
    
    def Get_Services(self,starwith,columns=[]):
        if "services" in self.data:
            services=self.data["services"]
        else:
            services=[]
        if len(columns)==0:          
            services={x["sname"]:{k:v for k,v in x.items()} for x in services if x["sname"].startswith(starwith)}
            for t in services:
                services[t]["methods"]=[x["mname"] for x in services[t]["methods"] if not x["mname"].startswith("G_E_T_")]
        else:
            services={x["sname"]:{k:v for k,v in x.items() if k in columns} for x in services if x["sname"].startswith(starwith)}
            if "methods" in columns:
                for t in services:
                    services[t]["methods"]=[x["mname"] for x in services[t]["methods"] if not x["mname"].startswith("G_E_T_") ]
        
        return services
    
    def Get_Processes(self,starwith,columns=[]):
        if "processes" in self.data:
            processes=self.data["processes"]
        else:
            processes=[]
        if len(columns)==0:          
            processes={x["uname"]:{k:v for k,v in x.items()} for x in processes if x["uname"].startswith(starwith)}
        else:
            processes={x["uname"]:{k:v for k,v in x.items() if k in columns} for x in processes if x["uname"].startswith(starwith)}
        return processes
    

    
    def Get_Agents(self,starwith,columns=[]):
        return self.Get_Processes(starwith,columns)
    
    def Get_Robot(self,robot):
        starwith=robot+"/"
        processes=self.Get_Processes(starwith)
        robots={k.split("/")[0]:[] for k in processes}
        for p in processes:
            topics={k:v for k,v in self.Get_Topics(starwith).items() if v["direction"]=="publisher"}
            robots[p.split("/")[0]]={"services":self.Get_Services(starwith),"topics":topics}
        return robots
    
    def Find_Agents(self,startswith):
        find=self.Get_Processes(startswith,columns=["pid","pname","hname","state","rclock"])
        return find
   
    def Find_Robots(self,split="/"):
        P=self.Get_Processes("",columns=["uname","pid"])
        Robots=[x.split("/")[0] for x in P if len(x.split("/"))>1]
        return list(set(Robots))
    
    def Is_Online(self,name,trays=10):
        duration=0.05
        find=False
        while trays>0 and not find:
            Agents=self.Find_Agents(name)
            find=len(Agents)>0
            trays=trays-1
            time.sleep(duration) 
        return find
        
    def Close(self):
        self.run=False
        libEcal.mon_finalize()
