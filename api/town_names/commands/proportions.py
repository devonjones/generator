import json
import importlib.resources as pkg_resources
from collections import Counter

from town_names.name import load_names
from town_names.meaning import load_meanings
import town_names.data as data

def proportion_command(towns):
    names = json.load(pkg_resources.open_text(data, "%s_place_names.json" % towns))
    parts = json.load(pkg_resources.open_text(data, "meanings.json"))
    names = load_names(names)
    word_db, _, _ = load_meanings(parts)
    good_names, bad_names = deconstruct_names(names, word_db)
    return set_proportions(good_names, bad_names)

def deconstruct_names(names, word_db):
    retval = [[],[]]
    counter = 0
    uncounted = 0
    word_names = 0
    word_saints = 0
    for name in names:
        name.find_meaning(word_db)
        if name.has_name():
            word_names += 1
        if name.has_saint():
            word_saints += 1
        if name.count_unaccounted() == 0:
            counter += 1
            retval[0].append(name)
        else:
            retval[1].append(name)
            uncounted += 1
    print("Perfect: %s, names: %s, saints: %s, unaccounted: %s, total: %s" % (counter, word_names, word_saints, uncounted, len(names)), file=sys.stderr)
    return retval

def set_proportions(names, missing):
    def gen_missing(missing):
        vals = set()
        for name in missing:
            unaccounted = name.get_unaccounted()
            for u in unaccounted:
                vals.add(str(u))
        retval = list(vals)
        retval.sort()
        return retval
    
    part_proportions = Counter()
    lone_proportions = Counter()
    struct_proportions = Counter()
    unaccounted = gen_missing(missing)
    for name in names:
        for u in name.get_samples():
            part_proportions[u] += 1
        for u in name.get_lone_samples():
            lone_proportions[u] += 1
        for structure in name.get_structure():
            struct_proportions[structure] += 1
    return {
        'usages': part_proportions,
        'single_usages': lone_proportions,
        'unaccounted': unaccounted,
        'structures': encode_structs(struct_proportions)}

def encode_structs(struct):
    structs = []
    for key, value in struct.items():
        newstruct = {"proportion": value}
        words = []
        for word in key:
            w = []
            for meaning in word:
                m = {}
                for quality in meaning:
                    if quality in ['pre', 'post', 'inner', 'word']:
                        m["location"] = quality
                    else:
                        m[quality] = True
                w.append(m)
            words.append(w)
        newstruct["words"] = words
        structs.append(newstruct)
    return structs
