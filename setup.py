import os
from distutils.core import setup
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
setup(name='pyoneall',
    version='0.1',
    packages=['pyoneall'],
    license='MIT License, see LICENSE file',
    description='OneAll API wrapper (http://www.oneall.com). Provides unified API for 20+ social networks',
    long_description=README,
    url='http://www.leandigo.com/',
    author='Michael Greenberg / Leandigo',
    author_email='michael@leandigo.com'
)