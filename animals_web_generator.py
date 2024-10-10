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
    output += "<div class='card__text'>\n<ul class='animal-details'>\n"

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
    output += "\n</ul>\n</div>\n</li>\n"

    return output


def get_animals_by_skin_type(animals_data):
    """Retrieves available skin types, prompts the user to select one,
    and returns animals matching the selected skin type.
    Args:
        animals_data (list): A list of animal data dictionaries.
    Returns:
        list: A list of animals filtered by the selected skin type.
    """
    skin_types = {animal["characteristics"].get("skin_type") for animal in animals_data if
                  animal["characteristics"].get("skin_type")}

    if not skin_types:
        print("No skin types available for this animal.")
        return None

    selected_skin_type = get_skin_type(skin_types)
    filtered_animals = [
        animal for animal in animals_data if animal["characteristics"].get("skin_type") == selected_skin_type
    ]

    if not filtered_animals:
        print(f"No animals found with skin type: {selected_skin_type}.")
        return None

    return filtered_animals


def load_html(html_template):
    """Loads an HTML template.
    Args:
        html_template (str): The file path of the HTML template to load.
    Returns:
        str: The content of the HTML template.
    """
    try:
        with open(html_template, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {html_template} was not found.")
        return ""
    except Exception as e:
        print(f"An error occurred while loading the HTML template: {e}")
        return ""


def new_animals_file(replaced_data):
    """Writes the final HTML data to a file.
    Args:
        replaced_data (str): The HTML data to write to the file.
    """
    try:
        with open("animals.html", "w") as new_file:
            new_file.write(replaced_data)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


def main():
    """This function prompts the user for an animal name, fetches data from the API,
    and generates an HTML file with details of the specified animals. It handles
    cases where the animal does not exist or where no data is available for the
    selected skin type.
    Returns:
        None: This function does not return a value but writes to an HTML file.
    """
    # Initialize error_message and output
    error_message = ""
    output = ""

    # Get a valid animal name and the corresponding data
    animal_name, animals_data = get_animal_name()

    # If no animal data found, show an error message
    if not animals_data:
        error_message = (
            "<div style='text-align: center; font-family: Arial, sans-serif;'>"
            f"<h2>Sorry, but the animal \"{animal_name}\" doesn't exist.</h2>"
            "<p style='font-size: 18px;'>Please check the name and try again.</p>"
            "</div>"
        )
    else:
        # Get filtered animals by skin type
        filtered_animals = get_animals_by_skin_type(animals_data)

        if filtered_animals:
            # If animals are found, serialize them for HTML
            output = "\n".join([serialize_animal(animal) for animal in filtered_animals])

    # Generate HTML output using a common template
    html_data = load_html("animals_template.html")
    replaced_data = html_data.replace("__REPLACE_ANIMALS_INFO__", error_message or output)
    new_animals_file(replaced_data)

    # Print appropriate message based on the outcome
    if error_message:
        print(f"\nWebsite generated with the error message for the animal: {animal_name}")
    else:
        print(f"\nWebsite generated with animals of the selected skin type.")


if __name__ == "__main__":
    main()
