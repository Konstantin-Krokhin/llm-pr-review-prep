import requests
import json
import os
import re

"""

GeminiQueryProcessor is a basic class for Gemini model used for initializing the API key and url strings from env variables.
The function query_model is used for sending the post request and receiving the response from the Gemini model

"""
class GeminiQueryProcessor:
    def __init__(self):
            self.api_url = "https://api.fakegemini.com/v1/query"  
            self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(f"KeyError Error inside GeminiQueryProcessor class in __init__ func\n")


    def query_model(self, prompt) -> str:
        # Sends a request to Gemini API and returns the response
        response = requests.post(self.api_url, json={"prompt": prompt, "key": self.api_key})
        # TODO: Check response if server down
        return response.json()

    def query_validation(self, query) -> bool:
        # Allow safe chars length
        if len(query) > 1000:
            raise ValueError("Query is too long!")

        # Check for bad chars
        if not re.match(r'^[a-zA-Z0-9\s.,?!-]*$', query):
            raise ValueError("Query contains forbidden characters!")
        
        return True