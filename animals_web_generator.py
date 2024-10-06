import json


def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


def load_html(html_template):
    with open(html_template, "r") as file:
        return file.read()


def get_animals(animals_data):
    output = ""
    for animal in animals_data:
        output += f"\nName: {animal["name"]}\n"
        output += f"Diet: {animal["characteristics"]["diet"]}\n"
        output += f"Location: {animal["locations"][0]}\n"

        if "type" in animal["characteristics"]:
            output += f"Type: {animal["characteristics"]["type"]}\n"
    return output


def new_animals_file(replaced_data):
    with open("animals.html", "w") as new_file:
        return new_file.write(replaced_data)


def main():
    animals_data = load_data('animals_data.json')
    html_data = load_html("animals_template.html")
    output = get_animals(animals_data)
    replaced_data = html_data.replace("__REPLACE_ANIMALS_INFO__", output)
    animals_html = new_animals_file(replaced_data)


if __name__ == "__main__":
    main()
