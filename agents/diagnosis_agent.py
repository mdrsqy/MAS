import numpy as np

class DiagnosisAgent:
    def __init__(self, model):
        self.model = model

    def predict(self, input_data):
        input_array = np.array(input_data).reshape(1, -1)
        return self.model.predict(input_array)[0]

    def predict_proba(self, input_data):
        input_array = np.array(input_data).reshape(1, -1)
        return self.model.predict_proba(input_array)[0]