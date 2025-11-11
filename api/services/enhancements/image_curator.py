# This file implements the "AI-Powered Image Curation" system.
# It finds a relevant, high-quality, free-to-use image for a given text response.

import requests
import os

# --- Configuration ---
# In a real-world scenario, you would hide this in an environment variable.
# For this project, we'll retrieve it from an environment variable for best practice.
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "YOUR_DEFAULT_PEXELS_API_KEY") # Replace with a real key if available
PEXELS_API_URL = "https://api.pexels.com/v1/search"

def get_relevant_image(text_response: str, keywords: list = None):
    """
    Finds a relevant image for the given text.
    It will prioritize provided keywords, otherwise, it will try to extract them.
    """
    if not PEXELS_API_KEY or PEXELS_API_KEY == "YOUR_DEFAULT_PEXELS_API_KEY":
        print("Image Curator: PEXELS_API_KEY not found. Skipping image search.")
        return None # Return None if the API key is not set

    # 1. Determine the search query
    if keywords:
        query = " ".join(keywords)
    else:
        # Simple keyword extraction: take the first few nouns/important words.
        # This is a placeholder for a more advanced NLP keyword extractor.
        # For now, we will just use the first 3 words of the response.
        query = " ".join(text_response.split()[:3])

    if not query:
        return None

    print(f"Image Curator: Searching for image with query: '{query}'")

    # 2. Make the API request to Pexels
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1, "page": 1}

    try:
        response = requests.get(PEXELS_API_URL, headers=headers, params=params, timeout=5)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()

        # 3. Extract the image URL
        if data.get("photos") and len(data["photos"]) > 0:
            image_url = data["photos"][0]["src"]["medium"] # Get a medium-sized image
            print(f"Image Curator: Found image URL: {image_url}")
            return image_url
        else:
            print("Image Curator: No image found for the query.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Image Curator ERROR: Failed to connect to Pexels API: {e}")
        return None

# --- Simple Test ---
if __name__ == '__main__':
    # You need to set the PEXELS_API_KEY environment variable to test this
    if PEXELS_API_KEY != "YOUR_DEFAULT_PEXELS_API_KEY":
        sample_text = "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France."
        url = get_relevant_image(sample_text, keywords=["Eiffel Tower", "Paris"])
        print(f"Test Result URL: {url}")
    else:
        print("Skipping test because PEXELS_API_KEY is not set.")
