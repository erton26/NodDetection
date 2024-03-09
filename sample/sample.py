import mediapipe as mp
import numpy as np
import cv2
#from mediapipe.tasks import python
#from mediapipe.tasks.python import vision

def getLeftScreen(frame) -> np.ndarray:
    (height, width) = frame.shape[:2]
    frameL = frame[0:height, 0:(int)(width/2)].copy()

    return frameL

def getLeftVideoLandmarks(data_path, options):
    detector = mp.tasks.vision.FaceLandmarker.create_from_options(options)

    video = cv2.VideoCapture(data_path)
    fps = video.get(cv2.CAP_PROP_FPS)

    frame_num = 0
    video_landmarks = []
    
    skipped_frame = 0

    while video.isOpened():
        frame_exists, frame = video.read()

        if frame_exists:
            frameL = getLeftScreen(frame)
            frame_landmarks = []
            #frame_timestamp_ms = int(frame_num / fps * 1000)
            frame_timestamp_ms = int(video.get(cv2.CAP_PROP_POS_MSEC))

            mp_images = mp.Image(image_format=mp.ImageFormat.SRGB, data=frameL)
            detection_result = detector.detect_for_video(mp_images, frame_timestamp_ms)

            print(len(detection_result.face_landmarks))

            if len(detection_result.face_landmarks) > 0:
                frame_a = {
                    "frame_num" : frame_num,
                    "frame_timestamp" : frame_timestamp_ms,
                    "frame_landmarks" : detection_result.face_landmarks[0]
                }
                video_landmarks.append(frame_a)
            else:
                skipped_frame += 1
            frame_num += 1
        else:
            print("left")
            print(f"skipped frame = {skipped_frame}")
            break

    video.release()

    return video_landmarks

def main():
    model_path = './model/face_landmarker.task'

    # Create a face landmarker instance with the video mode:
    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_faces=1
    )

    data_path = './input/data004/movie.mp4'
    video_landmarks_left = getLeftVideoLandmarks(data_path, options)

if __name__=="__main__": 
    main() 