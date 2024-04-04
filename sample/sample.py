import mediapipe as mp
import numpy as np
import cv2
import pandas as pd
from pathlib import Path
from facedetector import FaceDetector
from noddetector import NodDetector

def main():
    data_path = './input/data004/movie.mp4'
    model_path = './model/face_landmarker.task'
    output_path = './output/data004/'

    faceDetector = FaceDetector(model_path, data_path)
    #left_landmark = faceDetector.getVideoLandmarks()
    #print(left_landmark)
    #print(len(left_landmark))

    video_angle_left = faceDetector.getFaceAngle()

    video_angle_right = faceDetector.getFaceAngle(mode="right")

    video_angle_left_df = pd.DataFrame(video_angle_left)

    video_angle_right_df = pd.DataFrame(video_angle_right)

    video_angle_left_df.to_csv('./left_angle.csv')

    video_angle_right_df.to_csv('./right_angle.csv')

    nodDetectorLeft = NodDetector(video_angle_left, 3.0, 0.5)

    nodTimestampsLeft = nodDetectorLeft.getNodTimestamp()

    video_nod_left_df = pd.DataFrame(nodTimestampsLeft)

    video_nod_left_df.to_csv('./left_nod.csv')

if __name__=="__main__":
    main()