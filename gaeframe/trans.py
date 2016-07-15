# -*- coding: utf-8 -*-


class Trans:
    """Translations helper that map keys with translation strings

    Usage example:

    Trans({
        'Hello World': {
            'pl': 'Witaj Świecie',
        }
    }, 'pl')

    Trans('Hello World)  # will return: 'Witaj Świecie'
    """
    def __init__(self, translations, lang):
        self.lang = lang
        self.translations = translations

    def __call__(self, key):
        try:
            return unicode(self.translations[key][self.lang], 'utf-8')
        except KeyError:
            return key


def get_prefered_lang(accept_lang, supported_lang):
    """Returns prefered language based on accept-language string

    that match supported languages:

    Example:
       get_prefered_lang('en, en-gb;q=0.8, pl;q=0.7', ('en-gb', 'pl'))
        => will return 'en-gb'
    """
    for lang in accept_lang.split(','):
        l = lang.split(';')[0]
        if l in supported_lang:
            return l
    return supported_lang[0]
