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

def find_meaning_text(meaning):
    roots = find_roots(meaning)
    meanings = meaning.meanings
    return "%s %s" % (roots, ", ".join(meanings))

def find_roots(meaning):
    roots = []
    if "old_english" in meaning.sources:
        roots.append("EN")
    if "old_scandinavian" in meaning.sources:
        roots.append("SC")
    if "old_french" in meaning.sources:
        roots.append("FR")
    if "celtic_mix" in meaning.sources:
        roots.append("CL")
    if "latin" in meaning.sources:
        roots.append("LA")
    if "germanic" in meaning.sources:
        roots.append("GE")
    if "greek" in meaning.sources:
        roots.append("GR")
    return "/".join(roots)