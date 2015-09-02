import os
from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
setup(
    name='django-oneall',
    version='0.1.4',
    packages=['django_oneall'],
    requires=['Django (>=1.8)'],
    install_requires=['pyoneall == 0.1.1'],
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
        'Programming Language :: Python :: 3.4',  # Could be more! Not tested yet.
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)
