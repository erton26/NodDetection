import mediapipe as mp
import numpy as np
import cv2
from pathlib import Path
from facedetector import FaceDetector

def main():
    data_path = './input/data004/movie.mp4'
    model_path = './model/face_landmarker.task'

    faceDetector = FaceDetector(model_path, data_path)

    video_landmarks = faceDetector.getVideoLandmarks()

    video_landmarks2 = faceDetector.getVideoLandmarks(mode="right")

if __name__=="__main__":
    main()