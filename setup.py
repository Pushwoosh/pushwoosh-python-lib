from distutils.core import setup

from pypushwoosh import __version__


setup(
    name='pyPushwoosh',
    version=__version__,
    author='Konstantin Misyutin',
    author_email='ikeeip@gmail.com',
    maintainer='Konstantin Misyutin',
    maintainer_email='ikeeip@gmail.com',
    packages=['pypushwoosh'],
    url='http://pushwoosh.com/',
    keywords=['Pushwoosh'],
    license='MIT',
    description='Python client for Pushwoosh',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)
