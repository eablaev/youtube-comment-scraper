import google.generativeai as genai

class GeminiAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-1.5-pro-001")

    def analyze_comments(self, comments: list, user_input: str) -> str:
        """Analyze comments using Gemini AI."""
        prompt = f"{user_input}:\n\n{comments}"
        response = self.model.generate_content(prompt)
        return response.text