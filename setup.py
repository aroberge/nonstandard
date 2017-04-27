from setuptools import setup

setup(name='nonstandard',
    version='0.1',
    description="Enables easy modification of Python's syntax on the fly.",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Interpreters',
    ], 
    url='https://github.com/aroberge/nonstandard',
    author='André Roberge',
    author_email='Andre.Roberge@gmail.com',
    license='MIT',
    packages=['nonstandard'],
    zip_safe=False)