import json


EXTRACT_KEYS = ["name", "diet", "locations", "type", 'scientific_name']

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
        result[key_name.capitalize()[:-1]] = animal_dict[key_name][0]
    else:
      for key in animal_dict.keys():
        if key_name in animal_dict[key]:
          result[key_name.capitalize()] = animal_dict[key][key_name]
  return result


def extract_animal_info_from_data() -> list:
  """
  Returns a list of animal info from the data
  calls load_data()
  calls get_data_if_existent()
  """
  animals_data = load_data('animals_data.json')
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
  """ Generates a final HTML file 'animals.html' """
  with open("animals.html", "w") as file:
    file.write(html_string)


def serialize_animal(animal_object: dict) -> str:
  """ Serializes an animal object into a HTML string """
  result_html_li = f"""
            <li class=\"cards__item\">
              <div class=\"card__title\">{animal_object[EXTRACT_KEYS[0].capitalize()]}</div>
              <p class=\"card__text\">
                <strong>{EXTRACT_KEYS[1].capitalize()}:</strong> 
                {animal_object[EXTRACT_KEYS[1].capitalize()]}
                <br>
                <strong>{EXTRACT_KEYS[2].capitalize()[:-1]}:</strong> 
                {animal_object[EXTRACT_KEYS[2].capitalize()[:-1]]}
                <br>"""
  if EXTRACT_KEYS[3].capitalize() in animal_object:
    result_html_li += f"""
                <strong>{EXTRACT_KEYS[3].capitalize()}:</strong> 
                {animal_object[EXTRACT_KEYS[3].capitalize()]}
                <br>"""
  if EXTRACT_KEYS[4].capitalize() in animal_object:
    result_html_li += f"""
                <strong>{EXTRACT_KEYS[4].replace("scientific_name", "Scientific Name")}:</strong> 
                {animal_object[EXTRACT_KEYS[4].capitalize()]}
                <br>"""
  result_html_li += f"""
              </p>
            </li>"""
  return result_html_li


def fill_template_with_data() -> str:
  """
  Fills the HTML template with data
  calls load_html_template()
  calls extract_animal_info_from_data()
  calls serialize_animal()
  """
  template_file = load_html_template('animals_template.html')
  animal_data_list = extract_animal_info_from_data()
  result_html_li = ""
  for animal in animal_data_list:
    result_html_li += serialize_animal(animal)

  final_html = template_file.replace("__REPLACE_ANIMALS_INFO__", result_html_li.lstrip())
  return final_html

generate_final_html(fill_template_with_data())