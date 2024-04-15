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

    """
    video_angle_left = faceDetector.getFaceAngle()

    video_angle_right = faceDetector.getFaceAngle(mode="right")

    video_angle_left_df = pd.DataFrame(video_angle_left)

    video_angle_right_df = pd.DataFrame(video_angle_right)

    video_angle_left_df.to_csv('./left_angle.csv')

    video_angle_right_df.to_csv('./right_angle.csv')
    """
    video_angle_left_df = pd.read_csv("./output/left_angle.csv", index_col=0)
    video_angle_left = video_angle_left_df.to_dict("records")
    video_angle_left_filled = faceDetector.fillBlankAngle(video_angle_left)
    video_angle_left_filled_df = pd.DataFrame(video_angle_left_filled)
    video_angle_left_filled_df.to_csv('./left_angle_filled.csv')


    video_angle_right_df = pd.read_csv("./output/right_angle.csv", index_col=0)
    video_angle_right = video_angle_right_df.to_dict("records")
    
    """
    nodDetectorLeft = NodDetector(video_angle_left, 25, 3.0, 0.5)
    nodTimestampsLeft = nodDetectorLeft.getNodTimestamp()
    video_nod_left_df = pd.DataFrame(nodTimestampsLeft)
    video_nod_left_df.to_csv('./left_nod.csv')

    nodDetectorRight = NodDetector(video_angle_right, 25, 3.0, 0.5)
    nodTimestampsRight = nodDetectorRight.getNodTimestamp()
    jerkTimestampsRight = nodDetectorRight.getJerkTimestamp()
    allTimestampsRight = nodDetectorRight.getAllTimestamp()
    print(len(nodTimestampsRight))
    print(len(jerkTimestampsRight))
    print(len(allTimestampsRight))
    #video_nod_right_df = pd.DataFrame(nodTimestampsRight)
    #video_nod_right_df.to_csv('./right_nod.csv')
    video_all_right_df = pd.DataFrame(allTimestampsRight)
    video_all_right_df.to_csv('./right_all.csv')
    """

if __name__=="__main__":
    main()