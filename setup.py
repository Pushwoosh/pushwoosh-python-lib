from distutils.core import setup


setup(
    name='pyPushwoosh',
    version='0.1.0',
    author='Konstantin Misyutin',
    author_email='ikeeip@gmail.com',
    maintainer='Konstantin Misyutin',
    maintainer_email='ikeeip@gmail.com',
    packages=['pypushwoosh', 'pypushwoosh.test'],
    url='http://pushwoosh.com/',
    keywords=['Pushwoosh'],
    license='MIT',
    description='Python client for Pushwoosh',
    long_description=open('README.txt').read(),
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
