import json


def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


def load_html(html_template):
    """ Loads an HTML template """
    with open(html_template, "r") as file:
        return file.read()


def serialize_animal(animal_obj):
    """ Serializes a single animal object into HTML format with CSS classes """
    output = "<li class='cards__item'>\n"
    output += f"<div class='card__title'>{animal_obj['name']}</div>\n"
    output += "<div class='card__text'>\n"
    output += "<ul class='animal-details'>\n"

    # Create the list of characteristics
    list_items = [
        f"<li class='animal-detail-item'><strong>Diet:</strong> {animal_obj['characteristics']['diet']}</li>",
        f"<li class='animal-detail-item'><strong>Location:</strong> {animal_obj['locations'][0]}</li>",
        f"<li class='animal-detail-item'><strong>Skin-type:</strong> {animal_obj['characteristics']['skin_type']}</li>",
        f"<li class='animal-detail-item'><strong>Lifespan:</strong> {animal_obj['characteristics']['lifespan']}</li>",
    ]

    if "type" in animal_obj["characteristics"]:
        list_items.append(f"<li class='animal-detail-item'><strong>Type:</strong> "
                          f"{animal_obj['characteristics']['type']}</li>")

    if "color" in animal_obj["characteristics"]:
        list_items.append(f"<li class='animal-detail-item'><strong>Color:</strong> "
                          f"{animal_obj['characteristics']['color']}</li>")

    # Join all list items and append them to the output
    output += "\n".join(list_items)
    output += "\n</ul>\n"
    output += "</div>\n"
    output += "</li>\n"

    return output


def get_animals(animals_data):
    """ Serializes all animals into HTML format """
    output = ""
    for animal in animals_data:
        output += serialize_animal(animal)
    return output


def get_skin_types(animals_data):
    """ Retrieves unique skin types from the animals data """
    skin_types = set()
    for animal in animals_data:
        skin_type = animal["characteristics"].get("skin_type")
        if skin_type:
            skin_types.add(skin_type)
    return skin_types


def get_animals_by_skin_type(animals_data, selected_skin_type):
    """ Filters animals by selected skin type """
    filtered_animals = [
        animal for animal in animals_data
        if animal["characteristics"].get("skin_type") == selected_skin_type
    ]
    return filtered_animals


def new_animals_file(replaced_data):
    """ Writes the final HTML data to a file """
    with open("animals.html", "w") as new_file:
        return new_file.write(replaced_data)


def main():
    animals_data = load_data('animals_data.json')

    # Step 1: Get available skin types and display them
    skin_types = get_skin_types(animals_data)
    print("Available skin types:")
    for skin_type in skin_types:
        print(f"- {skin_type}")

    # Step 2: Get user input for skin type with validation
    while True:
        selected_skin_type = input("Please enter a skin type from the list above: ").strip()

        # Normalize to lower case for case insensitive comparison
        normalized_skin_type = selected_skin_type.lower()

        # Check if the input is a valid skin type
        if not normalized_skin_type or normalized_skin_type.isdigit():
            print("Invalid input. Please enter a valid skin type (not a number).")
            continue

        # Check if normalized input matches any skin types in the list
        if any(normalized_skin_type == skin_type.lower() for skin_type in skin_types):
            selected_skin_type = next(
                skin_type for skin_type in skin_types if skin_type.lower() == normalized_skin_type)
            break
        else:
            print("Invalid skin type. Please enter one of the available skin types.")

    # Step 3: Filter animals by selected skin type
    filtered_animals = get_animals_by_skin_type(animals_data, selected_skin_type)

    # If no animals found for selected skin type
    if not filtered_animals:
        print(f"No animals found with skin type: {selected_skin_type}.")
        return

    html_data = load_html("animals_template.html")
    output = get_animals(filtered_animals)  # Call the get_animals function here
    replaced_data = html_data.replace("__REPLACE_ANIMALS_INFO__", output)
    new_animals_file(replaced_data)


if __name__ == "__main__":
    main()
