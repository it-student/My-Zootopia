"""
This program uses the api-ninjas animals API to fetch animal data in
JSON format in order to manipulate a plain HTML file by filling in
the found animals data in form of card style chunks.
uses animals_web_generator module
uses data_fetcher module
"""

from animals_web_generator import generate_final_html, fill_template_with_data
import data_fetcher

def main():
    """
    Main function
    """
    while True:
        users_choice = input("Enter a name of an animal: ")
        animals_data = data_fetcher.fetch_data(users_choice)
        if len(animals_data) == 0:
            filled_template_html = fill_template_with_data([users_choice])
        else:
            filled_template_html = fill_template_with_data(animals_data)
        generate_final_html(filled_template_html)
        print("Website was successfully generated to the file animals.html.")
        break


if __name__ == '__main__':
    main()
