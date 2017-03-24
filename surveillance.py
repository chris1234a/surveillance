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
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

# Globals
tol = 150.0 # max MSE before we declare scene has changed
camera = cv2.VideoCapture(0) # opencv webcam object
height = 480 # height of image
width = 640 # width of image
hxw = float(height*width) 

fromAddr='mower.chris@gmail.com'
toAddr='mower.chris@gmail.com'

server = smtplib.SMTP('smtp.gmail.com', 587) # creates a connection to gmail
server.starttls()
    
def getImage():
    # Return image
    retval, img = camera.read()
    return img

def areNotTheSame(img1, img2):
    # Computes the Mean-Squared Error to check if images are similar
    mse = np.sum((img1.astype('float')-img2.astype('float'))**2)/hxw
    print 'time: ', datetime.datetime.now(), ', mse =', mse
    return mse > tol
    
def emailImage(img):
    # Emails me the picture

    # Gen msg
    msg=MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = 'Someone in room'

    # image -> attachment
    now = time()
    print 'Scene significantly changed at', now
    filename='img_' + str(now) + '.png'
    cv2.imwrite(filename, img)
    attachment = open(filename, 'rb')

    # Add attachment
    part=MIMEApplication(attachment.read(),Name=filename)
    part['Content-Disposition'] = 'attachment; filename="%s"' % filename
    msg.attach(part)
    
    server.sendmail(fromAddr, toAddr, msg.as_string())

def main():

    # Login to gmail
    print 'Password please'
    password = raw_input(':: ')

    print 'Logging in...',
    server.login(fromAddr, password)
    print 'complete!'

    # Wait then start
    print 'Waiting ..'
    sleep(10)
    print 'Starting'
    
    c_old = getImage()

    try:
        while True:
            c_new = getImage()
        
            # convert to gray
            g_old = cv2.cvtColor(c_old,cv2.COLOR_BGR2GRAY)
            g_new = cv2.cvtColor(c_new,cv2.COLOR_BGR2GRAY)

            # Compare old and new images
            if areNotTheSame(g_old, g_new):
                # images are significantly different -> email
                emailImage(c_new)
            
            g_old = g_new
            c_old = c_new

            sleep(1)
    except KeyboardInterrupt:
        print 'Quiting...'
        server.quit()

if __name__=='__main__':
    main()
