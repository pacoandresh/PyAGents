import PyAgent.libs_DDS.Ecal_Publisher as publisher
import ecal.proto.helper as pb_helper
import json
import capnp



class TopicPublisher(publisher.MessagePublisher):
    """Spezialized publisher that sends out protobuf messages
    """
    def __init__(self, name, model, type_=None,desc=None,qos="default",history="last",depth=10):
        self.name=name
        if model=="proto":
            self.type_ = "proto:" + type_.DESCRIPTOR.full_name
            self.desc = pb_helper.get_descriptor_from_type(type_)
            self.send=self.send_proto
        if model=="json":
            self.type_ = "json:" + name.split("/")[-1]
            self.desc=json.dumps(desc).encode()
            self.send=self.send_json
        if model == "string":
            self.type_ = "string:" +  name.split("/")[-1]
            self.desc = str(type(desc)).encode()
            self.send=self.send_string
        if model == "capnp":
            self.topic_type = "capnp:" + str(type_.schema)
            self.topic_desc = self.topic_type.encode()
            self.send=self.send_capnp
                    
        super(TopicPublisher, self).__init__(name, self.type_, self.desc)
        self.set_qos_historykind(history,depth)
        
 
    def send_proto(self, msg, time=-1):
        self.c_publisher.send(msg.SerializeToString(), time)
    
    def send_capnp(self, msg, time=-1):
        self.c_publisher.send(msg.to_bytes(), time)
        
    def send_json(self, msg, time=-1):
        self.c_publisher.send(json.dumps(msg).encode(), time)
        
    def send_string(self, msg, time=-1):
        self.c_publisher.send(str(msg).encode(), time)

