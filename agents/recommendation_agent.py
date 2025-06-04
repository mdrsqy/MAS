import requests
import os
from core.load_env import get_gemini_api_key

class RecommendationAgent:
    def __init__(self):
        self.api_key = get_gemini_api_key()
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan.")

    def recommend(self, context: dict) -> str:
        required_keys = ["diabetes", "heart", "stroke"]
        missing = [k for k in required_keys if k not in context]
        if missing:
            raise KeyError(f"Key(s) {missing} tidak ditemukan di context!")

        prompt_text = (
            "Saya memiliki pasien dengan hasil diagnosis:\n"
            f"- Diabetes: {'positif' if context['diabetes'] else 'negatif'}\n"
            f"- Penyakit Jantung: {'positif' if context['heart'] else 'negatif'}\n"
            f"- Stroke: {'positif' if context['stroke'] else 'negatif'}\n\n"
            "Berikan saran medis yang ringkas dan relevan dalam bahasa Indonesia."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_text}
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            try:
                res_json = response.json()
                candidates = res_json.get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"].strip()
                return "Maaf, AI tidak mengembalikan respons."
            except Exception:
                return "Format respons AI tidak sesuai."
        else:
            return f"Gagal memanggil API Gemini: {response.status_code} - {response.text}"