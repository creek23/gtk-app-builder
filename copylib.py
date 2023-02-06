#!/usr/bin/python3

from curses.ascii import NUL
import sys
import subprocess

__version__ = '0.1'
__author__ = "Mj Mendoza IV"
__copyright__ = "Copyleft (C) 2023 Mj Mendoza IV"

dictLIBS = dict()
g_dependencies = []
g_copylib = NUL

l_myapp = ""
if (len(sys.argv) > 1):
    l_myapp = sys.argv[1]
else:
    print("Usage: copylib.py myapp")
    exit();
g_copylib = open("copylib_" + l_myapp + ".sh", "w")

def main():
    #print("#!/bin/sh")
    g_copylib.write("#!/bin/sh\n")

    result = subprocess.run(["otool", "-L", l_myapp], capture_output=True)
    l_resultArray = result.stdout.decode().split("\n")
    l_dylibs = []
    for l_dylib in l_resultArray:
        l_temp = l_dylib.find(" (")
        if (l_temp > 0):
            l_dylib = l_dylib[1:l_temp] #disregard TAB
            l_dylibs.append(l_dylib)
            dictLIBS[l_dylib] = l_dylib

    for l_dylib in l_dylibs:
        if (l_dylib.find("/usr/local") >= 0):
            #print("cp \"" + l_dylib + "\" ../lib/\n")
            g_copylib.write("cp \"" + l_dylib + "\" ../lib/\n")
    
    changeInstallNameTool(l_dylibs)
    
    for l_dependency in g_dependencies:
        #print(l_dependency)
        g_copylib.write(l_dependency)
    
    print("created: copylib_" + l_myapp + ".sh")
    g_copylib.close()
    result = subprocess.run(["chmod", "+x", "copylib_" + l_myapp + ".sh"], capture_output=True)

def changeInstallNameTool(p_dylibs):
    for l_dylib in p_dylibs:
        result = subprocess.run(["otool", "-L", l_dylib], capture_output=True)
        l_resultArray = result.stdout.decode().split("\n")
        for l_dependency in l_resultArray:
            l_temp = l_dependency.find(" (")
            if (l_temp > 0 and l_dependency.find("/usr/local") >= 0):
                l_dependency = l_dependency[1:l_temp] #disregard TAB
                l_dylibNAME = l_dylib[l_dylib.find("/lib/")+5:]
                l_dependencyNAME = l_dependency[l_dependency.find("/lib/")+5:]
                if (l_dependency in dictLIBS):
                    pass
                else:
                    dictLIBS[l_dependency] = l_dependency
                    #print("cp \"" + l_dependency + "\" ../lib/")
                    g_copylib.write("cp \"" + l_dependency + "\" ../lib/\n")
                    #then do crawl newly added for libs
                    changeInstallNameTool([l_dependency])
                g_dependencies.append("install_name_tool -change \"" + l_dependency + "\" \"@executable_path/../Resources/lib/" + l_dependencyNAME + "\" ../lib/" + l_dylibNAME + "\n")

main()