import json
import sys
import importlib.resources as pkg_resources

from town_names.utils import filter_tag_list
from town_names.meaning import load_meanings
from town_names.proportions import load_proportions
import town_names.data as data

def tag_check(tags, full_tags):
    for tag in tags:
        tag_names = [t[0] for t in full_tags]
        if not tag in tag_names:
            tag_list = filter_tag_list(full_tags)
            print("Tag: %s not found" % tag, file=sys.stderr)
            print(file=sys.stderr)
            for t in tag_list:
                print(t, file=sys.stderr)
            sys.exit(1)

def generate_command(tag, towns):
    tags = list(tag)
    meanings = json.load(pkg_resources.open_text(data, "meanings.json"))
    proportions = json.load(pkg_resources.open_text(data, "%s_proportions.json" % towns))
    meaning_db, tag_db, full_tags = load_meanings(meanings)
    name_gen = load_proportions(proportions, meaning_db, tag_db)
    if len(tags) > 0:
        tag_check(tags, full_tags)
    return name_gen.select(*tags)
