""" Copyright Christopher E. Mower 2017

Takes continuous picutures, compares them, and if a signigicant change has 
taken place saves image.
"""
import os
import cv2
import numpy as np
from time import sleep, time
import datetime
from copy import deepcopy

dr='/home/chris/My-Projects/surveillance'

def date():
    return datetime.datetime.now()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class OutputProcessor(object):

    def __init__(self, fn='history.out', print_to_screen=True):
        self.print_to_screen=print_to_screen
        self.fn=fn
        self.f=open(fn, 'w')
        output="[OK, {}] session starting".format(date())
        self.writeToOutput(output, 'ok')

    def close(self):
        output="[OK, {}] quiting session".format(date())
        self.writeToOutput(output, 'ok')
        self.f.close()

    def sleep(self, t):
        output="[SLEEP, {}] sleeping for {} secs".format(date(),t)
        self.writeToOutput(output, 'sleep')
        sleep(t)

    def userExit(self):
        output="[OK, {}] user request exit".format(date())
        self.writeToOutput(output, 'ok')

    def writeToOutput(self,txt, typ):
        if self.print_to_screen:
            if typ=='warn':
                print bcolors.WARNING+txt+bcolors.ENDC
            elif typ=='disturb':
                print bcolors.FAIL+txt+bcolors.ENDC
            elif typ=='sleep':
                print bcolors.OKBLUE+txt+bcolors.ENDC
            elif typ=='ok':
                print bcolors.OKGREEN+txt+bcolors.ENDC
            elif typ=='err':
                print bcolors.FAIL+txt+bcolors.ENDC
        self.f.write(txt+'\n')

    def checkDirSize(self):
        total=0.0
        for f in os.listdir(dr):
            if f[-3:]=='png':
                total+=os.path.getsize(f)
        total=1e-9*total # byte->gb
        if total > 75.0:
            output="[WARN, {}] not enough storage space".format(date())
            self.writeToOutput(output, 'warn')
            return True
        else:
            return False
                
    def warnOfDisturbance(self, date, mse):
        output='>>>WARNING DISTURBANCE DETECTED<<< capture time: {}, mse: {}'.format(date, mse)
        self.writeToOutput(output, 'disturb')
            
class ImageProcessor(object):
    def __init__(self, prt, tol):
        self.w=640 # image width
        self.h=480 # image height
        self.camera=cv2.VideoCapture(prt)
        self.date=None
        self.img_old={'stamp': None, 'gray': None, 'bgr': None}
        self.img_new={'stamp': None, 'gray': None, 'bgr': None}
        self.tol=tol
        self.mse=-1.0

    def close(self):
        self.camera.release()

    def update(self):
        self.img_old=deepcopy(self.img_new)
        retval, im = self.camera.read()
        t=time()
        self.date=date()
        if retval is True:
            output="[OK, {}] image captured successfully".format(self.date)
            self.img_new['stamp']=t
            self.img_new['date']=self.date
            self.img_new['bgr']=im
            self.img_new['gray']=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            typ='ok'
        else:
            output="[ERROR, {}] image could not be retrieved from camera".format(self.date)
            typ='err'
        return output, typ

    def save(self):
        filename='img-{}.png'.format(self.img_new['stamp'])
        cv2.imwrite(filename,self.img_new['bgr'])
        
    def cmp(self):
        if self.img_old['gray'] is None or self.img_new['gray'] is None:
            return False
        im_old=self.img_old['gray'].astype('float')
        im_new=self.img_new['gray'].astype('float')
        self.mse = np.sum((im_old-im_new)**2)/float(self.w*self.h)
        return self.mse>self.tol

def main():

    sleep_time = 1
    rate=2 # Hz
    prt=0
    tol = 130.0 # max MSE before we declare scene has changed
    impro=ImageProcessor(prt, tol)
    oupro=OutputProcessor()
    oupro.sleep(sleep_time)
    
    try:
        while True:
            output, typ=impro.update()
            oupro.writeToOutput(output, typ)
            if impro.cmp():
                oupro.warnOfDisturbance(impro.date,impro.mse)
                impro.save()
            if oupro.checkDirSize():
                break
            sleep(1.0/rate)
    except KeyboardInterrupt:
        oupro.userExit()
    finally:
        impro.close()
        oupro.close()
        
if __name__=='__main__':
    main()
