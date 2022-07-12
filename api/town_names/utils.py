from town_names.meaning import Meaning

def filter_tag_list(full_tags):
    remove = ["Syntax", "Nominative"]
    tag_list = list(set([tag[0] for tag in full_tags if tag[1] not in remove]))
    tag_list.sort()
    return tag_list

def load_meanings(data):
    meaning_db = {}
    tags_db = {}
    full_tags = set()
    for subject in data:
        tags = subject['modifier_tags']
        modifier_type = subject['modifier_type']
        meanings = subject['meaning']
        for word in subject["words"]:
            usage = word["modern_usage"]
            sources = word
            del sources["modern_usage"]
            meaning = Meaning(usage, tags, meanings, sources)
            for tag in tags:
                t = tags_db.setdefault(tag, [])
                t.append(usage)
                full_tags.add((tag, modifier_type))
            w = meaning_db.setdefault(usage, [])
            w.append(meaning)
            if meaning.is_name():
                if not usage.endswith('s'):
                    plural = "%ss" % usage
                    plural_meaning = Meaning(plural, tags, meanings, sources)
                    for tag in tags:
                        t = tags_db.setdefault(tag, [])
                        t.append(plural)
                    w = meaning_db.setdefault(plural, [])
                    w.append(plural_meaning)
    return meaning_db, tags_db, full_tags

def word_to_key(word):
    elements = []
    for element in word:
        key = [element["location"]]
        if element.get("name", False):
            key.append("name")
        if element.get("saint", False):
            key.append("saint")
        elements.append(key)
    if len(word) == 1:
        elements[0].append("single")
    return tuple([tuple(e) for e in elements])
