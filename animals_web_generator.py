import json


EXTRACT_KEYS = ["name", "diet", "locations", "type"]

def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)


animals_data = load_data('animals_data.json')

def get_data_if_existent(animal_dict:dict) -> dict:
  """ Returns the animal data if it exists in animals_dict """
  result = dict()
  for key_name in EXTRACT_KEYS:
    if key_name in animal_dict:
      if isinstance(animal_dict[key_name], str):
        result[key_name.capitalize()] = animal_dict[key_name]
      elif isinstance(animal_dict[key_name], list):
        result["Location"] = animal_dict[key_name][0]
    else:
      for key in animal_dict.keys():
        if key_name in animal_dict[key]:
          result[key_name.capitalize()] = animal_dict[key][key_name]
  return result


list_of_animals_to_present = []

for animal in animals_data:
  found_data = get_data_if_existent(animal)
  for entry in found_data:
    print(f"{entry}: {found_data[entry]}")
  print()
