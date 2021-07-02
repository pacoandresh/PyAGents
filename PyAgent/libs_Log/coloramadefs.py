#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ____________developed by paco andres____________________
# ________in collaboration with cristian vazquez _________
from colorama import Cursor, init, Fore, Back, Style
import re

#init()
STYLE = re.compile("\[[F,B,S][A-Z]\]")
print(Style.RESET_ALL)

color = {"[FR]": Fore.RED,
         "[FY]": Fore.YELLOW,
         "[FB]": Fore.BLUE,
         "[FG]": Fore.GREEN,
         "[FM]": Fore.MAGENTA,
         "[FC]": Fore.CYAN,
         "[FW]": Fore.WHITE,
         "[FN]": Fore.BLACK,
         "[FS]": Fore.RESET,
         "[BB]": Back.BLUE,
         "[BR]": Back.RED,
         "[BG]": Back.GREEN,
         "[BY]": Back.YELLOW,
         "[BM]": Back.MAGENTA,
         "[BC]": Back.CYAN,
         "[BW]": Back.WHITE,
         "[BS]": Back.RESET,
         "[SD]": Style.DIM,
         "[SN]": Style.NORMAL,
         "[SB]": Style.BRIGHT,
         "[SR]": Style.RESET_ALL
         }


def pos(x, y):
    return Cursor.POS(x, y)


def up(n):
    return Cursor.UP(n)


def down(n):
    return Cursor.DOWN(n)


def forward(n):
    return Cursor.FORDWARD(n)


def back(n):
    return Cursor.BACK(n)


def log_color(mesaje):
    colors = [s for s in STYLE.findall(mesaje) if s in color]
    for s in colors:
        mesaje = mesaje.replace(s, color[s])
    return mesaje + Style.RESET_ALL


def rawlog_color(mesaje):
    colors = [s for s in STYLE.findall(mesaje) if s in color]
    for s in colors:
        mesaje = mesaje.replace(s, "")
    return mesaje

def P_Log(mesaje,ln=True):
    if ln:
        print(log_color(mesaje)) 
    else:
        print(log_color(mesaje),end="") 
    
def C_Err(condition,mesage):
    try:
        assert not condition
            
    except AssertionError:
        P_Log("[FR][ERROR][FY] Critical: [FW]{}".format(mesage))
        exit()
    except:
        P_Log("[FR] Error not evaluable: {}".format(mesage))
        
def C_War(condition,mesage):
    try:
        assert not condition
            
    except AssertionError:
        P_Log("[FY][Warning] [FW]{}".format(mesage))
    except:
        P_Log("[FR] Error not evaluable: {}".format(mesage))
    
def P_Debug(*mesage):
    #print(locals())
    for var in locals()["mesage"]:
        P_Log("[FC][DEBUGGER] [FW]{}".format(var))
