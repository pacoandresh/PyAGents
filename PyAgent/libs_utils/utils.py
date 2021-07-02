
#!/usr/bin/env python3
# ____________developed by paco andres_15/04/2019___________________

import netifaces as ni
import traceback
import sys
from termcolor import colored
import threading
import os
import socket
import setproctitle
import psutil
from subprocess import Popen
from PyAgent.libs_Log.coloramadefs import P_Log
import time
import socket


def change_process_name(name):
    setproctitle.setproctitle(name)

def get_process_name():
    return setproctitle.getproctitle()

def get_host_name():
    return socket.gethostname()

def get_ipbyname(name):
    return socket.gethostbyname(f"{name}.local")


def get_ip_address(ifname="lo"):
    """Return IP address from a specific interface."""
    try:
        ip = ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']
    except Exception:
        #  Invalid interface name
        try:
            interface_list = ni.interfaces()
            for x in interface_list:
                if x != "lo":
                    return ni.ifaddresses(x)[ni.AF_INET][0]['addr']
            ip = "127.0.0.1"
        except Exception:
            print("ERROR: Obtaining IP from the network interface. "
                  + colored(ifname, "red"))
            sys.exit()
    return ip

def get_all_ip_eths():
    address = []
    try:
        for x in ni.interfaces():
            add=ni.ifaddresses(x)
            ips=add.get(ni.AF_INET,[])
            if x!="lo":
                if len(ips)>0:
                    address.append((ips[0]["addr"],x))
    except Exception:
        print("ERROR: get_all_ip_eths")
        raise
    #print(address)
    return address

def get_ethernets():
    eths=get_all_ip_eths()
    sal={e:ip for ip,e in eths}
    sal["lo"]="127.0.0.1"
    return sal

def set_eth_ip(eth):
    ethernets=get_ethernets()
    ip="0.0.0.0"
    if eth in ethernets:
        ip=ethernets[eth]
    else:
        eth=list(ethernets)[0]
        ip=list(ethernets.values())[0]
    return eth,ip


def get_all_ip_address(broadcast=False):
    """Return the list of IPs of all network interfaces.

    If broadcast = True, returns the list of broadcast IPs of all network
    interfaces.
    """
    address = []
    try:
        for x in ni.interfaces():
            add = ni.ifaddresses(x)
            try:
                for ips in add[ni.AF_INET]:
                    if broadcast:
                        address.append(ips["broadcast"])
                    else:
                        address.append(ips["addr"])
            except Exception:
                pass
    except Exception:
        print("ERROR: utils.get_all_ip_address()")
        exit()
        raise
    return address


def get_gateway_address(ifname="lo"):
    """Return gateway address from a specific interface."""
    ip = None
    try:
        gateway_list = ni.gateways()
        for gw in gateway_list[2]:
            if gw[1] is ifname:
                ip = gw[0]
                break
    except Exception:
        raise
    return ip


def get_interface():
    """Return the name of the first network interface other than loopback."""
    interface = None
    loopback = None
    try:
        for x in ni.interfaces():
            try:
                if ni.ifaddresses(x)[ni.AF_INET][0]['addr'] != "127.0.0.1":
                    interface = x
                    break
                else:
                    loopback = x
            except Exception:
                pass
    except Exception:
        raise

    if not interface:
        interface = loopback

    return interface


def format_exception(e):
    """Representation of exceptions."""
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(
        sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)

    exception_str = exception_str[:-1]

    return exception_str

def kill_process(pid):
     p = psutil.Process(pid)
     p.terminate()

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''

    listOfProcessObjects = []

    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
           if len(pinfo['cmdline'])>0:
               if processName in pinfo['cmdline'][0] :
                   listOfProcessObjects.append(pinfo)

       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass

    return [(item["pid"],item["cmdline"][0]) for item in listOfProcessObjects];

def ping(uri):
    """Ping and return True if there is connection, False otherwise."""
    response = False
    try:
        response = os.system("ping -c 1 -w2 " + uri + " > /dev/null 2>&1")
    except Exception:
        pass
    return not response

def Get_Export(var):
    """ It turns back the environment path of the program Pyro4Bot """
    if var not in os.environ:
        print(f"ERROR: ${var} not setted")
        print(f"please type export {var}='<DIR>' to set it up")
        sys.exit()
    else:
        return os.environ[var]

def Add_Export(var):
    try:
        sys.path.append(Get_Export(var))
    except:
        exit(0)

    

