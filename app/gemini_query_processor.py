import requests
import os
import re
from dotenv import load_dotenv
import logging

# Load env variables
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


    def query_model(self, prompt: str) -> tuple[dict, int]:

        try:
            # --- Send POST request and store response ---
            response = requests.post(
                self.api_url,
                headers={"x-goog-api-key": self.api_key},
                json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
                timeout=5
            )

            # --- Raise HTTPError for 4xx/5xx ---
            response.raise_for_status()

            # --- Success ---
            if response.status_code == 200:
                logging.info("Request successful")
                return response.json(), 200

        # --- Handle timeouts ---
        except requests.exceptions.Timeout:
            logging.error("Request timed out")
            return {"error": "Timeout"}, 0

        # --- Handle connection errors ---
        except requests.exceptions.ConnectionError:
            logging.error("Connection failed")
            return {"error": "Connection error"}, 0

        # --- Handle HTTP errors ---
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else 0
            logging.error(f"HTTP error {status_code}")
            if e.response is not None:
                logging.error(f"API response text: {e.response.text}")
                print(e.response.status_code)
                print(e.response.text)  # often explains why the key is invalid or permission denied

            if status_code == 404:
                return {"error": "Endpoint not found (404)"}, 404
            elif status_code == 400:
                return {"error": "Bad request (400)"}, 400
            else:
                return {"error": f"Unexpected {status_code}"}, status_code

        # --- Catch all other request exceptions ---
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return {"error": "Request failed"}, 0

    def get_document(title: str):
        for doc in handler.documents:
            if doc["title"] == title:
                return doc
        return {"error": "Document not found"}, 404

    def query_validation(self, query) -> None:
        # Allow safe chars length
        if len(query) > 1000:
            raise ValueError("Query is too long!")

        # Check for bad chars
        if not re.match(r'^[a-zA-Z0-9\s.,?!-]*$', query):
            raise ValueError("Query contains forbidden characters!")