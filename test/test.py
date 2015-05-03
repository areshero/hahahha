import os
import cv2
from datetime import datetime
import time
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('Agg')
from scipy.cluster.vq import *
import pylab
import matplotlib.pyplot as plt
import cv2.cv as cv

import sqlite3
conn = sqlite3.connect('example.db:memory:')

class MotionDetectorInstantaneous():
    
    def getMSD(self,a,b):
        result = 0
        return result
    
    def saveQueryColorData(self):
        
        path = "/Users/hehehehehe/Desktop/mac/576/final/query/"
        subpath = ["first","second"]
        
        for sub in subpath:
            currentPath = os.listdir(path+sub)
            index = 0
            colorqueryResultFile = open("/Users/hehehehehe/Desktop/576/querydata/"+sub+".txt","w")
            while index < len(currentPath):
                suffix = currentPath[index].split(".")[-1]
                if suffix == "wav":
                    print suffix
                    index += 1
                if suffix == "rgb":
                    file1 = path + sub + "/" + currentPath[index]
                    res = self.getDominateColor(file1)
                    rrr = sub+str(index) +" "+ str(res[0]) + " " + str(res[1])+" " + str(res[2]) + "\n"
                    colorqueryResultFile.write(rrr)
                    index += 1
        return 
    
    def saveQueryMotionData(self):
        path = "/Users/hehehehehe/Desktop/mac/576/final/CSCI576_Project_Database/"
        subpath = ["sports","flowers","interview","movie","musicvideo","starcraft","traffic"]
        
        for sub in subpath:
            currentPath = os.listdir(path+sub)
            index = 0
            while index < len(currentPath)-1:
                
                suffix = currentPath[index].split(".")[-1]
                if suffix == ".DS_Store":
                    index += 1
                    continue
                if suffix == "wav":
                    print suffix
                    index += 1
                if suffix == "rgb":
                    file1 = path + sub + "/" + currentPath[index]
                    file2 = path + sub + "/" + currentPath[index + 1]
                    res = self.getMotion(file1, file2)
                    print str(res) +"    "+ str(file1) +"    " + str(file2)
                    index += 1
        return list
    
    
    def saveOriginMotionData(self):
        basePath = "/Users/hehehehehe/Desktop/576/database/"
        
        files = os.listdir(basePath)
        for queryDir in files:
            if queryDir == ".DS_Store":
                continue
            
            dataFolder = basePath + queryDir 
            queryFiles = os.listdir(dataFolder)
            
            for index in xrange(len(queryFiles) - 2):
                currentFile = queryFiles[index]
                suffix = currentFile.split(".")[-1]
                
                if suffix == "wav":
                    index += 1
                    continue
                if suffix == "rgb":
                    currentFileFullPath = basePath + queryDir+ "/"+ currentFile
                    file1 = basePath + queryDir + "/" + queryFiles[index]
                    file2 = basePath + queryDir + "/" + queryFiles[index+1]
                    file3 = basePath + queryDir + "/" + queryFiles[index+2]
                    motionResult = self.getMotion(file1, file2,file3)
                    print file2
                    print motionResult
                    break
                    
                    index += 3
        
#         
#         
#         for sub in subpath:
#             currentPath = os.listdir(path+sub)
#             index = 0
#             while index < len(currentPath)-1:
#                 
#                 suffix = currentPath[index].split(".")[-1]
#                 if suffix == ".DS_Store":
#                     index += 1
#                     continue
#                 if suffix == "wav":
#                     print suffix
#                     index += 1
#                 if suffix == "rgb":
#                     file1 = path + sub + "/" + currentPath[index]
#                     file2 = path + sub + "/" + currentPath[index + 1]
#                     res = self.getMotion(file1, file2)
#                     print str(res) +"    "+ str(file1) +"    " + str(file2)
#                     index += 1
        return list
    
    
    def extractDominateColor(self,queryFile):
        path = "/Users/hehehehehe/Desktop/576/traineddata/"
        path2 = [queryFile]
        
        colors = []
        trainedDataFiles = os.listdir(path)
        for cQueriedData in path2:
            if str(cQueriedData) == ".DS_Store":
                continue
            currentFile = open(cQueriedData,"r" )
            content = currentFile.readlines()
            queryArray = []
            for x1 in content:
                d = x1.split(" ")
                name = d[0]
                r = float(d[1])
                g = float(d[2])
                b = float(d[3])
                queryArray.append( (r,g,b) )
                
            indexs = []    
            for cTrainedData in trainedDataFiles:
                currentFile = open(path + cTrainedData,"r")
                content = currentFile.readlines()
                contentArray = []
                for x1 in content:
                    d = x1.split(" ")
                    name = d[0]
                    r = float(d[1])
                    g = float(d[2])
                    b = float(d[3])
                    contentArray.append( (r,g,b) )
                
                #for every query
                finalresult = []
                for x in xrange(450):
                    result = []
                    for y in xrange(150):
                        temp = (queryArray[y][0]-contentArray[y+x][0],
                                queryArray[y][1]-contentArray[y+x][1],
                                queryArray[y][2]-contentArray[y+x][2])
                        r = abs(temp[0]) + abs(temp[1]) +abs(temp[2])
                        result.append(r)
                    finalresult.append(sum(result))
                index = min(finalresult)
                indexs.append((cTrainedData,index))
                
            colors.append((cQueriedData,indexs))           

        string = ""
        list = dict()
        
        for k,v in colors:
            for k1,v1 in v:
                list[k1] = v1
                string +=  k1+":"+str(v1) + ";"
                
                
        return string,list
        
    def getDominateColor(self,fileName):    
        width = 352
        height = 288
        blank_image = np.zeros((height,width,3), np.uint8)
        data = np.fromfile(fileName,dtype=np.uint8)
        
        index = 0;
        r ,g , b= [], [],[]
        
        for y in xrange(height):
            for x in xrange(width):
                red = data[index]
                green = data[index+width*height]
                blue = data[index+height*width*2]
                blank_image[y][x] = (blue,green,red)
                index+=1
                
        blank_image=blank_image.reshape(1,width*height,3)
        blank_image = np.float32(blank_image)
        
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret,label,center=cv2.kmeans(blank_image,1,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        return center[0]
    
    def extractMotion(self,queryFile):       
        
        path = "/Users/hehehehehe/Desktop/mac/576/final/CSCI576_Project_Database/"
        subpath = ["sports","flowers","interview","movie","musicvideo","starcraft","traffic"]
        
        querypath = "/Users/hehehehehe/Desktop/workspace/final/query/first/"+queryFile
        
        for sub in subpath:
            currentPath = os.listdir(path+sub)
            index = 0
            while index < len(currentPath)-1:
                
                suffix = currentPath[index].split(".")[-1]
                if suffix == ".DS_Store":
                    index += 1
                    continue
                if suffix == "wav":
                    print suffix
                    index += 1
                if suffix == "rgb":
                    file1 = path + sub + "/" + currentPath[index]
                    file2 = path + sub + "/" + currentPath[index + 1]
                    res = self.getMotion(file1, file2)
                    print str(res) +"    "+ str(file1) +"    " + str(file2)
                    index += 1
        return list
                    
    def getMotion(self,fileName,fileName1,fileName2):
        width = 352
        height = 288
        
        blank_image = np.zeros((height,width,3), np.uint8)
        blank_image1 = np.zeros((height,width,3), np.uint8)
        blank_image2 = np.zeros((height,width,3), np.uint8)
        
        data = np.fromfile(fileName,dtype=np.uint8)
        data1 = np.fromfile(fileName1,dtype=np.uint8)
        data2 = np.fromfile(fileName2,dtype=np.uint8)
        
        index = 0;
        
        for y in xrange(height):
            for x in xrange(width):
                
                red = data[index]
                green = data[index+width*height]
                blue = data[index+height*width*2]
                blank_image[y][x] = (blue,green,red)
                
                red1 = data1[index]
                green1 = data1[index+width*height]
                blue1 = data1[index+height*width*2]
                blank_image1[y][x] = (blue1,green1,red1)
                
                red2 = data2[index]
                green2 = data2[index+width*height]
                blue2 = data2[index+height*width*2]
                blank_image2[y][x] = (blue2,green2,red2)
                
                index+=1
        
        #print blank_image
        frame = cv.fromarray(blank_image)
        frame1 = cv.fromarray(blank_image1)
        frame2 = cv.fromarray(blank_image2)
        
        cv.NamedWindow("Image")
#         cv.ShowImage("Res",frame)
#         cv.ShowImage("Res",frame1)
        
        frame2gray = cv.CreateMat(height, width, cv.CV_8U)
        frame2gray1 = cv.CreateMat(height, width, cv.CV_8U)
        frame2gray2 = cv.CreateMat(height, width, cv.CV_8U)
        
        cv.CvtColor(frame, frame2gray, cv.CV_RGB2GRAY)
        cv.CvtColor(frame1, frame2gray1, cv.CV_RGB2GRAY)
        cv.CvtColor(frame2, frame2gray2, cv.CV_RGB2GRAY)
        
#         #init
        res = cv.CreateMat(height, width, cv.CV_8U)
        #Absdiff to get the difference between to the frames
        cv.AbsDiff(frame2gray, frame2gray1, res)
        #Remove the noise and do the threshold
        cv.Smooth(res, res, cv.CV_BLUR, 5,5)
        cv.MorphologyEx(res, res, None, None, cv.CV_MOP_OPEN)
        cv.MorphologyEx(res,res, None, None, cv.CV_MOP_CLOSE)
        cv.Threshold(res, res, 10, 255, cv.CV_THRESH_BINARY_INV)
        
#         diff1 = cv.CreateMat(height, width, cv.CV_8U)
#         diff2 = cv.CreateMat(height, width, cv.CV_8U)
#         cv.AbsDiff(frame2gray,frame2gray1,diff1)
#         cv.AbsDiff(frame2gray2,frame2gray1,diff2)
#         res = cv2.bitwise_and(np.asarray(diff1),np.asarray(diff2))
        
        a = np.asarray(res)
        cv.ShowImage("res", cv.fromarray(res))
        
        ind = 0
        while True:
            ind += 1
        
        
        
        return np.asarray(res)
    
    '''
    def onChange(self, val): #callback when the user change the detection threshold
        self.threshold = val
    
    def __init__(self,threshold=8, doRecord=True, showWindows=True):
#         self.writer = None
#         self.font = None
#         self.doRecord=doRecord #Either or not record the moving object
#         self.show = showWindows #Either or not show the 2 windows
#         self.frame = None
#      
#         self.capture=cv.CaptureFromCAM(0)
#         self.frame = cv.QueryFrame(self.capture) #Take a frame to init recorder
#         if doRecord:
#             self.initRecorder()
#          
#         self.frame1gray = cv.CreateMat(self.frame.height, self.frame.width, cv.CV_8U) #Gray frame at t-1
#         cv.CvtColor(self.frame, self.frame1gray, cv.CV_RGB2GRAY)
#          
#         #Will hold the thresholded result
#         self.res = cv.CreateMat(self.frame.height, self.frame.width, cv.CV_8U)
#          
#         self.frame2gray = cv.CreateMat(self.frame.height, self.frame.width, cv.CV_8U) #Gray frame at t
#          
#         self.width = self.frame.width
#         self.height = self.frame.height
#         self.nb_pixels = self.width * self.height
#         self.threshold = threshold
#         self.isRecording = False
#         self.trigger_time = 0 #Hold timestamp of the last detection
#          
#         if showWindows:
#             cv.NamedWindow("Image")
#             cv.CreateTrackbar("Detection treshold: ", "Image", self.threshold, 100, self.onChange)
        return 
        
    def initRecorder(self): #Create the recorder
        codec = cv.CV_FOURCC('M', 'J', 'P', 'G') #('W', 'M', 'V', '2')
        self.writer=cv.CreateVideoWriter(datetime.now().strftime("%b-%d_%H_%M_%S")+".wmv", codec, 5, cv.GetSize(self.frame), 1)
        #FPS set to 5 because it seems to be the fps of my cam but should be ajusted to your needs
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 2, 8) #Creates a font

    def run(self):
        started = time.time()
        while True:
            
            curframe = cv.QueryFrame(self.capture)
            instant = time.time() #Get timestamp o the frame
            
            self.processImage(curframe) #Process the image
            
            if not self.isRecording:
                if self.somethingHasMoved():
                    self.trigger_time = instant #Update the trigger_time
                    if instant > started +5:#Wait 5 second after the webcam start for luminosity adjusting etc..
                        print datetime.now().strftime("%b %d, %H:%M:%S"), "Something is moving !"
                        if self.doRecord: #set isRecording=True only if we record a video
                            self.isRecording = True
            else:
                if instant >= self.trigger_time +10: #Record during 10 seconds
                    print datetime.now().strftime("%b %d, %H:%M:%S"), "Stop recording"
                    self.isRecording = False
                else:
                    cv.PutText(curframe,datetime.now().strftime("%b %d, %H:%M:%S"), (25,30),self.font, 0) #Put date on the frame
                    cv.WriteFrame(self.writer, curframe) #Write the frame
            
            if self.show:
                cv.ShowImage("Image", curframe)
                cv.ShowImage("Res", self.res)
                
            cv.Copy(self.frame2gray, self.frame1gray)
            c=cv.WaitKey(1) % 0x100
            if c==27 or c == 10: #Break if user enters 'Esc'.
                break            
    
    def somethingHasMoved(self):
        nb=0 #Will hold the number of black pixels

        for x in range(self.height): #Iterate the hole image
            for y in range(self.width):
                if self.res[x,y] == 0.0: #If the pixel is black keep it
                    nb += 1
        avg = (nb*100.0)/self.nb_pixels #Calculate the average of black pixel in the image

        if avg > self.threshold:#If over the ceiling trigger the alarm
            return True
        else:
            return False

    def processImage(self, frame):
        cv.CvtColor(frame, self.frame2gray, cv.CV_RGB2GRAY)
        
        #Absdiff to get the difference between to the frames
        cv.AbsDiff(self.frame1gray, self.frame2gray, self.res)
        
        #Remove the noise and do the threshold
        cv.Smooth(self.res, self.res, cv.CV_BLUR, 5,5)
        cv.MorphologyEx(self.res, self.res, None, None, cv.CV_MOP_OPEN)
        cv.MorphologyEx(self.res, self.res, None, None, cv.CV_MOP_CLOSE)
        cv.Threshold(self.res, self.res, 10, 255, cv.CV_THRESH_BINARY_INV)
    
    '''
    
    
    def query(self,queryFile):
        
#         c = conn.cursor()
#         
#         c.execute(''' CREATE TABLE video VALUES (id int, name text)''')
#         c.execute("INSERT INTO video VALUES (1,'sports')")
#         c.execute("INSERT INTO video VALUES (2,'flowers')")
#         c.execute("INSERT INTO video VALUES (3,'interview')")
#         c.execute("INSERT INTO video VALUES (4,'movie')")
#         c.execute("INSERT INTO video VALUES (5,'musicvideo')")
#         c.execute("INSERT INTO video VALUES (6,'starcraft')")
#         c.execute("INSERT INTO video VALUES (7,'traffic')")
#         
#         # Create table
#         c.execute('''CREATE TABLE motion
#                      (id int, )''')
#         
#         c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
#         
#         conn.commit()
#         conn.close()

        result = ""
        #extract motion
        self.saveOriginMotionData()
        
        #query part
#         result ,list = self.extractDominateColor("/Users/hehehehehe/Desktop/576/querydata/"+queryFile+".txt")
#         result1,list1 = self.extractMotion(queryFile)
        
        return result

if __name__=="__main__":
    detect = MotionDetectorInstantaneous()
    #detect.run()
    #detect.extractMotion()
    result = detect.query("first")
    print result
    print "done"
