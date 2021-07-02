import ecal.core.core as ecal_core
import ecal.core.service as ecal_service

class Service(object):
  def __init__(self, service_name):
    self.sname = service_name
    ecal_core.set_process_state(1, 1, "OK")
    self.server= ecal_service.Server(self.sname)

  def destroy(self):
    return ecal_core.server_destroy(self.server)

  def add_method(self, method_name, req_type, resp_type, callback):
    #print(self.server)
    #print(method_name)
    return self.server.add_method_callback(method_name, req_type, resp_type, callback)

  def remove_method(self, method_name):
    return self.server.rem_method_callback(method_name)