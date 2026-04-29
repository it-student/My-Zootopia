import json


EXTRACT_KEYS = ["name", "diet", "locations", "type", 'scientific_name', 'skin_type']

def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)


def get_data_if_existent(animal_dict:dict) -> dict:
  """ Returns the animal data if it exists in animals_dict """
  result = dict()
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
    new_data = dict()
    for entry in found_data:
      new_data[entry] = found_data[entry]
    list_of_animals_to_present.append(new_data)

  return list_of_animals_to_present

def load_html_template(file_path) -> str:
  """ Loads a HTML template file """
  with open(file_path, "r") as template_file:
    return template_file.read()


def generate_final_html(html_string: str) -> None:
  """ Generates | overwrites final HTML file 'animals.html' """
  with open("animals.html", "w") as file:
    file.write(html_string)


def serialize_animal(animal_object: dict) -> str:
  """ Serializes an animal object into a HTML string """
  result_html_li = f"<li class=\"cards__item\"><div class=\"card__title\">\
    {animal_object[EXTRACT_KEYS[0].capitalize()]}</div><div class=\"card__text\"><ul class=\"card__list\">"
  for key in EXTRACT_KEYS[1:]:
    if key.capitalize() in animal_object:
      if key.endswith('s'):
        result_html_li += f"<li><strong>{key.capitalize()[:-1]}:</strong> {animal_object[key.capitalize()]}</li>"
      else:
        result_html_li += f"<li><strong>{key.capitalize()}:</strong> {animal_object[key.capitalize()]}</li>"

  result_html_li += f"</ul></div></li>"
  return result_html_li


def fill_template_with_data(list_of_animal_dicts:list) -> str:
  """
  Fills the HTML template with data
  calls load_html_template()
  calls extract_animal_info_from_data()
  calls serialize_animal()
  """
  template_file = load_html_template('animals_template.html')
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
  animals_data = load_data('animals_data.json')
  available_skin_types = get_skin_types(animals_data)
  while True:
    print("Please choose one of following skin types: ")
    for skin_type in available_skin_types:
      print(skin_type)
    users_choice = input("Please type in which skin type you choose: ")
    if users_choice in available_skin_types:
      animals_with_that_skin_type = [animal for animal in animals_data if animal['characteristics']['skin_type'] == users_choice]
      filled_template_html = fill_template_with_data(animals_with_that_skin_type)
      generate_final_html(filled_template_html)
      break


if __name__ == '__main__':
  main()