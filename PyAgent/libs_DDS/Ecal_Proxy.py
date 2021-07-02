#!/usr/bin/env python3
# ____________developed by paco andres_26/11/2020___________________
import ecal.core.core as ecal_core


class Client(object):
  def __init__(self, service_name):
    self.sname = service_name
    self.shandle = ecal_core.client_create(self.sname)

  def destroy(self):
    return ecal_core.client_destroy(self.shandle)

  def add_response_callback(self, callback):
    return ecal_core.client_add_response_callback(self.shandle, callback)

  def remove_response_callback(self, method_name):
    return ecal_core.client_rem_response_callback(self.shandle)

  def call_method(self, method_name, request):
    try:
      status=ecal_core.client_call_method(self.shandle, method_name, request)==1
      return status
    except Exception as e:
      raise
      print("ERROR on Client  ",e)

