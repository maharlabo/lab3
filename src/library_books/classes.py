from dataclasses import dataclass
import json
from src.library_books.errors import CatalogError


@dataclass
class Book:
    id: str
    author: str
    name: str
    category: str
    year: int
    publisher: str

    def __post_init__(self):
        if self.id.strip() == "" or self.author.strip() == "" or self.name.strip() == "" or self.category.strip() == "" or self.publisher.strip() == "":
            raise CatalogError("Wrong format")
        if self.year > 2026:
            raise CatalogError("Wrong format")
        if len(self.id) != 17:
            raise CatalogError("Wrong format")
        digits = [int(i) for i in self.id if i.isdigit()]
        if len(digits) != 13 or len([i for i in self.id if i == "-"]) != 4 or self.id[:3] != "978" and self.id[:3] != "979" or not self.id[-1].isdigit():
            raise CatalogError("Wrong format")
        if (10-((sum([digits[i] for i in range(0, len(digits)-1, 2)])+sum([digits[i] for i in range(1, len(digits), 2)])*3)%10))%10 != digits[-1]:
            raise CatalogError("Wrong format")


class Catalog:
    def __init__(self, json_file):
        self.json_file = json_file
        self.format_version = 1
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                items_json = json.loads(f.read())
                if items_json["format_version"] != 1:
                    raise CatalogError("Wrong File")
                self.items = {}
                for item in items_json["items"]:
                    if item == "format_version":
                        continue
                    self.items[item] = Book(**items_json["items"][item])
                self.size = len(self.items) - 1
        except Exception:
            raise CatalogError("Wrong File")

    def add(self, book:Book) -> None:
        if book.id in self.items:
            raise CatalogError("ID already exists")
        self.items[book.id] = book
        self.size += 1

    def get(self, item_id:str) -> Book:
        return self.items[item_id]

    def remove(self, item_id:str):
        if item_id not in self.items:
            CatalogError("Object not found")
        del self.items[item_id]

    def find_by_category(self, category:str):
        ids = [i for i in self.items if self.items[i].category == category]
        ids.sort(key=lambda x: self.items[x].name)
        for id in ids:
            yield self.items[id]

    def find_by_name(self, name:str):
        ids = [i for i in self.items if name.lower() in self.items[i].name.lower()]
        ids.sort(key=lambda x: self.items[x].name)
        for id in ids:
            yield self.items[id]

    def load(self):
        try:
            with open(self.json_file, "r") as f:
                items_json = json.loads(f.read())
                if items_json["format_version"] != 1:
                    raise CatalogError("Wrong File")
                self.items = {}
                for item in items_json["items"]:
                    if item == "format_version":
                        continue
                    self.items[item] = Book(**items_json["items"][item])
                self.size = len(self.items) - 1
        except Exception:
            raise CatalogError("Wrong File")

    def save(self):
        items_json = {"format_version": 1}
        items_json["items"] = {}
        for item in self.items:
            items_json["items"][self.items[item].id] = self.items[item].__dict__
        with open(self.json_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(items_json))

    def __len__(self) -> int:
        return self.size

    def __iter__(self):
        ids = [i for i in self.items]
        ids.sort(key=lambda x: self.items[x].name)
        for id in ids:
            yield self.items[id]

    def __contains__(self, book:Book):
        return book.id in self.items
