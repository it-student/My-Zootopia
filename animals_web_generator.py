"""
This module uses the api-ninjas animals API to fetch animal data in
json format in order to manipulate a plain html file by filling in
the found animals data in form of card style chunks.
uses data_fetcher module
"""
import data_fetcher

EXTRACT_KEYS = ["name", "diet", "locations", "type", 'scientific_name', 'skin_type']


def get_data_if_existent(animal_dict:dict) -> dict:
    """ Returns the animal data if it exists in animals_dict """
    result = {}
    for key_name in EXTRACT_KEYS:
        if key_name in animal_dict:
            if isinstance(animal_dict[key_name], str):
                result[key_name.capitalize()] = animal_dict[key_name]
            elif isinstance(animal_dict[key_name], list):
                result[key_name.capitalize()] = animal_dict[key_name][0]
        else:
            for key in animal_dict.keys():
                if key_name in animal_dict[key]:
                    result[key_name.capitalize()] = animal_dict[key][key_name]
    return result


def extract_animal_info_from_data(list_of_animal_dicts:list) -> list:
    """
    Returns a list of animal info from the data
    calls get_data_if_existent()
    """
    animals_data = list_of_animal_dicts
    list_of_animals_to_present = []

    for animal in animals_data:
        found_data = get_data_if_existent(animal)
        new_data = {}
        for entry in found_data:
            new_data[entry] = found_data[entry]
        list_of_animals_to_present.append(new_data)

    return list_of_animals_to_present


def load_html_template(file_path) -> str:
    """ Loads an HTML template file """
    with open(file_path, "r", encoding='utf-8') as template_file:
        return template_file.read()


def generate_final_html(html_string: str) -> None:
    """ Generates | overwrites final HTML file 'animals.html' """
    with open("animals.html", "w", encoding='utf-8') as file:
        file.write(html_string)


def serialize_animal(animal_object: dict) -> str:
    """ Serializes an animal object into an HTML string """
    result_html_li = ("<li class=\"cards__item\"><div class=\"card__title\">"
                        f"{animal_object[EXTRACT_KEYS[0].capitalize()]}</div>"
                       "<div class=\"card__text\"><ul class=\"card__list\">")
    for key in EXTRACT_KEYS[1:]:
        if key.capitalize() in animal_object:
            if key.endswith('s'):
                result_html_li += (f"<li><strong>{key.capitalize()[:-1]}:</strong>"
                                   f" {animal_object[key.capitalize()]}</li>")
            else:
                result_html_li += (f"<li><strong>{key.capitalize()}:</strong>"
                                   f" {animal_object[key.capitalize()]}</li>")

    result_html_li += "</ul></div></li>"
    return result_html_li


def fill_template_with_data(list_of_animal_dicts:list) -> str:
    """
    Fills the HTML template with data
    calls load_html_template()
    calls extract_animal_info_from_data()
    calls serialize_animal()
    """
    template_file = load_html_template('animals_template.html')
    if isinstance(list_of_animal_dicts, list):
        result_html_li = f"<h2>The animal \"{list_of_animal_dicts}\" doesn't exist!</h2>"
    else:
        animal_data_list = extract_animal_info_from_data(list_of_animal_dicts)
        result_html_li = ""
        for animal in animal_data_list:
            result_html_li += serialize_animal(animal)

    final_html = template_file.replace("__REPLACE_ANIMALS_INFO__", result_html_li.lstrip())
    return final_html


def get_skin_types(animal_dict: dict) -> list:
    """ Returns a list of skin types """
    skin_types = []
    for animal in animal_dict:
        if animal['characteristics']['skin_type'] not in skin_types:
            skin_types.append(animal['characteristics']['skin_type'])
    return skin_types


def main():
    """
    Main function
    """
    while True:
        users_choice = input("Enter a name of an animal: ")
        animals_data = data_fetcher.fetch_data(users_choice)
        if len(animals_data) == 0:
            filled_template_html = fill_template_with_data(users_choice)
        else:
            filled_template_html = fill_template_with_data(animals_data)
        generate_final_html(filled_template_html)
        print("Website was successfully generated to the file animals.html.")
        break


if __name__ == '__main__':
    main()
