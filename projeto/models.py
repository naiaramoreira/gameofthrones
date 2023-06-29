# models.py
class Casa:
    def __init__(self, name, lord_id, region=None, founding_year=None, id=None):
        self.name = name
        self.region = region
        self.founding_year = founding_year
        self.lord_id = lord_id
        self.id = id

class Lord:
    def __init__(self, name, gender, culture, born, died, father, mother, spouse, id=None):
        self.name = name
        self.gender = gender
        self.culture = culture
        self.born = born
        self.died = died
        self.father = father
        self.mother = mother
        self.spouse = spouse
        self.id = id

class Alias:
    def __init__(self, lord_id, alias, id=None):
        self.lord_id = lord_id
        self.alias = alias
        self.id = id

class Book:
    def __init__(self, lord_id, book_url, id=None):
        self.lord_id = lord_id
        self.book_url = book_url
        self.id = id

class Allegiance:
    def __init__(self, lord_id, house_url, id=None):
        self.lord_id = lord_id
        self.house_url = house_url
        self.id = id

class PovBook:
    def __init__(self, lord_id, book_url, id=None):
        self.lord_id = lord_id
        self.book_url = book_url
        self.id = id

class TvSeries:
    def __init__(self, lord_id, serie_name, id=None):
        self.lord_id = lord_id
        self.serie_name = serie_name
        self.id = id

class PlayedBy:
    def __init__(self, lord_id, actor_name, id=None):
        self.lord_id = lord_id
        self.actor_name = actor_name
        self.id = id

class Title:
    def __init__(self, lord_id, title, id=None):
        self.lord_id = lord_id
        self.title = title
        self.id = id
