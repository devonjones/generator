from town_names.meaning import Meaning

class Word(object):
    def __init__(self, word):
        if isinstance(word, str):
            self.word = [word]
        else:
            self.word = word

    def __str__(self):
        return ''.join([str(w) for w in self.word])

    def __repr__(self):
        results = []
        for w in self.word:
            if isinstance(w, str):
                results.append("'%s'" % w)
            else:
                results.append(w.usage)
        return " ".join(results)

    def __eq__(self, word):
        text = word
        if isinstance(word, Word):
            text = word.word
        if len(self.word) != len(text):
            return False
        for i in range(0, len(self.word)):
            if self.word[i] != text[i]:
                return False
        return True

    def size(self):
        return len(self.word)

    def extract_meanings(self, meanings):
        results = []
        w = [w for w in self.word]
        prior = []
        prev_letter = None
        while len(w) > 0:
            curr = w.pop(0)
            if isinstance(curr, str):
                for meaning in meanings:
                    parts = None
                    if len(prior) == 0 and meaning.location == "word":
                        parts = meaning.test(curr)
                    elif len(w) == 0 and meaning.location == "post":
                        parts = meaning.test(curr, prev_letter)
                    elif len(prior) == 0 and meaning.location == "pre":
                        parts = meaning.test(curr)
                    elif meaning.location == 'inner':
                        parts  = meaning.test(curr, prev_letter)
                    if parts:
                        result = []
                        result.extend(prior)
                        result.extend(parts)
                        result.extend(w)
                        results.append(Word([r for r in result if r != u'']))
            else:
                if curr.usage.endswith("-") and len(curr.usage) > 2:
                    prev_letter = curr.usage[-2]
                elif len(curr.usage) > 1:
                    prev_letter = curr.usage[-1]
            prior.append(curr)
        summed_results = []
        for r in results:
            nr = r.extract_meanings(meanings)
            if len(nr) == 0:
                summed_results.append(r)
            else:
                summed_results.extend(nr)
        return summed_results

    def count_unaccounted(self):
        size =  0
        for w in self.word:
            if isinstance(w, str):
                size += len(w)
        return size

    def has_name(self):
        for m in self.word:
            if isinstance(m, Meaning):
                if m.is_name():
                    return True
        return False

    def has_saint(self):
        for m in self.word:
            if isinstance(m, Meaning):
                if m.is_saint():
                    return True
        return False

    def get_samples(self):
        usage_set = set()
        if len(self.word) > 1:
            for m in self.word:
                if isinstance(m, Meaning):
                    usage_set.add(m.usage)
        return usage_set

    def get_lone_samples(self):
        usage_set = set()
        if len(self.word) == 1:
            for m in self.word:
                if isinstance(m, Meaning):
                    usage_set.add(m.usage)
        return usage_set

    def get_structure(self):
        structure = []
        for m in self.word:
            if m.is_name():
                structure.append((m.location, "name"))
            elif m.usage == u'Saint-':
                structure.append((m.location, "saint"))
            else:
                structure.append((m.location,))
        return tuple(structure)
