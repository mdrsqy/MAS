class InputAgent:
    @staticmethod
    def get_input(streamlit_data: dict) -> dict:
        return {
            "diabetes": streamlit_data.get("diabetes") or [],
            "heart": streamlit_data.get("heart") or [],
            "stroke": streamlit_data.get("stroke") or []
        }