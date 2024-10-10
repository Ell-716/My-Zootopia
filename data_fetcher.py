import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


def load_data_api(animal_name):
    """Fetches animal data from the API based on the user-provided name.

    Args:
        animal_name (str): The name of the animal to fetch data for.

    Returns:
        list or None: A list of animal data if successful, or None if no data found or an error occurs.
    """

    api_url = f"https://api.api-ninjas.com/v1/animals?name={animal_name}"

    try:
        # Sending a GET request to the API
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        response.encoding = "utf-8"  # Set the response encoding

        # Check for response status
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        return response.json()  # Directly return the JSON data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None  # Return None if an HTTP error occurs
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API. Please check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again later.")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None  # Catch-all for any other request-related errors
