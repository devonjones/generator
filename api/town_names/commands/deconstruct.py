import json
import importlib.resources as pkg_resources

from town_names.name import Name
from town_names.proportions import NewName
from town_names.utils import load_meanings
import town_names.data as data

def deconstruct_command(namestr):
    parts = json.load(pkg_resources.open_text(data, "meanings.json"))
    meaning_db, _, _ = load_meanings(parts)
    name = Name(namestr)
    name.find_meaning(meaning_db)
    return name
