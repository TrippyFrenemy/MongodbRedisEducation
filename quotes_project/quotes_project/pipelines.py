import json
import os

from itemadapter import ItemAdapter


class JsonWriterPipeline(object):
    authors_seen = []
    quotes_seen = []

    def close_spider(self, spider):
        if not os.path.exists("quotes.json"):
            with open("quotes.json", "w", encoding="utf-8") as fd:
                json.dump({}, fd)
        with open("quotes.json", "w", encoding="utf-8") as fd:
            json.dump(list(self.quotes_seen), fd, ensure_ascii=False, indent=2)

        if not os.path.exists("authors.json"):
            with open("authors.json", "w", encoding="utf-8") as fd:
                json.dump({}, fd)
        with open("authors.json", "w", encoding="utf-8") as fd:
            json.dump(list(self.authors_seen), fd, ensure_ascii=False, indent=2)


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            author_data = {
                "fullname": adapter['fullname'],
                "born_date": adapter['born_date'],
                "born_location": adapter['born_location'],
                "description": adapter['description']
            }
            self.authors_seen.append(author_data)

        if 'quote' in adapter.keys():
            quote_data = {
                "tags": adapter['tags'],
                "author": adapter['author'],
                "quote": adapter['quote']
            }
            self.quotes_seen.append(quote_data)

        return item
