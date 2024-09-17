import numpy as np

class MovementComparator:
    def __init__(self, base_landmarks, comparison_landmarks):
        self.base_landmarks = base_landmarks
        self.comparison_landmarks = comparison_landmarks

    def calculate_differences(self, frame_num, threshold=0.05):
        diferencias = {}
        if str(frame_num) in self.base_landmarks and str(frame_num) in self.comparison_landmarks:
            for key in self.base_landmarks[str(frame_num)]:
                base_point = self.base_landmarks[str(frame_num)][key]
                comp_point = self.comparison_landmarks[str(frame_num)][key]
                distancia = self._euclidean_distance(base_point, comp_point)
                if distancia > threshold:
                    diferencias[key] = distancia
        return diferencias

    def _euclidean_distance(self, point1, point2):
        return np.sqrt((point1['x'] - point2['x'])**2 +
                       (point1['y'] - point2['y'])**2 +
                       (point1['z'] - point2['z'])**2)
