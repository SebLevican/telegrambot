class FeedbackGenerator:
    def __init__(self):
        self.landmark_names = {
            12: "Hombro derecho",
            14: "Codo derecho",
            16: "Muñeca derecha",
            24: "Cadera derecha",
            26: "Rodilla derecha",
            28: "Tobillo derecho",
            # Agregar más puntos clave según necesidad
        }

    def generate_feedback(self, differences):
        feedback = []
        for key in differences:
            landmark_idx = int(key.split('_')[1])
            if landmark_idx in self.landmark_names:
                feedback.append(f"Corrige tu {self.landmark_names[landmark_idx]}, está desalineado en {differences[key]:.2f} cm")
        return feedback
