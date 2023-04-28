from django import template

register = template.Library()

censor_words = ['редиска']


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр применим только к строкам ")

    words = value.split()

    for i, word in enumerate(words):
        if word.lower() in censor_words:
            words[i] = '*' * len(word)
    return ' '.join(words)
