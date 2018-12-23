# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 23:33:21 2018

@author: neilp
"""

dir = "./hw3dataset/"
f = open("genData.txt", "r")
directedgraph = open(dir + "dirgenData.txt", "w")
bidirectedgraph = open(dir + "bidirgenData.txt", "w")
for itemstring in f:
    value = itemstring.rstrip("\n").split(" ")
    print(value[0], value[1])
    directedgraph.write(str(value[0]) + "," +str(value[1]) + "\n")
    
    bidirectedgraph.write(str(value[0]) + "," +str(value[1]) + "\n")
    bidirectedgraph.write(str(value[1]) + "," +str(value[0]) + "\n")

directedgraph.close()
bidirectedgraph.close()