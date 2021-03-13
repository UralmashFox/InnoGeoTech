#!/usr/bin/env python
#coding: utf-8

import subprocess
import sys

# subprocess.check_call([sys.executable, "-m", "pip", "install", 'numpy'])
# subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
# subprocess.check_call([sys.executable, "-m", "pip", "install", 'opencv-python'])
# subprocess.check_call([sys.executable, "-m", "pip", "install", 'tqdm'])

import os
import numpy as np
import cv2
from tqdm import trange
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

print('Hi!')

parent_dir = input('Write the path please: ')
print('Directory collected!')

directory = "Processed"
# Path
path = parent_dir+ '/' +directory
# Folder creating
try:
    os.mkdir(path)
    print('Folder created!')
except:
    print('Folder already exists!')


for file in os.listdir(parent_dir):
    if file.endswith(".txt"):
        filename = parent_dir + '/' + os.path.join(file)
        filename = str(filename)
        if file.endswith("MTL.txt"):
            MTLdf = pd.read_csv(filename, delimiter = " = ")
            MTLdf = MTLdf.replace({'"':''}, regex=True)
        else:
            ANGdf = pd.read_csv(filename, delimiter = " = ")

for i in trange(1, 12 - 2):
    m_rho = 'REFLECTANCE_MULT_BAND_' + str(i)
    M_rho = float(MTLdf.loc[MTLdf['GROUP'] == m_rho, 'L1_METADATA_FILE'].values)
    a_rho = 'REFLECTANCE_ADD_BAND_' + str(i)
    A_rho = float(MTLdf.loc[MTLdf['GROUP'] == a_rho, 'L1_METADATA_FILE'].values)
    theta_SE = float(MTLdf.loc[MTLdf['GROUP'] == 'SUN_ELEVATION', 'L1_METADATA_FILE'].values)
    theta_SZ = 90 - theta_SE

    for file in os.listdir(parent_dir):
        if file.endswith('B' + str(i) + '.TIF'):
            filename = parent_dir + '/' + os.path.join(file)
            Q_cal = cv2.imread(filename, 0)
            Rho_lambda_prime = M_rho * Q_cal + A_rho
            Rho_lambda = Rho_lambda_prime / np.sin(theta_SE)
            cv2.imwrite(path + '/' + file, Rho_lambda)


print('All the processed images are there: ', parent_dir+'\\'+directory)







