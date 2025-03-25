# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:31:51 2022

@author: ilias
"""

import numpy as np
from scipy import stats
from pylab import *
import matplotlib.pyplot as plt



from scipy import signal
from scipy.fft import fftshift

from PIL import Image
from scipy import signal
from scipy.fft import fftshift
import time
import warnings


print("********** START **********")
print("********** IBO ***********")
print("Projet generation des spectres de réponses")
# Lancement du chronomètre
start_time = time.time()
c=0
while  c==0 :
# Number of samplepoints
   N = 320
# sample spacing
   T = 40 #durée enregistrée de séisme en s
   temps = np.linspace(0.0, T, N)
#Données statistiques des séismes
#onde P
   sigmap=0.1
   mup=0
#onde S
   sigmas=0.154
   mus=0.05
#génération du signal sismique
   d = np.concatenate((stats.norm.rvs(mup,sigmap,100),stats.norm.rvs(mus,sigmas,150),stats.norm.rvs(0.01,1.2,50),(stats.norm.rvs(mup,sigmap+0.1,20))))
# Tracé du signal sismique sample N
   d=exp(-(temps-20)**2/20**2)*d 
   plot(temps,d)
   show()

#Génération du spectre de réponse
#amortissement 
   x=0.05
#incrément de temps
   delta_T=temps[2]-temps[1]
#initialisation
   u=np.zeros((N))
   v=np.zeros((N))
   a=np.zeros((N))
   T=np.arange(0.7,100,0.1)
   Su=np.zeros(shape(T))
   Sv=np.zeros(shape(T))
   Sa=np.zeros(shape(T))
#shéma explicite de newmark
   beta=1/6
   gamma=1/2
   for i in range(0, 993):
       w=2*pi/T[i]
       for j in range(0,N-1):
           a[j+1]=(d[j+1]-w**2*u[j]-(2*x*w+2*delta_T*w**2)*v[j]-w*delta_T*(2*x*(1-gamma)+w*delta_T*(1-2*beta)/2)*a[j])/(1+((w*delta_T)**2)*beta+2*x*w*gamma)
           v[j+1]=v[j]+delta_T*((1-gamma)*a[j]+gamma*a[j+1])
           u[j+1]=u[j]+delta_T*v[j]+delta_T**2/2*((1-2*beta)*a[j]+2*beta*a[j+1])
       Sa[i]=np.max(a)
       Sv[i]=np.max(v)
       Su[i]=np.max(u)
       u=np.zeros((N))
       v=np.zeros((N))
       a=np.zeros((N))
       if Sv[0]>0.13:
          c=c+1 
#génération du spectre de réponse
plot(T,Sa)
plt.xscale('log')
plt.xlabel('periode en s')
plt.ylabel('acceleration en m/s2')
show()
plot(T,Su)
plt.xlabel('periode en s')
plt.ylabel('deplacement en m')
plt.xscale('log')
plt.show()
plot(T,Sv)
plt.xlabel('periode en s')
plt.ylabel('vitesse en m/s')
plt.xscale('log')
plt.show()
plot(1/T,Sv)
plt.xlabel('FREQUENCY en HZ')
plt.ylabel('vitesse en m/s')
plt.xscale('log')
plt.show()
print(Sa[0])
print(Sv[0])
#vitesse en m/S
Vs= np.concatenate((stats.norm.rvs(70,60,100), stats.norm.rvs(200,300,100), stats.norm.rvs(700,800,300), stats.norm.rvs(1600,100, 700)))

#Poids volumique de sol
#Profondeur en m
h=1200
f=linspace(0,h,1200)
plot(f,Vs)
plt.ylabel('Velocity(m/s)')
plt.xlabel('depth (m)')
show()
#duree de simulation en s
T=40
#Maillage

Nt=320
Nz=6
t1=T/Nt
z=h/Nz
# Initialisation
s=(Nt,Nz)
U=np.zeros(s)
Z=np.linspace(0,h,Nz)
U[0,:]=1
U[:,0]=d
U[1,:]=U[0,:]
for i in range(1,Nt-2):
    for j in range(1,Nz-2):
        U[i+1,j]=2*U[i,j]-U[i-1,j]+(t1/z)**2*(Vs[j+1]**2*(U[i,j+1]-U[i,j])-Vs[j]**2*(U[i,j]-U[i,j-1]))
        
#Condition de Neumann
for i in range(1,Nt-2):
    U[i+1,Nz-1]=2*U[i,Nz-1]-U[i-1,Nz-1]+2*(t1/z)**2*Vs[Nz-1]**2*(U[i,Nz-2]- U[i,Nz-1]) 
Onde=np.transpose(U)           



plt.plot(temps, U[:,1], label='depth 200m')   
plt.plot(temps, U[:,2], label='depth 400m')  
plt.plot(temps, U[:,3], label='depth 600m') 
plt.plot(temps, U[:,4], label='depth 800m') 
plt.plot(temps, U[:,5], label='depth 1000m') 
 
 
plt.title('Seismic amplification in heterogenous soil media')      
plt.xlabel('time(s)')                     
plt.ylabel('acceleration (m/s2)')                      
plt.legend()                        
plt.grid()                          
plt.show()                          




 


#génération de spectrogramme

fs=320/40
y=[0]*len(U[:,2])
f, t, Sxx = signal.spectrogram(U[:,3], fs, window=signal.get_window('hann',32))
freq_lim = 33
Sxx_red = Sxx[np.where(f < freq_lim)]
f_red = f[np.where(f < freq_lim)]
plt.plot(temps, y)
plt.pcolormesh(t, f_red, Sxx_red, shading='gouraud')
plt.ylabel('Fréquence (Hz)')
plt.xlabel('Temps (s)')
plt.title('Spectrogramme')
plt.show()
#######################
### MESSAGES DE FIN ###
#######################
# Arrêt du chronomètre
print("\nTemps écoulé: %.3f s" % (time.time() - start_time))
# Message de fin
print("\n********** END **********")
