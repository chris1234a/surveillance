# import cv2
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# class Camera(object):
#     def __init__(self, prt):
#         self.cam=cv2.VideoCapture(prt)

#     def close(self):
#         self.cam.release()

#     def read(self):
#         return self.cam.read()[1]

# def update():
#     img=c.read()

# if __name__=='__main__':
#     c=Camera(0)

#     try:
#         while True:

#     finally:
#         c.close()
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite('img.png', frame)
cap.release()
cv2.destroyAllWindows()
