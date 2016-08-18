from setuptools import setup


setup(
    name='gaeinit',
    version='0.1.0',
    description='Core for GAE based application',
    url='http://github.com/gaeinit/gaeinit',
    author='Roman Nowicki',
    author_email='roman.nowicki@inbox.com',
    license='MIT',
    packages=['gaeinit'],
    scripts=[
        'bin/gaeinit',
        'bin/runtests',
        ],
    include_package_data=True,
    zip_safe=False)
