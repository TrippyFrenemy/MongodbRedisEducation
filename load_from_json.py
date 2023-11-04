import json
from models import Author, Quote


# Функція для завантаження даних з файла
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Завантаження авторів
authors_data = load_json_data('authors.json')
for author_data in authors_data:
    author = Author(
        fullname=author_data['fullname'],
        born_date=author_data['born_date'],
        born_location=author_data['born_location'],
        description=author_data['description']
    )
    author.save()  # збереження автора у базі даних

# Завантаження цитат
quotes_data = load_json_data('quotes.json')
for quote_data in quotes_data:
    author = Author.objects(fullname=quote_data['author']).first()  # знаходимо автора у базі
    if author:
        quote = Quote(
            tags=quote_data['tags'],
            author=author,
            quote=quote_data['quote']
        )
        quote.save()  # збереження цитати у базі даних

