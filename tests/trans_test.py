# -*- coding: utf-8 -*-
import tests
import spiner.trans


class TestCase(tests.BaseTestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.trans = spiner.trans.Trans({
            'hello': {
                'world': {
                    'pl': 'AAA',
                    'en': 'BBB',
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
        }, 'en')

    def test_gettting_value_from_path(self):
        self.assertEquals('BBB', self.trans('hello.world'))
        self.trans.lang = 'pl'
        self.assertEquals('AAA', self.trans('hello.world'))
        self.assertEquals(['raz', 'dwa'], self.trans('hello.list'))
        self.assertEquals(1, self.trans('hello.number'))

    def test_gettting_value_from_invalid_path(self):
        self.assertEquals('x.world', self.trans('x.world'))
        self.assertEquals('invalidkey', self.trans('invalidkey'))

    def test_get_preffered_lang(self):
        self.assertEquals(
                'en-gb',
                spiner.trans.get_prefered_lang(
                    'en,en-gb;q=0.8,pl;q=0.7',
                    ('en-gb', 'pl')
                )
        )

        self.assertEquals(
                'pl',
                spiner.trans.get_prefered_lang(
                    'en,pl;q=0.8,en-gb;q=0.7',
                    ('en-gb', 'pl')
                )
        )

        self.assertEquals(
                'en-gb',
                spiner.trans.get_prefered_lang(
                    'de,fr',
                    ('en-gb', 'pl')
                )
        )
