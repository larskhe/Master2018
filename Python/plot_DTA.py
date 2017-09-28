## Program to read and plot .DTA files

from pylab import*
import scipy
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd


#plt.style.use('ggplot')

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

fileDir = '../Lab/Characterization/Linear_Sweep_Voltammetry/002/'

list_of_files_in_dir = []
for file in os.listdir(fileDir):
    if file.endswith(".DTA"):
    	list_of_files_in_dir.append(file)
list_of_files_to_compare = list(list_of_files_in_dir[i] for i in [2,3])

epsDir = os.path.join(fileDir, 'Figures', 'eps')
pngDir = os.path.join(fileDir, 'Figures', 'png')
if not os.path.exists(epsDir):
	os.makedirs(os.path.join(fileDir, 'Figures', 'eps'))
if not os.path.exists(pngDir):
	os.makedirs(os.path.join(fileDir, 'Figures', 'png'))

def data_collection(fileName):
	with open(fileDir + fileName, 'r') as data:
		data = data.read()
		scanRate = data.split('SCANRATE	QUANT	')[1].split('	&Scan Rate (mV/s)')[0]
		scanRate = float(scanRate.replace(',','.'))
		data = data.split('Cycle')[0]
		data_line_split = data.split('\n')
		number_of_header_rows = len(data_line_split)
	df = pd.read_csv(fileDir + fileName, sep='	',\
		header=number_of_header_rows, decimal=',')
	x = df['V vs. Ref.']
	y = df['A']
	return x,y,scanRate

def save_plot_large(x,y,fileName):
	scaling_factor_for_RHE = 0.5784
	fig = plt.figure(figsize=cm2inch(30,13))
	#fig.suptitle(fileName, fontsize=12, fontweight='light')
	ax = fig.add_subplot(1,1,1)
	ax.plot(x+scaling_factor_for_RHE,y*10**3,'-o', ms=2)
	ax.tick_params(labelsize=14)
	ax.set_xlabel(r'Potential / V$_{RHE}$',fontsize=16)
	ax.set_ylabel(r'Current / mA cm$^{-1}$',fontsize=16)
	fig.subplots_adjust(left=0.10, right=0.98, top=0.9, bottom=0.15)
	fig.savefig(pngDir + "/" + fileName + '_large' + ".png", format="png")
	fig.savefig(epsDir + "/" + fileName + '_large' + ".eps", format="eps")

def save_plot_small(x,y,fileName):
	scaling_factor_for_RHE = 0.5784
	fig = plt.figure(figsize=cm2inch(16,8))
	#fig.suptitle(fileName, fontsize=12, fontweight='light')
	ax = fig.add_subplot(1,1,1)
	ax.plot(x+scaling_factor_for_RHE,y*10**3,'-o', ms=2)
	ax.tick_params(labelsize=9)
	ax.set_xlabel(r'Potential / V$_{RHE}$',fontsize=11)
	ax.set_ylabel(r'Current / mA cm$^{-1}$',fontsize=11)
	fig.subplots_adjust(left=0.13, right=0.95, top=0.95, bottom=0.16)
	fig.savefig(pngDir + "/" + fileName + '_small' + ".png", format="png")
	fig.savefig(epsDir + "/" + fileName + '_small' + ".eps", format="eps")

def save_plot_with_underlay_large(x,y,fileName,scanRate,chopTime):

	fig = plt.figure(figsize=cm2inch(30,13))
	#fig.suptitle(fileName, fontsize=12, fontweight='light')
	ax = fig.add_subplot(1,1,1)
	ax.plot(x+0.5784,y*10**3,'-o', ms=2)
	ax.tick_params(labelsize=14)
	ax.set_xlabel(r'Potential / V$_{RHE}$',fontsize=16)
	ax.set_ylabel(r'Current / mA cm$^{-1}$',fontsize=16)
	ax.text(0.5, 0.47, r'Scan rate = %.0f mV s$^{-1}$'%(scanRate),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=14, color='black',
        alpha = 0.3,
        transform=ax.transAxes)
	ax.text(0.5, 0.53, 'Chop time = ' + str(chopTime) + ' s',
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=14, color='black',
        alpha = 0.3,
        transform=ax.transAxes)
	fig.subplots_adjust(left=0.10, right=0.98, top=0.9, bottom=0.15)
	fig.savefig(pngDir + "/" + fileName + '_withUnderlay_large' + ".png", format="png")
	fig.savefig(epsDir + "/" + fileName + '_withUnderlay_large' + ".eps", format="eps")

def save_plot_with_underlay_small(x,y,fileName,scanRate,chopTime):
	scaling_factor_for_RHE = 0.5784
	fig = plt.figure(figsize=cm2inch(16,8))
	#fig.suptitle(fileName, fontsize=12, fontweight='light')
	ax = fig.add_subplot(1,1,1)
	ax.plot(x + scaling_factor_for_RHE, y*10**3, '-o', ms=2)
	ax.tick_params(labelsize=9)
	ax.set_xlabel(r'Potential / V$_{RHE}$',fontsize=11)
	ax.set_ylabel(r'Current / mA cm$^{-1}$',fontsize=11)
	ax.text(0.5, 0.47, r'Scan rate = %.0f mV s$^{-1}$'%(scanRate),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=9, color='black',
        alpha = 0.3,
        transform=ax.transAxes)
	ax.text(0.5, 0.53, r'Chop time = %.0f s'%(chopTime),
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=9, color='black',
        alpha = 0.3,
        transform=ax.transAxes)
	fig.subplots_adjust(left=0.13, right=0.95, top=0.95, bottom=0.16)
	fig.savefig(pngDir + "/" + fileName + '_withUnderlay_small' + ".png", format="png")
	fig.savefig(epsDir + "/" + fileName + '_withUnderlay_small' + ".eps", format="eps")

def save_comparison_plot(x_list,y_list):

	fig = plt.figure(figsize=cm2inch(30,13))
	#fig.suptitle('Comparison test', fontsize=11)
	ax = fig.add_subplot(1,1,1)
	for i in range(len(list_of_files_to_compare)):
		if i==0:
			ax.plot(x_list[i]+0.5784,y_list[i]*10**3,'-o', ms=1, label='Run '+str(i+1))
		else:
			ax.plot(x_list[i]+0.5784,y_list[i]*10**3,'-o', ms=1, label='Run '+str(i+3))
	ax.tick_params(labelsize=14)
	ax.set_xlabel(r'Potential / V$_{RHE}$',fontsize=16)
	ax.set_ylabel(r'Current / mA cm$^{-1}$',fontsize=16)
	ax.legend(fontsize=14)
	fig.subplots_adjust(left=0.10, right=0.98, top=0.9, bottom=0.15)
	fig.savefig(pngDir + "/" + ' vs. ' + ".png", format="png")
	fig.savefig(epsDir + "/" + ' vs. ' + ".eps", format="eps")
'''
for file in list_of_files_in_dir:
	x,y,scanRate = data_collection(file)
	#save_plot_large(x,y,file)
	file = file.replace('.DTA','')
	save_plot_small(x,y,file)
	save_plot_with_underlay_large(x,y,file,scanRate,2)
	save_plot_with_underlay_small(x,y,file,scanRate,2)
'''
x_list = []
y_list = []
for file in list_of_files_to_compare:
	x,y,scanRate = data_collection(file)
	x_list.append(x)
	y_list.append(y)

save_comparison_plot(x_list,y_list)



