'''
Created on May 2, 2015

@author: hehehehehe
'''
import wave    
import matplotlib.pyplot as plt
from scipy.io import wavfile # get the api
from scipy.fftpack import fft
from pylab import *
import scipy as cp
import struct
import numpy
import os


def getMSD(d1, d2):
    diff = 0
    d11 = []
    d22 = []
    
    index = 0
     
    for index in xrange(9):
        chunk = d1[index * 22050: index * 22050 + 22050]
        x = cp.fft(chunk)
        maximum1 = max(x)
        d11.append(maximum1)
         
    index = 0
    for index in xrange(9):
        chunk = d2[index * 22050: index * 22050 + 22050]
        x = cp.fft(chunk)
        maximum1 = max(x)
        d22.append(maximum1)
    
    currentMax1 = max(d11)
    currentMax2 = max(d22)
    
    for x in xrange(len(d11)):
#         diff += abs(d11[x]/currentMax1 - d22[x]/currentMax2) * abs(d11[x]/currentMax1 - d22[x]/currentMax2)
        diff += abs(d11[x] - d22[x]) * abs(d11[x] - d22[x])
        

    diff /= len(d11)
    
    return diff

def getScore( basefile,queryfile ):
    inputfile = basefile
    inputqueryfile = queryfile
    
    originfs,orgindata = wavfile.read(inputfile)
    queryfs,querydata = wavfile.read(inputqueryfile)
    
    orgindata = orgindata / (2.**15)
    querydata = querydata / (2.**15)
    
    originMono = orgindata[:,0];
    totalLendiff = 44100 * 20 - len(originMono)
    originMono1 = np.zeros(44100 * 20)
    
    if(totalLendiff >= 0):
        for x in xrange(len(originMono)):
            originMono1[x] = originMono[x]
        for x in xrange(totalLendiff-1):
            originMono1[len(originMono) + 1+x] = 0
    else:
        for x in xrange(len(originMono1)):
            originMono1[x] = originMono[x]
   
    queryMono = querydata[:,0];
    totalLendiff1 = 44100 * 5 - len(queryMono)
    queryMono1 = np.zeros(44100 * 5) 
    
    if(totalLendiff1>=0):
        for x in xrange(len(queryMono)):
            queryMono1[x] = queryMono[x]
        for x in xrange(totalLendiff1-1):
            queryMono1[len(queryMono)+1+x] = 0
    else:
        for x in xrange(len(queryMono1)):
            queryMono1[x] = queryMono[x]
        
    #subset
    interval = 44100 * 5
    diffList = []
    
    # shi yu
#     chunkOriginMono = numpy.fft.fft(originMono1,131072)
#     chunkQueryMono = numpy.fft.fft(queryMono1,131072)
    
#     for ind in xrange(30):
#         temp=originMono1[ind * 44100 * 0.5: ind * 0.5 * 44100+interval]
#         
#         diff = getMSD(temp,queryMono1)
#         diffList.append(diff)
#         
# #     print diffList
#     MSD = min(diffList)
       
#     return MSD
    
    chunkOriginMono = numpy.fft.fft(originMono,131072)
    chunkQueryMono = numpy.fft.fft(queryMono,131072)
    
    mageOrigin =  numpy.abs(chunkOriginMono)
    mageQuery =  numpy.abs(chunkQueryMono)
    
    
    ratio = []
    for x in xrange(0,50000):
        if mageOrigin[x] == 0:
            ratio.append(1)
        else:
            ratio.append(mageQuery[x] /mageOrigin[x])
    
    N = len(ratio)
    narray = numpy.array(ratio)
    sum1 = narray.sum()
    narray2 = narray * narray
    sum2 = narray2.sum()
    mean = sum1 / N 
    var = sum2 / N - mean ** 2
    
    
    return var

def getBaseData():
#     queryFile = '/Users/hehehehehe/Downloads/new queries/From Searching Content/Q1/Q1.wav'
    queryFile = '/Users/hehehehehe/Desktop/workspace/final/query/first/first.wav'
    path = "/Users/hehehehehe/Desktop/workspace/CSCI576_Project_Database/"
    subpath = ["sports/sports.wav","flowers/flowers.wav","interview/interview.wav","movie/movie.wav","musicvideo/musicvideo.wav","starcraft/starcraft.wav","traffic/traffic.wav"]
    
    for sub in subpath:
        currentFile = path+sub
        print sub ,"\t\t", getScore(currentFile,queryFile)


def FFT():
    inputfile = '/Users/hehehehehe/Desktop/workspace/final/query/first/first.wav'

    fs, data = wavfile.read(inputfile) # load the data
    a = data.T[0] # this is a two channel soundtrack, I get the first track
    b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    c = numpy.fft.fft(a, 1024) # create a list of complex number
    
#     print len(c)
    
#     d = len(c)/2  # you only need half of the fft list
#     plt.plot(abs(c[:(d-1)]),'r') 
#     plt.show()

def test():
    rate, data = wavfile.read('/Users/hehehehehe/Desktop/workspace/final/data/musicvideo/musicvideo.wav')
    filtereddata = numpy.fft.rfft(data, axis=0)
    print (data)
    filteredwrite = numpy.fft.irfft(filtereddata, axis=0)
    print (filteredwrite)
    wavfile.write('TestFiltered.wav', rate, filteredwrite)
    
def f(filename):
    fs, data = wavfile.read(filename) # load the data
    a = data.T[0] # this is a two channel soundtrack, I get the first track
    b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    c = fft(b) # create a list of complex number
    print c
    d = len(c)/2  # you only need half of the fft list
    plt.plot(abs(c[:(d-1)]),'r')
    savefig(filename+'.png',bbox_inches='tight')
    
def read_wave_data(file_path):  
    #open a wave file, and return a Wave_read object  
    f = wave.open(file_path,"rb")  
    #read the wave's format infomation,and return a tuple  
    params = f.getparams()  
    #get the info  
    nchannels, sampwidth, framerate, nframes = params[:4]  
    #Reads and returns nframes of audio, as a string of bytes.   
    str_data = f.readframes(nframes)  
    #close the stream  
    f.close()  
    #turn the wave's data to array  
    wave_data = np.fromstring(str_data, dtype = np.short)  
    #for the data is stereo,and format is LRLRLR...  
    #shape the array to n*2(-1 means fit the y coordinate)  
    wave_data.shape = -1, 2  
    #transpose the data  
    wave_data = wave_data.T  
    #calculate the time bar  
    time = np.arange(0, nframes) * (1.0/framerate)  
    return wave_data, time  
#   
# def main():  
#     wave_data, time = read_wave_data('/Users/hehehehehe/Desktop/workspace/final/data/musicvideo/musicvideo.wav')   
#     wave_data1, time1 = read_wave_data('/Users/hehehehehe/Desktop/workspace/final/query/first/first.wav')     
#     #draw the wave  
#     plt.subplot(211)
#     #print wave_data
#     plt.plot(time, wave_data[0])  
#     plt.subplot(212)  
#     plt.plot(time, wave_data[1], c = "g")  
#     plt.show()  
#   
if __name__ == "__main__":  
#     FFT()
    getBaseData()