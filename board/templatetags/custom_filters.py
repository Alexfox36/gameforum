from django import template


register = template.Library()



@register.filter()
def censor(value):
    dct = ['редиска', 'сосиска']

    for wrd in dct:
        if wrd in value:
            cens_wrd = wrd[0] + '*' * (len(wrd) -1)
            value = value.replace(wrd, cens_wrd)
    return value