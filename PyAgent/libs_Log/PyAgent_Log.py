#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ____________developed by paco andres____________________
# ________in collaboration with cristian vazquez _________
from PyAgent.libs_Log.coloramadefs import *

level_DEBUG = 40
level_INFO = 30
level_WARNING = 20
level_ERROR = 10
level_CRITICAL = 0

class Logging(object):
    def __init__(self,name,level=30):
        self._Log_Level=level
        self._Log_Name=name
        self._Log_cache=[]

    def Level_reconfigure(self,level=20):
        self._Log_Level=level
        for men in self._Log_cache:
            if men[0]==level_DEBUG:
                self.L_debug(men[1]) 
            if men[0]==level_WARNING:
                self.L_warning(men[1])
            if men[0]==level_INFO:
                self.L_info(men[1])  
        self._Log_cache=[]

    def L_debug(self, men):
        if self._Log_Level >= level_DEBUG:
            print(log_color(f"[[FG]Debug[SR]] <{self._Log_Name}>::{str(men)}"))
        else:
            self._Log_cache.append((level_DEBUG,men))

    def L_warning(self, men):
        if self._Log_Level>= level_WARNING:
            print(log_color(f"[[FY]Warning[SR]] <{self._Log_Name}>::{str(men)}"))
        else:
            self._Log_cache.append((level_WARNING,men))

    def L_info(self, men):
        if self._Log_Level>= level_INFO:
            print(log_color(f"[[FC]Info[SR]] <{self._Log_Name}>::{str(men)}"))
        else:
            self._Log_cache.append((level_INFO,men))

    def L_error(self, men):
        if self._Log_Level>= level_ERROR:
            print(log_color(f"[[FR]ERROR[SR]] <{self._Log_Name}>::{str(men)}"))

    def L_critical(self, men):
        if self._Log_Level>= level_CRITICAL:
            print(log_color(f"[[FR]CRITICAL[SR]]:<{self._Log_Name}>::{str(men)}"))

    def L_print(self, men,handler=False):
        if handler:
            print(log_color(f"[FG]<{self._Log_Name}> [SR]{str(men)}"))
        else:
            print(log_color(str(men)))

    def L_Def(self, men,handler=False):
        if handler:

            print(log_color(f"[FG]<{self._Log_Name}> [SR]{str(men)}"))
        else:
            print(log_color(str(men)))
