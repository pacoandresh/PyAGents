import ecal.core.core as ecal_core
import ecal.proto.helper as pb_helper

QOS={"default":0,"best_effort":1,"reliable":2}
LAYER={"udp":0,"shm":1,"hdf5":2}
HISTORY={"last":0,"all":1}
MODE={"off":0,"on":1,"auto":2}

class MessagePublisher(object):
  """Message publisher - Base class for all specialized publishers
  Classes inheriting from this class need to implement the 
  :func:`~msg_publisher.msg_publisher.send` function.
  """
  def __init__(self, name, topic_type="", topic_descriptor=""):
    """ Initialize a message publisher

    :param name:             subscription name of the publisher
    :type name:              string
    :param topic_type:       optional, type of the transported payload, eg a a string, a protobuf message
    :type topic_type:        string
    :param topic_descriptor: optional, a string which can be registered with ecal to allow io
      reflection features
    :type topic_descriptor:  string

    """
    self.c_publisher = ecal_core.publisher(name, topic_type, topic_descriptor)

  def send(self, msg, time=-1):
    """ Send out a message

    :param msg:  Message object to send
    :param time: optional, timestamp which to send
    :type time:  int

    """
    raise NotImplementedError("Please Implement this method")

  def set_qos(self, qos="reliable"):
    """ set publisher quality of service

    :param qos: 0 = default, 1 = best effort, 2 = reliable
    :type qos:  int

    """

    return self.c_publisher.set_qos_reliability(QOS.get(qos,2))

  def set_qos_historykind(self, qpolicy="last", depth=10):  
    """ set quality of service historykind mode and depth

    :param qpolicy: 0 = keep_last_history_qos, 1 = keep_all_history_qos
    :param depth:   history kind buffer depth

    """
    return self.c_publisher.set_qos_historykind(HISTORY.get(qpolicy,0),depth)
  
  def set_layer_mode(self, layer="udp", mode="auto"):
    """ set send mode for specific transport layer

    :param layer: 0 = udp, 1 = shm, 2 = hdf5
    :type layer:  int
    :param mode:  0 = off, 1 = on,  2 = auto
    :type layer:  int

    """
    return self.c_publisher.set_layer_mode(LAYER.get(layer,0),MODE.get(mode,2))

  def set_max_bandwidth_udp(self, bandwidth):
    """ set publisher maximum transmit bandwidth for the udp layer.

    :param bandwidth:    maximum bandwidth in bytes/s (-1 == unlimited)
    :type bandwidth:     int

    """

    return self.c_publisher.pub_set_max_bandwidth_upd(bandwidth)


