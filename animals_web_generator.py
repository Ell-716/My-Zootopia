import requests

API_KEY = "ay9ZVJ5nVCOlksb1Dzw5+w==kuK8tkVKdvf8Q7CA"


def load_data_api(animal_name):
    """Fetches animal data from the API based on the user-provided name."""
    api_url = f"https://api.api-ninjas.com/v1/animals?name={animal_name}"
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})

    response.encoding = "utf-8"  # Set the response encoding

    # Check for response status
    if response.status_code == requests.codes.ok:
        return response.json()  # Directly return the JSON data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None  # Return None if no data found or error occurs


def get_animal_name():
    """Prompts the user for a valid animal name and validates it against the API."""
    while True:
        animal_name = input("Please enter a name of an animal: ").lower().strip()
        if not animal_name or animal_name.isdigit():
            print("Invalid input. Please try again.")
            continue

        # Check if the API has data for this animal name
        animals_data = load_data_api(animal_name)
        if animals_data is not None:
            return animal_name, animals_data
        else:
            print("Sorry, no data found for this animal. Please try again.")


def get_skin_type(skin_types):
    """Prompts the user to select a skin type, with validation."""
    print("Available skin types:")
    for skin_type in skin_types:
        print(f"- {skin_type}")

    while True:
        selected_skin_type = input("Please enter a skin type from the list above: ").strip().lower()
        if selected_skin_type and any(selected_skin_type == skin_type.lower() for skin_type in skin_types):
            # Return the exact match (case-insensitive)
            return next(skin_type for skin_type in skin_types if skin_type.lower() == selected_skin_type)
        print("Invalid input. Please enter a valid skin type from the list.")


def serialize_animal(animal_obj):
    """Serializes a single animal object into HTML format with CSS classes."""
    output = "<li class='cards__item'>\n"
    output += f"<div class='card__title'>{animal_obj['name']}</div>\n"
    output += "<div class='card__text'>\n"
    output += "<ul class='animal-details'>\n"

    list_items = [
        f"<li class='animal-detail-item'><strong>Diet:</strong> "
        f"{animal_obj['characteristics'].get('diet', 'Unknown')}</li>",
        f"<li class='animal-detail-item'><strong>Location:</strong> "
        f"{animal_obj.get('locations', ['Unknown'])[0]}</li>",
        f"<li class='animal-detail-item'><strong>Skin-type:</strong> "
        f"{animal_obj['characteristics'].get('skin_type', 'Unknown')}</li>",
        f"<li class='animal-detail-item'><strong>Lifespan:</strong> "
        f"{animal_obj['characteristics'].get('lifespan', 'Unknown')}</li>",
        f"<li class='animal-detail-item'><strong>Type:</strong> "
        f"{animal_obj['characteristics'].get('type', 'Unknown')}</li>",
        f"<li class='animal-detail-item'><strong>Color:</strong> "
        f"{animal_obj['characteristics'].get('color', 'Unknown')}</li>"
    ]

    output += "\n".join(list_items)
    output += "\n</ul>\n"
    output += "</div>\n"
    output += "</li>\n"

    return output


def get_animals_by_skin_type(animals_data, selected_skin_type):
    """Filters animals by selected skin type."""
    return [
        animal for animal in animals_data
        if animal["characteristics"].get("skin_type") == selected_skin_type
    ]


def load_html(html_template):
    """Loads an HTML template."""
    with open(html_template, "r") as file:
        return file.read()


def new_animals_file(replaced_data):
    """Writes the final HTML data to a file."""
    with open("animals.html", "w") as new_file:
        return new_file.write(replaced_data)


def get_skin_types(animals_data):
    """Retrieves unique skin types from the animals data."""
    skin_types = set()
    for animal in animals_data:
        skin_type = animal["characteristics"].get("skin_type")
        if skin_type:
            skin_types.add(skin_type)
    return skin_types


def main():
    # Get a valid animal name and the corresponding data
    animal_name, animals_data = get_animal_name()

    # If animals_data is None (not found), display an error message
    if not animals_data:
        error_message = (
            "<div style='text-align: center; font-family: Arial, sans-serif;'>"
            f"<h2>Sorry, but the animal \"{animal_name}\" doesn't exist.</h2>"
            "<p style='font-size: 18px;'>Please check the name and try again.</p>"
            "</div>"
        )
        html_data = load_html("animals_template.html")
        replaced_data = html_data.replace("__REPLACE_ANIMALS_INFO__", error_message)
        new_animals_file(replaced_data)
        print(f"\nWebsite generated with the error message for the animal: {animal_name}")
        return

    # Extract available skin types
    skin_types = get_skin_types(animals_data)

    if not skin_types:
        print("No skin types available for this animal.")
        return

    # Get user input for skin type
    selected_skin_type = get_skin_type(skin_types)

    # Filter animals by the selected skin type
    filtered_animals = get_animals_by_skin_type(animals_data, selected_skin_type)

    if not filtered_animals:
        print(f"No animals found with skin type: {selected_skin_type}.")
        return

    # Generate HTML output
    html_data = load_html("animals_template.html")
    output = "\n".join([serialize_animal(animal) for animal in filtered_animals])
    replaced_data = html_data.replace("__REPLACE_ANIMALS_INFO__", output)
    new_animals_file(replaced_data)
    print(f"\nWebsite generated with animals of skin type: {selected_skin_type}")


if __name__ == "__main__":
    main()
