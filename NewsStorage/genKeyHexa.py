import cv2
import numpy as np
from scipy.fftpack import dct

def create1dArray(imagePath):
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (32, 32))
    dctMatrix = dct(dct(image.astype(float), axis=0, norm='ortho'), axis=1, norm='ortho')
    dctArray8x8 = dctMatrix[:8, :8]
    dctArray1D = dctArray8x8.flatten()
    return dctArray1D

def createKey(imagePath):
    dctArray1D = create1dArray(imagePath)
    stdDev = np.var(dctArray1D)
    s = int(stdDev)
    med = int(10000*np.median(dctArray1D))
    key = s - med
    return key

def getHexadecimal(imagePath):
    dctArray1D = create1dArray(imagePath)
    binaryHash = ""
    median = np.median(dctArray1D[1:])
    for x in dctArray1D:
        if x > median:
            binaryHash = binaryHash + '1'
        else:
            binaryHash = binaryHash + '0'
    hexadecimalHash = '{:0{}x}'.format(int(binaryHash, 2), len(binaryHash) // 4)
    return hexadecimalHash
