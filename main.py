from redis import Redis
import re
import json
from models import Author, Quote

# Створення клієнта Redis
redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)


def get_cache_key(command, value):
    """Функція для створення унікального ключа для кешу"""
    return f"{command}:{value}"


def search_authors_by_name(name):
    """Функція для пошуку авторів за ім'ям"""
    # Використання регулярного виразу для пошуку за частиною імені
    regex = re.compile(f'^{re.escape(name)}', re.IGNORECASE)
    return Author.objects(fullname=regex)


def search_quotes_by_tag(tag):
    """Функція для пошуку цитат за тегом"""
    # Використання регулярного виразу для пошуку за частиною тега
    regex = re.compile(f'^{re.escape(tag)}', re.IGNORECASE)
    return Quote.objects(tags=regex)


def search_quotes(command, value):
    cache_key = get_cache_key(command, value)
    cached_results = redis_client.get(cache_key)

    # Якщо в кеші є результат, повернути його
    if cached_results:
        return json.loads(cached_results)

    # Інакше, виконати пошук і зберегти результат у кеші
    if command == 'name':
        authors = search_authors_by_name(value)
        quotes = Quote.objects(author__in=authors)
    elif command == 'tag':
        quotes = search_quotes_by_tag(value)
    else:
        return "Невідома команда."

    quotes_list = [q.quote for q in quotes]
    # Кешуємо результати на 1 годину
    redis_client.set(cache_key, json.dumps(quotes_list), ex=3600)

    return quotes_list


# Головний цикл
while True:
    input_data = input('Введіть команду: ').strip()
    if input_data.lower() == 'exit':
        break

    try:
        command, value = input_data.split(':', 1)
        results = search_quotes(command.strip(), value.strip())
        if isinstance(results, list):
            for result in results:
                print(result)
        else:
            print(results)
    except ValueError as e:
        print(f"Некоректний ввід: {e}")