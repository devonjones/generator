def filter_tag_list(full_tags):
    remove = ["Syntax", "Nominative"]
    tag_list = list(set([tag[0] for tag in full_tags if tag[1] not in remove]))
    tag_list.sort()
    return tag_list
