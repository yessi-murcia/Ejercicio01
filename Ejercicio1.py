# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 23:46:02 2021

@author: yessi
"""

###   PASO 1: HACER UNA LISTA CON LOS ARCHIVOS .AS Y CREAR LOS ARCHIVOS DE OBSERVACION


import os
import math
import statistics
from tkinter import filedialog #For browse files

AS_files = []

X_list = []

Y_list = []

Z_list = []

cwd = os.getcwd() #Get current directory

def list_ASfiles(cwd):
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if file[-3:] == '.AS':
                AS_files.append(file)
                
list_ASfiles(cwd)

def convert_obs(AS_files):
    for file in AS_files:
        #Convert files
        out_name = file.split('_')[0]+'.o'
        os.system ('teqc.exe -O.dec 30 +obs ' + out_name + ' ' + file)
        
convert_obs(AS_files)

def extract_coordinates():
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if file[-2:] == '.o':
                with open(file) as f:
                    lines = f.readlines()[9:10]
                    for line in lines:
                        new_line = line.strip().split(' ')
                        x = float(new_line[0])
                        X_list.append(x)
                        y = float(new_line[1])
                        Y_list.append(y)
                        z = float(new_line[3])
                        Z_list.append(z)

extract_coordinates()

print('Coordenadas Geocentricas')

X_mean = statistics.mean(X_list)
Y_mean = statistics.mean(Y_list)
Z_mean = statistics.mean(Z_list)
       
print(f'X = {X_mean}')
print(f'Y = {Y_mean}')
print(f'Z = {Z_mean}')

def convert_degress(phi, lamb):
    '''
    Toma dos parámetros con los ángulos phi(φ) y lambda (λ), expresados en radianes
    y los convierte a grados
    
    phi, lamb (float): dos variables con los angulos en radianes
    
    devuelve: una tupla, phi y lambda expresados en grados
    '''
    lamb_deg = math.degrees(lamb)
    phi_deg = math.degrees(phi)
    return lamb_deg, phi_deg


def calcular_parametros(X, Y, Z):
    (a,b) = (6378137, 6356752.31424)
    #Calcula la primera excentricidad (e)
    e = ((a**2) - (b**2))/(a**2)
    #Calcula la segunda excentricidad (e_prim)
    e_prim = ((a**2) - (b**2))/(b**2)
    #Calcula el valor de p (p)
    p = math.sqrt((X**2) + (Y**2))
    #Calcula el valor de ϴ (theta)
    theta = math.atan((Z*a)/(p*b))
    #Calcula el valor de φ (phi)
    phi = math.atan((Z+(e_prim)*b*(math.pow(math.sin(theta),3)))/(p-(e)*a*(math.pow(math.cos(theta),3))))
    #Calcula el valor de N (N)
    N = a/(math.sqrt(1-(e)*(math.sin(phi)**2)))
    #Calcula el valor de h (h) o altura elipsoidal
    h = (p/math.cos(phi))-N
    #Calcula el valor de λ (lamb)
    lamb = math.atan(Y/X)
    #Convierte el valor de λ y φ a grados (lamb_deg, phi_deg) utilizando la función convert_degress(phi, lamb)
    (lamb_deg, phi_deg) = convert_degress(phi, lamb)
    #Muestrale al usuario los resultados finales
    print('\nCoordenadas Geodesicas')
    print('φ =',phi_deg)
    print('λ =',lamb_deg)
    print('h =',h)
    with open('Coordenadas.csv', 'w') as coord:
        coord.write('LAT,LONG,ALTURA\n')
        coord.write(str(phi_deg) + ',' + str(lamb_deg) + ',' + str(h) + '\n')
    #return lamb_deg, phi_deg, h
    
calcular_parametros(X_mean, Y_mean, Z_mean)                   
