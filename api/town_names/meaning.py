
class Meaning(object):
    def __init__(self, usage, tags, meanings, sources):
        self.usage = usage
        self.tags = tags
        self.meanings = meanings
        self.sources = sources
        self.__set_location__()

    def __set_location__(self):
        if self.usage.startswith('-') and self.usage.endswith('-'):
            self.location = 'inner'
        elif self.usage.endswith('-'):
            self.location = 'pre'
        elif self.usage.startswith("-"):
            self.location = 'post'
        else:
            self.location = "word"

    def __str__(self):
        return self.usage.lower().replace("-", "")

    def __repr__(self):
        return ("{usage: %s, tags: %s, meanings: %s}"
            ", sources: %s, location: %s") % (
                self.usage, self.tags, self.meanings, self.sources,
                self.location)

    def word_has_meaning(self, word):
        if word.find(str(self)) > -1:
            return True
        return False

    def test(self, word):
        if self.location == "word":
            if word.lower() == str(self):
                return [self, word.lower()]
        elif self.location == "pre":
            if word.lower().startswith(str(self)):
                return [self, word.lower().replace(str(self), "")]
        elif self.location == "post":
            if word.lower().endswith(str(self)):
                return [word.replace(str(self), ""), self]
        else:
            if word.find(str(self)) > -1:
                parts = word.split(str(self))
                return [parts[0], self, parts[1]]

    def is_name(self):
        for tag in self.tags:
            if tag in ("female name", "male name", "family name"):
                return True
        return False

    def is_saint(self):
        for tag in self.tags:
            if tag in ("saint"):
                return True
        return False

    def key(self):
        key = [self.location]
        if self.is_name():
            key.append("name")
        elif self.usage.replace("-", "").lower() == 'saint':
            key.append("saint")
        return tuple(key)


