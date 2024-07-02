import cv2 as cv
import numpy as np
import filtro
#import mediapipe as mp

def tirarFoto():

    capture = cv.VideoCapture(0)
    #solucao_rec_rosto = mp.solutions.face_detection

    if capture.isOpened():
        validacao, frame = capture.read()
        while validacao:
            validacao, frame = capture.read()
            cv.imshow('Video da Webcam', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cv.imwrite('Foto_C.png',frame)
    
    capture.release()
    #cv.destroyAllWindows