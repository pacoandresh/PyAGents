import setproctitle
import socket
import ecal.core.core as libEcal
import sys


def change_process_name(name):
    setproctitle.setproctitle(name)

def get_process_name():
    return setproctitle.getproctitle()

def get_host_name():
    return socket.gethostname()

def DDS_Initialize(name_agent,proc_agent=None,status="Running"):
    if proc_agent is None:
        proc_agent=name_agent
    setproctitle.setproctitle(proc_agent)
    libEcal.initialize([], name_agent)
    libEcal.set_process_state(1,1,status)
    #libEcal.mon_initialize()
    #libEcal.mon_pubmonitoring(True,"Mon/Monitoring")

def DDS_Ok():
    return libEcal.ok()

def DDS_Monitor(channel_name):
    setproctitle.setproctitle(channel_name)
    libEcal.mon_initialize()
    libEcal.mon_pubmonitoring(True,channel_name)

def DDS_Monitor_End():
    libEcal.mon_pubmonitoring(False,"")    
    
def DDS_Finalize():
    return libEcal.finalize()

def DDS_Getversion():
    return libEcal.getversion()

def DDS_Getdate():
    return libEcal.getdate()

def DDS_shutdown_process_name(unit_name):
    return libEcal.shutdown_process_uname(unit_name)

def DDS_shutdown_process_id(process_id):
    return libEcal.shutdown_process_id(process_id)

def DDS_shutdown_processes():
    return libEcal.shutdown_processes()

def DDS_shutdown_core():
    return libEcal.shutdown_core()