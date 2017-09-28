#!/usr/bin/python3

import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import codecs

plt.style.use('ggplot')

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

fileDir = '../Lab/XRD/all_in_one/'
custom_dir = '/Users/lars/Skole/Master/Thesis/LaTeX/Figures'

list_of_files_in_dir = []
for file in os.listdir(fileDir):
    if file.endswith(".ras"):
        list_of_files_in_dir.append(file)
# print(list_of_files_in_dir)

epsDir = os.path.join(fileDir,"Images", "eps")
pngDir = os.path.join(fileDir,"Images", "png")
if not os.path.exists(epsDir):
    os.makedirs(os.path.join(fileDir, "Images", "eps"))
if not os.path.exists(pngDir):
    os.makedirs(os.path.join(fileDir, "Images", "png"))

def data_collection(fileName):
    
    with codecs.open(fileDir + fileName, 'r',encoding='ascii', errors='ignore') as data:
        data = data.read()
        scan_step = float(data.split('*MEAS_SCAN_STEP "')[1].split('"')[0])
        scan_start = float(data.split('MEAS_SCAN_START "')[1].split('"')[0])
        scan_stop = float(data.split('MEAS_SCAN_STOP "')[1].split('"')[0])
        data = data.split('RAS_INT_START')[0]
        data_line_split = data.split('\n')
        headerRows = len(data_line_split)

    with codecs.open(fileDir + fileName, 'r',encoding='ascii', errors='ignore') as data:
        data = data.read()
        data = data.split('*RAS_INT_END')[1]
        data_line_split = data.split('\n')
        footerRows = len(data_line_split)
    
    df = pd.read_csv(fileDir + fileName, header=headerRows, sep=' ',  skipfooter=footerRows,\
            engine='python', names = ["Angle", "Intensity", "Error"])
    
    if want_custom_angle == True:
        start_angle = (wanted_start_angle - scan_start) / scan_step
        end_angle = (wanted_end_angle - scan_start) / scan_step
        df = df.loc[start_angle:end_angle, :]

    return df['Angle'], df['Intensity']

def save_plot_large(two_theta,intensity,fileName):
    fig = plt.figure(figsize=cm2inch(30,13))
    #fig.suptitle(fileName, fontsize=12, fontweight='light')
    ax = fig.add_subplot(1,1,1)
    ax.plot(two_theta,intensity, lw=1)
    ax.tick_params(labelsize=14)
    ax.set_xlabel(r'$\theta/2\theta$',fontsize=16)
    ax.set_ylabel(r'A.u.',fontsize=16)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.9, bottom=0.15)
    fig.savefig(pngDir + "/" + fileName + '_large' + ".png", format="png")
    fig.savefig(epsDir + "/" + fileName + '_large' + ".eps", format="eps")
    ## Include if want to save to LaTeX custom directory as well
    '''
    user_input = input(' Want to save \n %s \n to \n %s \n as well? (y/n)' %(fileName, custom_dir))
    if user_input == 'y':
        fig.savefig(custom_dir + "/" + fileName + '_small' + ".eps", format="eps")
    '''
def save_plot_small(two_theta,intensity,fileName):
    fig = plt.figure(figsize=cm2inch(16,8))
    #fig.suptitle(fileName, fontsize=12, fontweight='light')
    ax = fig.add_subplot(1,1,1)
    ax.plot(two_theta,intensity, lw=1)
    ax.tick_params(labelsize=9)
    ax.set_xlabel(r'Potential / V$_{RHE}$',fontsize=11)
    ax.set_ylabel(r'Current / mA cm$^{-1}$',fontsize=11)
    fig.subplots_adjust(left=0.13, right=0.95, top=0.95, bottom=0.16)
    fig.savefig(pngDir + "/" + fileName + '_small' + ".png", format="png")
    fig.savefig(epsDir + "/" + fileName + '_small' + ".eps", format="eps")
    '''
    ## Include if want to save to LaTeX custom directory as well
    user_input = input(' Want to save \n %s \n to \n %s \n as well? (y/n)' %(fileName, custom_dir))
    if user_input == 'y':
        fig.savefig(custom_dir + "/" + fileName + '_small' + ".eps", format="eps")
    '''

def save_comparison_plot(two_theta,intensity_array):
    
    #fig.suptitle(fileName, fontsize=12, fontweight='light')
    
    for n in range(len(intensity_array[0])):
        intensity_array[:,n] += max(intensity_array[:,n-1])*1.05

    fig = plt.figure(figsize=cm2inch(30,30))
    ax = fig.add_subplot(1,1,1)
    ax.plot(two_theta,intensity_array, lw=1)
    ax.tick_params(labelsize=9)
    ax.set_xlabel(r'$\theta/2\theta$',fontsize=11)
    ax.set_ylabel(r'A.u.',fontsize=11)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.10)
    fig.savefig(pngDir + "/" + 'Comparison_of_the_above' + ".png", format="png")
    fig.savefig(epsDir + "/" + 'Comparison_of_the_above' + ".eps", format="eps")
    '''
    ## Include if want to save to LaTeX custom directory as well
    user_input = input(' Want to save \n %s \n to \n %s \n as well? (y/n)' %(fileName, custom_dir))
    if user_input == 'y':
        fig.savefig(custom_dir + "/" + fileName + '_small' + ".eps", format="eps")
    '''
    

intensity_list = []

wanted_start_angle = 30
wanted_end_angle = 85

for file in list_of_files_in_dir:

    want_custom_angle = 1  ## 0 = No, 1 = Yes
    two_theta,intensity = data_collection(file)
    intensity_list.append(intensity)
    intensity_array = np.column_stack(intensity_list)
    #save_plot_large(two_theta,intensity,file)
    save_plot_small(two_theta,intensity,file)

#save_comparison_plot(two_theta,intensity_array)
