import requests

API_KEY = "ay9ZVJ5nVCOlksb1Dzw5+w==kuK8tkVKdvf8Q7CA"


def load_data_api(animal_name):
    """Fetches animal data from the API based on the user-provided name.
    Args:
        animal_name (str): The name of the animal to fetch data for.
    Returns:
        list or None: A list of animal data if successful, or None if no data found or an error occurs.
    """
    api_url = f"https://api.api-ninjas.com/v1/animals?name={animal_name}"
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})

    response.encoding = "utf-8"  # Set the response encoding

    # Check for response status
    if response.status_code == requests.codes.ok:
        return response.json()  # Directly return the JSON data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None  # Return None if no data found or error occurs
