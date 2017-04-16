from setuptools import setup


setup(
    name='spiner',
    version='0.1.0',
    description='Extension package for webapp2 apps running on GAE',
    url='http://github.com/gae-toolbox/spiner',
    author='Roman Nowicki',
    author_email='peengle@gmail.com',
    license='MIT',
    packages=[
        'spiner',
        'spiner.middlewares',
        'spiner.handlers'],
    zip_safe=False)
