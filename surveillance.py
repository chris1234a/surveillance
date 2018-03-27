""" Copyright Christopher E. Mower 2017

Takes continuous picutures, compares them, and if a signigicant change has 
taken place emails you the picture.
"""
# For images
import cv2
import numpy as np

# For alerts
from time import sleep, time
import datetime

# For emails
from getpass import getpass
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

# Globals
prt=1
tol = 150.0 # max MSE before we declare scene has changed
camera = cv2.VideoCapture(prt) # opencv webcam object
height = 480 # height of image
width = 640 # width of image
hxw = float(height*width) 

# fromAddr='mower.chris@gmail.com'
# toAddr='mower.chris@gmail.com'
fromAddr='mower.chris@gmail.com'
toAddr='stoutheo@gmail.com' # email here


server = smtplib.SMTP('smtp.gmail.com', 587) # creates a connection to gmail
server.starttls()
    
def getImage():
    # Return image
    retval, img_bgr = camera.read()
    img={}
    img['time']=time()
    img['bgr']=img_bgr
    img['gray']=cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)
    return img

def areNotTheSame(img1, img2):
    # Computes the Mean-Squared Error to check if images are similar
    mse = np.sum((img1.astype('float')-img2.astype('float'))**2)/hxw
    print 'time: ', datetime.datetime.now(), ', mse =', mse
    return mse > tol

def saveImage(img):
    filename='img-{}.png'.format(img['time'])
    print ">>>Saving image: {}<<<".format(filename)
    cv2.imwrite(filename, img['bgr'])
    
def emailImage(img):
    # Emails me the picture

    # Gen msg
    msg=MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = '>>>DISTURBANCE DETECTED<<<'

    # image -> attachment
    print 'Scene significantly changed at', img['time']
    saveImage(img)
    attachment = open(filename, 'rb')

    # Add attachment
    part=MIMEApplication(attachment.read(),Name=filename)
    part['Content-Disposition'] = 'attachment; filename="%s"' % filename
    msg.attach(part)
    
    server.sendmail(fromAddr, toAddr, msg.as_string())

def main():

    # # Login to gmail
    # password=getpass('Password: ')
    
    # print 'Logging in...',
    # server.login(fromAddr, password)
    # print 'complete!'

    # Wait then start
    print 'Waiting ..'
    sleep(10)
    print 'Starting'
    
    img_old = getImage()

    try:
        while True:
            img_new = getImage()
        
            # Compare old and new images
            if areNotTheSame(img_old['gray'], img_new['gray']):
                # images are significantly different -> email
                #emailImage(img_new)
                saveImage(img_new)
            img_old=img_new
            sleep(1)
    except KeyboardInterrupt:
        print 'Quiting...'
        server.quit()

if __name__=='__main__':
    main()
