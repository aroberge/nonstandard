from setuptools import setup, find_packages

setup(name='nonstandard',
    version='0.9.1',
    description="Enables easy modification of Python's syntax on the fly.",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Interpreters',
    ], 
    url='https://github.com/aroberge/nonstandard',
    author='André Roberge',
    author_email='Andre.Roberge@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['dist', 'build', 'tools']),
    zip_safe=False)