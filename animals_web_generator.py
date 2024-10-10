import data_fetcher


def get_animal_name():
    """Prompts the user for a valid animal name and validates it against the API.
    Returns:
        tuple: A tuple containing the animal name (str) and its corresponding data (list).
    """
    while True:
        animal_name = input("Please enter a name of an animal: ").lower().strip()
        if not animal_name or animal_name.isdigit():
            print("Invalid input. Please try again.")
            continue

        # Check if the API has data for this animal name
        animals_data = data_fetcher.load_data_api(animal_name)
        if animals_data is not None:
            return animal_name, animals_data
        else:
            print("Sorry, no data found for this animal. Please try again.")


def get_skin_type(skin_types):
    """Prompts the user to select a skin type, with validation.
    Args:
        skin_types (set): A set of available skin types.
    Returns:
        str: The selected skin type.
    """
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
    """Serializes a single animal object into HTML format with CSS classes.
    Args:
        animal_obj (dict): A dictionary containing animal data.
    Returns:
        str: An HTML string representation of the animal object.
    """
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
    """Filters animals by selected skin type.
    Args:
        animals_data (list): A list of animal data dictionaries.
        selected_skin_type (str): The selected skin type to filter by.
    Returns:
        list: A list of animals that match the selected skin type.
    """
    return [
        animal for animal in animals_data
        if animal["characteristics"].get("skin_type") == selected_skin_type
    ]


def load_html(html_template):
    """Loads an HTML template.
    Args:
        html_template (str): The file path of the HTML template to load.
    Returns:
        str: The content of the HTML template.
    """
    with open(html_template, "r") as file:
        return file.read()


def new_animals_file(replaced_data):
    """Writes the final HTML data to a file.
    Args:
        replaced_data (str): The HTML data to write to the file.
    """
    with open("animals.html", "w") as new_file:
        return new_file.write(replaced_data)


def get_skin_types(animals_data):
    """Retrieves unique skin types from the animals data.
    Args:
        animals_data (list): A list of animal data dictionaries.
    Returns:
        set: A set of unique skin types from the animals data.
    """
    skin_types = set()
    for animal in animals_data:
        skin_type = animal["characteristics"].get("skin_type")
        if skin_type:
            skin_types.add(skin_type)
    return skin_types


def main():
    """This function prompts the user for an animal name, fetches data from the API,
        and generates an HTML file with details of the specified animals. It handles
        cases where the animal does not exist or where no data is available for the
        selected skin type.
        Returns:
            None: This function does not return a value but writes to an HTML file.
    """

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
