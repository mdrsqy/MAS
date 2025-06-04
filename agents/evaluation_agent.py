class EvaluationAgent:
    def evaluate(self, diagnosis_result: dict) -> str:
        positive_count = sum(1 for v in diagnosis_result.values() if bool(v))

        if positive_count >= 2:
            return "Tinggi"
        elif positive_count == 1:
            return "Sedang"
        else:
            return "Rendah"