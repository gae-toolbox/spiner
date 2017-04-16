# -*- coding: utf-8 -*-


class Trans:
    """Translations helper that map keys with translation strings

    Usage example:

    trans = Trans({
        'hello': {
            'short': {
                'pl': 'Witaj Świecie',
                'en': 'Hello World',
            },
            'list': {
                'pl': ['raz', 'dwa'],
                'en': ['one', 'two'],
            },
            'number': {
                'pl': 1,
                'en': 2,
            },
        }
    }, 'pl')

    trans('hello.short')  # will return: 'Witaj Świecie'
    trans('hello.list')  # will return: ['raz', 'dwa']
    trans('hello.number')  # will return: 1
    """
    def __init__(self, translations, lang):
        self.lang = lang
        self.translations = translations

    def __call__(self, path):
        try:
            keys = path.split('.')
            d = self.translations
            for key in keys:
                d = d[key]

            v = d[self.lang]
            if isinstance(v, str):
                return unicode(v, 'utf-8')

            if isinstance(v, (tuple, list)):
                return [unicode(line, 'utf-8') for line in v]

            return v
        except KeyError:
            return path


def get_prefered_lang(accept_lang, supported_lang):
    """Returns prefered language based on accept-language string

    that match supported languages:

    Example:
       get_prefered_lang('en,en-gb;q=0.8,pl;q=0.7', ('en-gb', 'pl'))
        => will return 'en-gb'
    """
    for lang in accept_lang.split(','):
        l = lang.split(';')[0]
        if l in supported_lang:
            return l
    return supported_lang[0]
