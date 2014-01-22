import os
from setuptools import setup
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
setup(name='django-oneall',
    version='0.1.3-django1.5',
    packages=['django_oneall'],
    requires=['Django (>=1.4)',],
    install_requires=['pyoneall == 0.1'],
    license='MIT License, see LICENSE file',
    description='Django Authentication support for OneAll. Provides unified authentication for 20+ social networks',
    long_description=README,
    url='http://www.leandigo.com/',
    author='Michael Greenberg / Leandigo',
    author_email='michael@leandigo.com'
)
