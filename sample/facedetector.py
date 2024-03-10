import mediapipe as mp
import numpy as np
import cv2
import scipy
from pathlib import Path
from typing import Tuple, List, Dict

class FaceDetector:
    def __init__(self, model_path: Path, data_path: Path, num_faces: int = 1):
        self.model_path = model_path
        self.data_path = data_path
        self.num_faces = num_faces

        video = cv2.VideoCapture(self.data_path)
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

    def getLeftScreen(self, frame: np.ndarray) -> np.ndarray:
        frameL = frame[0:self.height, 0:(int)(self.width/2)].copy()

        return frameL
    
    def getRightScreen(self, frame: np.ndarray) -> np.ndarray:
        frameR = frame[0:self.height, (int)(self.width/2):self.width].copy()

        return frameR
    
    def getVideoLandmarks(self, mode: str = "left") -> List[Dict[str, any]]:
        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=self.model_path),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_faces=self.num_faces
        )

        detector = mp.tasks.vision.FaceLandmarker.create_from_options(options)
        
        video = cv2.VideoCapture(self.data_path)

        frame_num = 0
        video_landmarks = []

        while video.isOpened():
            frame_exists, frame = video.read()

            if frame_exists:
                if (mode == "left"):
                    frame = self.getLeftScreen(frame)
                elif (mode == "right"):
                    frame = self.getRightScreen(frame)
                
                #frame_timestamp_ms = int(frame_num / fps * 1000)
                frame_timestamp_ms = int(video.get(cv2.CAP_PROP_POS_MSEC))

                mp_images = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                detection_result = detector.detect_for_video(mp_images, frame_timestamp_ms)
                
                if len(detection_result.face_landmarks) > 0:
                    frame_a = {
                        "frame_num" : frame_num,
                        "frame_timestamp" : frame_timestamp_ms,
                        "frame_landmarks" : detection_result.face_landmarks[0]
                    }
                    video_landmarks.append(frame_a)
                break
                frame_num += 1
            else:
                print(f"{mode} finished")
                break

        video.release()

        return video_landmarks
    
    def getR(self, lm:List[any]) -> np.ndarray:
        """
        Calculate rotation matrix.
        Rotate the FaceMesh by R to face the front
        """
        img_w = int(self.width/2)
        img_h = self.height

        scale_vec = np.array([img_w, img_h, img_w])
        p33 = np.array([lm[33].x, lm[33].y, lm[33].z]) * scale_vec
        p263 = np.array([lm[263].x, lm[263].y, lm[263].z]) * scale_vec
        p152 = np.array([lm[152].x, lm[152].y, lm[152].z]) * scale_vec
        p10 = np.array([lm[10].x, lm[10].y, lm[10].z]) * scale_vec

        _x = p263 - p33
        x = _x / np.linalg.norm(_x)

        _y = p152 - p10
        xy = x * np.dot(x, _y)
        y = _y - xy
        y = y / np.linalg.norm(y)

        z = np.cross(x, y)
        z = z / np.linalg.norm(y)

        R = np.array([x, y, z])

        return R
    
    def getEulerAngle(self, R:List[float]) -> np.ndarray:
        r =  scipy.spatial.transform.Rotation.from_matrix(R)
        angle = r.as_euler("xyz",degrees=True)

        return angle
    
    def getFaceAngle(self, mode: str = "left"):
        angle_arr = np.array([0,0,0,0])
        
        video_landmarks = self.getVideoLandmarks(self, mode=mode)

        for video_landmark in video_landmarks:
            #print("frame no: {:d}, eulervector: {}".format(video_landmark['frame_num'], calc_R(video_landmark['frame_landmarks'], 1920, 1080)[2]))
            R = self.getR(video_landmark['frame_landmarks'])
            angle = self.getEulerAngle(R)
            frame_num = np.empty(1)
            frame_num[0] = video_landmark['frame_num']
            a = np.concatenate((frame_num, angle), axis=None)
            angle_arr = np.append(angle_arr, a, axis=None)
            #print(angle_arr)
        angle_arr = np.reshape(angle_arr, (-1, 4))
        angle_arr = np.delete(angle_arr,0,0)

        return angle_arr