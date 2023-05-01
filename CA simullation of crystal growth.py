# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:08:19 2023

@author: Shalom
"""

import numpy as np
import math
import random
import time
from itertools import cycle 
import matplotlib.pyplot as plt
from matplotlib import cm

clock1=time.time()

''' Defining a class name Layer to run the simulation 
    z =0,1,2,3,4 --> particle mobility
    relaxtion_time = number of time steps after which deposition will happen'''
class Layer():
    
   
    def __init__(self,length,width,TAU,THETA,z):     #defining the constructure
        self.length=length      #length of the matrix
        self.width=width       #width of the marix
        self.Z=z
        
        
        # defining the initial parameters
        self.relaxtion_time = int(TAU * self.length *self.width)       #Relaxation time --> No.of step after which deposition will happen 
        self.theta_dep=int(THETA* self.length *self.width)    #number of deposition 
         
        
    ''' Defining four preodic boundary '''
        
    def point(self,row,col):     # preiodic bounday for up-point 
         return [((row-1)-((math.floor((row-1)/(self.length)) * (self.length))),col),
                 ((row+1)-((math.floor((row+1)/(self.length)) * (self.length))),col),
                 (row,(col-1)-((math.floor((col-1)/(self.width))*(self.width)))),
                 (row,(col+1)-((math.floor((col+1)/(self.width))*(self.width))))]
     
    def neighbour(self,arr,row,col):
        c=[]
        l=self.point(row,col)
        
        if  (arr[row,col] == arr[l[0]]) :   #up-neighbouring point 
            c.append((l[0]))
            
        if (arr[row,col] == arr[l[1]]):  #down-neighbouring point 
            c.append((l[1]))
            
        if (arr[row,col] == arr[l[2]]): #left-neighbouring point 
            c.append((l[2]))
            
        if (arr[row,col] == arr[l[3]]):   #right-neighbouring point 
            c.append((l[3]))
        
        return c
    
    def vaccant_site(self,arr,row,col):
        c=[]
        l=self.point(row,col)
        
        if (arr[row,col] > arr[l[0]]):   #up-vaccant site 
            c.append((l[0]))
            
        if (arr[row,col] > arr[l[1]]):  #down-vaccant site 
            c.append((l[1]))
            
        if (arr[row,col] > arr[l[2]]): #left-vaccant site
            c.append((l[2]))
            
        if (arr[row,col] > arr[l[3]]):   #right-vaccant site 
            c.append((l[3]))
        
        return c
    
    def deposition(self,arr,b):
          ''' method for depositing on the existing layer,
              input: arr = array , b = int --> non-zero value
              return: arr = array'''
              
          for i in range(self.theta_dep):
              arr[random.randint(0,self.length-1),random.randint(0,self.width-1)] += b #random.randint function return a random value
              
          return arr
    def simulation(self,arr,theta_max,m):
          n=0;i=0;count=0
          
          arr_3d=np.zeros((self.length,self.width))
    
          for k in cycle(range(0,1)):
              if np.mean(arr)> theta_max :
                  break
              
              # self.mean_std(arr,count)
              arr_depo=np.zeros((self.length,self.width))  
              arr_depo=self.deposition(arr_depo, 1)        
              
              arr= arr + arr_depo
              self.mean_std(arr,count)
              if n % m==0:
                 # print(i)
                 i+=1
                 arr_3d=np.append(arr_3d,arr,axis=0)
                 self.plot_3d(arr)
                 
              n+=1
              
              
              for j in range(self.relaxtion_time): 
                    
                  
                    
                    count +=1   #total time variable
                    row,col=random.randint(0,self.length-1),random.randint(0,self.width-1)
                  
                    neighbour=self.neighbour(arr, row, col)
                    
                    if arr[row,col] !=0:
                           
                            
                            if len(neighbour)<self.Z :
                                vaccant_sites=self.vaccant_site(arr, row, col)
                                
                                if len(vaccant_sites)==0:
                                    pass
                                else: 
                                    x,y=random.choice(vaccant_sites)
                                    arr[row,col] -=1
                                    arr[x,y] +=1
                            
                            
                             
                              
        
          
          print(f"Time taken : {count}")
          arr_3d=np.reshape(arr_3d,(i+1,self.length,self.width))
          
          return arr_3d                 
        
    ''' Code for plotting and stastical calculation'''    
    def plot_3d(self,arr):
       fig = plt.figure()
       
       ax = plt.axes( projection='3d')
       ax.set_zlim(0,theta_max)
       x_data, y_data = np.meshgrid( np.arange(arr.shape[1]),
                              np.arange(arr.shape[0]) ) 
       
       ax.set(xlabel='matrix-width', ylabel='matrix-length', zlabel='growth with time')
       x_data = x_data.flatten()
       y_data = y_data.flatten()
       z_data = arr.flatten()
       cmap = cm.get_cmap('jet') # Get desired colormap - you can change this!
       max_height = np.max(z_data)   # get range of colorbars so we can normalize
       min_height = np.min(z_data )
       # scale each z to [0,1], and get their rgb values
       rgba = [cmap((k-min_height)/max_height) for k in z_data] 
       ax.bar3d( x_data,
              y_data,
              np.zeros(len(z_data)),
              1, 1, z_data ,color=rgba)
       fig.savefig(f"deposition {self.theta_dep} relaxation time {self.relaxtion_time} array length {self.length} array width {self.width} z- {self.Z}.jpeg")
           
  
          
    def mean_std(self,arr,time):
        mean = np.mean(arr)
        standard_deviation = np.std(arr)
        with open(f"deposition {self.theta_dep} relaxation time {self.relaxtion_time} array length {self.length} array width {self.width} z- {self.Z}.txt",'a') as f:
            f.write(str(mean)+"\t"+ str(standard_deviation)+"\t"+ str(np.max(arr))+"\t"+ str(np.min(arr))+"\t"+str(time)+"\n")
    
    def prt(self):
        with open(f"deposition {self.theta_dep} relaxation time {self.relaxtion_time} array length {self.length} array width {self.width} z- {self.Z}.txt",'a') as f:
            f.write("mean"+"\t"+ "standard_deviation"+"\t"+ "maximum"+"\t"+ "minimum"+"\t"+"time"+"\n")
    
   
        
if __name__=='__main__':
    length=100 ; width =100; theta_max=10; tau=0.1 ;theta=0.1;z=3;m=2
    obj=Layer(length,width,tau,theta,z)
    arr=np.zeros((length,width))#, dtype=np.uint16)
    obj.prt()
    p=obj.simulation(arr, theta_max,m)
   
    clock2=time.time()
    print("Total time taken for excutaion of program is :", clock2-clock1)