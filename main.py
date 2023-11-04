from models import Author, Quote


def search_quotes(command, value):
    if command == 'name':
        author = Author.objects(fullname=value).first()
        if not author:
            return "Автора не знайдено."
        quotes = Quote.objects(author=author)
    elif command == 'tag':
        quotes = Quote.objects(tags=value)
    elif command == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
    else:
        return "Невідома команда."

    return [q.quote for q in quotes]  # повертаємо лише текст цитат


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
                print(result.encode('utf-8'))
        else:
            print(results.encode('utf-8'))
    except ValueError as e:
        print(f"Некоректний ввід: {e}")
