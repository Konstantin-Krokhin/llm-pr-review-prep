import requests
import os
import re
from dotenv import load_dotenv
load_dotenv()

"""

GeminiQueryProcessor is a basic class for Gemini model used for initializing the API key and url strings from env variables.
The function query_model is used for sending the post request and receiving the response from the Gemini model

"""
class GeminiQueryProcessor:
    def __init__(self):
            self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"  
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError(f"GEMINI_API_KEY env variable is missing (GeminiQueryProcessor class: __init__ func)\n")


    def query_model(self, prompt) -> str:
        # Sends a request to Gemini API and returns the response
        # Check response if server down
        try:
            response = requests.post(self.api_url, json={"prompt": prompt, "key": self.api_key})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                return {"error": "Endpoint not found (404)"}
            #raise RuntimeError(f"Wrong query response, status: {e}")

    def query_validation(self, query) -> None:
        # Allow safe chars length
        if len(query) > 1000:
            raise ValueError("Query is too long!")

        # Check for bad chars
        if not re.match(r'^[a-zA-Z0-9\s.,?!-]*$', query):
            raise ValueError("Query contains forbidden characters!")