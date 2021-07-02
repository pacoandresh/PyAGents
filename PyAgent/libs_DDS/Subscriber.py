import PyAgent.libs_DDS.Ecal_Subscriber as Subscriber


class TopicSubscriber(Subscriber.MessageSubscriber):
    """Spezialized subscriber that subscribes to protobuf messages
    """
    def __init__(self, name, descriptor,callback=None,qos="default",history="last",depth=20):
        super(TopicSubscriber, self).__init__(name, descriptor)
        self.name=name
        self.set_qos_reliability(qos)
        self.set_qos_historykind(history,depth)
        self.set_callback(callback)

    def _on_receive(self, topic_name, msg, time):
        raise NotImplementedError("Please Implement this method on_receive")
        
