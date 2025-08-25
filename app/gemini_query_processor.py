import requests
import os
import re
from dotenv import load_dotenv

# Load env viriables
load_dotenv()
# Setup basic logging
logging.basicConfig(level = logging.INFO)

"""

GeminiQueryProcessor is a basic class for Gemini model used for initializing the API key and url strings from env variables.
The function query_model is used for sending the post request and receiving the response from the Gemini model

"""
class GeminiQueryProcessor:
    def __init__(self): 
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(f"GEMINI_API_KEY env variable is missing (GeminiQueryProcessor class: __init__ func)\n")

        # Base API
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" 


    def query_model(self, prompt) -> str:
        # Sends a request to Gemini API and returns the response
        # Check response if server down
        try:
            response = requests.post(self.api_url, json={"prompt": prompt, "key": self.api_key}, timeout = 5)
            response.raise_for_status()
            if response.status_code == 200:
                logging.info("Request successful")
                return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                logging.error("Not found 404")
                return {"error": "Endpoint not found (404)"}
            elif status_code == 400:
                logging.error("Bad request (400)")
                return {"error": "Bad request"}
            else:
                logging.error(f"Unexpected error: {response.status_code}")
                return {"error": f"Unexpected {response.status_code}"}
            #raise RuntimeError(f"Wrong query response, status: {e}")

    def query_validation(self, query) -> None:
        # Allow safe chars length
        if len(query) > 1000:
            raise ValueError("Query is too long!")

        # Check for bad chars
        if not re.match(r'^[a-zA-Z0-9\s.,?!-]*$', query):
            raise ValueError("Query contains forbidden characters!")