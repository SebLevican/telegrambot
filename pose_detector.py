import cv2
import mediapipe as mp
import json
import os

class PoseDetector:
    def __init__(self):
        #self.video_path = video_path
        self.pose_landmarks = {}
        self.mp_pose = mp.solutions.pose

    def process_video(self,video_path):
        cap = cv2.VideoCapture(video_path)
        frame_num = 0
        
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                
                if results.pose_landmarks:
                    self.pose_landmarks[frame_num] = self._store_landmarks(results.pose_landmarks)
                
                frame_num += 1
        cap.release()

    def _store_landmarks(self, landmarks):
        pose_data = {}
        for idx, landmark in enumerate(landmarks.landmark):
            pose_data[f'landmark_{idx}'] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }
        return pose_data

    def save_landmarks_to_json(self, output_path):

        with open(output_path, 'w') as f:
            json.dump(self.pose_landmarks, f)

        print('landmark guardado')

    def load_landmarks_from_json(self, input_path):
        with open(input_path, 'r') as f:
            self.pose_landmarks = json.load(f)
