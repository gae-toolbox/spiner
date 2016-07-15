from setuptools import setup


setup(
    name='gaeframe',
    version='0.1.0',
    description='Core for GAE based application',
    url='http://github.com/gaeframe/gaeframe',
    author='Roman Nowicki',
    author_email='roman.nowicki@inbox.com',
    license='MIT',
    packages=['gaeframe'],
    scripts=[
        'bin/gaeframe',
        'bin/runtests',
        'bin/run.py',
        'bin/appengine_config.py'],
    include_package_data=True,
    zip_safe=False)
