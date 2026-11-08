from dataclasses import dataclass
from errors import CatalogError


@dataclass
class Book:
    id: str
    author: str
    name: str
    category: str
    year: int
    isbn: str


class Catalog:
    items:dict[Book] = {}
    size:int = 0

    def add(self, book:Book) -> None:
        if book.id in self.items:
            raise CatalogError("ID already exists")
        self.items[book.id] = book
        self.size += 1

    def get(self, item_id:str) -> Book:
        return self.items[item_id]

    def remove(self, item_id:str):
        if item_id not in
        del self.items[item_id]

    def finc_by_category(self, category:str) -> list:
        return [i for i in self.items if i.category == category]

    def find_by_name(self, name:str) -> list:
        return [i for i in self.items if i.name.lower() == name.lower()]

    def __len__(self) -> int:
        return self.size

    def __iter__(self):
        for id in self.items:
            yield self.items[id]

    def __contains__(self, book:Book):
        return book.id in self.items
