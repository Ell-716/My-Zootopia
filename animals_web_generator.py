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
    """ Serializes a single animal object into HTML format """
    output = '<li class="cards__item">\n'
    output += f'<div class="card__title">{animal_obj["name"]}</div>\n'
    output += '<p class="card__text">\n'
    output += f"<strong>Diet:</strong> {animal_obj['characteristics']['diet']}<br/>\n"
    output += f"<strong>Location:</strong> {animal_obj['locations'][0]}<br/>\n"

    if "type" in animal_obj["characteristics"]:
        output += f"<strong>Type:</strong> {animal_obj['characteristics']['type']}<br/>\n"

    output += '</p>\n'
    output += '</li>\n'
    return output


def get_animals(animals_data):
    """ Serializes all animals into HTML format """
    output = ""
    for animal in animals_data:
        output += serialize_animal(animal)
    return output


def new_animals_file(replaced_data):
    """ Writes the final HTML data to a file """
    with open("animals.html", "w") as new_file:
        return new_file.write(replaced_data)


def main():
    animals_data = load_data('animals_data.json')
    html_data = load_html("animals_template.html")
    output = get_animals(animals_data)
    replaced_data = html_data.replace("__REPLACE_ANIMALS_INFO__", output)
    new_animals_file(replaced_data)


if __name__ == "__main__":
    main()
