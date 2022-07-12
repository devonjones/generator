import json
import importlib.resources as pkg_resources

from town_names.utils import filter_tag_list, load_meanings
import town_names.data as data

def tag_command():
    meanings = json.load(pkg_resources.open_text(data, "meanings.json"))
    _, _, full_tags = load_meanings(meanings)
    return filter_tag_list(full_tags)
