from django import template

register = template.Library()

BAN_WORDS = [
    'редиска',
    'блять',
    'пиздец',
    'охуеть'
]


@register.filter()
def censor(text):
    for word in BAN_WORDS:
        text = text.replace(word, '*****')
    return text
