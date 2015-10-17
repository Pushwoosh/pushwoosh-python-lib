from setuptools import setup
from os import path
from codecs import open

from pypushwoosh import __version__


with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pypushwoosh',
    version=__version__,
    author='Konstantin Misyutin',
    author_email='ikeeip@gmail.com',
    maintainer='Konstantin Misyutin',
    maintainer_email='ikeeip@gmail.com',
    packages=['pypushwoosh'],
    url='https://github.com/Pushwoosh/pushwoosh-python-lib',
    keywords=['Pushwoosh'],
    license='MIT',
    description='Python client for Pushwoosh',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=['six'],
)
