# -*- coding: utf-8 -*-
from os.path import join, dirname

from setuptools import setup, find_packages

README = open(join(dirname(__file__), 'README.rst')).read()
setup(
    name='django-oneall',
    version='1.0.2',
    packages=find_packages(),
    package_data={
        'django_oneall/templates/oneall': [
            'header.html',
            'login.html',
            'profile.html',
            'social_login.html'
        ],
    },
    include_package_data=True,
    install_requires=['pyoneall>=0.2.3', 'django>=1.8'],
    license='MIT License, see LICENSE file',
    description='Django Authentication support for OneAll. Provides unified authentication for 30+ social networks',
    long_description=README,
    url='http://www.leandigo.com/',
    author='Michael Greenberg / Leandigo',
    author_email='michael@leandigo.com',
    maintainer='Ekevoo',
    maintainer_email='ekevoo@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # Python 3.2 is not supported because "future" is incompatible with it.
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)
