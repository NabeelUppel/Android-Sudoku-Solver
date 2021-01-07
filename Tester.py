import cv2
import numpy as np

samples = np.loadtxt('generalsamples.data', np.float32)
responses = np.loadtxt('generalresponses.data', np.float32)
responses = responses.reshape((responses.size, 1))

model = cv2.ml.KNearest_create()
model.train(samples, cv2.ml.ROW_SAMPLE, responses)

#im = cv2.imread('train.png')
#out = np.zeros(im.shape, np.uint8)
#gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]

#contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

def ocr(im,thresh ,cont):
    for cnt in cont:
        if 850 < cv2.contourArea(cnt) < 4000:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > 28:
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                roismall = roismall.reshape((1, 100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                string = int((results[0][0]))
                return string
                #cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))

#cv2.imshow('im', im)
#cv2.imshow('out', out)
#cv2.waitKey(0)
