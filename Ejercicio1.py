# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 23:46:02 2021

@author: yessi
"""

###   PASO 1: HACER UNA LISTA CON LOS ARCHIVOS .AS Y CREAR LOS ARCHIVOS DE OBSERVACION


import os

cwd= os.getcwd()    

for root, dirs, files in os.walk(cwd): 
    for ASfile in files:
            if ASfile.endswith(".AS"):
                os.system("teqc -O.dec 30 +obs {}.o {}".format(ASfile.split("_")[0],ASfile))     


###     PASO 2 EXTRAER LOS DATOS

    
for root, dirs, files in os.walk(cwd): 
    for ASfile in files:
        if ASfile.endswith(".o"):
            with open("ASfile") as f:
                lines=f.readlines()[9:10]
                for line in lines:
                      new_line = line.strip().split(' ')
                      print(new_line)
                    
                    
                    
                    
                    