"""View module for spiner apps

This module initialize jinja2 templates engine

Example:

    tpl = view.get_template('path/to/template.html')
    self.response.write(tpl.render({
        'var1': 1,
        'var2': 2,
    }))
"""
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from webapp2 import uri_for
import os

view = Environment(loader=FileSystemLoader(os.path.join(os.getcwd())))
view.globals['uri_for'] = uri_for
