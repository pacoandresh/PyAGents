import ecal.core.core as ecal_core
import ecal.proto.helper as pb_helper

QOS={"default":0,"best_effort":1,"reliable":2}
LAYER={"udp":0,"shm":1,"hdf5":2}
HISTORY={"last":0,"all":1}
MODE={"off":0,"on":1,"auto":2}

class MessageSubscriber(object):
  """Message subscriber - Base class for all specialized subscribers
  Classes inheriting from this class need to implement the 
  :func:`~subscriber.MessageSubscriber.receive`, 
  :func:`~subscriber.MessageSubscriber.set_callback` and
  :func:`~subscriber.MessageSubscriber.rem_callback` functions.
  """
  
  def __init__(self, name, topic_type=""):
    self.c_subscriber = ecal_core.subscriber(name, topic_type)

  def set_qos_historykind(self, qpolicy="last", depth=10):
    """ set quality of service historykind mode and depth

    :param qpolicy: 0 = keep_last_history_qos, 1 = keep_all_history_qos
    :param depth:   history kind buffer depth

    """

    return self.c_subscriber.set_qos_historykind(HISTORY.get(qpolicy,0), depth)

  def set_qos_reliability(self, qpolicy="reliable"):
    """ set quality of service reliability mode

    :param qpolicy: 0 = best_effort_reliability_qos, 1 = reliable_reliability_qos

    """

    return self.c_subscriber.set_qos_reliability( QOS.get(qpolicy))

  def receive(self, timeout=0):
    """ receive subscriber content with timeout

    :param timeout: receive timeout in ms
    :type timeout:  int

    """
    raise NotImplementedError("Please Implement this method")

  def set_callback(self, callback):
    """ set callback function for incoming messages

    :param callback: python callback function (f(topic_name, msg, time))

    """
    self.callback = callback
    self.c_subscriber.set_callback(callback)

  def rem_callback(self):
    """ remove callback function for incoming messages

    :param callback: python callback function (f(topic_name, msg, time))

    """
    self.c_subscriber.rem_callback(self.callback)
    self.callback = None
    
