"""View module for gaeinit apps

This module initialize jinja2 templates engine

Example:

    tpl = view.get_template('path/to/template.html')
    self.response.write(tpl.render({
        'var1': 1,
        'var2': 2,
    }))
"""
from jinja2 import Environment, FileSystemLoader
import os

view = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), 'app')))
